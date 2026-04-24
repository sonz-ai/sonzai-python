"""Sonzai backend for LoCoMo.

Flow (per sample):
1. For each (chronologically-ordered) session, build messages from two
   perspectives (A and B), then call /process once per POV per batch. Min batch
   size is 2 (server constraint); default 2 to match mem0's ingest cadence,
   0 = whole-session ablation.
2. Between sessions, advance_time(gap_hours) concurrently for both users.
   Final 25h flush so the last session's consolidation fires.
3. QA phase (Task 9): memory.search per user → Gemini reader → judge.

Only /process is used for ingest — not sessions.start/end, not /chat,
not memory/facts/bulk. See spec §2 for endpoint rationale.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterator

from pydantic import BaseModel
from sonzai import AsyncSonzai

from ...common.sdk_extras import (
    async_memory,
    async_process,
    clear_agent_memory_async,
)
from ...common.workbench_compat import advance_time_chunked_async
from ..dataset import LocomoSample, LocomoSession, LocomoTurn
from . import LocomoBackendResult, RankedMemoryItem

logger = logging.getLogger(__name__)

FINAL_FLUSH_HOURS = 25.0
MIN_GAP_HOURS = 25.0
DEFAULT_INGEST_BATCH_SIZE = 2

_META_MARKERS = (":comm_style", ":side_effect:", ":interest:")


# ---------------------------------------------------------------------------
# Pure helpers — deterministic, unit-tested
# ---------------------------------------------------------------------------


def _sonzai_session_id(sample_id: str, session_index: int, pov: str) -> str:
    """Deterministic session_id passed to /process so extracted facts are
    tagged under a predictable key."""
    return f"{sample_id}-s{session_index}-{pov}"


def _build_messages(
    session: LocomoSession, speaker_a: str, speaker_b: str, *, pov: str,
) -> list[dict[str, str]]:
    """Render one session's turns as /process messages from speaker_a/b POV.

    POV "a": speaker_a turns become role "user", speaker_b turns "assistant".
    POV "b": reversed. Turn text is prefixed with `"{speaker}: "` so the
    extractor preserves speaker context (mem0-parity).
    """
    assert pov in ("a", "b"), f"pov must be 'a' or 'b', got {pov}"
    me = speaker_a if pov == "a" else speaker_b
    out: list[dict[str, str]] = []
    for t in session.turns:
        role = "user" if t.speaker == me else "assistant"
        out.append({"role": role, "content": f"{t.speaker}: {t.text}"})
    return out


def _batch_messages(
    messages: list[dict[str, str]], batch_size: int,
) -> Iterator[list[dict[str, str]]]:
    """Yield message batches respecting /process's >=2 constraint.

    batch_size=0 → yield the whole list as one batch (if len>=2, else empty).
    batch_size>=2 → chunk into size-`batch_size` pieces. If the last chunk
    would be size-1, instead re-draw the final boundary so the last batch
    is the last `batch_size` messages (overlapping by 1 with the previous
    batch's tail). This ensures every batch has exactly `batch_size`
    messages and no size-1 batch is ever emitted. If n < 2, yield nothing.
    """
    n = len(messages)
    if n < 2:
        return
    if batch_size <= 0:
        yield messages
        return
    if batch_size < 2:
        raise ValueError("batch_size must be 0 (whole session) or >=2")

    # Normal chunking
    i = 0
    boundaries: list[tuple[int, int]] = []
    while i < n:
        boundaries.append((i, min(i + batch_size, n)))
        i += batch_size

    # If the last chunk is size-1 AND there's a previous chunk to anchor against,
    # replace it with the last batch_size messages (overlapping with prev tail).
    if len(boundaries) >= 2 and (boundaries[-1][1] - boundaries[-1][0]) == 1:
        boundaries[-1] = (n - batch_size, n)

    for start, end in boundaries:
        yield messages[start:end]


def _is_metadata_fact(fact_id: str) -> bool:
    """Filter agent-level metadata facts (comm_style, side_effect, interest:*).

    Matches the LongMemEval backend's filter — these are per-(agent, user)
    profile entries, not session-grounded facts. They lack session attribution
    and crowd out the specific LoCoMo-relevant facts in the top-k window.
    """
    return any(m in fact_id for m in _META_MARKERS)


# ---------------------------------------------------------------------------
# Ingest — /process per speaker POV + advance_time between sessions
# ---------------------------------------------------------------------------


async def ingest_sample(
    client: AsyncSonzai,
    sample: LocomoSample,
    *,
    shared_agent_id: str,
    ingest_batch_size: int = DEFAULT_INGEST_BATCH_SIZE,
    skip_advance_time: bool = False,
    clear_before: bool = True,
) -> dict[str, int]:
    """Ingest one sample end-to-end. Returns diagnostics dict."""
    user_a = f"lc-{sample.sample_id}-a"
    user_b = f"lc-{sample.sample_id}-b"

    if clear_before:
        await asyncio.gather(
            clear_agent_memory_async(client, agent_id=shared_agent_id, user_id=user_a),
            clear_agent_memory_async(client, agent_id=shared_agent_id, user_id=user_b),
        )

    process_calls = 0
    facts_extracted = 0
    advance_calls = 0
    advance_failures = 0

    async def _advance(hours: float) -> None:
        nonlocal advance_calls, advance_failures
        if skip_advance_time or hours <= 0:
            return
        try:
            results = await asyncio.gather(
                advance_time_chunked_async(
                    client, agent_id=shared_agent_id, user_id=user_a, total_hours=hours,
                ),
                advance_time_chunked_async(
                    client, agent_id=shared_agent_id, user_id=user_b, total_hours=hours,
                ),
                return_exceptions=True,
            )
            for r in results:
                if isinstance(r, Exception):
                    advance_failures += 1
                    logger.warning("advance_time failed (non-fatal): %s", r)
                else:
                    advance_calls += len(r)
        except Exception as e:
            advance_failures += 1
            logger.warning("advance_time wrapper failed: %s", e)

    prev_dt = None
    for session in sample.sessions:
        dt = session.parsed_date_time
        if prev_dt is not None and dt is not None:
            delta_h = max((dt - prev_dt).total_seconds() / 3600.0, MIN_GAP_HOURS)
            await _advance(delta_h)

        msgs_a = _build_messages(session, sample.speaker_a, sample.speaker_b, pov="a")
        msgs_b = _build_messages(session, sample.speaker_a, sample.speaker_b, pov="b")

        for batch in _batch_messages(msgs_a, ingest_batch_size):
            try:
                resp = await async_process(
                    client,
                    agent_id=shared_agent_id,
                    user_id=user_a,
                    messages=batch,
                    session_id=_sonzai_session_id(sample.sample_id, session.index, "a"),
                )
                process_calls += 1
                facts_extracted += int((resp or {}).get("facts_extracted") or 0)
            except Exception as e:
                logger.warning(
                    "process(A) failed for sample=%s session=%d: %s",
                    sample.sample_id, session.index, e,
                )
        for batch in _batch_messages(msgs_b, ingest_batch_size):
            try:
                resp = await async_process(
                    client,
                    agent_id=shared_agent_id,
                    user_id=user_b,
                    messages=batch,
                    session_id=_sonzai_session_id(sample.sample_id, session.index, "b"),
                )
                process_calls += 1
                facts_extracted += int((resp or {}).get("facts_extracted") or 0)
            except Exception as e:
                logger.warning(
                    "process(B) failed for sample=%s session=%d: %s",
                    sample.sample_id, session.index, e,
                )
        prev_dt = dt

    # Final flush
    await _advance(FINAL_FLUSH_HOURS)

    return {
        "process_calls": process_calls,
        "facts_extracted": facts_extracted,
        "advance_time_calls": advance_calls,
        "advance_time_failures": advance_failures,
    }


# ---------------------------------------------------------------------------
# QA — memory.search per user + Gemini reader
# ---------------------------------------------------------------------------


def _render_answer_prompt(
    *,
    question: str,
    speaker_1: str,
    speaker_1_memories: list[RankedMemoryItem],
    speaker_2: str,
    speaker_2_memories: list[RankedMemoryItem],
) -> str:
    """Render mem0's ANSWER_PROMPT with Jinja-style placeholders.

    mem0 uses Jinja Template — we do a light string-replace so we don't need
    Jinja at runtime. Placeholders are all well-known and the template is
    under our control (ported verbatim).
    """
    import json
    from ..prompts import ANSWER_PROMPT

    def _fmt(mems: list[RankedMemoryItem]) -> str:
        # mem0 formats each memory as "{timestamp}: {memory_text}" in a JSON array
        return json.dumps(
            [f"{m.timestamp}: {m.text}" if m.timestamp else m.text for m in mems],
            indent=4,
        )

    return (
        ANSWER_PROMPT
        .replace("{{speaker_1_user_id}}", speaker_1)
        .replace("{{speaker_2_user_id}}", speaker_2)
        .replace("{{speaker_1_memories}}", _fmt(speaker_1_memories))
        .replace("{{speaker_2_memories}}", _fmt(speaker_2_memories))
        .replace("{{question}}", question)
    )


class _ReaderAnswer(BaseModel):
    answer: str


async def _ask_reader(
    judge,
    *,
    question: str,
    speaker_1: str, speaker_1_memories: list[RankedMemoryItem],
    speaker_2: str, speaker_2_memories: list[RankedMemoryItem],
) -> str:
    """Run the Gemini reader over mem0's ported ANSWER_PROMPT."""
    prompt = _render_answer_prompt(
        question=question,
        speaker_1=speaker_1, speaker_1_memories=speaker_1_memories,
        speaker_2=speaker_2, speaker_2_memories=speaker_2_memories,
    )
    verdict = await judge.grade_async(prompt, _ReaderAnswer)
    return verdict.answer


async def _build_fact_to_session_map(
    client: AsyncSonzai, *, agent_id: str, user_id: str,
) -> dict[str, str]:
    """Map fact_id → Sonzai session_id for this (agent, user).

    Mirrors the LongMemEval helper of the same name. The session_id returned
    here is the one we passed to /process (e.g. "lc-sample0-s3-a"), not
    LoCoMo's "session_3" yet — caller does the final projection.
    """
    memory = async_memory(client)
    mapping: dict[str, str] = {}
    try:
        timeline = await memory.timeline(agent_id=agent_id, user_id=user_id)
        for sess in timeline.sessions:
            fallback = sess.session_id if sess.session_id and sess.session_id != "unknown" else ""
            for fact in sess.facts:
                sid = fact.session_id or fallback
                if fact.fact_id and sid and sid != "unknown":
                    mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.timeline failed: %s", e)

    try:
        facts = await memory.list_facts(agent_id=agent_id, user_id=user_id, limit=5000)
        for fact in facts.facts:
            if fact.fact_id in mapping:
                continue
            sid = fact.session_id or fact.source_id
            if sid and sid != "unknown":
                mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.list_facts failed: %s", e)

    return mapping


def _sonzai_sid_to_locomo(sonzai_sid: str) -> str:
    """Project "lc-{sample}-s{N}-{a|b}" → "session_{N}"."""
    import re as _re
    m = _re.search(r"-s(\d+)-[ab]$", sonzai_sid or "")
    if not m:
        return ""
    return f"session_{int(m.group(1))}"


async def _retrieve_for_user(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    query: str,
    top_k: int,
    session_dates: dict[str, str],
) -> list[RankedMemoryItem]:
    """Run memory.search and project to RankedMemoryItem with LoCoMo session_ids."""
    memory = async_memory(client)
    fact_to_sid = await _build_fact_to_session_map(client, agent_id=agent_id, user_id=user_id)
    results = await memory.search(
        agent_id=agent_id, user_id=user_id, query=query, limit=top_k,
    )
    out: list[RankedMemoryItem] = []
    for r in results.results:
        if _is_metadata_fact(r.fact_id):
            continue
        sonzai_sid = str(getattr(r, "session_id", "") or "") or fact_to_sid.get(r.fact_id, "")
        locomo_sid = _sonzai_sid_to_locomo(sonzai_sid)
        out.append(
            RankedMemoryItem(
                memory_id=r.fact_id,
                text=r.content or "",
                timestamp=session_dates.get(locomo_sid, ""),
                score=float(getattr(r, "score", 0.0) or 0.0),
                session_id=locomo_sid,
            )
        )
    return out


async def answer_one_qa(
    client: AsyncSonzai,
    sample: LocomoSample,
    qa_question: str,
    *,
    shared_agent_id: str,
    top_k: int,
    reader,
) -> LocomoBackendResult:
    user_a = f"lc-{sample.sample_id}-a"
    user_b = f"lc-{sample.sample_id}-b"

    session_dates: dict[str, str] = {
        f"session_{s.index}": s.date_time for s in sample.sessions
    }

    a_mems, b_mems = await asyncio.gather(
        _retrieve_for_user(
            client, agent_id=shared_agent_id, user_id=user_a,
            query=qa_question, top_k=top_k, session_dates=session_dates,
        ),
        _retrieve_for_user(
            client, agent_id=shared_agent_id, user_id=user_b,
            query=qa_question, top_k=top_k, session_dates=session_dates,
        ),
    )

    from ..scoring import merge_speaker_rankings
    merged = merge_speaker_rankings(a_mems, b_mems)

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
        retrieved_session_ids=merged,
        extra={},
    )
