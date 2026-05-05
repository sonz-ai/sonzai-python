"""LIFELONG-SOTOPIA scoring datatypes and aggregation.

One ``EpisodeRun`` per (pair, episode_index). Aggregation collapses across
pairs for a given episode index (so a 5-pair × 40-episode run produces 40
trajectory points each with ``n=5``). Linear slope on the per-episode
trajectory is the headline "is the agent declining or holding?" signal —
the paper's central observation.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class EpisodeScore:
    believability: float       # 0..10 (raw SOTOPIA Bel)
    goal: float                # 0..10
    bel_extended: float        # 0..10 (BelExt formula applied)
    checkpoints_failed: list[str] = field(default_factory=list)
    judge_rationale: str = ""


@dataclass
class EpisodeRun:
    pair_id: str
    relationship_type: str
    episode_index: int   # 0-based
    scenario_id: str
    is_memory_required: bool
    transcript: list[dict[str, str]]
    score: EpisodeScore


@dataclass
class IndexAgg:
    episode_index: int
    bel: float           # mean
    goal: float          # mean
    bel_ext: float       # mean
    n: int               # number of runs at this index


def aggregate_by_episode_index(
    runs: Sequence[EpisodeRun],
) -> dict[int, IndexAgg]:
    """Average each metric across all pairs sharing an episode index."""
    by_idx: dict[int, list[EpisodeRun]] = {}
    for r in runs:
        by_idx.setdefault(r.episode_index, []).append(r)
    out: dict[int, IndexAgg] = {}
    for idx, rs in by_idx.items():
        out[idx] = IndexAgg(
            episode_index=idx,
            bel=sum(r.score.believability for r in rs) / len(rs),
            goal=sum(r.score.goal for r in rs) / len(rs),
            bel_ext=sum(r.score.bel_extended for r in rs) / len(rs),
            n=len(rs),
        )
    return out


def linear_slope(series: Sequence[float]) -> float:
    """Least-squares slope over (x=index, y=value). NaN entries are dropped.

    Returns ``nan`` if fewer than 2 finite points remain.
    """
    pts = [(i, v) for i, v in enumerate(series) if not math.isnan(v)]
    if len(pts) < 2:
        return float("nan")
    n = len(pts)
    sx = sum(x for x, _ in pts)
    sy = sum(y for _, y in pts)
    sxy = sum(x * y for x, y in pts)
    sxx = sum(x * x for x, _ in pts)
    denom = n * sxx - sx * sx
    if denom == 0:
        return float("nan")
    return (n * sxy - sx * sy) / denom


def memory_required_summary(runs: Sequence[EpisodeRun]) -> dict[str, float]:
    """Summarize the subset of episodes flagged as memory-required."""
    mr = [r for r in runs if r.is_memory_required]
    if not mr:
        return {
            "n": 0,
            "bel_mean": float("nan"),
            "goal_mean": float("nan"),
            "bel_ext_mean": float("nan"),
        }
    return {
        "n": len(mr),
        "bel_mean": sum(r.score.believability for r in mr) / len(mr),
        "goal_mean": sum(r.score.goal for r in mr) / len(mr),
        "bel_ext_mean": sum(r.score.bel_extended for r in mr) / len(mr),
    }


def trajectory_series(
    runs: Sequence[EpisodeRun], n_episodes: int
) -> dict[str, list[float]]:
    """Return ``{metric: [val_at_idx_0, ..., val_at_idx_{N-1}]}`` (NaN for empty)."""
    agg = aggregate_by_episode_index(runs)
    series_bel = [agg[i].bel if i in agg else float("nan") for i in range(n_episodes)]
    series_goal = [agg[i].goal if i in agg else float("nan") for i in range(n_episodes)]
    series_bel_ext = [
        agg[i].bel_ext if i in agg else float("nan") for i in range(n_episodes)
    ]
    return {
        "believability": series_bel,
        "goal": series_goal,
        "bel_extended": series_bel_ext,
    }
