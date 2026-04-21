"""LongMemEval runner: ingest haystacks, score retrieval + QA, write JSONL.

Parity note — this file is deliberately shaped to match MemPalace's own
``benchmarks/longmemeval_bench.py``:

- Same rank-metric grid: ks = [1, 3, 5, 10, 30, 50].
- Same three metrics at each k: ``recall_any``, ``recall_all``, ``ndcg_any``.
- Same session/turn split (turn-level = corpus_id retains its turn suffix;
  session-level = turn ids collapsed via ``session_id_from_corpus_id``).
- Same per-question-type breakdown at ``recall_any@10``.
- Output JSONL mirrors MemPalace's ``retrieval_results`` schema so either
  benchmark's log can be fed to either scorer.

Concurrency is bounded by ``--concurrency`` over questions. Each question is
fully independent (fresh agent, fresh user_id), so parallelism is clean.

Output schema (one line per question)::

    {
      "question_id": "...",
      "question_type": "temporal-reasoning",
      "backend": "sonzai" | "mempalace",
      "question": "...",
      "answer": "...",
      "answer_session_ids": ["s023"],
      "retrieval_results": {
        "query": "...",
        "ranked_items": [{"corpus_id": "s023", "text": "...", "timestamp": "..."}, ...],
        "metrics": {
          "session": {"recall_any@1": ..., "ndcg_any@50": ...},
          "turn":    {"recall_any@1": ..., "ndcg_any@50": ...}
        }
      },
      "agent_answer": "...",
      "qa_correct": true, "qa_rationale": "...",
      "extra": {...}    # backend-specific diagnostics, plus mempalace_metrics for parity
    }
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from sonzai import AsyncSonzai
from tqdm.asyncio import tqdm_asyncio

from ..common.dataset_cache import cache_root
from ..common.gemini_judge import (
    DEFAULT_MODEL as DEFAULT_JUDGE_MODEL,
    GeminiJudge,
    judge_qa_async,
)
from .backends import BackendResult, RankedItem
from .backends import mempalace as mempalace_backend
from .backends import sonzai as sonzai_backend
from .dataset import LongMemEvalQuestion, load_questions, resolve_dataset_path
from .scoring import (
    fact_ndcg_at_k,
    fact_recall_at_k,
    ndcg_at_k,
    recall_all_at_k,
    recall_any_at_k,
    recall_at_g,
    session_id_from_corpus_id,
)

logger = logging.getLogger("benchmarks.longmemeval")

# MemPalace's default evaluation grid — we mirror it exactly.
KS = (1, 3, 5, 10, 30, 50)
METRIC_NAMES = ("recall_any", "recall_all", "ndcg_any")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.longmemeval",
        description="Run the LongMemEval benchmark against Sonzai or MemPalace.",
    )
    p.add_argument(
        "--backend",
        choices=["sonzai", "mempalace"],
        default="sonzai",
        help="Memory system to evaluate (default: sonzai).",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of questions to evaluate (0 = all 500). Default 20 for a smoke run.",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Max questions in flight concurrently (default 4).",
    )
    p.add_argument(
        "--mode",
        choices=["retrieval", "qa", "both"],
        default="both",
        help="What to score (default both).",
    )
    p.add_argument(
        "--judge-model",
        default=DEFAULT_JUDGE_MODEL,
        help=f"Gemini model for QA judging (default {DEFAULT_JUDGE_MODEL}).",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSONL path (default: benchmarks/longmemeval/results/<backend>_<ts>.jsonl).",
    )
    p.add_argument(
        "--mempalace-mode",
        default="raw",
        help="MemPalace retrieval mode (raw | hybrid | hybrid_v3 | palace | ...). Default raw.",
    )
    p.add_argument(
        "--skip-advance-time",
        action="store_true",
        help="Sonzai only: skip advance_time between sessions. "
        "Produces a baseline without self-learning — the delta vs normal runs is the measured lift.",
    )
    p.add_argument(
        "--max-sessions-per-question",
        type=int,
        default=0,
        help="Sonzai only: cap haystack size per question (0 = full). "
        "Answer-bearing sessions are kept preferentially. Use for fast smoke runs.",
    )
    p.add_argument(
        "--dataset-path",
        type=Path,
        default=None,
        help="Override the dataset JSON file (default: auto-download LongMemEval-S). "
        "Use a pre-trimmed copy to match Sonzai's --max-sessions-per-question on the MemPalace side.",
    )
    p.add_argument(
        "--compare",
        nargs=2,
        metavar=("FILE_A", "FILE_B"),
        help="Compare two JSONL result files; print a markdown table and exit.",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
    )
    return p.parse_args(argv)


# ---------------------------------------------------------------------------
# Sonzai backend orchestration
# ---------------------------------------------------------------------------


async def _run_sonzai_backend(
    questions: list[LongMemEvalQuestion],
    *,
    concurrency: int,
    mode: str,
    judge: GeminiJudge | None,
    skip_advance_time: bool,
    max_sessions: int,
) -> list[dict]:
    # advance_time runs the full CE worker stack per simulated day and can take
    # minutes per call. The SDK default timeout (30s) is way too short.
    client = AsyncSonzai(timeout=600.0)
    sem = asyncio.Semaphore(concurrency)

    async def one(q: LongMemEvalQuestion) -> dict:
        async with sem:
            try:
                br = await sonzai_backend.run_question(
                    client,
                    q,
                    include_qa=(mode in {"qa", "both"}),
                    skip_advance_time=skip_advance_time,
                    max_sessions=max_sessions,
                )
            except Exception as e:
                logger.exception("sonzai backend failed on %s", q.question_id)
                return _error_row(q, "sonzai", str(e))
            return await _score_and_serialize(q, br, backend="sonzai", judge=judge, mode=mode)

    try:
        rows = await tqdm_asyncio.gather(*(one(q) for q in questions), desc="sonzai")
    finally:
        await client.close()
    return rows


# ---------------------------------------------------------------------------
# MemPalace backend orchestration (retrieval via their script; QA via Gemini reader)
# ---------------------------------------------------------------------------


_MEMPALACE_READER_PROMPT = """Answer the question using only the provided context from
prior conversations. If the answer isn't in the context, say "I don't know."
Be concise — one sentence typically.

