"""Sonzai backend for LongMemEval.

Uses the public Sonzai SDK end-to-end. Only one call differs from a normal
production integration: ``workbench.advance_time`` between sessions, which
runs the background CE workers (diary, consolidation, decay) as if simulated
time had passed. Without this, self-learning would only fire on the real clock.

Flow per question:

1. ``agents.create`` — fresh agent so memory state is scoped to this question.
2. For each haystack session (grouped by calendar date, in order):
   a. ``sessions.start`` with a deterministic session_id.
   b. Replay the canned user+assistant transcript via ``sessions.end(messages=...)``
      — no new text is generated; we're feeding LongMemEval's scripted history
      verbatim into the CE pipeline for fact extraction.
   c. At date boundaries only, ``workbench.advance_time`` runs
      ``((next_date - prev_date).days * 24h)`` simulated hours. Multiple
      sessions on the same calendar day share one clock tick — matches
      the real CE worker cadence (daily jobs per 24h, weekly consolidation
      per 7 days) without inflating the advance-time budget.
3. Final ``advance_time(24h)`` so the last day's diary/consolidation fires.
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
from ..dataset import LongMemEvalQuestion, Session
from . import BackendResult, RankedItem

logger = logging.getLogger(__name__)

# Flush budget after the last ingested session so the final day's daily
# jobs (diary, consolidation, decay) fire at least once before retrieval.
FINAL_FLUSH_HOURS = 24.0


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
    # ``wait=True`` asks the server to run the full OnSessionEnd pipeline
    # (segmentation, memory.ProcessSessionEnd for fact extraction, summary
    # storage, side-effects) synchronously before responding. Without this,
    # the pipeline runs in a detached goroutine with a 5-min budget — the
    # bench's next step (advance_time or the final memory.search) would
    # race the extractor and potentially measure an incomplete memory state.
    # This makes the dev-API session-end behave like the workbench's
    # SSE-waiting path: deterministic "data is ready" semantics.
    await sessions.end(
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_id,
        total_messages=len(messages),
        messages=messages,
        wait=True,
    )


async def _build_fact_to_session_map(
    client: AsyncSonzai, *, agent_id: str, user_id: str
) -> dict[str, str]:
    """Build ``fact_id → session_id`` from the agent's memory state.

    ``memory.search`` returns ``fact_id`` but not the source session, so we
    reconstruct the mapping. Both ``memory.timeline`` (per-fact
    ``AtomicFact.session_id``) and ``memory.list_facts`` (``Fact.session_id``
    / ``Fact.source_id``) now expose the source session directly. We still
    guard against the ``"unknown"`` bucket because ``memory.timeline``'s
    aggregation key falls back to that string when a fact predates server-
    side session tagging, and such pre-fix data may still linger. Facts
    don't move between sessions, so combining both sources cannot collide.
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
                sid = fact.session_id or fallback
                if fact.fact_id and sid and sid != "unknown":
                    mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.timeline failed: %s", e)

    # list_facts as a backstop — Fact.session_id is typed; source_id is the
    # secondary signal for facts whose session_id is empty (e.g., manually
    # created facts tagged only with the source message/episode).
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


