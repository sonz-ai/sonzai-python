"""End-to-end smoke test of the baseline backend with a fully-mocked judge."""

from __future__ import annotations

from pathlib import Path

import pytest

from benchmarks.common.gemini_judge import (
    AgentTurn,
    BelExtScore,
    PartnerTurn,
    SessionSummary,
    SotopiaScore,
)
from benchmarks.lifelong_sotopia.backends.baseline import (
    run_all_pairs_baseline,
)
from benchmarks.lifelong_sotopia.scenarios import load_corpus

FIXTURE = Path(__file__).parent / "fixtures" / "mini_corpus.json"


class _FakeJudge:
    """Stand-in for GeminiJudge that returns scripted responses by schema."""

    def __init__(self) -> None:
        self.calls: list[type] = []

    async def grade_async(self, prompt, schema):
        self.calls.append(schema)
        if schema is PartnerTurn:
            return PartnerTurn(content="partner says hi", end_conversation=False)
        if schema is AgentTurn:
            return AgentTurn(content="agent says hi back")
        if schema is SotopiaScore:
            return SotopiaScore(
                believability=8.0, relationship=2.0, knowledge=5.0, secret=0.0,
                social_rules=0.0, financial_and_material=0.0, goal=7.0,
                memory_continuity=5.0, overall=7.5, rationale="ok",
            )
        if schema is BelExtScore:
            return BelExtScore(
                believability=8.0,
                no_verbatim_repetition=True, character_consistency=True,
                no_stalling=True, no_mode_collapse=True,
                appropriate_emotional_register=True,
                no_unprompted_secret_disclosure=True,
                acknowledges_scenario_change=True, stays_in_agent_voice=True,
                rationale="all good",
            )
        if schema is SessionSummary:
            return SessionSummary(summary="they exchanged greetings.")
        raise AssertionError(f"unhandled schema {schema!r}")


@pytest.mark.asyncio
async def test_baseline_runs_3_episodes_end_to_end():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    judge = _FakeJudge()

    runs = await run_all_pairs_baseline(
        corpus=corpus,
        pairs=[pair],
        n_episodes=3,
        judge=judge,
        memory_mode="summary",
        seed=11,
        include_memory_required=False,
        max_turn_pairs=2,  # cap so the smoke test stays fast
    )
    assert len(runs) == 3
    assert all(r.score.believability == 8.0 for r in runs)
    assert all(r.score.bel_extended == 8.0 for r in runs)  # no failures from fake judge
    assert all(r.transcript for r in runs)


@pytest.mark.asyncio
async def test_baseline_full_history_mode_runs():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    judge = _FakeJudge()
    runs = await run_all_pairs_baseline(
        corpus=corpus,
        pairs=[pair],
        n_episodes=2,
        judge=judge,
        memory_mode="full-history",
        seed=11,
        include_memory_required=False,
        max_turn_pairs=2,
    )
    assert len(runs) == 2
