"""mem0 cloud backend for LoCoMo.

Direct port of mem0's own evaluation pipeline (evaluation/src/memzero/{add,search}.py)
so our head-to-head numbers land at the same capability level mem0 publishes.
Reader + judge are ours (Gemini); everything upstream (ingest, search,
custom_instructions) is mem0's.

Optional dependency: mem0ai. Import is lazy so sonzai installs don't pull it in.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Any

from ..dataset import LocomoSample, LocomoSession
from . import LocomoBackendResult, RankedMemoryItem

logger = logging.getLogger("benchmarks.locomo.mem0")


# Ported verbatim from mem0's evaluation/src/memzero/add.py. Tunes extraction
# toward rich narrative memories with names/dates — load-bearing for mem0's
# published LoCoMo numbers. DO NOT edit to "improve" — that would sandbag the
# comparison.
MEM0_CUSTOM_INSTRUCTIONS = """
Generate personal memories that follow these guidelines:

1. Each memory should be self-contained with complete context, including:
   - The person's name, do not use "user" while creating memories
   - Personal details (career aspirations, hobbies, life circumstances)
   - Emotional states and reactions
   - Ongoing journeys or future plans
   - Specific dates when events occurred

2. Include meaningful personal narratives focusing on:
   - Identity and self-acceptance journeys
   - Family planning and parenting
   - Creative outlets and hobbies
   - Mental health and self-care activities
   - Career aspirations and education goals
   - Important life events and milestones

3. Make each memory rich with specific details rather than general statements
   - Include timeframes (exact dates when possible)
   - Name specific activities (e.g., "charity race for mental health" rather than just "exercise")
   - Include emotional context and personal growth elements

4. Extract memories only from user messages, not incorporating assistant responses

5. Format each memory as a paragraph with a clear narrative structure that captures
   the person's experience, challenges, and aspirations
"""

DEFAULT_TOP_K = 30
DEFAULT_INGEST_BATCH_SIZE = 2
MAX_429_RETRIES = 8
BASE_429_BACKOFF = 2.0


def _import_mem0():
    try:
        from mem0 import MemoryClient  # type: ignore
        return MemoryClient
    except ImportError as e:
        raise RuntimeError(
            "mem0ai package not installed. Install with `pip install mem0ai` "
            "(only needed when running `--backend mem0`)."
        ) from e


def _mem0_user_id(sample_id: str, speaker: str) -> str:
    """mem0's evaluation uses `{speaker}_{idx}`. We use sample_id as idx so
    multi-run isolation holds even across non-numeric sample IDs."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", speaker)
    return f"{safe}_{sample_id}"


def _session_messages_mem0(
    session: LocomoSession, speaker_a: str, speaker_b: str, *, pov: str,
) -> list[dict[str, str]]:
    """Format one session's turns for mem0.add — identical shape to _build_messages."""
    me = speaker_a if pov == "a" else speaker_b
    out: list[dict[str, str]] = []
    for t in session.turns:
        role = "user" if t.speaker == me else "assistant"
        out.append({"role": role, "content": f"{t.speaker}: {t.text}"})
    return out


def _hits_to_items(raw_hits: list[dict[str, Any]]) -> list[RankedMemoryItem]:
    items: list[RankedMemoryItem] = []
    for h in raw_hits:
        meta = h.get("metadata") or {}
        items.append(
            RankedMemoryItem(
                memory_id=str(h.get("id") or ""),
                text=str(h.get("memory") or h.get("text") or ""),
                timestamp=str(meta.get("timestamp") or ""),
                score=float(h.get("score") or 0.0),
                session_id=str(meta.get("session_id") or ""),
            )
        )
    return items


def _call_with_retry_sync(fn, *, op: str, retries: int = MAX_429_RETRIES):
    import time as _time
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt + 1 < retries:
                backoff = BASE_429_BACKOFF * (2 ** attempt)
                logger.info("mem0 %s 429 — backing off %.1fs", op, backoff)
                _time.sleep(backoff)
                continue
            logger.warning("mem0 %s failed (non-retryable): %s", op, e)
            return None
    return None


# ---------------------------------------------------------------------------
# Ingest — dual-POV in mem0's own batched/threaded style
# ---------------------------------------------------------------------------