# Context
{context}

# Question
{question}

# Answer"""


async def _mempalace_read_answer(
    judge: GeminiJudge, *, question: LongMemEvalQuestion, ranked_session_ids: list[str]
) -> str:
    """Gemini-based reader over MemPalace's retrieved top-k sessions.

    Retrieval-only systems need a reader for end-to-end QA comparison. We use
    the same Gemini model as the judge but in generation mode.
    """
    by_id = {s.session_id: s for s in question.sessions}
    top = [by_id[sid] for sid in ranked_session_ids[:5] if sid in by_id]
    if not top:
        return ""
    context = "\n\n".join(
        f"[{s.session_id} @ {s.date}]\n"
        + "\n".join(f"{t.role}: {t.content}" for t in s.turns)
        for s in top
    )
    resp = await judge._client.aio.models.generate_content(  # noqa: SLF001
        model=judge._model,  # noqa: SLF001
        contents=_MEMPALACE_READER_PROMPT.format(context=context, question=question.question),
    )
    return (resp.text or "").strip()


async def _run_mempalace_backend(
    questions: list[LongMemEvalQuestion],
    *,
    mempalace_mode: str,
    mode: str,
    judge: GeminiJudge | None,
    concurrency: int,
    dataset_path: Path,
) -> list[dict]:
    results = mempalace_backend.run_all(
        questions, dataset_path=dataset_path, mempalace_mode=mempalace_mode
    )

    sem = asyncio.Semaphore(concurrency)

    async def one(q: LongMemEvalQuestion) -> dict:
        br = results.get(q.question_id, BackendResult())
        if mode in {"qa", "both"} and br.ranked_session_ids and judge is not None:
            async with sem:
                br.agent_answer = await _mempalace_read_answer(
                    judge, question=q, ranked_session_ids=br.ranked_session_ids
                )
        return await _score_and_serialize(q, br, backend="mempalace", judge=judge, mode=mode)

    return await tqdm_asyncio.gather(*(one(q) for q in questions), desc="mempalace")


