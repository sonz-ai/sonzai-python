"""Exports + aliases for the unified benchmark agent preset."""

from __future__ import annotations


def test_benchmark_agent_name_is_exported():
    from sonzai.benchmarks import BENCHMARK_AGENT_NAME

    assert BENCHMARK_AGENT_NAME == "sonzai-benchmark-agent"


def test_ensure_benchmark_agent_async_is_callable():
    from sonzai.benchmarks import ensure_benchmark_agent_async

    assert callable(ensure_benchmark_agent_async)


def test_longmemeval_aliases_point_to_unified_exports():
    """Back-compat: old names still resolve to the new ones."""
    from sonzai.benchmarks import (
        BENCHMARK_AGENT_NAME,
        LONGMEMEVAL_AGENT_NAME,
        ensure_benchmark_agent_async,
        ensure_longmemeval_agent_async,
    )

    assert LONGMEMEVAL_AGENT_NAME == BENCHMARK_AGENT_NAME
    assert ensure_longmemeval_agent_async is ensure_benchmark_agent_async


def test_sync_aliases_point_to_unified_exports():
    from sonzai.benchmarks import ensure_benchmark_agent, ensure_longmemeval_agent

    assert ensure_longmemeval_agent is ensure_benchmark_agent
