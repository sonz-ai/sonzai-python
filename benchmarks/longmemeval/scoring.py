"""Retrieval scoring — bit-for-bit parity with MemPalace's longmemeval_bench.py.

MemPalace computes three rank metrics at k ∈ {1, 3, 5, 10, 30, 50} at both
session and turn granularity:

    recall_any@k : 1.0 iff ANY ground-truth session appears in the top-k.
    recall_all@k : 1.0 iff ALL ground-truth sessions appear in the top-k.
    ndcg_any@k   : DCG(top-k) / DCG(ideal sorting of top-k relevances).

The NDCG denominator is the ideal sort of the *retrieved* top-k, not the
theoretical maximum assuming all GT items are retrieved — this matches
MemPalace's ``ndcg()`` in ``benchmarks/longmemeval_bench.py``. Keeping the same
formula means our head-to-head numbers are directly comparable to MemPalace's
published results.

Fact-level variants (``fact_recall_at_k`` / ``fact_ndcg_at_k``) are kept for
Sonzai's fact-extracting backend, which doesn't store whole sessions — an
item is a hit if its text contains the ground-truth answer (normalized).
"""

from __future__ import annotations

import math
import re
from collections.abc import Sequence


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def session_id_from_corpus_id(corpus_id: str) -> str:
    """Map a turn-level corpus id (``sess_123_turn_4``) to its session (``sess_123``).

    MemPalace's ``longmemeval_bench.py`` uses the same rule: anything with a
    ``_turn_`` suffix is a turn doc, everything else is already a session doc.
    """
    if "_turn_" in corpus_id:
        return corpus_id.rsplit("_turn_", 1)[0]
    return corpus_id


def _dcg(relevances: Sequence[float], k: int) -> float:
    score = 0.0
    for i, rel in enumerate(relevances[:k]):
        score += rel / math.log2(i + 2)
    return score


# ---------------------------------------------------------------------------
# Session-level metrics (apples-to-apples with MemPalace)
# ---------------------------------------------------------------------------


def recall_any_at_k(
    ranked_session_ids: Sequence[str], ground_truth: Sequence[str], k: int
) -> float:
    """1.0 iff any ground-truth session appears in the top-k.

    Matches MemPalace's ``float(any(cid in top_k_ids for cid in correct_ids))``
    including the empty-GT case — ``any([])`` is False → 0.0.
    """
    top = set(ranked_session_ids[:k])
    return float(any(gt in top for gt in ground_truth))


def recall_all_at_k(
    ranked_session_ids: Sequence[str], ground_truth: Sequence[str], k: int
) -> float:
    """1.0 iff every ground-truth session appears in the top-k.

    Matches MemPalace's ``float(all(cid in top_k_ids for cid in correct_ids))``
    including the empty-GT vacuous-truth case — ``all([])`` is True → 1.0.
    Bench callers that want a custom empty-GT policy should filter upstream
    rather than special-case it here (parity > defensive defaults).
    """
    top = set(ranked_session_ids[:k])
    return float(all(gt in top for gt in ground_truth))


def ndcg_at_k(
    ranked_session_ids: Sequence[str], ground_truth: Sequence[str], k: int
) -> float:
    """MemPalace-identical NDCG — ideal denominator is the sort of the top-k itself.

    Empty GT falls through naturally: all relevances are 0, IDCG=0, and we
    return 0.0 — same as MemPalace's early ``if idcg == 0: return 0.0``.
    """
    gt_set = set(ground_truth)
    relevances = [1.0 if sid in gt_set else 0.0 for sid in ranked_session_ids[:k]]
    ideal = sorted(relevances, reverse=True)
    idcg = _dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _dcg(relevances, k) / idcg


def recall_at_g(
    ranked_session_ids: Sequence[str], ground_truth: Sequence[str]
) -> float:
    """Fractional recall at k = |ground_truth| (R@G).

    R@G normalizes across questions with different numbers of answer-bearing
    sessions: take the top |GT| retrievals and return the fraction that are
    ground-truth hits. A question with 3 GT sessions that surfaces 2 of them
    in the top 3 scores 0.667, regardless of how many distractors the haystack
    contains.

    This is the metric Mem0 / A-Mem / Zep benchmarks headline against. We
    compute it per-question and let the runner average across the set.
    """
    g = len(ground_truth)
    if g == 0:
        return 0.0
    gt_set = set(ground_truth)
    top = ranked_session_ids[:g]
    hits = sum(1 for sid in top if sid in gt_set)
    return hits / g


# Back-compat alias. Kept because callers outside this benchmark (and older
# result files) refer to ``recall_at_k`` expecting "any" semantics.
recall_at_k = recall_any_at_k


# ---------------------------------------------------------------------------
# Fact-level (Sonzai's fact-extracting backend)
# ---------------------------------------------------------------------------


_NORM = re.compile(r"[^a-z0-9 ]+")


def _normalize(s: str) -> str:
    return _NORM.sub("", s.lower()).strip()


def _contains_answer(fact_text: str, answer: str) -> bool:
    nf = _normalize(fact_text)
    na = _normalize(answer)
    if not nf or not na:
        return False
    if na in nf:
        return True
    tokens = na.split()
    if not tokens:
        return False
    return all(t in nf for t in tokens)


def fact_recall_at_k(ranked_fact_texts: Sequence[str], answer: str, k: int) -> float:
    """1.0 if any of the top-k retrieved facts contains the ground-truth answer."""
    if not answer:
        return 0.0
    return 1.0 if any(_contains_answer(f, answer) for f in ranked_fact_texts[:k]) else 0.0


def fact_ndcg_at_k(ranked_fact_texts: Sequence[str], answer: str, k: int) -> float:
    if not answer:
        return 0.0
    relevances = [
        1.0 if _contains_answer(f, answer) else 0.0 for f in ranked_fact_texts[:k]
    ]
    ideal = sorted(relevances, reverse=True)
    idcg = _dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _dcg(relevances, k) / idcg