def _batch_2(messages: list[dict[str, str]], batch_size: int) -> list[list[dict[str, str]]]:
    if batch_size <= 0:
        return [messages] if messages else []
    return [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]


def ingest_sample_sync(
    mem0_client,
    sample: LocomoSample,
    *,
    ingest_batch_size: int = DEFAULT_INGEST_BATCH_SIZE,
) -> None:
    user_a = _mem0_user_id(sample.sample_id, sample.speaker_a)
    user_b = _mem0_user_id(sample.sample_id, sample.speaker_b)

    _call_with_retry_sync(lambda: mem0_client.delete_all(user_id=user_a), op=f"delete_all({user_a})")  # noqa: E501
    _call_with_retry_sync(lambda: mem0_client.delete_all(user_id=user_b), op=f"delete_all({user_b})")  # noqa: E501

    for session in sample.sessions:
        msgs_a = _session_messages_mem0(session, sample.speaker_a, sample.speaker_b, pov="a")
        msgs_b = _session_messages_mem0(session, sample.speaker_a, sample.speaker_b, pov="b")
        meta = {
            "timestamp": session.date_time,
            "session_id": f"session_{session.index}",
        }

        for batch in _batch_2(msgs_a, ingest_batch_size):
            _call_with_retry_sync(
                lambda b=batch: mem0_client.add(
                    b, user_id=user_a, version="v2", metadata=meta,
                ),
                op=f"add(A, sample={sample.sample_id}, session={session.index})",
            )
        for batch in _batch_2(msgs_b, ingest_batch_size):
            _call_with_retry_sync(
                lambda b=batch: mem0_client.add(
                    b, user_id=user_b, version="v2", metadata=meta,
                ),
                op=f"add(B, sample={sample.sample_id}, session={session.index})",
            )


# ---------------------------------------------------------------------------
# QA — dual search → Gemini reader
# ---------------------------------------------------------------------------


async def answer_one_qa(
    mem0_client,
    sample: LocomoSample,
    qa_question: str,
    *,
    top_k: int,
    reader,
) -> LocomoBackendResult:
    user_a = _mem0_user_id(sample.sample_id, sample.speaker_a)
    user_b = _mem0_user_id(sample.sample_id, sample.speaker_b)

    def _search(uid: str) -> list[dict]:
        raw = _call_with_retry_sync(
            lambda: mem0_client.search(qa_question, user_id=uid, top_k=top_k),
            op=f"search({uid})",
        ) or []
        if isinstance(raw, dict):
            raw = raw.get("results") or []
        return list(raw)

    loop = asyncio.get_running_loop()
    a_raw, b_raw = await asyncio.gather(
        loop.run_in_executor(None, _search, user_a),
        loop.run_in_executor(None, _search, user_b),
    )
    a_mems = _hits_to_items(a_raw)
    b_mems = _hits_to_items(b_raw)

    from ..scoring import merge_speaker_rankings
    from .sonzai import _ask_reader

    answer = await _ask_reader(
        reader,
        question=qa_question,
        speaker_1=sample.speaker_a, speaker_1_memories=a_mems,
        speaker_2=sample.speaker_b, speaker_2_memories=b_mems,
    )

    return LocomoBackendResult(
        speaker_a_memories=a_mems,
        speaker_b_memories=b_mems,
        agent_answer=answer,
        retrieved_session_ids=merge_speaker_rankings(a_mems, b_mems),
        extra={"mem0_hits_a": len(a_raw), "mem0_hits_b": len(b_raw)},
    )


# ---------------------------------------------------------------------------
# Bootstrapping
# ---------------------------------------------------------------------------


def build_client():
    memory_client_cls = _import_mem0()
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY is required for --backend mem0.")
    client = memory_client_cls(
        api_key=api_key,
        org_id=os.environ.get("MEM0_ORGANIZATION_ID"),
        project_id=os.environ.get("MEM0_PROJECT_ID"),
    )
    try:
        client.update_project(custom_instructions=MEM0_CUSTOM_INSTRUCTIONS)
    except Exception as e:
        logger.warning("mem0 update_project failed (custom_instructions not applied): %s", e)
    return client