# ---------------------------------------------------------------------------
# Shared scoring / serialization
# ---------------------------------------------------------------------------


def _retrieval_metrics(
    items: list[RankedItem], answer_session_ids: list[str]
) -> dict[str, dict[str, float]]:
    """Compute MemPalace's full k-grid at both session and turn granularity.

    Bit-for-bit parity with MemPalace's ``benchmarks/longmemeval_bench.py``
    evaluation block (around line 3155 in their file):

    - **session-level**: each ranked item's ``corpus_id`` is mapped through
      ``session_id_from_corpus_id``. The resulting list is scored positionally
      — *no dedup before scoring*. If the same session shows up at rank 1
      and rank 3 (e.g. two retrieved facts from the same session), both
      positions contribute to DCG, matching MemPalace's ``session_level_ids``
      approach. Dedup before scoring would slightly undercount NDCG versus
      MemPalace's published numbers, so we avoid it.
    - **turn-level**: ``turn_correct`` set is the set of corpus_ids whose
      ``session_id_from_corpus_id`` is in ``answer_session_ids`` — identical
      to MemPalace's ``turn_correct`` set comprehension. Scoring runs over
      the turn-granular ranking directly.

    LongMemEval doesn't publish answer turn ids, so the turn-level metric
    here measures "any turn from an answer-bearing session shows up" — which
    is exactly MemPalace's definition, not a Sonzai-specific choice.
    """
    if not items:
        return {"session": {}, "turn": {}}

    corpus_ids_turn = [it.corpus_id for it in items]
    session_correct = set(answer_session_ids)
    # Positional session-id list, NO dedup — mirrors MemPalace's
    # ``session_level_ids = [session_id_from_corpus_id(cid) for cid in corpus_ids]``.
    session_level_ids = [session_id_from_corpus_id(cid) for cid in corpus_ids_turn]
    turn_correct = [cid for cid in corpus_ids_turn if session_id_from_corpus_id(cid) in session_correct]

    metrics: dict[str, dict[str, float]] = {"session": {}, "turn": {}}
    for k in KS:
        metrics["session"][f"recall_any@{k}"] = recall_any_at_k(
            session_level_ids, answer_session_ids, k
        )
        metrics["session"][f"recall_all@{k}"] = recall_all_at_k(
            session_level_ids, answer_session_ids, k
        )
        metrics["session"][f"ndcg_any@{k}"] = ndcg_at_k(
            session_level_ids, answer_session_ids, k
        )

        # Turn-level scoring runs over the original turn-granular ranking and
        # judges each corpus_id against the turn_correct set — same as MemPalace.
        metrics["turn"][f"recall_any@{k}"] = recall_any_at_k(
            corpus_ids_turn, turn_correct, k
        )
        metrics["turn"][f"recall_all@{k}"] = recall_all_at_k(
            corpus_ids_turn, turn_correct, k
        )
        metrics["turn"][f"ndcg_any@{k}"] = ndcg_at_k(
            corpus_ids_turn, turn_correct, k
        )

    # R@G — fractional recall at k = |GT|. For session-level we use the
    # positional list (same as above); a session hit at rank N counts as one
    # "correct" item in the top-|GT| window. For turn-level, ``turn_correct``
    # defines the GT set, identical to MemPalace's comprehension.
    metrics["session"]["recall_at_g"] = recall_at_g(session_level_ids, answer_session_ids)
    metrics["turn"]["recall_at_g"] = recall_at_g(corpus_ids_turn, turn_correct)
    return metrics


