"""LIFELONG-SOTOPIA CLI runner.

Drives the chosen backend over ``--pairs`` × ``--episodes-per-pair`` runs,
writes a jsonl + trajectory PNG, prints a per-metric trajectory table.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import math
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ..common.gemini_judge import DEFAULT_MODEL as DEFAULT_JUDGE_MODEL
from ..common.gemini_judge import GeminiJudge
from .scenarios import (
    CorpusBundle,
    Pair,
    load_default_corpus,
)
from .scoring import (
    EpisodeRun,
    linear_slope,
    memory_required_summary,
    trajectory_series,
)

logger = logging.getLogger("benchmarks.lifelong_sotopia")

QUICK = {"pairs": 1, "episodes_per_pair": 5}
FULL = {"pairs": 5, "episodes_per_pair": 40}


def _select_pairs(corpus: CorpusBundle, n: int) -> list[Pair]:
    """Pick the first ``n`` pairs that have at least one scenario in their type."""
    out: list[Pair] = []
    for rel in corpus.relationships:
        if rel.type not in corpus.scenarios_by_relationship:
            continue
        if not corpus.scenarios_by_relationship[rel.type]:
            continue
        out.append(corpus.pair_for_relationship(rel))
        if len(out) >= n:
            break
    if not out:
        raise SystemExit(
            "no usable pairs in the corpus (no relationship has any scenarios)"
        )
    return out


def _write_runs_jsonl(path: Path, runs: list[EpisodeRun]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in runs:
            row: dict[str, Any] = {
                "pair_id": r.pair_id,
                "relationship_type": r.relationship_type,
                "episode_index": r.episode_index,
                "scenario_id": r.scenario_id,
                "is_memory_required": r.is_memory_required,
                "transcript": r.transcript,
                "score": asdict(r.score),
            }
            f.write(json.dumps(row) + "\n")


def _plot_trajectory(path: Path, runs: list[EpisodeRun], n_episodes: int) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not installed — skipping trajectory chart")
        return

    series = trajectory_series(runs, n_episodes)
    xs = list(range(1, n_episodes + 1))  # 1-based for display
    fig, ax = plt.subplots(figsize=(10, 6))
    for label, ys in series.items():
        ax.plot(xs, ys, marker="o", linewidth=1.5, label=label)
    # Mark memory-required episodes as vertical lines
    mr_indices = sorted({r.episode_index + 1 for r in runs if r.is_memory_required})
    for x in mr_indices:
        ax.axvline(x, color="gray", linestyle=":", alpha=0.4)
    ax.set_xlabel("Episode index")
    ax.set_ylabel("Score (0..10)")
    ax.set_ylim(0, 10)
    ax.set_title("LIFELONG-SOTOPIA trajectory")
    ax.legend(loc="best", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _resolve_snapshot_indices(spec: str, n_episodes: int) -> list[int]:
    """Parse ``--snapshot-at`` (1-based, comma-separated). Returns 0-based indices.

    Indices outside ``[1, n_episodes]`` are dropped (so a 30-snapshot list still
    works on a 10-episode run — you just see the surviving columns).
    """
    raw = [int(x) for x in spec.split(",") if x.strip()]
    out = sorted({i - 1 for i in raw if 1 <= i <= n_episodes})
    return out or [0, max(0, n_episodes - 1)]


def _print_summary(runs: list[EpisodeRun], n_episodes: int, snapshot_at: str) -> None:
    if not runs:
        print("[lifelong-sotopia] no runs to summarize")
        return
    series = trajectory_series(runs, n_episodes)
    print("\n=== LIFELONG-SOTOPIA trajectory ===")
    snap_idx = _resolve_snapshot_indices(snapshot_at, n_episodes)
    header = "metric".ljust(15) + "".join(f"e{i+1:>4}".rjust(10) for i in snap_idx) + "    slope"
    print(header)
    for metric, ys in series.items():
        slope = linear_slope(ys)
        row = metric.ljust(15)
        for i in snap_idx:
            v = ys[i]
            row += (f"{v:>10.2f}" if not math.isnan(v) else f"{'-':>10}")
        slope_str = f"{slope:+.4f}/ep" if not math.isnan(slope) else "(insufficient data)"
        row += f"  {slope_str}"
        print(row)

    # Δ first→last (paper-style headline)
    if len(snap_idx) >= 2:
        first, last = snap_idx[0], snap_idx[-1]
        print(f"\nΔ (e{first+1} → e{last+1}):")
        for metric, ys in series.items():
            v0, vN = ys[first], ys[last]
            if math.isnan(v0) or math.isnan(vN):
                continue
            delta = vN - v0
            arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
            print(f"  {metric.ljust(15)} {v0:>5.2f} → {vN:>5.2f}   Δ={delta:+.2f} {arrow}")

    mr = memory_required_summary(runs)
    if mr["n"] > 0:
        print(
            f"\nMemory-required slice (n={int(mr['n'])}): "
            f"bel={mr['bel_mean']:.2f}  goal={mr['goal_mean']:.2f}  "
            f"bel_ext={mr['bel_ext_mean']:.2f}"
        )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.lifelong_sotopia",
        description="Run the LIFELONG-SOTOPIA benchmark.",
    )
    p.add_argument("--backend", choices=("sonzai", "baseline"), default="sonzai")
    p.add_argument(
        "--memory",
        choices=("none", "summary", "full-history"),
        default="summary",
        help="Memory mode for the baseline backend (ignored for sonzai).",
    )
    p.add_argument("--pairs", type=int, default=2, help="Number of character pairs (default 2).")
    p.add_argument(
        "--episodes-per-pair", type=int, default=10,
        help="Episodes per pair (default 10).",
    )
    p.add_argument("--quick", action="store_true", help="1 pair × 5 episodes (smoke).")
    p.add_argument("--full", action="store_true",
                   help="5 pairs × 40 episodes (paper-comparable).")
    p.add_argument("--max-turn-pairs", type=int, default=4,
                   help="Max (partner, agent) turn-pairs per episode (default 4).")
    p.add_argument("--seed", type=int, default=13, help="RNG seed for episode planning.")
    p.add_argument(
        "--snapshot-at",
        default="1,10,20,30",
        help="Comma-separated 1-based episode indices to snapshot in the printed table "
        "(default 1,10,20,30 — matches existing sotopia bench convention).",
    )
    p.add_argument("--include-memory-required", dest="include_memory_required",
                   action="store_true", default=True,
                   help="Insert memory-required scenarios at deterministic indices (default on).")
    p.add_argument("--no-memory-required", dest="include_memory_required",
                   action="store_false")
    p.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--pair-concurrency", type=int, default=1)
    p.add_argument("--no-advance-time", dest="advance_time", action="store_false", default=True,
                   help="Skip workbench.advance_time between Sonzai episodes.")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args(argv)


async def _amain(args: argparse.Namespace) -> int:
    logging.basicConfig(
        level=logging.WARNING - 10 * min(args.verbose, 2),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.quick:
        args.pairs = QUICK["pairs"]
        args.episodes_per_pair = QUICK["episodes_per_pair"]
    if args.full:
        args.pairs = FULL["pairs"]
        args.episodes_per_pair = FULL["episodes_per_pair"]

    if args.backend == "sonzai" and not os.environ.get("SONZAI_API_KEY"):
        print("error: SONZAI_API_KEY must be set for --backend sonzai", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        print("error: GEMINI_API_KEY must be set", file=sys.stderr)
        return 2

    corpus = load_default_corpus()
    pairs = _select_pairs(corpus, args.pairs)
    print(
        f"Running LIFELONG-SOTOPIA [{args.backend}, memory={args.memory}]: "
        f"{len(pairs)} pairs × {args.episodes_per_pair} episodes",
        file=sys.stderr,
    )

    judge = GeminiJudge(model=args.judge_model)

    t0 = time.time()
    if args.backend == "sonzai":
        from .backends.sonzai import run_all_pairs_sonzai
        runs = await run_all_pairs_sonzai(
            corpus=corpus,
            pairs=pairs,
            n_episodes=args.episodes_per_pair,
            judge=judge,
            seed=args.seed,
            include_memory_required=args.include_memory_required,
            max_turn_pairs=args.max_turn_pairs,
            pair_concurrency=args.pair_concurrency,
            advance_time_between=args.advance_time,
        )
    else:
        from .backends.baseline import run_all_pairs_baseline
        runs = await run_all_pairs_baseline(
            corpus=corpus,
            pairs=pairs,
            n_episodes=args.episodes_per_pair,
            judge=judge,
            memory_mode=args.memory,
            seed=args.seed,
            include_memory_required=args.include_memory_required,
            max_turn_pairs=args.max_turn_pairs,
            pair_concurrency=args.pair_concurrency,
        )
    elapsed = time.time() - t0

    ts = time.strftime("%Y%m%d-%H%M%S")
    results_dir = Path(__file__).parent / "results"
    suffix = args.backend if args.backend == "sonzai" else f"baseline-{args.memory}"
    jsonl_out = args.output or results_dir / f"lifelong_sotopia_{suffix}_{ts}.jsonl"
    chart_out = jsonl_out.with_suffix("").with_name(jsonl_out.stem + "_trajectory.png")

    _write_runs_jsonl(jsonl_out, runs)
    _plot_trajectory(chart_out, runs, args.episodes_per_pair)
    _print_summary(runs, args.episodes_per_pair, args.snapshot_at)

    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {jsonl_out}")
    print(f"Chart  : {chart_out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))
