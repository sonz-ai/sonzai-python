"""Multi-run LongMemEval aggregator.

Takes N bench JSONL files, produces:
  1. A per-question_type summary table (accuracy, Wilson 95% CI, flip rate,
     failure-bucket counts) printed to stdout.
  2. A ``failures.json`` sidecar file listing each failing (question_id,
     run_index) pair with classification, ready for ``inspect.py``.

No dependencies beyond the standard library.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable


def wilson_ci(*, successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score 95% CI for a binomial proportion.

    Prefer this over Normal approximation when n is small or p is near 0/1 —
    Wilson stays inside [0,1] by construction. At LongMemEval's n=30
    subtype level, this matters: Normal CIs would extend below 0 at p=0.1
    or above 1 at p=0.9.

    Returns (lower, upper). Zero-n sample degenerates to (0, 0).
    """
    if n <= 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1.0 + (z * z) / n
    center = (p + (z * z) / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + (z * z) / (4 * n * n))) / denom
    lo = max(0.0, center - half)
    hi = min(1.0, center + half)
    return (lo, hi)


def flip_rate(*, correct: int, runs: int) -> float:
    """Per-question noise estimator across N bench runs.

    Given how many of ``runs`` marked a question correct, returns
    ``2 * p * (1 - p)`` where ``p = correct / runs``. Maxes at 0.5 when
    perfectly split, drops to 0 when the question is stable (all-correct
    or all-wrong across runs).

    Interpretation: the mean flip_rate across a subtype is an empirical
    lower bound on how much of that subtype's miss rate is reducible
    via better retrieval vs. judge/LLM stochasticity.
    """
    if runs <= 0:
        return 0.0
    p = correct / runs
    return 2 * p * (1 - p)


class FailureBucket(str, Enum):
    """Classification of a failing (question, run) pair.

    Each bucket points at a different class of intervention:
      RETRIEVAL_MISS     → upstream retrieval-side fix (decomposition,
                           graph walks, entity seeding).
      RETRIEVAL_HIT_QA_MISS → downstream composition fix (ensemble
                              answering, better prompting, render-cap
                              logic).
      MARGINAL           → render-cap tuning or fact-ordering fix.
      AMBIGUOUS          → not a system failure; judge-side noise.
    """

    RETRIEVAL_MISS = "retrieval-miss"
    RETRIEVAL_HIT_QA_MISS = "retrieval-hit / qa-miss"
    MARGINAL = "marginal"
    AMBIGUOUS = "ambiguous"


# String-match phrases that signal the judge found the answer defensible
# despite marking it wrong. Imperfect heuristic by design — see spec.
_AMBIGUOUS_PHRASES = (
    "partially",
    "defensible",
    "close to",
    "not quite",
    "mostly",
)


def classify_failure(record: dict) -> FailureBucket | None:
    """Classify a single bench record into a failure bucket, or None.

    Returns None for:
      - correct answers (qa_correct=True)
      - errored records (extra.error present)
      - records with no qa_correct field (retrieval-only runs)
    """
    if record.get("extra", {}).get("error"):
        return None
    if "qa_correct" not in record:
        return None
    if record.get("qa_correct") is True:
        return None

    expected = set(record.get("answer_session_ids") or [])
    retrieved_items = (record.get("retrieval_results") or {}).get("ranked_items") or []
    retrieved_top10 = [it.get("corpus_id") for it in retrieved_items[:10]]
    hit_ranks = [i for i, cid in enumerate(retrieved_top10) if cid in expected]

    if not hit_ranks:
        return FailureBucket.RETRIEVAL_MISS
    if min(hit_ranks) >= 8:
        return FailureBucket.MARGINAL

    rationale = (record.get("qa_rationale") or "").lower()
    if any(phrase in rationale for phrase in _AMBIGUOUS_PHRASES):
        return FailureBucket.AMBIGUOUS

    return FailureBucket.RETRIEVAL_HIT_QA_MISS


def load_records(paths: Iterable[Path | str]) -> list[dict]:
    """Read JSONL records from each path; skip blank lines and malformed JSON.

    Malformed lines are skipped with a printed warning — we don't want
    a single truncated record to abort a 5-run aggregation.
    """
    out: list[dict] = []
    for p in paths:
        path = Path(p)
        with path.open() as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"warn: {path}:{lineno} skipped malformed JSON: {e}", file=sys.stderr)
    return out


@dataclass
class SubtypeSummary:
    subtype: str
    n_total: int
    n_correct: int
    accuracy: float
    ci_lo: float
    ci_hi: float
    mean_flip_rate: float
    bucket_counts: dict[str, int]


@dataclass
class AggregateResult:
    total_scored: int  # (question × run) pairs with qa_correct present
    errored_count: int
    missing_qa_count: int
    subtypes: list[SubtypeSummary]
    failures: list[dict] = field(default_factory=list)


