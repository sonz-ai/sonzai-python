"""Sonzai backend for LongMemEval.

Uses the public Sonzai SDK end-to-end. Only one call differs from a normal
production integration: ``workbench.advance_time`` between sessions, which
runs the background CE workers (diary, consolidation, decay) as if simulated
time had passed. Without this, self-learning would only fire on the real clock.

Flow per question:

1. ``agents.create`` — fresh agent so memory state is scoped to this question.
2. For each haystack session (in date order):
   a. ``sessions.start`` with a deterministic session_id.
   b. Replay the canned user+assistant transcript via ``sessions.end(messages=...)``
      — no new text is generated; we're feeding LongMemEval's scripted history
      verbatim into the CE pipeline for fact extraction.
   c. ``workbench.advance_time`` with the gap to the next session (floor 25h so
      at least one full day of CE workers runs).
3. Final ``advance_time(25h)`` to flush consolidation for the last session.
4. Retrieval: ``memory.search`` → map fact_ids to session_ids via ``memory.timeline``
   → Recall@5 / NDCG@5.
5. QA: ``agents.chat`` with the question → Gemini judge vs ground truth.
6. ``agents.delete`` — cleanup.
"""

from __future__ import annotations

import logging
import uuid

from sonzai import AsyncSonzai

from ...common.sdk_extras import async_memory, async_sessions
from ...common.workbench_compat import advance_time_chunked_async
from ..dataset import LongMemEvalQuestion, Session, hours_between
from . import BackendResult

logger = logging.getLogger(__name__)

# Ensures at least one full simulated day elapses per gap so daily CE workers
# (diary, consolidation, decay) actually run. LongMemEval's haystacks are
# typically days apart anyway, but clamp defensively.
MIN_GAP_HOURS = 25.0


async def _replay_session(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    session_id: str,
    session: Session,
) -> None:
    """Feed a pre-scripted LongMemEval session into Sonzai's CE pipeline.

    We bypass ``agents.chat`` because LongMemEval's sessions have canned
    assistant replies — generating new ones would break the benchmark premise.
    ``sessions.end(messages=...)`` ingests the transcript verbatim.
    """
    sessions = async_sessions(client)
    await sessions.start(
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_id,
    )
    from sonzai.types import ChatMessage

    messages: list[ChatMessage | dict[str, str]] = [
        {"role": t.role, "content": t.content} for t in session.turns
    ]
    await sessions.end(
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_id,
        total_messages=len(messages),
        messages=messages,
    )


async def _build_fact_to_session_map(
    client: AsyncSonzai, *, agent_id: str, user_id: str
) -> dict[str, str]:
    """Build ``fact_id → session_id`` from the agent's memory state.

    ``memory.search`` returns ``fact_id`` but not the source session, so we
    reconstruct the mapping. The typed ``Fact`` schema on ``list_facts``
    doesn't include ``session_id`` today (server returns it as an extra
    field), and ``memory.timeline``'s aggregation key occasionally falls
    back to ``"unknown"``. We try both sources and use whichever actually
    gives us session IDs — facts don't move between sessions, so collision
    is impossible.
    """
    memory = async_memory(client)
    mapping: dict[str, str] = {}

    # Timeline first — AtomicFact.session_id is populated per-fact even when
    # the aggregation-level session_id is empty.
    try:
        timeline = await memory.timeline(agent_id=agent_id, user_id=user_id)
        for sess in timeline.sessions:
            fallback = sess.session_id if sess.session_id and sess.session_id != "unknown" else ""
            for fact in sess.facts:
                sid = getattr(fact, "session_id", "") or fallback
                if fact.fact_id and sid and sid != "unknown":
                    mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.timeline failed: %s", e)

    # list_facts as a backstop — Fact has extra="allow" so session_id lives in
    # model_extra if the server populates it.
    try:
        facts = await memory.list_facts(agent_id=agent_id, user_id=user_id, limit=5000)
        for fact in facts.facts:
            if fact.fact_id in mapping:
                continue
            extra = fact.model_extra or {}
            sid = extra.get("session_id") or extra.get("source_id") or ""
            if sid and sid != "unknown":
                mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.list_facts failed: %s", e)

    return mapping


async def _retrieve(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    question: str,
    limit: int,
) -> tuple[list[str], list[str]]:
    """Return ``(ranked_session_ids, ranked_fact_texts)`` for the question.

    Sonzai's memory is fact-oriented — retrieved facts are the first-class
    result. Session IDs are best-effort via a fact-to-session mapping (not
    always populated server-side).
    """
    memory = async_memory(client)
    results = await memory.search(agent_id=agent_id, query=question, limit=limit)
    fact_to_session = await _build_fact_to_session_map(
        client, agent_id=agent_id, user_id=user_id
    )

    seen: set[str] = set()
    ranked_sessions: list[str] = []
    ranked_facts: list[str] = []
    for r in results.results:
        if r.content:
            ranked_facts.append(r.content)
        sid = fact_to_session.get(r.fact_id, "")
        if sid and sid not in seen:
            seen.add(sid)
            ranked_sessions.append(sid)
    return ranked_sessions, ranked_facts


