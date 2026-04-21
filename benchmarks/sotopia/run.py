"""SOTOPIA longitudinal runner.

For each scenario:

- Create ONE fresh Sonzai agent with the scenario's agent character profile.
- Create ONE synthetic user_id for the scenario's partner character.
- Loop N times (default 30):
    - ``sessions.start`` with a new session_id.
    - Alternate turns: Gemini generates the partner's utterance, Sonzai
      generates the agent's reply via ``agents.chat``.
    - ``sessions.end`` with the full transcript.
    - ``workbench.advance_time(25h)`` so consolidation/diary/decay fire.
    - Score this session with the SOTOPIA 7-dim rubric via Gemini.

Output is two artifacts:
- ``results/sotopia_<ts>.jsonl`` — one row per (scenario, session_index).
- ``results/sotopia_<ts>_trajectory.png`` — matplotlib chart per dimension,
  session 1 → N, averaged across scenarios.

Headline metric: Δoverall between session 1 and session N. A positive delta
with scenario-level consistency means self-learning is working.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sonzai import AsyncSonzai
from tqdm import tqdm

from ..common.gemini_judge import (
    DEFAULT_MODEL as DEFAULT_JUDGE_MODEL,
    GeminiJudge,
    judge_sotopia_async,
    partner_turn_async,
)
from ..common.sdk_extras import async_sessions
from ..common.workbench_compat import advance_time_chunked_async
from .scenarios import Scenario, load_scenarios
from .scoring import SCORE_DIMS, SessionRun, snapshot, trajectory_per_dimension

logger = logging.getLogger("benchmarks.sotopia")

MIN_GAP_HOURS = 25.0


# ---------------------------------------------------------------------------
# Session simulation
# ---------------------------------------------------------------------------


async def _simulate_session(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    session_id: str,
    scenario: Scenario,
    judge: GeminiJudge,
) -> list[dict[str, str]]:
    """Run one scenario session and return the transcript."""
    sessions = async_sessions(client)
    await sessions.start(agent_id=agent_id, user_id=user_id, session_id=session_id)

    scenario_text = (
        f"{scenario.setting}\n\n"
        f"{scenario.partner.name}: {scenario.partner.background}"
    )

    transcript: list[dict[str, str]] = []
    for _turn in range(scenario.max_turns):
        partner_text = (
            "\n".join(f"{t['role']}: {t['content']}" for t in transcript)
            if transcript
            else ""
        )
        try:
            partner = await partner_turn_async(
                judge,
                scenario=scenario_text,
                transcript_text=partner_text,
                partner_name=scenario.partner.name,
                partner_goal=scenario.partner.goal,
                partner_secret=scenario.partner.secret,
            )
        except Exception as e:
            logger.warning("partner_turn failed: %s — ending session early", e)
            break

        transcript.append({"role": "user", "content": partner.content})
        if partner.end_conversation:
            break

        try:
            agent_resp = await client.agents.chat(
                agent_id=agent_id,
                user_id=user_id,
                session_id=session_id,
                messages=[{"role": "user", "content": partner.content}],
            )
        except Exception as e:
            logger.warning("agents.chat failed: %s — ending session early", e)
            break

        agent_text = getattr(agent_resp, "content", "") or ""
        transcript.append({"role": "assistant", "content": agent_text})

    try:
        await sessions.end(
            agent_id=agent_id,
            user_id=user_id,
            session_id=session_id,
            total_messages=len(transcript),
        )
    except Exception as e:
        logger.warning("sessions.end failed (non-fatal): %s", e)

    return transcript


# ---------------------------------------------------------------------------
# Scenario orchestration
# ---------------------------------------------------------------------------


async def _run_scenario(
    client: AsyncSonzai,
    *,
    scenario: Scenario,
    sessions_per_scenario: int,
    judge: GeminiJudge,
    min_gap_hours: float,
) -> list[SessionRun]:
    """Run N sessions for one scenario, score each, advance time between."""
    agent_name = f"sotopia-{scenario.scenario_id[:16]}-{uuid.uuid4().hex[:6]}"
    user_id = f"sotopia-user-{scenario.scenario_id[:16]}"

    agent = await client.agents.create(
        name=agent_name,
        personality_prompt=(
            f"You are {scenario.agent.name}. {scenario.agent.background} "
            f"Your goal in interactions with {scenario.partner.name}: "
            f"{scenario.agent.goal}"
        ),
        true_interests=[],
        true_dislikes=[],
    )
    agent_id = agent.agent_id
    runs: list[SessionRun] = []

    try:
        for idx in range(1, sessions_per_scenario + 1):
            session_id = f"{scenario.scenario_id}-s{idx:02d}-{uuid.uuid4().hex[:4]}"
            transcript = await _simulate_session(
                client,
                agent_id=agent_id,
                user_id=user_id,
                session_id=session_id,
                scenario=scenario,
                judge=judge,
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
                )
            except Exception as e:
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

            if idx < sessions_per_scenario:
                try:
                    await advance_time_chunked_async(
                        client,
                        agent_id=agent_id,
                        user_id=user_id,
                        total_hours=min_gap_hours,
                    )
                except Exception as e:
                    logger.warning("advance_time failed between sessions: %s", e)
    finally:
        try:
            await client.agents.delete(agent_id)
        except Exception as e:
            logger.warning("agents.delete(%s) cleanup failed: %s", agent_id, e)

    return runs


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _write_runs_jsonl(path: Path, runs: list[SessionRun]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in runs:
            row: dict[str, Any] = {
                "scenario_id": r.scenario_id,
                "session_index": r.session_index,
                "transcript": r.transcript,
                "score": asdict(r.score)
                if hasattr(r.score, "__dataclass_fields__")
                else r.score.model_dump(),
            }
            f.write(json.dumps(row) + "\n")


def _plot_trajectory(path: Path, runs: list[SessionRun]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not installed — skipping trajectory chart")
        return

    traj = trajectory_per_dimension(runs)
    if not traj or not any(traj.values()):
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    xs = list(range(1, len(next(iter(traj.values()))) + 1))
    for dim in SCORE_DIMS:
        ys = traj[dim]
        if ys:
            ax.plot(xs, ys, marker="o", linewidth=1.5, label=dim)
    ax.set_xlabel("Session index")
    ax.set_ylabel("Score (per-dim range)")
    ax.set_title("Sonzai SOTOPIA longitudinal — score vs session")
    ax.legend(loc="best", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _print_summary(runs: list[SessionRun], at_sessions: list[int]) -> None:
    snap = snapshot(runs, at_sessions)
    if not snap:
        print("[sotopia] no runs to summarize")
        return

    print("\n=== SOTOPIA longitudinal snapshot ===")
    header = "dim".ljust(25) + "".join(f"s{idx:>4}".rjust(10) for idx in at_sessions)
    print(header)
    for dim in SCORE_DIMS:
        row = dim.ljust(25)
        for idx in at_sessions:
            v = snap.get(idx, {}).get(dim)
            row += (f"{v:>10.2f}" if v is not None else f"{'-':>10}")
        print(row)

    first, last = at_sessions[0], at_sessions[-1]
    if first in snap and last in snap:
        delta = snap[last]["overall"] - snap[first]["overall"]
        direction = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
        print(f"\nΔoverall (s{first} → s{last}): {delta:+.2f} {direction}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.sotopia",
        description="Run the longitudinal SOTOPIA benchmark on Sonzai.",
    )
    p.add_argument("--scenarios", type=int, default=4, help="Number of scenarios (default 4).")
    p.add_argument(
        "--sessions-per-scenario",
        type=int,
        default=30,
        help="Sessions per scenario (default 30).",
    )
    p.add_argument(
        "--snapshot-at",
        default="1,10,30",
        help="Comma-separated session indices to snapshot (default 1,10,30).",
    )
    p.add_argument(
        "--scenario-concurrency",
        type=int,
        default=2,
        help="Max scenarios running concurrently (default 2).",
    )
    p.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument(
        "--no-hf",
        action="store_true",
        help="Skip the HuggingFace dataset and use bundled seed scenarios only.",
    )
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args(argv)


async def _amain(args: argparse.Namespace) -> int:
    logging.basicConfig(
        level=logging.WARNING - 10 * min(args.verbose, 2),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if not os.environ.get("SONZAI_API_KEY"):
        print("error: SONZAI_API_KEY must be set", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        print("error: GEMINI_API_KEY must be set", file=sys.stderr)
        return 2

    at_sessions = [int(x) for x in args.snapshot_at.split(",") if x.strip()]
    scenarios = load_scenarios(limit=args.scenarios, prefer_hf=not args.no_hf)
    print(
        f"Running SOTOPIA longitudinal: {len(scenarios)} scenarios × "
        f"{args.sessions_per_scenario} sessions",
        file=sys.stderr,
    )

    judge = GeminiJudge(model=args.judge_model)
    # advance_time can take minutes per call (runs CE workers per simulated day).
    client = AsyncSonzai(timeout=600.0)

    all_runs: list[SessionRun] = []
    sem = asyncio.Semaphore(args.scenario_concurrency)

    async def one(sc: Scenario) -> list[SessionRun]:
        async with sem:
            try:
                return await _run_scenario(
                    client,
                    scenario=sc,
                    sessions_per_scenario=args.sessions_per_scenario,
                    judge=judge,
                    min_gap_hours=MIN_GAP_HOURS,
                )
            except Exception:
                logger.exception("scenario %s failed", sc.scenario_id)
                return []

    t0 = time.time()
    try:
        grouped = await asyncio.gather(
            *(one(sc) for sc in tqdm(scenarios, desc="scenarios", unit="sc"))
        )
    finally:
        await client.close()
    for g in grouped:
        all_runs.extend(g)
    elapsed = time.time() - t0

    ts = time.strftime("%Y%m%d-%H%M%S")
    results_dir = Path(__file__).parent / "results"
    jsonl_out = args.output or results_dir / f"sotopia_{ts}.jsonl"
    chart_out = jsonl_out.with_suffix("").with_name(jsonl_out.stem + "_trajectory.png")

    _write_runs_jsonl(jsonl_out, all_runs)
    _plot_trajectory(chart_out, all_runs)
    _print_summary(all_runs, at_sessions)

    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {jsonl_out}")
    print(f"Chart  : {chart_out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
