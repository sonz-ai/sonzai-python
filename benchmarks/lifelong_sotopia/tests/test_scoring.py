"""Tests for LIFELONG-SOTOPIA scoring helpers."""

from __future__ import annotations

import math

import pytest

from benchmarks.lifelong_sotopia.scoring import (
    EpisodeRun,
    EpisodeScore,
    aggregate_by_episode_index,
    linear_slope,
    memory_required_summary,
)


def _ep(idx: int, bel: float, goal: float, mr: bool = False) -> EpisodeRun:
    return EpisodeRun(
        pair_id="p1",
        relationship_type="mentor-mentee",
        episode_index=idx,
        scenario_id=f"sc-{idx:02d}",
        is_memory_required=mr,
        transcript=[],
        score=EpisodeScore(
            believability=bel,
            goal=goal,
            bel_extended=bel,  # no failures in this fixture
            checkpoints_failed=[],
            judge_rationale="ok",
        ),
    )


def test_aggregate_by_episode_index_averages_per_index():
    runs = [
        _ep(0, 9.0, 8.0),
        _ep(0, 7.0, 6.0),
        _ep(1, 8.0, 7.0),
    ]
    agg = aggregate_by_episode_index(runs)
    assert agg[0].bel == pytest.approx(8.0)
    assert agg[0].goal == pytest.approx(7.0)
    assert agg[0].n == 2
    assert agg[1].bel == pytest.approx(8.0)
    assert agg[1].n == 1


def test_aggregate_handles_empty_input():
    assert aggregate_by_episode_index([]) == {}


def test_linear_slope_descending_series_negative():
    slope = linear_slope([10.0, 9.0, 8.0, 7.0])
    assert slope < 0
    assert slope == pytest.approx(-1.0)


def test_linear_slope_constant_series_zero():
    assert linear_slope([5.0, 5.0, 5.0]) == pytest.approx(0.0)


def test_linear_slope_handles_nan_in_series():
    # NaN values are dropped while preserving original x-indices
    # input → [(0, 10), (2, 8), (3, 7)] → slope is exactly -1.0
    slope = linear_slope([10.0, math.nan, 8.0, 7.0])
    assert slope == pytest.approx(-1.0)


def test_linear_slope_too_few_points_returns_nan():
    assert math.isnan(linear_slope([5.0]))
    assert math.isnan(linear_slope([]))


def test_memory_required_summary_isolates_those_episodes():
    runs = [
        _ep(1, 8.0, 7.0, mr=False),
        _ep(2, 6.0, 5.0, mr=True),
        _ep(3, 7.0, 6.0, mr=True),
    ]
    summary = memory_required_summary(runs)
    assert summary["n"] == 2
    assert summary["bel_mean"] == pytest.approx(6.5)
    assert summary["goal_mean"] == pytest.approx(5.5)