async def _score_and_serialize(
    q: LongMemEvalQuestion,
    br: BackendResult,
    *,
    backend: str,
    judge: GeminiJudge | None,
    mode: str,
) -> dict:
    items = br.ranked_items
    if not items and br.ranked_session_ids:
        # Backends that only surfaced a session-id projection (e.g. older
        # outputs) still get scored — synthesize RankedItems.
        items = [RankedItem(corpus_id=sid, text="") for sid in br.ranked_session_ids]

    row: dict = {
        "question_id": q.question_id,
        "question_type": q.question_type,
        "backend": backend,
        "question": q.question,
        "answer": q.answer,
        "answer_session_ids": q.answer_session_ids,
        "retrieval_results": {
            "query": q.question,
            "ranked_items": [
                {"corpus_id": it.corpus_id, "text": it.text[:500], "timestamp": it.timestamp}
                for it in items[:50]
            ],
            "metrics": {"session": {}, "turn": {}},
        },
        "agent_answer": br.agent_answer,
        "extra": dict(br.extra),
    }

    if mode in {"retrieval", "both"}:
        metrics = _retrieval_metrics(items, q.answer_session_ids)
        row["retrieval_results"]["metrics"] = metrics
        # Sonzai-specific fact-level recall (an extra signal, not part of parity).
        if br.ranked_fact_texts:
            row["extra"]["fact_recall_at_5"] = fact_recall_at_k(br.ranked_fact_texts, q.answer, 5)
            row["extra"]["fact_ndcg_at_5"] = fact_ndcg_at_k(br.ranked_fact_texts, q.answer, 5)

    if mode in {"qa", "both"} and br.agent_answer and judge is not None:
        try:
            verdict = await judge_qa_async(
                judge,
                question=q.question,
                ground_truth=q.answer,
                agent_answer=br.agent_answer,
            )
            row["qa_correct"] = verdict.correct
            row["qa_rationale"] = verdict.rationale
        except Exception as e:
            logger.warning("judge failed on %s: %s", q.question_id, e)
            row["qa_correct"] = None
            row["qa_rationale"] = f"judge-error: {e}"

    return row


def _error_row(q: LongMemEvalQuestion, backend: str, err: str) -> dict:
    return {
        "question_id": q.question_id,
        "question_type": q.question_type,
        "backend": backend,
        "question": q.question,
        "answer": q.answer,
        "answer_session_ids": q.answer_session_ids,
        "retrieval_results": {"query": q.question, "ranked_items": [], "metrics": {"session": {}, "turn": {}}},
        "agent_answer": "",
        "extra": {"error": err},
    }


# ---------------------------------------------------------------------------
# Output & summary
# ---------------------------------------------------------------------------


def _default_output_path(backend: str) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    return results_dir / f"{backend}_{ts}.jsonl"


def _write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def _summarize(rows: list[dict]) -> dict:
    if not rows:
        return {}
    n = len(rows)
    qa_rows = [r for r in rows if r.get("qa_correct") is True or r.get("qa_correct") is False]

    summary: dict = {"n": n}

    # Aggregate retrieval metrics across the full k-grid.
    sums: dict[str, dict[str, float]] = {"session": defaultdict(float), "turn": defaultdict(float)}
    counts: dict[str, dict[str, int]] = {"session": defaultdict(int), "turn": defaultdict(int)}
    for r in rows:
        metrics = (r.get("retrieval_results") or {}).get("metrics") or {}
        for gran in ("session", "turn"):
            for key, val in (metrics.get(gran) or {}).items():
                sums[gran][key] += float(val)
                counts[gran][key] += 1

    retrieval: dict[str, dict[str, float]] = {"session": {}, "turn": {}}
    for gran in ("session", "turn"):
        for key, total in sums[gran].items():
            c = counts[gran][key]
            if c:
                retrieval[gran][key] = total / c
    summary["retrieval"] = retrieval

    if qa_rows:
        summary["qa_accuracy"] = sum(1 for r in qa_rows if r["qa_correct"]) / len(qa_rows)

    # Per-type breakdown — R@G, R@10, R@30, QA accuracy.
    by_type: dict[str, dict] = {}
    for r in rows:
        t = r["question_type"]
        bucket = by_type.setdefault(
            t,
            {
                "n": 0,
                "qa_correct_sum": 0,
                "rg_sum": 0.0,
                "r10_sum": 0.0,
                "r30_sum": 0.0,
            },
        )
        bucket["n"] += 1
        if r.get("qa_correct") is True:
            bucket["qa_correct_sum"] += 1
        session_metrics = ((r.get("retrieval_results") or {}).get("metrics") or {}).get("session") or {}
        bucket["rg_sum"] += float(session_metrics.get("recall_at_g", 0.0))
        bucket["r10_sum"] += float(session_metrics.get("recall_any@10", 0.0))
        bucket["r30_sum"] += float(session_metrics.get("recall_any@30", 0.0))
    for t, b in by_type.items():
        if b["n"]:
            b["qa_accuracy"] = b["qa_correct_sum"] / b["n"]
            b["recall_at_g"] = b["rg_sum"] / b["n"]
            b["recall_any@10"] = b["r10_sum"] / b["n"]
            b["recall_any@30"] = b["r30_sum"] / b["n"]
    summary["by_type"] = by_type

    # Advance-time diagnostics — proves CE workers actually ran.
    adv_calls = [int(r.get("extra", {}).get("advance_time_calls", 0) or 0) for r in rows]
    adv_cons = [int(r.get("extra", {}).get("consolidation_events", 0) or 0) for r in rows]
    adv_fail = [int(r.get("extra", {}).get("advance_time_failures", 0) or 0) for r in rows]
    if any(adv_calls) or any(adv_fail):
        summary["advance_time"] = {
            "total_calls": sum(adv_calls),
            "total_consolidations": sum(adv_cons),
            "total_failures": sum(adv_fail),
            "avg_calls": sum(adv_calls) / max(len(adv_calls), 1),
        }

    return summary


