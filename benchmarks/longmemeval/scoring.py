"""Retrieval scoring: session-level (MemPalace-style) + fact-level (Sonzai-style).

Session-level matches MemPalace's published Recall@5 methodology: an item is a
hit if its session ID appears in ``answer_session_ids``. Fact-level is used for
systems that store extracted facts instead of raw sessions — an item is a hit
if its text contains the ground-truth answer (normalized).
"""

from __future__ import annotations

import math
import re
from collections.abc import Sequence


def recall_at_k(ranked_session_ids: Sequence[str], ground_truth: Sequence[str], k: int) -> float:
    """1.0 if any ground-truth session appears in the top-k, else 0.0."""
    if not ground_truth:
        return 0.0
    top = ranked_session_ids[:k]
    return 1.0 if any(gt in top for gt in ground_truth) else 0.0


def ndcg_at_k(ranked_session_ids: Sequence[str], ground_truth: Sequence[str], k: int) -> float:
    """Binary-relevance NDCG@k — same formula MemPalace uses in longmemeval_bench.py."""
    if not ground_truth:
        return 0.0
    gt_set = set(ground_truth)
    dcg = 0.0
    for i, sid in enumerate(ranked_session_ids[:k]):
        if sid in gt_set:
            dcg += 1.0 / math.log2(i + 2)
    ideal_hits = min(len(gt_set), k)
    idcg = sum(1.0 / math.log2(i + 2) for i in range(ideal_hits))
    return dcg / idcg if idcg > 0 else 0.0


# ---------------------------------------------------------------------------
# Fact-level (Sonzai)
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
    # Token-overlap fallback: all answer tokens present in the fact.
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
    dcg = 0.0
    hits = 0
    for i, f in enumerate(ranked_fact_texts[:k]):
        if _contains_answer(f, answer):
            dcg += 1.0 / math.log2(i + 2)
            hits += 1
    idcg = sum(1.0 / math.log2(i + 2) for i in range(max(hits, 1)))
    return dcg / idcg if idcg > 0 else 0.0