async def _retrieve(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    question: str,
    limit: int,
    session_dates: dict[str, str],
) -> tuple[list[str], list[str], list[RankedItem]]:
    """Return ``(ranked_session_ids, ranked_fact_texts, ranked_items)`` for the question.

    Sonzai's memory is fact-oriented — retrieved facts are the first-class
    result. Session IDs are best-effort via a fact-to-session mapping (not
    always populated server-side). ``ranked_items`` is the MemPalace-compatible
    projection: one entry per retrieved fact, ``corpus_id`` set to the source
    session id when known (so session-level recall works), falling back to the
    fact_id so the item is still identifiable even when the mapping is sparse.
    """
    memory = async_memory(client)
    # Pass user_id so the server uses cosine-similarity semantic search over
    # fact embeddings instead of falling back to BM25 token search.
    results = await memory.search(
        agent_id=agent_id, user_id=user_id, query=question, limit=limit
    )
    fact_to_session = await _build_fact_to_session_map(
        client, agent_id=agent_id, user_id=user_id
    )

    seen: set[str] = set()
    ranked_sessions: list[str] = []
    ranked_facts: list[str] = []
    ranked_items: list[RankedItem] = []
    for r in results.results:
        if r.content:
            ranked_facts.append(r.content)
        sid = fact_to_session.get(r.fact_id, "")
        corpus_id = sid or r.fact_id
        ranked_items.append(
            RankedItem(
                corpus_id=corpus_id,
                text=(r.content or "")[:500],
                timestamp=session_dates.get(sid, ""),
            )
        )
        if sid and sid not in seen:
            seen.add(sid)
            ranked_sessions.append(sid)
    return ranked_sessions, ranked_facts, ranked_items


async def _ask_question(
    client: AsyncSonzai, *, agent_id: str, user_id: str, question: str
) -> tuple[str, dict]:
    """Send the question and return ``(agent_answer, diagnostic)``.

    We consume the SSE stream directly rather than go through the SDK's
    ``_chat_aggregate`` so we can capture the ``context_ready`` event's
    ``enriched_context`` payload — the authoritative view of what reached
    the prompt builder. Lets the benchmark's per-question diagnostics show
    the exact ``LoadedFacts`` count and preview, proving whether a fact the
    bench *retrieved* actually reaches the LLM's system prompt.

    Diagnostic dict shape::

        {
          "loaded_facts_count": int,
          "loaded_facts_preview": [first few fact texts],
          "build_duration_ms": int,
        }
    """
    from sonzai.types import ChatStreamEvent

    content_parts: list[str] = []
    diag: dict = {}
    # ``answer`` is what the bench calls the ground-truth for per-question
    # hit-detection in the diag. Populated from the caller's closure when
    # available — we keep it optional so callsites without an answer hint
    # still work.
    answer_text: str = ""
    try:
        async for event in client._http.stream_sse(  # type: ignore[attr-defined]
            "POST",
            f"/api/v1/agents/{agent_id}/chat",
            json_data={
                "messages": [{"role": "user", "content": question}],
                "user_id": user_id,
            },
        ):
            etype = str(event.get("type") or "")
            if etype == "context_ready":
                enriched = event.get("enriched_context") or {}
                loaded = list(enriched.get("loaded_facts") or enriched.get("LoadedFacts") or [])
                diag["loaded_facts_count"] = len(loaded)
                # Keep a short preview for at-a-glance inspection, but ALSO
                # scan every loaded fact for the answer text if we have it,
                # so the diag reports "answer present somewhere in
                # LoadedFacts" vs "answer absent". That's the signal that
                # separates "retrieval/injection broken" from "facts there
                # but render-sort demoting them".
                texts = [
                    str(f.get("atomic_text") or f.get("AtomicText") or "")
                    for f in loaded
                    if isinstance(f, dict)
                ]
                diag["loaded_facts_preview"] = [t[:200] for t in texts[:5]]
                # Keep the full text list too (capped) so downstream diag
                # scripts can do arbitrary analysis without another deploy.
                diag["loaded_facts_texts"] = [t[:300] for t in texts]
                if "build_duration_ms" in event:
                    diag["build_duration_ms"] = int(event["build_duration_ms"])
            else:
                # Content chunks arrive in OpenAI-compat form:
                #   {"choices":[{"delta":{"content":"..."}, ...}], ...}
                # Use the SDK's ChatStreamEvent validator so our parser
                # matches what client.agents.chat(stream=False) sees —
                # otherwise the raw ``event.get("content")`` misses
                # delta-style content and agent_answer comes back empty.
                try:
                    parsed = ChatStreamEvent.model_validate(event)
                except Exception:
                    parsed = None
                if parsed and parsed.content:
                    content_parts.append(str(parsed.content))
    except Exception as e:
        logger.debug("_ask_question stream failed, falling back to non-stream: %s", e)
        # Fallback — never let instrumentation break the bench.
        resp = await client.agents.chat(
            agent_id=agent_id,
            user_id=user_id,
            messages=[{"role": "user", "content": question}],
        )
        return getattr(resp, "content", "") or "", diag

    return "".join(content_parts), diag