def _print_summary(summary: dict, *, label: str) -> None:
    if not summary:
        print(f"[{label}] no results")
        return
    print(f"\n=== {label} (n={summary['n']}) ===")
    retrieval = summary.get("retrieval") or {}
    session_m = retrieval.get("session") or {}

    # Headline: the three numbers we compare against MemPalace —
    # R@G, R@10, R@30, plus QA accuracy.
    rg = session_m.get("recall_at_g")
    r10 = session_m.get("recall_any@10")
    r30 = session_m.get("recall_any@30")
    qa = summary.get("qa_accuracy")
    headline_bits = []
    if rg is not None:
        headline_bits.append(f"R@G={rg:.3f}")
    if r10 is not None:
        headline_bits.append(f"R@10={r10:.3f}")
    if r30 is not None:
        headline_bits.append(f"R@30={r30:.3f}")
    if qa is not None:
        headline_bits.append(f"QA={qa:.3f}")
    if headline_bits:
        print("  HEADLINE: " + "   ".join(headline_bits))

    def _row(gran: str) -> None:
        g = retrieval.get(gran) or {}
        if not g:
            return
        print(f"  {gran.upper()}-LEVEL METRICS:")
        rg_ = g.get("recall_at_g")
        if rg_ is not None:
            print(f"    R@G={rg_:.3f}")
        for k in KS:
            ra = g.get(f"recall_any@{k}")
            rl = g.get(f"recall_all@{k}")
            nd = g.get(f"ndcg_any@{k}")
            parts = []
            if ra is not None:
                parts.append(f"R_any@{k}={ra:.3f}")
            if rl is not None:
                parts.append(f"R_all@{k}={rl:.3f}")
            if nd is not None:
                parts.append(f"NDCG@{k}={nd:.3f}")
            if parts:
                print("    " + "  ".join(parts))

    _row("session")
    _row("turn")

    # Diagnostics: did advance_time actually fire on the Sonzai runs?
    advance = summary.get("advance_time") or {}
    if advance:
        print(
            f"  advance_time   : calls={advance['total_calls']}"
            f"  consolidations={advance['total_consolidations']}"
            f"  failures={advance['total_failures']}"
            f"  avg_calls/q={advance['avg_calls']:.1f}"
        )

    by_type = summary.get("by_type") or {}
    if by_type:
        print(
            f"  {'type':<30} {'n':>4} {'R@G':>6} {'R@10':>6} {'R@30':>6} {'QA':>6}"
        )
        for t, b in sorted(by_type.items()):
            qa_s = (
                f"{b['qa_accuracy']:.3f}" if b.get("qa_accuracy") is not None else "  -  "
            )
            rg_ = b.get("recall_at_g", 0.0)
            r10_ = b.get("recall_any@10", 0.0)
            r30_ = b.get("recall_any@30", 0.0)
            print(
                f"  {t:<30} {b['n']:>4} {rg_:>6.3f} {r10_:>6.3f} {r30_:>6.3f} {qa_s:>6}"
            )


