"""LoCoMo scoring — token-F1, session-level Recall@K, NDCG@K, aggregation.

mem0 reports per-category LLM-judge accuracy as the headline; we mirror that
plus token-F1 (paper-original metric) plus retrieval Recall@K / NDCG@K at
session granularity. dia_id-level retrieval isn't comparable across systems
that don't track per-turn provenance.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Sequence

from .backends import RankedMemoryItem

KS = (1, 3, 5, 10, 30)

# LoCoMo dia_ids look like "D3:14" — leading digits of the first half are the
# session index.
_DIA_ID_RE = re.compile(r"^D(\d+):\d+$")


# ---------------------------------------------------------------------------
# Text normalisation + token-F1
# ---------------------------------------------------------------------------


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(s: str) -> list[str]:
    return _WORD_RE.findall((s or "").lower())


def token_f1(pred: str, gold: str) -> float:
    """Harmonic mean of token-precision and token-recall (SQuAD-style F1)."""
    pt = _tokens(pred)
    gt = _tokens(gold)
    if not pt or not gt:
        return 0.0
    common: dict[str, int] = {}
    pt_count: dict[str, int] = {}
    gt_count: dict[str, int] = {}
    for t in pt:
        pt_count[t] = pt_count.get(t, 0) + 1
    for t in gt:
        gt_count[t] = gt_count.get(t, 0) + 1
    for t, c in pt_count.items():
        common[t] = min(c, gt_count.get(t, 0))
    n_common = sum(common.values())
    if n_common == 0:
        return 0.0
    precision = n_common / len(pt)
    recall = n_common / len(gt)
    return 2 * precision * recall / (precision + recall)


# ---------------------------------------------------------------------------
# Evidence projection — dia_id → session_id
# ---------------------------------------------------------------------------


def evidence_to_session_ids(evidence: Iterable[str]) -> set[str]:
    """Map dia_ids (e.g. "D3:14") to LoCoMo session_ids ("session_3")."""
    out: set[str] = set()
    for e in evidence:
        m = _DIA_ID_RE.match((e or "").strip())
        if m:
            out.add(f"session_{int(m.group(1))}")
    return out


# ---------------------------------------------------------------------------
# Ranking helpers — merge per-speaker lists before scoring
# ---------------------------------------------------------------------------


def merge_speaker_rankings(
    speaker_a: Sequence[RankedMemoryItem],
    speaker_b: Sequence[RankedMemoryItem],
) -> list[str]:
    """Merge dual-speaker retrievals into a single dedup session-id ranking.

    Sort-by-score across both lists; dedup by session_id, preserving first
    occurrence. Items with no session_id are skipped.
    """
    combined = sorted(
        list(speaker_a) + list(speaker_b),
        key=lambda it: -it.score,
    )
    seen: set[str] = set()
    out: list[str] = []
    for it in combined:
        if not it.session_id or it.session_id in seen:
            continue
        seen.add(it.session_id)
        out.append(it.session_id)
    return out


# ---------------------------------------------------------------------------
# Retrieval metrics
# ---------------------------------------------------------------------------


def recall_any_at_k(
    retrieved: Sequence[str], ground_truth: "set[str] | Sequence[str]", k: int,
) -> float:
    """1.0 iff any ground-truth session appears in the top-k retrieval."""
    gt = set(ground_truth)
    if not gt:
        return 0.0
    top = set(retrieved[:k])
    return float(bool(gt & top))


def _dcg(relevances: Sequence[float], k: int) -> float:
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances[:k]))


def ndcg_at_k(
    retrieved: Sequence[str], ground_truth: "set[str] | Sequence[str]", k: int,
) -> float:
    gt = set(ground_truth)
    if not gt:
        return 0.0
    relevances = [1.0 if sid in gt else 0.0 for sid in retrieved[:k]]
    ideal = sorted(relevances, reverse=True)
    idcg = _dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _dcg(relevances, k) / idcg


def retrieval_metrics_grid(
    retrieved: Sequence[str], ground_truth: "set[str] | Sequence[str]",
) -> dict[str, float]:
    out: dict[str, float] = {}
    for k in KS:
        out[f"recall_any@{k}"] = recall_any_at_k(retrieved, ground_truth, k)
        out[f"ndcg_any@{k}"] = ndcg_at_k(retrieved, ground_truth, k)
    return out


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_rows(rows: list[dict]) -> dict:
    """Per-category means + overall — mirrors mem0's report table shape."""
    by_cat: dict[int, list[dict]] = {}
    for r in rows:
        c = int(r.get("category") or 0)
        by_cat.setdefault(c, []).append(r)

    def _mean(values: list[float]) -> float:
        vs = [v for v in values if v is not None]
        return sum(vs) / len(vs) if vs else 0.0

    per_cat: dict[int, dict[str, float]] = {}
    for cat, group in by_cat.items():
        per_cat[cat] = {
            "n": len(group),
            "llm_accuracy": _mean([float(g.get("llm_correct") or False) for g in group]),
            "token_f1": _mean([float(g.get("token_f1") or 0.0) for g in group]),
        }
        for k in KS:
            per_cat[cat][f"recall_any@{k}"] = _mean([
                float((g.get("retrieval") or {}).get(f"recall_any@{k}") or 0.0) for g in group
            ])
            per_cat[cat][f"ndcg_any@{k}"] = _mean([
                float((g.get("retrieval") or {}).get(f"ndcg_any@{k}") or 0.0) for g in group
            ])

    overall = {
        "n": sum(len(g) for g in by_cat.values()),
        "llm_accuracy": _mean([float(r.get("llm_correct") or False) for r in rows]),
        "token_f1": _mean([float(r.get("token_f1") or 0.0) for r in rows]),
    }
    for k in KS:
        overall[f"recall_any@{k}"] = _mean([
            float((r.get("retrieval") or {}).get(f"recall_any@{k}") or 0.0) for r in rows
        ])
        overall[f"ndcg_any@{k}"] = _mean([
            float((r.get("retrieval") or {}).get(f"ndcg_any@{k}") or 0.0) for r in rows
        ])

    return {"per_category": per_cat, "overall": overall}
