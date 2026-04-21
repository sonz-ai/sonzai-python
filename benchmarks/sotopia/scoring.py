"""SOTOPIA scoring + longitudinal trajectory helpers."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..common.gemini_judge import SotopiaScore

SCORE_DIMS = (
    "believability",
    "relationship",
    "knowledge",
    "secret",
    "social_rules",
    "financial_and_material",
    "goal",
    "overall",
)


@dataclass
class SessionRun:
    scenario_id: str
    session_index: int  # 1-based
    transcript: list[dict[str, str]]
    score: SotopiaScore


def trajectory_per_dimension(
    runs: Sequence[SessionRun], scenario_id: str | None = None
) -> dict[str, list[float]]:
    """Return ``{dimension: [score_at_session_1, ..., score_at_session_N]}``.

    If ``scenario_id`` is given, restrict to that scenario; otherwise average
    across all scenarios session-by-session.
    """
    filtered = [r for r in runs if (scenario_id is None or r.scenario_id == scenario_id)]
    if not filtered:
        return {d: [] for d in SCORE_DIMS}

    max_session = max(r.session_index for r in filtered)
    out: dict[str, list[float]] = {}
    for dim in SCORE_DIMS:
        series: list[float] = []
        for idx in range(1, max_session + 1):
            at_idx = [getattr(r.score, dim) for r in filtered if r.session_index == idx]
            series.append(sum(at_idx) / len(at_idx) if at_idx else float("nan"))
        out[dim] = series
    return out


def snapshot(runs: Sequence[SessionRun], at_sessions: Sequence[int]) -> dict[int, dict[str, float]]:
    """Average score per dimension at each session index in ``at_sessions``."""
    out: dict[int, dict[str, float]] = {}
    for idx in at_sessions:
        rows = [r for r in runs if r.session_index == idx]
        if not rows:
            continue
        out[idx] = {
            dim: sum(getattr(r.score, dim) for r in rows) / len(rows) for dim in SCORE_DIMS
        }
    return out
