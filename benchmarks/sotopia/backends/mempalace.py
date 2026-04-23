"""MemPalace SOTOPIA backend.

Pairs MemPalace's verbatim retrieval with Gemini Flash Lite (the same model
Sonzai's chat handler uses server-side) so the longitudinal comparison
isolates the memory layer, not the LLM.

Per-scenario state lives on disk:

- palace: ``<root>/mempalace_palaces/<scenario_id>/`` — ChromaDB-backed drawers
- convos: ``<root>/mempalace_convos/<scenario_id>/`` — one ``.md`` per session,
  formatted in MemPalace's ``> Partner: …`` / agent-reply convention so
  ``chunk_exchanges`` pairs them into exchange-level drawers.

Flow per session:

1. Generate partner turn via ``partner_turn_async`` (shared with Sonzai path).
2. Search the palace for top-K drawers against the partner utterance.
3. Generate the agent turn via ``agent_turn_async`` with the drawers injected
   as ``# What you remember from past sessions`` context.
4. After the turn loop, write the transcript to ``session_<idx>.md`` and
   call ``mine_convos`` on the scenario's convos dir — idempotent via
   ``file_already_mined``, so re-mining is cheap.

No ``advance_time`` hook: MemPalace has no simulated time / consolidation
clock. Session gaps exist only as separate files in the convos dir.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from tqdm import tqdm

from ..scenarios import Scenario
from ..scoring import SessionRun

logger = logging.getLogger("benchmarks.sotopia.mempalace")

# --- MemPalace import ------------------------------------------------------
# MemPalace is expected as a sibling checkout at ``sonzai-sdk/mempalace``
# (same convention as the LongMemEval backend). Import eagerly so the error
# surface on missing checkout is a clear message at runtime, not a cryptic
# traceback mid-scenario.
def _import_mempalace():
    try:
        from mempalace import convo_miner, searcher  # type: ignore

        return convo_miner, searcher
    except ImportError as e:
        sibling = (
            Path(__file__).resolve().parents[4]  # sotopia/backends/mempalace.py
            / "mempalace"
        )
        if sibling.exists():
            sys.path.insert(0, str(sibling))
            from mempalace import convo_miner, searcher  # type: ignore

            return convo_miner, searcher
        raise RuntimeError(
            "mempalace package not importable and no sibling checkout at "
            f"{sibling}. Either `pip install mempalace` or clone the repo "
            "alongside sonzai-python."
        ) from e


_convo_miner, _searcher = _import_mempalace()


DEFAULT_SEARCH_K = 5
DEFAULT_MAX_DRAWER_CHARS = 600  # per drawer when formatting into the prompt


# ---------------------------------------------------------------------------
# Palace paths
# ---------------------------------------------------------------------------


def _bench_root() -> Path:
    override = os.environ.get("SONZAI_BENCH_CACHE")
    base = Path(override).expanduser() if override else Path.home() / ".cache" / "sonzai-bench"
    return base / "sotopia-mempalace"


def _scenario_paths(scenario_id: str) -> tuple[Path, Path]:
    root = _bench_root()
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", scenario_id)[:64]
    palace = root / "palaces" / safe
    convos = root / "convos" / safe
    palace.mkdir(parents=True, exist_ok=True)
    convos.mkdir(parents=True, exist_ok=True)
    # Eagerly create the drawers collection so session-1 searches (which run
    # before any mine_convos call) return an empty result set instead of
    # logging a "collection does not exist" error on every turn.
    try:
        from mempalace.palace import get_collection  # type: ignore

        get_collection(str(palace), create=True)
    except Exception as e:  # pragma: no cover — defensive, non-fatal
        logger.debug("pre-create palace collection failed for %s: %s", safe, e)
    return palace, convos


# ---------------------------------------------------------------------------
# Memory formatting helpers
# ---------------------------------------------------------------------------


def _format_retrieved(hits: list[dict[str, Any]], max_chars: int) -> str:
    if not hits:
        return ""
    lines: list[str] = []
    for i, h in enumerate(hits, 1):
        text = (h.get("text") or "").strip()
        if not text:
            continue
        if len(text) > max_chars:
            text = text[:max_chars].rstrip() + "…"
        sim = h.get("similarity")
        header = f"[{i}]" + (f" (sim={sim})" if isinstance(sim, (int, float)) else "")
        lines.append(f"{header}\n{text}")
    return "\n\n".join(lines)


async def _search_memories_async(query: str, palace_path: str, n_results: int):
    """Run MemPalace's sync searcher in a thread so we don't block the loop."""

    def _run():
        try:
            return _searcher.search_memories(
                query=query,
                palace_path=palace_path,
                n_results=n_results,
            )
        except Exception as e:
            logger.warning("mempalace search failed: %s", e)
            return {"results": []}

    result = await asyncio.to_thread(_run)
    if isinstance(result, dict) and result.get("results"):
        return list(result["results"])
    return []


async def _mine_convos_async(convos_dir: Path, palace_path: Path) -> None:
    def _run():
        try:
            _convo_miner.mine_convos(
                str(convos_dir),
                str(palace_path),
                wing="sotopia",
                agent="mempalace",
                extract_mode="exchange",
            )
        except Exception as e:
            logger.warning("mempalace mine_convos failed: %s", e)

    await asyncio.to_thread(_run)


def _write_session_file(
    convos_dir: Path,
    session_index: int,
    transcript: list[dict[str, str]],
) -> Path:
    """Write a transcript to disk in MemPalace's ``> user``/reply convention."""
    path = convos_dir / f"session_{session_index:03d}.md"
    lines: list[str] = [f"# Session {session_index}", ""]
    for turn in transcript:
        content = (turn.get("content") or "").strip()
        if not content:
            continue
        role = turn.get("role", "user")
        if role == "user":
            lines.append(f"> {content}")
        else:
            lines.append(content)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Session + scenario orchestration
