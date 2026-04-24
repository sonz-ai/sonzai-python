"""Sonzai backend for ConvoMem.

Flow per question:

1. Reuse the shared ConvoMem agent (pinned via ``ensure_convomem_agent_async``).
2. Derive ``user_id`` from ``question_id`` so memory stays isolated per-question
   under the shared agent — same model longmemeval uses.
3. For each conversation in ``question.conversations``:
   - ``sessions.start`` with a deterministic session_id.
   - ``sessions.end(messages=..., wait=True)`` — feed the canned transcript
     into the CE pipeline for fact extraction, synchronously. No per-message
     generation; we're testing memory, not chat.
   - **No** ``advance_time`` between conversations. ConvoMem has no dates;
     forcing gaps would be synthetic overhead.
4. **Single flush:** one ``advance_time(168h)`` after all conversations
   are ingested. That catches daily consolidation plus the ``sessionCount
   % 7 == 0`` weekly gate without paying the per-conversation advance-time
   cost (each call takes 1-5 minutes).
5. ``memory.search`` — diagnostic, not scored.
6. ``agents.chat`` — the headline QA path. SSE-stream consumed directly so
   we capture ``context_ready.loaded_facts`` for the MemScore context-token
   proxy.
"""

from __future__ import annotations

import logging
from sonzai import AsyncSonzai

from ...common.sdk_extras import async_memory, async_sessions, clear_agent_memory_async
from ...common.workbench_compat import advance_time_chunked_async
from ..dataset import ConvoMemQuestion, Conversation
from . import BackendResult

logger = logging.getLogger(__name__)

# Single post-ingest flush. 168h = 7 simulated days — catches daily
# consolidation + the sessionCount % 7 weekly gate.
DEFAULT_FLUSH_HOURS = 168.0

# Agent-metadata fact IDs follow a deterministic suffix pattern. We filter
# them from ranked_fact_texts for diagnostic clarity — same filter
# longmemeval applies. Not scored, but keeps the diagnostic clean.
_META_MARKERS = (":comm_style", ":side_effect:", ":interest:")


def _is_metadata_fact(fact_id: str) -> bool:
    return any(m in fact_id for m in _META_MARKERS)


async def _replay_conversation(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    conv: Conversation,
) -> None:
    """Feed one ConvoMem conversation into Sonzai via sessions.end(wait=True)."""
    sessions = async_sessions(client)
    await sessions.start(
        agent_id=agent_id, user_id=user_id, session_id=conv.conversation_id,
    )
    await sessions.end(
        agent_id=agent_id,
        user_id=user_id,
        session_id=conv.conversation_id,
        total_messages=len(conv.messages),
        messages=[{"role": m.role, "content": m.content} for m in conv.messages],
        wait=True,
    )


async def _retrieve(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    question: str,
    limit: int,
) -> list[str]:
    """Run memory.search — diagnostic only, not scored against ground truth."""
    memory = async_memory(client)
    results = await memory.search(
        agent_id=agent_id, user_id=user_id, query=question, limit=limit,
    )
    return [
        r.content
        for r in results.results
        if r.content and not _is_metadata_fact(r.fact_id)
    ]


async def _ask_question(
    client: AsyncSonzai, *, agent_id: str, user_id: str, question: str,
) -> tuple[str, dict]:
    """Consume the /chat SSE stream directly so we can capture context_ready.

    Diagnostics captured::

        {
          "loaded_facts_count": int,
          "loaded_facts_preview": [first 5 fact texts, 200 chars each],
          "loaded_facts_texts":   [all loaded fact texts, 300 chars each],
          "build_duration_ms":    int,
        }
    """
    from sonzai.types import ChatStreamEvent

    content_parts: list[str] = []
    diag: dict = {}
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
                texts = [
                    str(f.get("atomic_text") or f.get("AtomicText") or "")
                    for f in loaded
                    if isinstance(f, dict)
                ]
                diag["loaded_facts_count"] = len(loaded)
                diag["loaded_facts_preview"] = [t[:200] for t in texts[:5]]
                diag["loaded_facts_texts"] = [t[:300] for t in texts]
                if "build_duration_ms" in event:
                    diag["build_duration_ms"] = int(event["build_duration_ms"])
            else:
                try:
                    parsed = ChatStreamEvent.model_validate(event)
                except Exception:
                    parsed = None
                if parsed and parsed.content:
                    content_parts.append(str(parsed.content))
    except Exception as e:
        logger.debug("_ask_question stream failed, falling back to non-stream: %s", e)
        resp = await client.agents.chat(
            agent_id=agent_id,
            user_id=user_id,
            messages=[{"role": "user", "content": question}],
        )
        return getattr(resp, "content", "") or "", diag

    return "".join(content_parts), diag