async def _ask_question(
    client: AsyncSonzai, *, agent_id: str, user_id: str, question: str
) -> str:
    resp = await client.agents.chat(
        agent_id=agent_id,
        user_id=user_id,
        messages=[{"role": "user", "content": question}],
    )
    # ``agents.chat`` returns ChatResponse in non-streaming mode.
    return getattr(resp, "content", "") or ""


async def run_question(
    client: AsyncSonzai,
    question: LongMemEvalQuestion,
    *,
    min_gap_hours: float = MIN_GAP_HOURS,
    retrieval_limit: int = 50,
    include_qa: bool = True,
    skip_advance_time: bool = False,
    max_sessions: int = 0,
) -> BackendResult:
    """Ingest one LongMemEval question's haystack and evaluate Sonzai's memory.

    ``skip_advance_time=True`` disables self-learning simulation entirely —
    useful as a baseline. The delta between the normal run and this one is
    the measured effect of Sonzai's background CE workers.

    ``max_sessions > 0`` truncates the haystack for fast smoke runs; keeps
    answer-bearing sessions preferentially.
    """
    agent_name = f"lme-{question.question_id[:12]}-{uuid.uuid4().hex[:6]}"
    user_id = f"lme-user-{question.question_id[:12]}"

    # Optionally trim haystack for smoke runs — keep answer-bearing sessions.
    haystack = question.sessions
    if max_sessions and len(haystack) > max_sessions:
        answer_set = set(question.answer_session_ids)
        keep_ids = {s.session_id for s in haystack if s.session_id in answer_set}
        filler_budget = max(max_sessions - len(keep_ids), 0)
        filler_ids = {
            s.session_id
            for s in [s for s in haystack if s.session_id not in keep_ids][-filler_budget:]
        } if filler_budget else set()
        keep = keep_ids | filler_ids
        haystack = sorted(
            (s for s in haystack if s.session_id in keep),
            key=lambda s: s.parsed_date,
        )

    agent = await client.agents.create(name=agent_name)
    agent_id = agent.agent_id
    advance_calls = 0
    consolidation_events = 0

    advance_failures = 0

    async def _try_advance(hours: float) -> None:
        nonlocal advance_calls, consolidation_events, advance_failures
        if skip_advance_time:
            return
        try:
            results = await advance_time_chunked_async(
                client,
                agent_id=agent_id,
                user_id=user_id,
                total_hours=hours,
            )
            advance_calls += len(results)
            consolidation_events += sum(1 for r in results if r.consolidation_ran)
        except Exception as e:
            advance_failures += 1
            logger.warning(
                "advance_time(%s, %.1fh) failed (non-fatal, CE may not be fully consolidated): %s",
                agent_id, hours, e,
            )

    try:
        prev_session: Session | None = None
        for session in haystack:
            if prev_session is not None:
                gap = max(min_gap_hours, hours_between(prev_session, session))
                await _try_advance(gap)

            # Use LongMemEval's own session IDs (e.g., "answer_280352e9",
            # "sharegpt_xxx_0") so memory.timeline groups extracted facts
            # under the same IDs that `answer_session_ids` references — that's
            # what session-level Recall@5 is scored against.
            await _replay_session(
                client,
                agent_id=agent_id,
                user_id=user_id,
                session_id=session.session_id,
                session=session,
            )
            prev_session = session

        # Final advance-time lets the last session's consolidation/diary fire.
        await _try_advance(min_gap_hours)

        ranked_sessions, ranked_facts = await _retrieve(
            client,
            agent_id=agent_id,
            user_id=user_id,
            question=question.question,
            limit=retrieval_limit,
        )

        agent_answer = ""
        if include_qa:
            agent_answer = await _ask_question(
                client, agent_id=agent_id, user_id=user_id, question=question.question
            )

        return BackendResult(
            ranked_session_ids=ranked_sessions,
            ranked_fact_texts=ranked_facts,
            agent_answer=agent_answer,
            extra={
                "agent_id": agent_id,
                "advance_time_calls": advance_calls,
                "advance_time_failures": advance_failures,
                "consolidation_events": consolidation_events,
                "sessions_replayed": len(haystack),
                "skip_advance_time": skip_advance_time,
                "facts_retrieved": len(ranked_facts),
            },
        )
    finally:
        try:
            await client.agents.delete(agent_id)
        except Exception as e:
            logger.warning("agents.delete(%s) failed during cleanup: %s", agent_id, e)
