"""mem0 cloud SOTOPIA backend.

Pairs mem0's hosted memory API with Gemini Flash Lite (the same model Sonzai
and the MemPalace backend use for agent/partner turns) so the longitudinal
comparison isolates the memory layer, not the LLM.

Flow per session, per scenario user_id:

1. Generate partner turn via ``partner_turn_async`` (shared with Sonzai /
   MemPalace paths — same prompt, same generator).
2. Call ``mem0.search(partner_utterance, user_id=…)`` for top-K memories.
3. Generate the agent turn via ``agent_turn_async`` with the memories
   injected as ``# What you remember from past sessions`` context.
4. After the session, ``mem0.add(messages, user_id=…)`` ingests the full
   transcript. mem0 does its own LLM extraction server-side.

No ``advance_time`` hook: mem0 has no simulated-time / consolidation
concept. Session gaps are just separate ``add`` calls.

**Optional dependency** — ``mem0ai`` is imported lazily, so installing the
``sonzai`` package or running Sonzai-only benchmarks never pulls it in. The
error on missing package names the one-line install.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

from tqdm import tqdm

from ..scenarios import Scenario
from ..scoring import SessionRun

logger = logging.getLogger("benchmarks.sotopia.mem0")


# --- mem0 import -----------------------------------------------------------
# Lazy: only imported when this backend is actually instantiated. Keeps the
# sonzai SDK install path and other-backend bench runs clean.
def _import_mem0():
    try:
        from mem0 import AsyncMemoryClient  # type: ignore

        return AsyncMemoryClient
    except ImportError as e:
        raise RuntimeError(
            "mem0ai package not installed. Install with `pip install mem0ai` "
            "(only needed when running `--backend mem0`)."
        ) from e


DEFAULT_SEARCH_K = 5
DEFAULT_MAX_MEMORY_CHARS = 600  # per hit when formatting into the prompt
DEFAULT_INGEST_WAIT = 3.0  # seconds to wait after add() for async ingest
MAX_429_RETRIES = 6
BASE_429_BACKOFF = 2.0  # seconds


# ---------------------------------------------------------------------------
# mem0 namespacing
# ---------------------------------------------------------------------------


def _user_id_for(scenario_id: str) -> str:
    """Stable per-scenario user_id. Scopes mem0 memories to this benchmark run
    of this scenario so cross-scenario memories never leak. The prefix is long
    enough to avoid collisions with real users of the same mem0 account."""
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", scenario_id)[:48]
    return f"sonzai-sotopia-bench-{safe}"


def _state_root() -> Path:
    override = os.environ.get("SONZAI_BENCH_CACHE")
    base = Path(override).expanduser() if override else Path.home() / ".cache" / "sonzai-bench"
    return base / "sotopia-mem0"


def _progress_path(scenario_id: str) -> Path:
    root = _state_root()
    root.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", scenario_id)[:64]
    return root / f"{safe}.progress"


def _read_progress(scenario_id: str) -> int:
    p = _progress_path(scenario_id)
    if not p.is_file():
        return 0
    try:
        return int(p.read_text().strip())
    except Exception:
        return 0


def _write_progress(scenario_id: str, session_index: int) -> None:
    _progress_path(scenario_id).write_text(str(session_index))


# ---------------------------------------------------------------------------
# Memory formatting + rate-limit-aware wrappers
# ---------------------------------------------------------------------------


def _format_retrieved(hits: list[dict[str, Any]], max_chars: int) -> str:
    if not hits:
        return ""
    lines: list[str] = []
    for i, h in enumerate(hits, 1):
        text = (h.get("memory") or h.get("text") or "").strip()
        if not text:
            continue
        if len(text) > max_chars:
            text = text[:max_chars].rstrip() + "…"
        score = h.get("score")
        header = f"[{i}]" + (f" (score={score:.3f})" if isinstance(score, (int, float)) else "")
        lines.append(f"{header}\n{text}")
    return "\n\n".join(lines)


async def _search_with_retry(client, *, query: str, user_id: str, limit: int) -> list[dict[str, Any]]:
    """mem0 cloud is aggressive with 429s — back off exponentially."""
    for attempt in range(MAX_429_RETRIES):
        try:
            res = await client.search(query, user_id=user_id, limit=limit, output_format="v1.1")
            if isinstance(res, dict):
                res = res.get("results") or []
            return list(res or [])
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt + 1 < MAX_429_RETRIES:
                backoff = BASE_429_BACKOFF * (2**attempt)
                logger.info("mem0 search 429 — backing off %.1fs (attempt %d)", backoff, attempt + 1)
                await asyncio.sleep(backoff)
                continue
            logger.warning("mem0 search failed (non-retryable): %s", e)
            return []
    logger.warning("mem0 search: exhausted retries for user_id=%s", user_id)
    return []


async def _add_with_retry(client, *, messages: list[dict[str, str]], user_id: str) -> None:
    """Add session transcript to mem0. Server does async extraction — returns
    PENDING — so callers may want to pause before the next search."""
    for attempt in range(MAX_429_RETRIES):
        try:
            await client.add(messages, user_id=user_id, output_format="v1.1")
            return
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt + 1 < MAX_429_RETRIES:
                backoff = BASE_429_BACKOFF * (2**attempt)
                logger.info("mem0 add 429 — backing off %.1fs (attempt %d)", backoff, attempt + 1)
                await asyncio.sleep(backoff)
                continue
            logger.warning("mem0 add failed (non-retryable): %s", e)
            return


# ---------------------------------------------------------------------------
# Session + scenario orchestration
# ---------------------------------------------------------------------------


async def _simulate_session_mem0(
    *,
    scenario: Scenario,
    session_index: int,
    user_id: str,
    client,
    judge,  # GeminiJudge — duck-typed to avoid cyclic import
    search_k: int,
    max_memory_chars: int,
    ingest_wait: float,
    prior_sessions_summary: str = "",
) -> list[dict[str, str]]:
    """Run one scenario session with mem0 retrieval + Gemini generation."""
    from ...common.gemini_judge import agent_turn_async, partner_turn_async

    scenario_text = (
        f"{scenario.setting}\n\n{scenario.partner.name}: {scenario.partner.background}"
    )

    transcript: list[dict[str, str]] = []
    for _turn in range(scenario.max_turns):
        partner_transcript_text = (
            "\n".join(
                f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
                for t in transcript
            )
            if transcript
            else ""
        )

        try:
            partner = await partner_turn_async(
                judge,
                scenario=scenario_text,
                transcript_text=partner_transcript_text,
                partner_name=scenario.partner.name,
                partner_goal=scenario.partner.goal,
                partner_secret=scenario.partner.secret,
                agent_name=scenario.agent.name,
                prior_sessions_summary=prior_sessions_summary,
            )
        except Exception as e:
            logger.warning("partner_turn failed: %s — ending session early", e)
            break

        transcript.append({"role": "user", "content": partner.content})
        if partner.end_conversation:
            break

        # Retrieve mem0 memories for the agent's reply. Only returns whatever
        # mem0 extracted from prior `add` calls — nothing from the in-flight
        # session leaks into its own retrieval.
        hits = await _search_with_retry(
            client, query=partner.content, user_id=user_id, limit=search_k
        )
        retrieved = _format_retrieved(hits, max_memory_chars)

        agent_transcript_text = "\n".join(
            f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
            for t in transcript
        )
        try:
            reply = await agent_turn_async(
                judge,
                scenario=scenario_text,
                transcript_text=agent_transcript_text,
                agent_name=scenario.agent.name,
                agent_background=scenario.agent.background,
                agent_goal=scenario.agent.goal,
                agent_secret=scenario.agent.secret,
                partner_name=scenario.partner.name,
                retrieved_memories=retrieved,
            )
        except Exception as e:
            logger.warning("agent_turn failed: %s — ending session early", e)
            break

        transcript.append({"role": "assistant", "content": reply.content})

    # Ingest the full session transcript. mem0 does its own fact extraction
    # server-side; we wait a beat so the extraction completes before the next
    # session's search runs.
    mem_messages = [
        {
            "role": "user" if t["role"] == "user" else "assistant",
            "content": t["content"],
        }
        for t in transcript
        if t.get("content")
    ]
    if mem_messages:
        await _add_with_retry(client, messages=mem_messages, user_id=user_id)
        await asyncio.sleep(ingest_wait)

    return transcript


async def _run_scenario_mem0(
    *,
    scenario: Scenario,
    sessions_per_scenario: int,
    client,
    judge,
    search_k: int,
    max_memory_chars: int,
    ingest_wait: float,
) -> list[SessionRun]:
    """Run N sessions for one scenario, score each, persist mem0 state."""
    from ...common.gemini_judge import judge_sotopia_async, summarize_session_async
    from ..run import _format_prior_summaries

    user_id = _user_id_for(scenario.scenario_id)

    # Resume: mem0 state is stored server-side; we track local progress in a
    # small file so `--sessions-per-scenario 90` after a `30` run continues
    # the trajectory instead of redoing session 1 with a populated palace.
    last_idx = _read_progress(scenario.scenario_id)
    start_idx = max(1, last_idx + 1)
    if start_idx > sessions_per_scenario:
        logger.info(
            "mem0 scenario %s already at session %d ≥ target %d — nothing to do",
            scenario.scenario_id, last_idx, sessions_per_scenario,
        )
        return []
    logger.info(
        "mem0 scenario %s user_id=%s (resume from %d → %d)",
        scenario.scenario_id, user_id, start_idx, sessions_per_scenario,
    )

    prior_summaries: list[str] = []
    runs: list[SessionRun] = []
    for idx in range(start_idx, sessions_per_scenario + 1):
        prior_block = _format_prior_summaries(prior_summaries)
        transcript = await _simulate_session_mem0(
            scenario=scenario,
            session_index=idx,
            user_id=user_id,
            client=client,
            judge=judge,
            search_k=search_k,
            max_memory_chars=max_memory_chars,
            ingest_wait=ingest_wait,
            prior_sessions_summary=prior_block,
        )

        transcript_text = "\n".join(
            f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
            for t in transcript
        )
        try:
            score = await judge_sotopia_async(
                judge,
                scenario=f"{scenario.setting}\n\nAgent ({scenario.agent.name}): "
                f"{scenario.agent.background}",
                transcript=transcript_text,
                agent_name=scenario.agent.name,
                agent_goal=scenario.agent.goal,
                agent_secret=scenario.agent.secret,
                prior_sessions_summary=prior_block,
            )
        except Exception:
            logger.exception("sotopia judge failed on %s s%d", scenario.scenario_id, idx)
            continue

        runs.append(
            SessionRun(
                scenario_id=scenario.scenario_id,
                session_index=idx,
                transcript=transcript,
                score=score,
            )
        )
        _write_progress(scenario.scenario_id, idx)

        try:
            summary = await summarize_session_async(
                judge,
                transcript_text=transcript_text,
                agent_name=scenario.agent.name,
                partner_name=scenario.partner.name,
            )
            prior_summaries.append(summary.summary)
        except Exception as e:
            logger.warning(
                "mem0 session summarizer failed on %s s%d: %s",
                scenario.scenario_id, idx, e,
            )
            prior_summaries.append("(summary unavailable)")
    return runs


async def run_all_scenarios_mem0(
    *,
    scenarios: list[Scenario],
    sessions_per_scenario: int,
    scenario_concurrency: int,
    judge,
    search_k: int = DEFAULT_SEARCH_K,
    max_memory_chars: int = DEFAULT_MAX_MEMORY_CHARS,
    ingest_wait: float = DEFAULT_INGEST_WAIT,
) -> list[SessionRun]:
    AsyncMemoryClient = _import_mem0()
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY is required for --backend mem0.")
    client = AsyncMemoryClient(api_key=api_key)

    sem = asyncio.Semaphore(scenario_concurrency)

    async def _one(sc: Scenario) -> list[SessionRun]:
        async with sem:
            try:
                return await _run_scenario_mem0(
                    scenario=sc,
                    sessions_per_scenario=sessions_per_scenario,
                    client=client,
                    judge=judge,
                    search_k=search_k,
                    max_memory_chars=max_memory_chars,
                    ingest_wait=ingest_wait,
                )
            except Exception:
                logger.exception("mem0 scenario %s failed", sc.scenario_id)
                return []

    grouped = await asyncio.gather(
        *(_one(sc) for sc in tqdm(scenarios, desc="scenarios", unit="sc"))
    )
    out: list[SessionRun] = []
    for g in grouped:
        out.extend(g)
    return out


__all__ = ["run_all_scenarios_mem0"]
