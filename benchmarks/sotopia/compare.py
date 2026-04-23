"""Side-by-side snapshot comparison for two SOTOPIA JSONL runs.

Usage:
  python -m benchmarks.sotopia.compare <sonzai.jsonl> <mempalace.jsonl> \
      [--at 1,5,10,20,30]

Prints per-dimension average at each session index, the Δoverall (s1→sN) for
each run, and the head-to-head delta (Sonzai − MemPalace) at each snapshot.
Useful alongside the trajectory PNGs to read the longitudinal story at a glance.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .scoring import SCORE_DIMS, SessionRun, snapshot

try:  # SotopiaScore is a pydantic model; use it if available for validation.
    from ..common.gemini_judge import SotopiaScore
except Exception:  # pragma: no cover — scoring helpers degrade gracefully
    SotopiaScore = None  # type: ignore


def _load(paths: list[Path]) -> list[SessionRun]:
    """Load and merge SessionRuns from one or more JSONL files.

    Resume-driven runs split the trajectory across files (e.g. s1–30 in one
    run, s31–60 in a second); concatenating all SessionRuns lets
    `snapshot(runs, at_sessions)` compute per-index averages over the full
    range regardless of which file each row came from.
    """
    runs: list[SessionRun] = []
    for path in paths:
        with open(path) as f:
            for line in f:
                row = json.loads(line)
                score = row.get("score") or {}
                if SotopiaScore is not None:
                    try:
                        score = SotopiaScore.model_validate(score)
                    except Exception:
                        pass
                runs.append(
                    SessionRun(
                        scenario_id=row["scenario_id"],
                        session_index=int(row["session_index"]),
                        transcript=row.get("transcript") or [],
                        score=score,
                    )
                )
    return runs


def _print_side_by_side(
    name_a: str,
    runs_a: list[SessionRun],
    name_b: str,
    runs_b: list[SessionRun],
    at: list[int],
) -> None:
    snap_a = snapshot(runs_a, at)
    snap_b = snapshot(runs_b, at)

    col_w = 9
    print(f"\n=== SOTOPIA comparison: {name_a} vs {name_b} ===")
    header = "dim".ljust(22) + "".join(
        f" │ s{idx}:{name_a[:4]}".rjust(col_w * 2)
        + f" {name_b[:4]}".rjust(col_w)
        + " Δ".rjust(col_w)
        for idx in at
    )
    print(header)
    for dim in SCORE_DIMS:
        row = dim.ljust(22)
        for idx in at:
            a = snap_a.get(idx, {}).get(dim)
            b = snap_b.get(idx, {}).get(dim)
            row += f" │ s{idx}:".rjust(col_w)
            row += (f"{a:>{col_w}.2f}" if a is not None else f"{'-':>{col_w}}")
            row += (f"{b:>{col_w}.2f}" if b is not None else f"{'-':>{col_w}}")
            if a is not None and b is not None:
                row += f"{(a - b):>+{col_w}.2f}"
            else:
                row += f"{'-':>{col_w}}"
        print(row)

    print()
    first, last = at[0], at[-1]

    def _delta(sn: dict[int, dict[str, float]]) -> float | None:
        if first in sn and last in sn:
            return sn[last]["overall"] - sn[first]["overall"]
        return None

    da = _delta(snap_a)
    db = _delta(snap_b)
    if da is not None:
        direction = "↑" if da > 0 else ("↓" if da < 0 else "=")
        print(f"{name_a}: Δoverall s{first}→s{last} = {da:+.2f} {direction}")
    if db is not None:
        direction = "↑" if db > 0 else ("↓" if db < 0 else "=")
        print(f"{name_b}: Δoverall s{first}→s{last} = {db:+.2f} {direction}")
    if da is not None and db is not None:
        print(f"\nLearning-curve advantage ({name_a} − {name_b}): {(da - db):+.2f}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m benchmarks.sotopia.compare")
    p.add_argument(
        "--sonzai",
        type=Path,
        nargs="+",
        required=True,
        help="One or more Sonzai run JSONLs. Pass several when the trajectory "
        "was produced by incremental resumes (e.g. s1-30, s31-60, s61-90).",
    )
    p.add_argument(
        "--mempalace",
        type=Path,
        nargs="+",
        required=True,
        help="One or more MemPalace run JSONLs (same multi-file semantics).",
    )
    p.add_argument("--at", default="1,5,10,20,30", help="Session indices to snapshot")
    p.add_argument("--name-a", default="Sonzai")
    p.add_argument("--name-b", default="MemPalace")
    args = p.parse_args(argv)

    at = [int(x) for x in args.at.split(",") if x.strip()]
    runs_a = _load(args.sonzai)
    runs_b = _load(args.mempalace)
    _print_side_by_side(args.name_a, runs_a, args.name_b, runs_b, at)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
