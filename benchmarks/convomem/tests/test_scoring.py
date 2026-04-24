"""Unit tests for ConvoMem scoring helpers.

The Gemini client is mocked via a dummy judge shim. No network calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from benchmarks.common.gemini_judge import QAVerdict
from benchmarks.convomem.scoring import (
    CATEGORY_ORDER,
    aggregate_summary,
)


@dataclass
class _FakeJudge:
    """Stand-in for GeminiJudge that returns pre-canned verdicts by agent_answer text."""

    canned: dict[str, QAVerdict]

    async def grade_async(self, prompt: str, schema: Any) -> Any:  # noqa: ANN401
        # The abstention prompt embeds the agent_answer; find the matching key.
        for needle, verdict in self.canned.items():
            if needle in prompt:
                return verdict
        return QAVerdict(correct=False, rationale="no canned match")


@pytest.mark.asyncio
async def test_judge_abstention_recognises_decline():
    from benchmarks.common.gemini_judge import judge_abstention_async

    judge = _FakeJudge(canned={
        "I don't have that information": QAVerdict(correct=True, rationale="declined"),
        "His number is 555-1234":          QAVerdict(correct=False, rationale="fabricated"),
    })
    decline = await judge_abstention_async(
        judge,  # type: ignore[arg-type]
        question="What is John's phone number?",
        agent_answer="I don't have that information in our prior conversation.",
    )
    assert decline.correct is True

    fabricated = await judge_abstention_async(
        judge,  # type: ignore[arg-type]
        question="What is John's phone number?",
        agent_answer="His number is 555-1234.",
    )
    assert fabricated.correct is False


def test_category_order_matches_spec():
    assert CATEGORY_ORDER == [
        "user_evidence",
        "assistant_facts_evidence",
        "preference_evidence",
        "changing_evidence",
        "implicit_connection_evidence",
        "abstention_evidence",
    ]


def _row(qid: str, qtype: str, correct: bool, elapsed_ms: int, tokens: int) -> dict:
    return {
        "question_id": qid,
        "question_type": qtype,
        "qa_correct": correct,
        "elapsed_ms": elapsed_ms,
        "extra": {
            "chat_loaded_facts_count": tokens,  # proxy for MemScore context tokens
            "advance_time_calls": 1,
            "consolidation_events": 0,
            "advance_time_failures": 0,
        },
    }


def test_aggregate_summary_basic():
    rows = [
        _row("q1", "user_evidence",              True,  1000, 10),
        _row("q2", "user_evidence",              False, 2000, 12),
        _row("q3", "abstention_evidence",        True,  1500,  8),
    ]
    s = aggregate_summary(rows)
    assert s["n"] == 3
    assert s["qa_accuracy"] == pytest.approx(2 / 3)
    by_type = s["by_type"]
    assert by_type["user_evidence"]["n"] == 2
    assert by_type["user_evidence"]["qa_accuracy"] == pytest.approx(0.5)
    assert by_type["abstention_evidence"]["qa_accuracy"] == pytest.approx(1.0)
    ms = s["memscore"]
    assert ms["accuracy_pct"] == pytest.approx(200 / 3)          # ~66.67
    assert ms["avg_latency_ms"] == pytest.approx(1500)           # mean of 1000,2000,1500
    assert ms["avg_context_tokens"] == pytest.approx(10)         # mean of 10,12,8


def test_aggregate_handles_missing_qa_correct():
    rows = [
        _row("q1", "user_evidence", True, 1000, 10),
        {"question_id": "q2", "question_type": "user_evidence", "elapsed_ms": 500, "extra": {}},
    ]
    s = aggregate_summary(rows)
    # q2 is unscored — counted in n but excluded from qa_accuracy.
    assert s["n"] == 2
    assert s["qa_accuracy"] == pytest.approx(1.0)  # 1 scored, 1 correct
    assert s["by_type"]["user_evidence"]["qa_scored"] == 1
