"""ConvoMem scoring and summary aggregation.

Headline: per-category QA accuracy + MemScore (accuracy% / avg_latency_ms /
avg_context_tokens). MemScore is intentionally a triple rather than a single
number — collapsing quality, latency, and cost into one value hides tradeoffs.

Mirrors Supermemory's published shape so the comparison table drops straight
into the README.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

# Display order for per-category tables. Matches ConvoMem paper layout:
# Information Extraction first (user / assistant facts), then preferences,
# then dynamic capabilities (changing, implicit connections), then abstention.
CATEGORY_ORDER: list[str] = [
    "user_evidence",
    "assistant_facts_evidence",
    "preference_evidence",
    "changing_evidence",
    "implicit_connection_evidence",
    "abstention_evidence",
]


def aggregate_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-question JSONL rows into a summary dict.

    Schema expected per row::

        {
          "question_id": str,
          "question_type": str,    # one of CATEGORY_ORDER
          "qa_correct": bool | None,
          "elapsed_ms": int | None,
          "extra": {
            "chat_loaded_facts_count": int | None,   # MemScore context-token proxy
            "advance_time_calls": int,
            "consolidation_events": int,
            "advance_time_failures": int,
          }
        }

    Missing ``qa_correct`` (retrieval-only / error rows) contribute to ``n`` but
    are excluded from QA accuracy — matches longmemeval's convention so
    retrieval-only runs report accuracy on the rows where QA was actually
    attempted, not 0% on rows where it wasn't.
    """
    n = len(rows)
    if n == 0:
        return {"n": 0}

    scored = [r for r in rows if r.get("qa_correct") is True or r.get("qa_correct") is False]
    correct = sum(1 for r in scored if r.get("qa_correct") is True)

    # Per-type breakdown
    by_type: dict[str, dict[str, Any]] = {}
    type_scored: dict[str, int] = defaultdict(int)
    type_correct: dict[str, int] = defaultdict(int)
    type_n: dict[str, int] = defaultdict(int)
    for r in rows:
        t = str(r.get("question_type") or "")
        type_n[t] += 1
        qc = r.get("qa_correct")
        if qc is True or qc is False:
            type_scored[t] += 1
            if qc is True:
                type_correct[t] += 1
    for t, total in type_n.items():
        s = type_scored[t]
        by_type[t] = {
            "n": total,
            "qa_scored": s,
            "qa_correct": type_correct[t],
            "qa_accuracy": (type_correct[t] / s) if s else None,
        }

    # MemScore
    latencies = [int(r.get("elapsed_ms") or 0) for r in rows if r.get("elapsed_ms")]
    ctx_tokens = [
        int((r.get("extra") or {}).get("chat_loaded_facts_count") or 0)
        for r in rows
    ]
    ctx_tokens = [v for v in ctx_tokens if v > 0] or ctx_tokens  # tolerate zeros
    memscore = {
        "accuracy_pct": (correct / len(scored) * 100.0) if scored else None,
        "avg_latency_ms": (sum(latencies) / len(latencies)) if latencies else None,
        "avg_context_tokens": (sum(ctx_tokens) / len(ctx_tokens)) if ctx_tokens else None,
    }

    # advance_time diagnostics
    adv_calls = sum(int((r.get("extra") or {}).get("advance_time_calls", 0) or 0) for r in rows)
    adv_cons = sum(int((r.get("extra") or {}).get("consolidation_events", 0) or 0) for r in rows)
    adv_fail = sum(int((r.get("extra") or {}).get("advance_time_failures", 0) or 0) for r in rows)

    return {
        "n": n,
        "qa_accuracy": (correct / len(scored)) if scored else None,
        "qa_scored": len(scored),
        "qa_correct": correct,
        "by_type": by_type,
        "memscore": memscore,
        "advance_time": {
            "total_calls": adv_calls,
            "total_consolidations": adv_cons,
            "total_failures": adv_fail,
            "avg_calls": (adv_calls / n) if n else 0.0,
        },
    }


def format_percent(v: float | None) -> str:
    """Format a 0..1 accuracy as XX.YY%, or '-' for missing/unscored."""
    if v is None:
        return "-"
    return f"{v * 100:.2f}%"
