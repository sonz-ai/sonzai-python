"""mem0 cloud LongMemEval backend.

Ingests each question's haystack into mem0 cloud (one ``add`` per session,
namespaced by a per-question ``user_id``), then searches for the question
and returns top-K session-level rankings for head-to-head with MemPalace
and Sonzai.

Fairness / parity notes:

- Same ``ranked_items`` shape as the MemPalace backend, so the scoring block
  (``_retrieval_metrics``) is unchanged.
- ``session_id`` is attached to every mem0 memory via ``metadata`` at add
  time so the ``search`` response can be mapped back to session IDs for
  session-level recall.
- End-to-end QA uses the same Gemini reader the MemPalace backend uses
  (``_mempalace_read_answer`` in ``run.py``), fed the top retrieved sessions.

**Optional dependency** — ``mem0ai`` is imported lazily, so ``sonzai``
installs and Sonzai-only bench runs never pull it in.

**mem0 rate limits are real.** We throttle with:

- Low default concurrency (``run_all(..., concurrency=2)``).
- Exponential backoff on 429 per call.
- ``per_question_pause`` seconds after each question finishes ingesting,
  so the account-level rate envelope has time to recover.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from dataclasses import dataclass
from typing import Any

from tqdm.asyncio import tqdm_asyncio

from ..dataset import LongMemEvalQuestion, Session
from . import BackendResult, RankedItem

logger = logging.getLogger("benchmarks.longmemeval.mem0")


def _import_mem0():
    try:
        from mem0 import AsyncMemoryClient  # type: ignore

        return AsyncMemoryClient
    except ImportError as e:
        raise RuntimeError(
            "mem0ai package not installed. Install with `pip install mem0ai` "
            "(only needed when running `--backend mem0`)."
        ) from e


DEFAULT_SEARCH_K = 30  # matches MemPalace's k-grid ceiling
DEFAULT_INGEST_PAUSE = 0.5  # seconds between per-session adds
DEFAULT_POST_INGEST_WAIT = 5.0  # seconds after last add before searching
DEFAULT_PER_QUESTION_PAUSE = 1.0  # seconds between questions (rate-envelope)
MAX_429_RETRIES = 8
BASE_429_BACKOFF = 2.0


def _user_id_for(question_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", question_id)[:48]
    return f"sonzai-lme-bench-{safe}"


async def _call_with_retry(coro_factory, *, op: str) -> Any:
    """Call an async mem0 method with exponential backoff on 429."""
    for attempt in range(MAX_429_RETRIES):
        try:
            return await coro_factory()
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt + 1 < MAX_429_RETRIES:
                backoff = BASE_429_BACKOFF * (2**attempt)
                logger.info("mem0 %s 429 — backing off %.1fs (attempt %d)", op, backoff, attempt + 1)
                await asyncio.sleep(backoff)
                continue
            logger.warning("mem0 %s failed (non-retryable): %s", op, e)
            return None
    logger.warning("mem0 %s: exhausted retries", op)
    return None


def _session_to_messages(session: Session) -> list[dict[str, str]]:
    """Turn a LongMemEval session into the OpenAI-style list mem0.add expects."""
    out: list[dict[str, str]] = []
    for t in session.turns:
        # mem0 accepts only "user" / "assistant"; skip anything exotic.
        role = t.role if t.role in ("user", "assistant") else "user"
        content = (t.content or "").strip()
        if not content:
            continue
        out.append({"role": role, "content": content})
    return out


async def _ingest_question(
    client,
    *,
    question: LongMemEvalQuestion,
    user_id: str,
    ingest_pause: float,
    post_ingest_wait: float,
) -> None:
    # Reset this user_id so prior runs of the same question don't contaminate
    # retrieval. mem0 deletes are cheap and idempotent.
    await _call_with_retry(
        lambda: client.delete_all(user_id=user_id),
        op=f"delete_all({question.question_id})",
    )

    for session in question.sessions:
        messages = _session_to_messages(session)
        if not messages:
            continue
        await _call_with_retry(
            lambda m=messages, s=session: client.add(
                m,
                user_id=user_id,
                metadata={"session_id": s.session_id, "date": s.date},
                output_format="v1.1",
            ),
            op=f"add({question.question_id}/{session.session_id})",
        )
        if ingest_pause:
            await asyncio.sleep(ingest_pause)

    # mem0 does server-side extraction asynchronously; give it a moment so
    # the question-time search sees the just-ingested haystack.
    if post_ingest_wait:
        await asyncio.sleep(post_ingest_wait)


def _hits_to_backend_result(
    hits: list[dict[str, Any]],
    *,
    search_k: int,
) -> BackendResult:
    items: list[RankedItem] = []
    ranked_sids: list[str] = []
    ranked_texts: list[str] = []
    seen_sids: set[str] = set()

    for h in hits[:search_k]:
        text = (h.get("memory") or h.get("text") or "").strip()
        meta = h.get("metadata") or {}
        sid = str(meta.get("session_id") or "")
        date = str(meta.get("date") or "")
        corpus_id = sid or str(h.get("id") or "")
        items.append(RankedItem(corpus_id=corpus_id, text=text, timestamp=date))
        if sid and sid not in seen_sids:
            seen_sids.add(sid)
            ranked_sids.append(sid)
        if text:
            ranked_texts.append(text)

    return BackendResult(
        ranked_items=items,
        ranked_session_ids=ranked_sids,
        ranked_fact_texts=ranked_texts,
        agent_answer="",
        extra={"mem0_hits": len(hits)},
    )


async def _process_question(
    client,
    question: LongMemEvalQuestion,
    *,
    search_k: int,
    ingest_pause: float,
    post_ingest_wait: float,
) -> tuple[str, BackendResult]:
    user_id = _user_id_for(question.question_id)
    await _ingest_question(
        client,
        question=question,
        user_id=user_id,
        ingest_pause=ingest_pause,
        post_ingest_wait=post_ingest_wait,
    )

    raw = await _call_with_retry(
        lambda: client.search(
            question.question,
            user_id=user_id,
            limit=search_k,
            output_format="v1.1",
        ),
        op=f"search({question.question_id})",
    )
    if isinstance(raw, dict):
        raw = raw.get("results") or []
    hits = list(raw or [])
    return question.question_id, _hits_to_backend_result(hits, search_k=search_k)


async def run_all(
    questions: list[LongMemEvalQuestion],
    *,
    concurrency: int = 2,
    search_k: int = DEFAULT_SEARCH_K,
    ingest_pause: float = DEFAULT_INGEST_PAUSE,
    post_ingest_wait: float = DEFAULT_POST_INGEST_WAIT,
    per_question_pause: float = DEFAULT_PER_QUESTION_PAUSE,
) -> dict[str, BackendResult]:
    AsyncMemoryClient = _import_mem0()
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY is required for --backend mem0.")
    client = AsyncMemoryClient(api_key=api_key)

    sem = asyncio.Semaphore(concurrency)

    async def one(q: LongMemEvalQuestion) -> tuple[str, BackendResult]:
        async with sem:
            try:
                res = await _process_question(
                    client,
                    q,
                    search_k=search_k,
                    ingest_pause=ingest_pause,
                    post_ingest_wait=post_ingest_wait,
                )
            except Exception:
                logger.exception("mem0 backend failed on %s", q.question_id)
                return q.question_id, BackendResult()
            if per_question_pause:
                await asyncio.sleep(per_question_pause)
            return res

    pairs = await tqdm_asyncio.gather(*(one(q) for q in questions), desc="mem0")
    return dict(pairs)


__all__ = ["run_all"]
