"""Tests for BelExt scoring math (the 8-checkpoint extended believability)."""

from __future__ import annotations

import pytest

from benchmarks.common.gemini_judge import (
    BEL_EXTENDED_CHECKPOINTS,
    BelExtScore,
    bel_extended_value,
)


def test_bel_extended_checkpoints_count_is_eight():
    assert len(BEL_EXTENDED_CHECKPOINTS) == 8
    # all unique snake_case names
    assert all(c == c.lower() for c in BEL_EXTENDED_CHECKPOINTS)
    assert len(set(BEL_EXTENDED_CHECKPOINTS)) == 8


def test_bel_extended_value_no_failures_equals_bel():
    score = BelExtScore(
        believability=8.0,
        no_verbatim_repetition=True,
        character_consistency=True,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="all good",
    )
    assert bel_extended_value(score) == pytest.approx(8.0)


def test_bel_extended_value_one_failure_subtracts_five():
    score = BelExtScore(
        believability=8.0,
        no_verbatim_repetition=False,  # 1 failure
        character_consistency=True,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="repeat",
    )
    assert bel_extended_value(score) == pytest.approx(3.0)


def test_bel_extended_value_clamps_at_zero():
    score = BelExtScore(
        believability=4.0,
        no_verbatim_repetition=False,
        character_consistency=False,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="two fails",
    )
    # 4 - 5*2 = -6 → clamp to 0
    assert bel_extended_value(score) == pytest.approx(0.0)


def test_bel_extended_score_failures_helper_lists_only_falses():
    score = BelExtScore(
        believability=9.0,
        no_verbatim_repetition=True,
        character_consistency=False,
        no_stalling=False,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="drift + stall",
    )
    fails = score.failures()
    assert sorted(fails) == ["character_consistency", "no_stalling"]
