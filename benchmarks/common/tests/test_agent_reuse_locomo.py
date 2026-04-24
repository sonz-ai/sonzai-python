"""Tests that SliceKey recognises the 'locomo' benchmark."""

from __future__ import annotations

from benchmarks.common.agent_reuse import SliceKey


def test_locomo_slice_matches_on_benchmark_and_limit():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="locomo", limit=10)
    assert a.matches(b)


def test_locomo_slice_mismatch_on_benchmark():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="longmemeval", limit=10)
    assert not a.matches(b)


def test_locomo_slice_mismatch_on_limit():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="locomo", limit=5)
    assert not a.matches(b)


def test_locomo_slice_ignores_max_sessions_per_question():
    """LoCoMo doesn't use the per-question session cap — should not invalidate reuse."""
    a = SliceKey(benchmark="locomo", limit=10, max_sessions_per_question=0)
    b = SliceKey(benchmark="locomo", limit=10, max_sessions_per_question=5)
    assert a.matches(b)