async def run_question(
    client: AsyncSonzai,
    question: LongMemEvalQuestion,
    *,
    final_flush_hours: float = FINAL_FLUSH_HOURS,
    retrieval_limit: int = 50,
    include_qa: bool = True,
    skip_advance_time: bool = False,
    max_sessions: int = 0,
    existing_agent_id: str | None = None,
    existing_user_id: str | None = None,
    skip_ingest: bool = False,
    clear_memory_before_reuse: bool = False,
    keep_agent_alive: bool = False,
) -> BackendResult:
    """Ingest one LongMemEval question's haystack and evaluate Sonzai's memory.

    ``skip_advance_time=True`` disables self-learning simulation entirely —
    useful as a baseline. The delta between the normal run and this one is
    the measured effect of Sonzai's background CE workers.

    ``max_sessions > 0`` truncates the haystack for fast smoke runs; keeps
    answer-bearing sessions preferentially.

    **Reuse mode** (``existing_agent_id`` + ``existing_user_id``): skip
    agent creation, session replay, and all advance_time calls; reuse the
    pre-populated agent directly for retrieval + QA. Cuts per-question wall
    time from ~1–2 min to ~5–10 s, letting the outer iteration loop focus
    on chat-path fixes without re-ingesting haystacks each run. Set
    ``clear_memory_before_reuse=True`` to call ``memory.reset`` first if
    the reused state is stale and you want a clean slate (rarely needed —
    re-ingest in that case).

    ``keep_agent_alive`` suppresses the ``agents.delete`` cleanup so future
    reuse runs can pick the agent back up. Automatically true when an
    existing agent is passed in (never delete what we didn't create).

    Shared-agent model note: ``existing_agent_id`` can be the run-level
    shared agent while ``skip_ingest=False`` means "this user hasn't been
    populated yet, do the ingest under the shared agent". That's the
    difference between "agent exists" and "data for THIS user exists."
    """
    reuse = bool(skip_ingest) and existing_agent_id is not None

    # Model: Sonzai is multi-tenant by (agent_id, user_id). An agent in
    # production serves many users, each with their own memory scope. The
    # bench should reflect that: ONE shared agent answers all questions,
    # while each question gets its own user_id so memory stays isolated.
    # Caller passes ``existing_agent_id`` (the shared agent) and we
    # deterministically derive a per-question ``user_id`` from
    # ``question.question_id``. If no shared agent is provided the backend
    # falls back to the legacy per-question-agent path for backward-compat.
    user_id = f"lme-user-{question.question_id[:12]}"
    if existing_user_id:  # explicit override wins (rarely needed)
        user_id = str(existing_user_id)

    if existing_agent_id:
        agent_id = str(existing_agent_id)
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
    else:
        # Legacy path: per-question agent. Kept for callers that haven't
        # moved to the shared-agent bench model.
        agent_name = f"lme-{question.question_id[:12]}-{uuid.uuid4().hex[:6]}"
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

    if reuse and clear_memory_before_reuse:
        from ...common.sdk_extras import clear_agent_memory_async

        await clear_agent_memory_async(
            client, agent_id=agent_id, user_id=user_id
        )

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
        # Skip ingest + advance_time when reusing a pre-populated agent.
        # The outer iteration loop only changes the chat path; the agent's
        # memory state from the original ingest is still the authoritative
        # corpus for retrieval + QA on this question.
        if not reuse:
            # Group sessions by calendar date. advance_time runs only at date
            # boundaries, in whole-day increments. Same-day sessions share one
            # simulated clock — matches the CE worker model (daily jobs per
            # 24h of advance, weekly consolidation every 7 days) without
            # inflating the advance-time budget when the haystack contains
            # morning+evening chats on the same date.
            prev_date = None
            for session in haystack:
                sess_date = session.parsed_date.date()
                if prev_date is not None and sess_date != prev_date:
                    day_gap = (sess_date - prev_date).days
                    # advance_time_chunked_async splits into 24h chunks — an
                    # N-day gap yields N daily worker passes and triggers
                    # the weekly consolidation every 7 cumulative days.
                    await _try_advance(float(day_gap) * 24.0)

                # Use LongMemEval's own session IDs (e.g., "answer_280352e9",
                # "sharegpt_xxx_0") so memory.timeline groups extracted facts
                # under the same IDs that `answer_session_ids` references —
                # that's what session-level Recall@5 is scored against.
                await _replay_session(
                    client,
                    agent_id=agent_id,
                    user_id=user_id,
                    session_id=session.session_id,
                    session=session,
                )
                prev_date = sess_date

            # Final flush: one more day so the last date's diary/consolidation fires.
            await _try_advance(final_flush_hours)

        session_dates = {s.session_id: s.date for s in haystack}
        ranked_sessions, ranked_facts, ranked_items = await _retrieve(
            client,
            agent_id=agent_id,
            user_id=user_id,
            question=question.question,
            limit=retrieval_limit,
            session_dates=session_dates,
        )

        agent_answer = ""
        chat_diag: dict = {}
        if include_qa:
            agent_answer, chat_diag = await _ask_question(
                client, agent_id=agent_id, user_id=user_id, question=question.question
            )

        # Diagnostic: count facts actually stored for this (agent, user).
        # Helps distinguish "CE didn't extract the fact" from "search didn't
        # find it" or "advance-time pruned it".
        facts_stored = 0
        facts_sample: list[str] = []
        try:
            memory = async_memory(client)
            fact_list = await memory.list_facts(
                agent_id=agent_id, user_id=user_id, limit=500
            )
            facts_stored = len(fact_list.facts)
            facts_sample = [f.content for f in fact_list.facts[:5]]
        except Exception as e:
            logger.debug("memory.list_facts diagnostic failed: %s", e)

        return BackendResult(
            ranked_items=ranked_items,
            ranked_session_ids=ranked_sessions,
            ranked_fact_texts=ranked_facts,
            agent_answer=agent_answer,
            extra={
                "agent_id": agent_id,
                "user_id": user_id,
                "reused_agent": reuse,
                "session_ids_ingested": [s.session_id for s in haystack] if not reuse else [],
                "advance_time_calls": advance_calls,
                "advance_time_failures": advance_failures,
                "consolidation_events": consolidation_events,
                "sessions_replayed": 0 if reuse else len(haystack),
                "skip_advance_time": skip_advance_time,
                "facts_retrieved": len(ranked_facts),
                "facts_stored": facts_stored,
                "facts_sample": facts_sample,
                # Chat-path diagnostics captured from the SSE context_ready
                # event. ``loaded_facts_count`` + ``loaded_facts_preview``
                # show the exact fact set the prompt compiler saw — proves
                # whether a retrieved fact actually reaches the LLM.
                **({f"chat_{k}": v for k, v in chat_diag.items()} if chat_diag else {}),
            },
        )
    finally:
        # Never delete an agent we didn't create — reuse mode hands us an
        # existing one and may reuse it on the next iteration. Ingest mode
        # can opt into keep-alive via ``keep_agent_alive`` so the caller
        # can persist the snapshot and reuse on the next run.
        if not reuse and not keep_agent_alive:
            try:
                await client.agents.delete(agent_id)
            except Exception as e:
                logger.warning("agents.delete(%s) failed during cleanup: %s", agent_id, e)
