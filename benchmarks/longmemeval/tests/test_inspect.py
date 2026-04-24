"""Unit tests for inspect.py — the markdown failure-report generator."""

from __future__ import annotations

import json

from benchmarks.longmemeval.inspect import format_report


SAMPLE_FAILURES = [
    {
        "question_id": "q2",
        "question_type": "multi-session",
        "bucket": "retrieval-miss",
        "question": "Average age of family?",
        "answer": "59.6",
        "agent_answer": "I don't know",
        "qa_rationale": "incorrect",
        "expected_sessions": ["s_ma", "s_mb", "s_mc"],
        "retrieved_top10": ["s_x", "s_y", "s_z"],
        "hit_ranks": [],
    },
    {
        "question_id": "q3",
        "question_type": "multi-session",
        "bucket": "retrieval-hit / qa-miss",
        "question": "Siblings?",
        "answer": "Alex, Sam",
        "agent_answer": "Alex only",
        "qa_rationale": "partial mismatch",
        "expected_sessions": ["s_nh"],
        "retrieved_top10": ["s_nh", "s_x"],
        "hit_ranks": [0],
    },
]


def test_format_report_groups_by_subtype_then_bucket():
    md = format_report(SAMPLE_FAILURES)
    # Both failures in multi-session, two different buckets.
    assert md.count("### multi-session") == 1
    assert "#### retrieval-miss" in md
    assert "#### retrieval-hit / qa-miss" in md


def test_format_report_includes_per_question_fields():
    md = format_report(SAMPLE_FAILURES)
    # Expected / agent_answer / judge rationale must all appear.
    assert "Average age of family?" in md
    assert "**Expected:** 59.6" in md
    assert "**Agent said:** I don't know" in md
    assert "**Judge:** incorrect" in md


def test_format_report_shows_hit_ranks_or_none():
    md = format_report(SAMPLE_FAILURES)
    # q2 has empty hit_ranks → should render "NONE".
    assert "**Hit ranks:** NONE" in md
    # q3 has hit_ranks [0] → should render "0".
    assert "**Hit ranks:** [0]" in md


def test_format_report_subtype_filter():
    md = format_report(SAMPLE_FAILURES, subtype="multi-session")
    assert "### multi-session" in md
    md_other = format_report(SAMPLE_FAILURES, subtype="temporal-reasoning")
    assert "### temporal-reasoning" not in md_other  # no matching entries
    assert md_other.startswith("# LongMemEval Failure Report")  # still emits header


def test_format_report_bucket_filter():
    md = format_report(SAMPLE_FAILURES, bucket="retrieval-miss")
    assert "#### retrieval-miss" in md
    assert "#### retrieval-hit / qa-miss" not in md


def test_format_report_empty_failures_is_valid_markdown():
    md = format_report([])
    # Header always present even with no failures.
    assert md.startswith("# LongMemEval Failure Report")


from pathlib import Path

from benchmarks.longmemeval.inspect import main as inspect_main


def test_inspect_main_cli_end_to_end(tmp_path, capsys):
    failures_path = tmp_path / "failures.json"
    report_path = tmp_path / "report.md"
    failures_path.write_text(__import__("json").dumps(SAMPLE_FAILURES))

    rc = inspect_main(["--failures", str(failures_path), "--output", str(report_path)])
    assert rc == 0
    assert report_path.exists()
    content = report_path.read_text()
    assert content.startswith("# LongMemEval Failure Report")
    assert "### multi-session" in content


def test_inspect_main_missing_failures_file_returns_2(tmp_path, capsys):
    missing = tmp_path / "nope.json"
    rc = inspect_main(["--failures", str(missing), "--output", str(tmp_path / "out.md")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not found" in err
