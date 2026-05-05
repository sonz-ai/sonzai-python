"""Tests for the LIFELONG-SOTOPIA scenario loader and pair-episode planner."""

from __future__ import annotations

from pathlib import Path

import pytest

from benchmarks.lifelong_sotopia.scenarios import (
    Character,
    CorpusBundle,
    EpisodePlan,
    Pair,
    Scenario,
    load_corpus,
    memory_required_indices,
    plan_episodes,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mini_corpus.json"


def test_load_corpus_shape():
    corpus = load_corpus(path=FIXTURE)
    assert isinstance(corpus, CorpusBundle)
    assert len(corpus.characters) == 2
    assert len(corpus.relationships) == 1
    assert "peer-collaborator" in corpus.scenarios_by_relationship
    assert len(corpus.scenarios_by_relationship["peer-collaborator"]) == 3
    assert len(corpus.memory_required) == 1


def test_load_corpus_resolves_relationship_to_characters():
    corpus = load_corpus(path=FIXTURE)
    rel = corpus.relationships[0]
    pair = corpus.pair_for_relationship(rel)
    assert isinstance(pair, Pair)
    assert pair.char_a.name == "Alice Chen"
    assert pair.char_b.name == "Bob Lin"
    assert pair.relationship_type == "peer-collaborator"


def test_memory_required_indices_full_size():
    # paper-size run, N=40
    assert memory_required_indices(40) == [5, 10, 20, 30, 38]


def test_memory_required_indices_default_size():
    # local default, N=10
    assert memory_required_indices(10) == [1, 2, 5, 7, 9]


def test_memory_required_indices_quick_size():
    # quick smoke, N=5: clamped, deduped, monotonic
    out = memory_required_indices(5)
    assert out == sorted(set(out))
    assert all(0 <= i < 5 for i in out)


def test_memory_required_indices_floor_first_slot():
    # N=6, the smallest size where the floor matters
    out = memory_required_indices(6)
    assert out[0] >= 1


def test_plan_episodes_uses_memory_required_at_planned_indices():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=4,
        seed=42,
        include_memory_required=True,
    )
    assert isinstance(plan, EpisodePlan)
    assert len(plan.episodes) == 4
    # at least one episode is memory-required
    mr_count = sum(1 for ep in plan.episodes if ep.is_memory_required)
    assert mr_count >= 1
    # every episode has a Scenario
    for ep in plan.episodes:
        assert isinstance(ep.scenario, Scenario)


def test_plan_episodes_disables_memory_required_when_flag_off():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=4,
        seed=42,
        include_memory_required=False,
    )
    assert all(not ep.is_memory_required for ep in plan.episodes)


def test_plan_episodes_seed_is_deterministic():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan_a = plan_episodes(
        corpus=corpus, pair=pair, n_episodes=4, seed=123, include_memory_required=False
    )
    plan_b = plan_episodes(
        corpus=corpus, pair=pair, n_episodes=4, seed=123, include_memory_required=False
    )
    assert [ep.scenario.scenario_id for ep in plan_a.episodes] == [
        ep.scenario.scenario_id for ep in plan_b.episodes
    ]


def test_plan_episodes_no_immediate_repeats_when_corpus_large_enough():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=3,
        seed=7,
        include_memory_required=False,
    )
    ids = [ep.scenario.scenario_id for ep in plan.episodes]
    # corpus has 3 scenarios, plan has 3 episodes — should be a permutation
    assert sorted(ids) == sorted(
        s.scenario_id for s in corpus.scenarios_by_relationship["peer-collaborator"]
    )


def test_load_corpus_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_corpus(path=Path("/nonexistent/lifelong_sotopia_fixture.json"))