async def run_question(
    client: AsyncSonzai,
    question: ConvoMemQuestion,
    *,
    existing_agent_id: str,
    existing_user_id: str | None = None,
    include_qa: bool = True,
    skip_advance_time: bool = False,
    skip_ingest: bool = False,
    clear_memory_before_reuse: bool = False,
    flush_hours: float = DEFAULT_FLUSH_HOURS,
    retrieval_limit: int = 50,
) -> BackendResult:
    """Run one ConvoMem question end-to-end against Sonzai.

    ``existing_agent_id`` is the shared ConvoMem agent (see
    :func:`sonzai.benchmarks.ensure_convomem_agent_async`). Each question
    scopes its memory under a deterministic per-question ``user_id``.

    ``skip_advance_time=True`` → pure session-end path (no CE worker sim).
    Produces a baseline; the delta vs a normal run is the measured lift.

    ``skip_ingest=True`` (reuse mode) → retrieval + QA only, assumes the
    agent/user pair was populated in a prior run. Controlled by the
    orchestrator via ``--reuse-agents``.
    """
    user_id = existing_user_id or f"convomem-user-{question.question_id[:16]}"
    agent_id = str(existing_agent_id)

    advance_calls = 0
    consolidation_events = 0
    advance_failures = 0

    # Idempotency: wipe prior-run memory for this (agent, user) before
    # re-ingesting, so rerunning the bench with the same question_id lands
    # on a clean state. Skipped in reuse mode unless explicitly asked for.
    if not skip_ingest:
        await clear_agent_memory_async(client, agent_id=agent_id, user_id=user_id)
    elif clear_memory_before_reuse:
        await clear_agent_memory_async(client, agent_id=agent_id, user_id=user_id)

    # ── Ingest ───────────────────────────────────────────────────────────
    if not skip_ingest:
        for conv in question.conversations:
            await _replay_conversation(
                client, agent_id=agent_id, user_id=user_id, conv=conv,
            )

    # ── Single flush ────────────────────────────────────────────────────
    if not skip_ingest and not skip_advance_time and flush_hours > 0:
        try:
            results = await advance_time_chunked_async(
                client, agent_id=agent_id, user_id=user_id, total_hours=flush_hours,
            )
            advance_calls = len(results)
            consolidation_events = sum(1 for r in results if r.consolidation_ran)
        except Exception as e:
            advance_failures += 1
            logger.warning(
                "advance_time(%s, %.1fh) failed (non-fatal): %s",
                agent_id, flush_hours, e,
            )

    # ── Retrieval (diagnostic) ──────────────────────────────────────────
    ranked_facts: list[str] = []
    try:
        ranked_facts = await _retrieve(
            client,
            agent_id=agent_id,
            user_id=user_id,
            question=question.question,
            limit=retrieval_limit,
        )
    except Exception as e:
        logger.debug("memory.search failed (diagnostic only): %s", e)

    # ── QA (headline) ───────────────────────────────────────────────────
    agent_answer = ""
    chat_diag: dict = {}
    if include_qa:
        agent_answer, chat_diag = await _ask_question(
            client, agent_id=agent_id, user_id=user_id, question=question.question,
        )

    # Stored-fact count diagnostic.
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
        agent_answer=agent_answer,
        ranked_fact_texts=ranked_facts,
        extra={
            "agent_id": agent_id,
            "user_id": user_id,
            "reused_agent": skip_ingest,
            "conversations_ingested": 0 if skip_ingest else len(question.conversations),
            "advance_time_calls": advance_calls,
            "advance_time_failures": advance_failures,
            "consolidation_events": consolidation_events,
            "skip_advance_time": skip_advance_time,
            "facts_retrieved": len(ranked_facts),
            "facts_stored": facts_stored,
            "facts_sample": facts_sample,
            **({f"chat_{k}": v for k, v in chat_diag.items()} if chat_diag else {}),
        },
    )
