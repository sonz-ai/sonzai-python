"""Tests for the LoCoMo judge wrapper."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from benchmarks.common.gemini_judge import LocomoVerdict, judge_locomo_async


def test_locomo_verdict_schema():
    v = LocomoVerdict(label="CORRECT")
    assert v.label == "CORRECT"

    # Allow WRONG too
    v2 = LocomoVerdict(label="WRONG")
    assert v2.label == "WRONG"


@pytest.mark.asyncio
async def test_judge_locomo_async_returns_structured_verdict():
    judge = MagicMock()
    judge.grade_async = AsyncMock(return_value=LocomoVerdict(label="CORRECT"))

    result = await judge_locomo_async(
        judge,
        question="What color is Bob's bike?",
        gold_answer="red",
        generated_answer="The bike is red.",
    )

    assert isinstance(result, LocomoVerdict)
    assert result.label == "CORRECT"
    judge.grade_async.assert_awaited_once()
    prompt_arg, schema_arg = judge.grade_async.call_args.args
    assert "What color is Bob's bike?" in prompt_arg
    assert "red" in prompt_arg
    assert "The bike is red." in prompt_arg
    assert schema_arg is LocomoVerdict
