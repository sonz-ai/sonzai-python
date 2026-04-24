"""Unit tests for the LongMemEval multi-run aggregator.

The aggregator is pure-function by design — every unit we test takes in
primitives + dataclasses and returns primitives + dataclasses. That keeps
these tests fast and deterministic.
"""

from __future__ import annotations

import json
from pathlib import Path

from benchmarks.longmemeval.aggregate import (
    FailureBucket,
    classify_failure,
    load_records,
)
from benchmarks.longmemeval.aggregate import wilson_ci

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_run.jsonl"


def _by_id(records):
    return {r["question_id"]: r for r in records}


def test_wilson_ci_perfect_score_on_small_n():
    # 10 of 10 correct: p=1.0. Wilson interval has upper bound at 1, lower
    # bound below 1 — much tighter than Normal, which would extend above 1.
    lo, hi = wilson_ci(successes=10, n=10)
    assert hi == 1.0
    assert 0.65 < lo < 0.73  # known-good Wilson result for 10/10 with z=1.96 ≈ 0.7225


def test_wilson_ci_symmetric_around_point_five():
    lo, hi = wilson_ci(successes=5, n=10)
    assert abs((lo + hi) / 2 - 0.5) < 0.01


def test_wilson_ci_returns_zero_for_zero_n():
    lo, hi = wilson_ci(successes=0, n=0)
    assert lo == 0.0
    assert hi == 0.0


def test_wilson_ci_matches_known_value_n30_p0_67():
    # 20 of 30 correct: p=0.667. Wilson 95% CI well-known to be ~[0.49, 0.81]
    # for this sample (table value, hand-computed).
    lo, hi = wilson_ci(successes=20, n=30)
    assert 0.47 < lo < 0.51
    assert 0.80 < hi < 0.83


def test_wilson_ci_bounds_never_escape_unit_interval():
    # Adversarial: large z, tiny n, extreme p. Wilson must still return [0,1]
    # bounds — this is its whole reason for existing over Normal approximation.
    for s, n in [(0, 1), (1, 1), (3, 4), (999, 1000)]:
        lo, hi = wilson_ci(successes=s, n=n)
        assert 0.0 <= lo <= 1.0
        assert 0.0 <= hi <= 1.0
        assert lo <= hi


from benchmarks.longmemeval.aggregate import flip_rate


def test_flip_rate_zero_when_all_correct():
    # 5 of 5 correct → p=1 → 2p(1-p) = 0.
    assert flip_rate(correct=5, runs=5) == 0.0


def test_flip_rate_zero_when_all_wrong():
    # 0 of 5 correct → p=0 → 0.
    assert flip_rate(correct=0, runs=5) == 0.0


def test_flip_rate_maxes_at_half():
    # Perfectly split 3/6 → p=0.5 → 2(0.5)(0.5) = 0.5 — the max possible.
    assert flip_rate(correct=3, runs=6) == 0.5


def test_flip_rate_asymmetric_case():
    # 4 of 5 correct → p=0.8 → 2(0.8)(0.2) = 0.32.
    assert abs(flip_rate(correct=4, runs=5) - 0.32) < 1e-9


def test_flip_rate_zero_runs_is_zero():
    # Never-observed question: degenerate to 0.
    assert flip_rate(correct=0, runs=0) == 0.0


def test_classify_retrieval_miss():
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q2"])
    assert bucket == FailureBucket.RETRIEVAL_MISS


def test_classify_retrieval_hit_qa_miss():
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q3"])
    assert bucket == FailureBucket.RETRIEVAL_HIT_QA_MISS


def test_classify_marginal():
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q4"])
    assert bucket == FailureBucket.MARGINAL


def test_classify_ambiguous_via_rationale_phrase():
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q5"])
    assert bucket == FailureBucket.AMBIGUOUS


def test_classify_correct_answer_returns_none():
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q1"])
    assert bucket is None


def test_classify_errored_returns_none():
    # Errored questions shouldn't be classified as a failure bucket —
    # they're a separate category surfaced in the summary header.
    records = _by_id(load_records([FIXTURE_PATH]))
    bucket = classify_failure(records["q6"])
    assert bucket is None


def test_load_records_skips_blank_lines(tmp_path):
    # Real bench JSONL may have trailing newlines; loader must handle them.
    src = tmp_path / "run.jsonl"
    src.write_text('{"question_id":"a","question_type":"t"}\n\n{"question_id":"b","question_type":"t"}\n')
    records = load_records([src])
    assert [r["question_id"] for r in records] == ["a", "b"]