# ---------------------------------------------------------------------------


async def _simulate_session_mempalace(
    *,
    scenario: Scenario,
    session_index: int,
    palace_path: Path,
    convos_dir: Path,
    judge,  # GeminiJudge — cyclic import avoided by duck-typing
    search_k: int,
    max_drawer_chars: int,
    prior_sessions_summary: str = "",
) -> list[dict[str, str]]:
    """Run one scenario session with MemPalace retrieval + Gemini generation."""
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

        # Retrieve MemPalace context for the agent's reply. Only searches
        # drawers ingested from prior session files, which is exactly what
        # a "learning across sessions" measurement needs — nothing from the
        # in-flight session leaks into its own retrieval.
        hits = await _search_memories_async(
            query=partner.content,
            palace_path=str(palace_path),
            n_results=search_k,
        )
        retrieved = _format_retrieved(hits, max_drawer_chars)

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

    # Persist the session transcript and ingest it so future sessions can
    # retrieve from it. mine_convos is idempotent (file_already_mined guards
    # re-mining), so it's safe to call after every session.
    _write_session_file(convos_dir, session_index, transcript)
    await _mine_convos_async(convos_dir, palace_path)

    return transcript


async def _run_scenario_mempalace(
    *,
    scenario: Scenario,
    sessions_per_scenario: int,
    judge,
    search_k: int,
    max_drawer_chars: int,
) -> list[SessionRun]:
    """Run N sessions for one scenario, score each, persist palace state."""
    from ...common.gemini_judge import judge_sotopia_async, summarize_session_async
    from ..run import _PRIOR_SUMMARY_WINDOW, _format_prior_summaries

    palace_path, convos_dir = _scenario_paths(scenario.scenario_id)

    # Resume: palace contents + convos dir are persistent across runs. Start
    # at max(existing session_NNN.md) + 1 so calling `--sessions-per-scenario
    # 60` after a prior `30` continues the trajectory instead of redoing
    # session 1 with an already-populated palace. Matches the Sonzai
    # --reuse-agents semantics.
    existing = sorted(convos_dir.glob("session_*.md"))
    last_idx = 0
    if existing:
        try:
            last_idx = int(existing[-1].stem.split("_")[-1])
        except Exception:
            last_idx = 0
    start_idx = max(1, last_idx + 1)
    if start_idx > sessions_per_scenario:
        logger.info(
            "mempalace scenario %s already at session %d ≥ target %d — nothing to do",
            scenario.scenario_id, last_idx, sessions_per_scenario,
        )
        return []
    logger.info(
        "mempalace scenario %s palace=%s (resume from %d → %d)",
        scenario.scenario_id, palace_path, start_idx, sessions_per_scenario,
    )

    # Rolling prior-session summaries for the partner + judge prompts.
    # Same accumulation strategy as the Sonzai backend — stays in memory
    # for the duration of this run. Resume across invocations doesn't
    # carry this forward; run fresh for the clean longitudinal curve.
    prior_summaries: list[str] = []

    runs: list[SessionRun] = []
    for idx in range(start_idx, sessions_per_scenario + 1):
        prior_block = _format_prior_summaries(prior_summaries)
        transcript = await _simulate_session_mempalace(
            scenario=scenario,
            session_index=idx,
            palace_path=palace_path,
            convos_dir=convos_dir,
            judge=judge,
            search_k=search_k,
            max_drawer_chars=max_drawer_chars,
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
                "mempalace session summarizer failed on %s s%d: %s",
                scenario.scenario_id, idx, e,
            )
            prior_summaries.append("(summary unavailable)")
    return runs


async def run_all_scenarios_mempalace(
    *,
    scenarios: list[Scenario],
    sessions_per_scenario: int,
    scenario_concurrency: int,
    judge,
    search_k: int = DEFAULT_SEARCH_K,
    max_drawer_chars: int = DEFAULT_MAX_DRAWER_CHARS,
) -> list[SessionRun]:
    sem = asyncio.Semaphore(scenario_concurrency)

    async def _one(sc: Scenario) -> list[SessionRun]:
        async with sem:
            try:
                return await _run_scenario_mempalace(
                    scenario=sc,
                    sessions_per_scenario=sessions_per_scenario,
                    judge=judge,
                    search_k=search_k,
                    max_drawer_chars=max_drawer_chars,
                )
            except Exception:
                logger.exception("mempalace scenario %s failed", sc.scenario_id)
                return []

    grouped = await asyncio.gather(
        *(_one(sc) for sc in tqdm(scenarios, desc="scenarios", unit="sc"))
    )
    out: list[SessionRun] = []
    for g in grouped:
        out.extend(g)
    return out


__all__ = ["run_all_scenarios_mempalace"]