def aggregate_runs(
    paths: Iterable[Path | str],
    *,
    failures_out: Path | str | None = None,
) -> AggregateResult:
    """Aggregate across N bench runs. See module docstring for shape."""
    records = load_records(paths)

    # Group correct/total by (question_id, subtype) for flip-rate;
    # separately group records by subtype for bucket classification + CI.
    # A record is scoreable iff it has qa_correct and no error.
    per_question_runs: dict[str, list[dict]] = defaultdict(list)
    scoreable: list[dict] = []
    errored = 0
    missing_qa = 0
    for r in records:
        if r.get("extra", {}).get("error"):
            errored += 1
            continue
        if "qa_correct" not in r:
            missing_qa += 1
            continue
        scoreable.append(r)
        per_question_runs[r["question_id"]].append(r)

    # Per-subtype accumulators.
    by_subtype: dict[str, list[dict]] = defaultdict(list)
    for r in scoreable:
        by_subtype[r.get("question_type", "unknown")].append(r)

    subtypes: list[SubtypeSummary] = []
    failures: list[dict] = []
    for subtype, rs in sorted(by_subtype.items()):
        n_total = len(rs)
        n_correct = sum(1 for r in rs if r["qa_correct"])
        accuracy = n_correct / n_total if n_total else 0.0
        lo, hi = wilson_ci(successes=n_correct, n=n_total)

        # Bucket counts and failures list.
        bucket_counts: dict[str, int] = defaultdict(int)
        for r in rs:
            bucket = classify_failure(r)
            if bucket is not None:
                bucket_counts[bucket.value] += 1
                failures.append(_failure_entry(r, bucket))

        # Per-question flip rate, meaned across the questions in this subtype.
        qids_in_subtype = {r["question_id"] for r in rs}
        fr_values: list[float] = []
        for qid in qids_in_subtype:
            runs_of_q = per_question_runs[qid]
            fr_values.append(flip_rate(
                correct=sum(1 for r in runs_of_q if r["qa_correct"]),
                runs=len(runs_of_q),
            ))
        mean_fr = sum(fr_values) / len(fr_values) if fr_values else 0.0

        subtypes.append(SubtypeSummary(
            subtype=subtype,
            n_total=n_total,
            n_correct=n_correct,
            accuracy=accuracy,
            ci_lo=lo,
            ci_hi=hi,
            mean_flip_rate=mean_fr,
            bucket_counts=dict(bucket_counts),
        ))

    result = AggregateResult(
        total_scored=len(scoreable),
        errored_count=errored,
        missing_qa_count=missing_qa,
        subtypes=subtypes,
        failures=failures,
    )

    if failures_out is not None:
        Path(failures_out).write_text(json.dumps(failures, indent=2))

    return result


def _failure_entry(record: dict, bucket: FailureBucket) -> dict:
    """Shape the record consumed by inspect.py."""
    retrieved_items = (record.get("retrieval_results") or {}).get("ranked_items") or []
    top10 = [it.get("corpus_id") for it in retrieved_items[:10]]
    expected = list(record.get("answer_session_ids") or [])
    hit_ranks = [i for i, cid in enumerate(top10) if cid in set(expected)]
    return {
        "question_id": record.get("question_id"),
        "question_type": record.get("question_type"),
        "bucket": bucket.value,
        "question": record.get("question"),
        "answer": record.get("answer"),
        "agent_answer": record.get("agent_answer"),
        "qa_rationale": record.get("qa_rationale"),
        "expected_sessions": expected,
        "retrieved_top10": top10,
        "hit_ranks": hit_ranks,
    }


def _print_summary(result: AggregateResult) -> None:
    """Human-readable summary table on stdout."""
    print(f"scored: {result.total_scored}  errored: {result.errored_count}  missing_qa: {result.missing_qa_count}")
    print()
    bucket_header = f"{'R-miss':>6} / {'R-hit-QA':>8} / {'marginal':>8} / {'ambig':>5}"
    header = f"{'subtype':<30} {'n':>4} {'acc':>6} {'CI 95%':>16} {'flip':>6}  {bucket_header}"
    print(header)
    print("-" * len(header))
    for s in result.subtypes:
        ci = f"[{s.ci_lo:.2f}, {s.ci_hi:.2f}]"
        bc = s.bucket_counts
        buckets = f"{bc.get('retrieval-miss', 0):>6} / {bc.get('retrieval-hit / qa-miss', 0):>8} / {bc.get('marginal', 0):>8} / {bc.get('ambiguous', 0):>5}"
        print(f"{s.subtype:<30} {s.n_total:>4} {s.accuracy:>6.3f} {ci:>16} {s.mean_flip_rate:>6.3f}  {buckets}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Aggregate LongMemEval bench runs")
    p.add_argument("paths", nargs="+", help="JSONL files to aggregate (glob-expanded by shell)")
    p.add_argument(
        "--output",
        default="failures.json",
        help="Path to write failures.json sidecar (default: ./failures.json)",
    )
    args = p.parse_args(argv)

    out_path = Path(args.output).resolve()
    result = aggregate_runs(args.paths, failures_out=out_path)
    _print_summary(result)
    print()
    print(f"failures written: {len(result.failures)} → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
