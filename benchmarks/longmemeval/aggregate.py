"""Multi-run LongMemEval aggregator.

Takes N bench JSONL files, produces:
  1. A per-question_type summary table (accuracy, Wilson 95% CI, flip rate,
     failure-bucket counts) printed to stdout.
  2. A ``failures.json`` sidecar file listing each failing (question_id,
     run_index) pair with classification, ready for ``inspect.py``.

No dependencies beyond the standard library.
"""

from __future__ import annotations

import math


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


import json
from enum import Enum
from pathlib import Path
from typing import Iterable


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
    "partially correct",
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
                    print(f"warn: {path}:{lineno} skipped malformed JSON: {e}")
    return out