# ---------------------------------------------------------------------------
# Compare mode
# ---------------------------------------------------------------------------


def _compare(file_a: Path, file_b: Path) -> None:
    rows_a = [json.loads(l) for l in open(file_a)]
    rows_b = [json.loads(l) for l in open(file_b)]
    sum_a, sum_b = _summarize(rows_a), _summarize(rows_b)
    label_a = rows_a[0].get("backend", file_a.stem) if rows_a else file_a.stem
    label_b = rows_b[0].get("backend", file_b.stem) if rows_b else file_b.stem
    _print_summary(sum_a, label=label_a)
    _print_summary(sum_b, label=label_b)

    print("\n### Side-by-side (session-level)\n")
    print(f"| Metric                 | {label_a:>12} | {label_b:>12} |")
    print("|------------------------|-------------:|-------------:|")

    # Headline row order: n, R@G, R@10, R@30, then the rest of the k-grid, then QA.
    headline_keys: list[tuple[str, str]] = [
        ("n", "n"),
        ("recall_at_g", "R@G"),
        ("recall_any@10", "R@10"),
        ("recall_any@30", "R@30"),
    ]
    for k in KS:
        headline_keys.append((f"recall_any@{k}", f"recall_any@{k}"))
        headline_keys.append((f"ndcg_any@{k}", f"ndcg_any@{k}"))
    headline_keys.append(("qa_accuracy", "qa_accuracy"))

    def _lookup(summary: dict, key: str):
        if key == "n":
            return summary.get("n")
        if key == "qa_accuracy":
            return summary.get("qa_accuracy")
        return (summary.get("retrieval") or {}).get("session", {}).get(key)

    seen_labels: set[str] = set()
    for key, label in headline_keys:
        if label in seen_labels:
            continue
        seen_labels.add(label)
        va = _lookup(sum_a, key)
        vb = _lookup(sum_b, key)
        va_s = f"{va:.3f}" if isinstance(va, float) else str(va if va is not None else "-")
        vb_s = f"{vb:.3f}" if isinstance(vb, float) else str(vb if vb is not None else "-")
        print(f"| {label:<22} | {va_s:>12} | {vb_s:>12} |")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def _amain(args: argparse.Namespace) -> int:
    logging.basicConfig(
        level=logging.WARNING - 10 * min(args.verbose, 2),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.compare:
        _compare(Path(args.compare[0]), Path(args.compare[1]))
        return 0

    if not os.environ.get("SONZAI_API_KEY") and args.backend == "sonzai":
        print("error: SONZAI_API_KEY must be set for the sonzai backend", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY") and args.mode in {"qa", "both"}:
        print("error: GEMINI_API_KEY must be set for QA scoring", file=sys.stderr)
        return 2

    dataset_path = resolve_dataset_path(str(args.dataset_path) if args.dataset_path else None)
    questions = load_questions(limit=args.limit, path=str(dataset_path))
    print(
        f"Loaded {len(questions)} questions from LongMemEval "
        f"(cache: {cache_root()}).",
        file=sys.stderr,
    )

    judge: GeminiJudge | None = (
        GeminiJudge(model=args.judge_model) if args.mode in {"qa", "both"} else None
    )

    t0 = time.time()
    if args.backend == "sonzai":
        rows = await _run_sonzai_backend(
            questions,
            concurrency=args.concurrency,
            mode=args.mode,
            judge=judge,
            skip_advance_time=args.skip_advance_time,
            max_sessions=args.max_sessions_per_question,
        )
    else:
        rows = await _run_mempalace_backend(
            questions,
            mempalace_mode=args.mempalace_mode,
            mode=args.mode,
            judge=judge,
            concurrency=args.concurrency,
            dataset_path=dataset_path,
        )
    elapsed = time.time() - t0

    output = args.output or _default_output_path(args.backend)
    _write_jsonl(output, rows)

    summary = _summarize(rows)
    _print_summary(summary, label=args.backend)
    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
