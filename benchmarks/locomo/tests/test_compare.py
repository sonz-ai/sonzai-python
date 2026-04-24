"""Tests for the compare utility — side-by-side JSONL aggregation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from benchmarks.locomo.compare import load_jsonl, render_table


def _write_jsonl(p: Path, rows: list[dict]) -> Path:
    p.write_text("\n".join(json.dumps(r) for r in rows))
    return p


def test_load_jsonl_handles_trailing_newline(tmp_path: Path):
    p = _write_jsonl(tmp_path / "a.jsonl", [{"category": 1, "llm_correct": True}])
    rows = load_jsonl(p)
    assert len(rows) == 1
    assert rows[0]["category"] == 1


def test_render_table_has_per_category_and_overall(tmp_path: Path):
    rows_sonzai = [
        {"category": 1, "llm_correct": True, "token_f1": 1.0, "backend": "sonzai",
         "retrieval": {}},
        {"category": 2, "llm_correct": True, "token_f1": 0.5, "backend": "sonzai",
         "retrieval": {}},
    ]
    rows_mem0 = [
        {"category": 1, "llm_correct": False, "token_f1": 0.0, "backend": "mem0",
         "retrieval": {}},
        {"category": 2, "llm_correct": True, "token_f1": 0.5, "backend": "mem0",
         "retrieval": {}},
    ]
    md = render_table({
        "sonzai": rows_sonzai, "mem0": rows_mem0,
    })
    assert "| Category |" in md
    assert "sonzai" in md
    assert "mem0" in md
    # Category 1: sonzai 100%, mem0 0%
    assert "1.000" in md
    assert "0.000" in md


def test_render_table_rejects_single_file():
    with pytest.raises(ValueError):
        render_table({"only_one": []})
