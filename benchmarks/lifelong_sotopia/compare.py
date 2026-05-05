"""Side-by-side trajectory comparison for two-or-more LIFELONG-SOTOPIA JSONL runs.

Usage::

    python -m benchmarks.lifelong_sotopia.compare \
        path/to/sonzai.jsonl path/to/baseline-summary.jsonl \
        [--names sonzai,baseline-summary] \
        [--at 1,10,20,30]

Prints per-metric snapshot at each chosen episode index, the Δfirst→last
for each run, and a winner-per-row marker. Useful to read the s1→sN story
at a glance and to point at "did the memory layer hold the line?".
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from .scoring import EpisodeRun, EpisodeScore, linear_slope, trajectory_series

METRICS = ("believability", "goal", "bel_extended")


def _load(path: Path) -> list[EpisodeRun]:
    runs: list[EpisodeRun] = []
    with open(path) as f:
        for line in f:
            row = json.loads(line)
            sc = row.get("score") or {}
            runs.append(
                EpisodeRun(
                    pair_id=str(row.get("pair_id", "")),
                    relationship_type=str(row.get("relationship_type", "")),
                    episode_index=int(row["episode_index"]),
                    scenario_id=str(row.get("scenario_id", "")),
                    is_memory_required=bool(row.get("is_memory_required", False)),
                    transcript=row.get("transcript") or [],
                    score=EpisodeScore(
                        believability=float(sc.get("believability", float("nan"))),
                        goal=float(sc.get("goal", float("nan"))),
                        bel_extended=float(sc.get("bel_extended", float("nan"))),
                        checkpoints_failed=list(sc.get("checkpoints_failed", []) or []),
                        judge_rationale=str(sc.get("judge_rationale", "")),
                    ),
                )
            )
    return runs


def _max_episode(runs: list[EpisodeRun]) -> int:
    return max((r.episode_index for r in runs), default=-1) + 1


def _series(runs: list[EpisodeRun]) -> dict[str, list[float]]:
    n = _max_episode(runs)
    return trajectory_series(runs, n_episodes=n) if n > 0 else {m: [] for m in METRICS}


def _at(series: list[float], idx_1based: int) -> float:
    i = idx_1based - 1
    if 0 <= i < len(series):
        return series[i]
    return float("nan")


def _fmt(v: float) -> str:
    return f"{v:>6.2f}" if not math.isnan(v) else f"{'-':>6}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m benchmarks.lifelong_sotopia.compare")
    p.add_argument("inputs", type=Path, nargs="+", help="Two or more JSONL paths.")
    p.add_argument("--names", default=None, help="Comma-separated labels (defaults to file stems).")
    p.add_argument("--at", default="1,10,20,30",
                   help="Comma-separated 1-based episode indices to snapshot.")
    args = p.parse_args(argv)

    if len(args.inputs) < 2:
        p.error("at least two inputs required")

    names = (
        [n.strip() for n in args.names.split(",")]
        if args.names else [pth.stem.split("_")[1] if "_" in pth.stem else pth.stem
                            for pth in args.inputs]
    )
    if len(names) != len(args.inputs):
        p.error("--names count must match number of inputs")

    runs_per_input = [_load(p) for p in args.inputs]
    series_per_input = [_series(rs) for rs in runs_per_input]
    snap = [int(x) for x in args.at.split(",") if x.strip()]

    print("\n=== LIFELONG-SOTOPIA snapshot comparison ===")
    for metric in METRICS:
        print(f"\n[{metric}]")
        header = "run".ljust(22) + "".join(f"e{i:>4}".rjust(8) for i in snap) + "    Δfirst→last     slope"
        print(header)
        for name, ser in zip(names, series_per_input):
            ys = ser[metric]
            slope = linear_slope(ys)
            row = name.ljust(22)
            for i in snap:
                row += _fmt(_at(ys, i))
            v0 = _at(ys, snap[0])
            vN = _at(ys, snap[-1])
            delta = (vN - v0) if not (math.isnan(v0) or math.isnan(vN)) else float("nan")
            arrow = "↑" if (not math.isnan(delta) and delta > 0) else (
                "↓" if (not math.isnan(delta) and delta < 0) else "="
            )
            row += f"   {('-' if math.isnan(delta) else f'{delta:+.2f}'):>7} {arrow}"
            slope_str = f"{slope:+.4f}/ep" if not math.isnan(slope) else "(insufficient)"
            row += f"   {slope_str}"
            print(row)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
