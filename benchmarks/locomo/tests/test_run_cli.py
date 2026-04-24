"""Smoke tests for the LoCoMo CLI parser — no live API calls."""

from __future__ import annotations

from benchmarks.locomo.run import _default_output_path, _parse_args


def test_parse_args_defaults():
    ns = _parse_args(["--limit", "2"])
    assert ns.backend == "sonzai"
    assert ns.limit == 2
    assert ns.concurrency == 2
    assert ns.top_k == 30
    assert ns.ingest_batch_size == 2
    assert ns.skip_advance_time is False
    assert ns.include_adversarial is False
    assert ns.mode == "both"


def test_parse_args_mem0_backend():
    ns = _parse_args(["--backend", "mem0", "--limit", "5"])
    assert ns.backend == "mem0"
    assert ns.limit == 5


def test_parse_args_compare():
    ns = _parse_args(["--compare", "a.jsonl", "b.jsonl"])
    assert ns.compare == ["a.jsonl", "b.jsonl"]


def test_default_output_path_contains_backend_and_ts():
    path = _default_output_path("sonzai")
    assert path.parent.name == "results"
    assert "sonzai_" in path.name
    assert path.suffix == ".jsonl"
