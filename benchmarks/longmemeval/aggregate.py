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
