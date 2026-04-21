"""LongMemEval runner: ingest haystacks, score retrieval + QA, write JSONL.

Concurrency is bounded by ``--concurrency`` over questions. Each question is
fully independent (fresh agent, fresh user_id), so parallelism is clean.

Output schema (one line per question)::

    {
      "question_id": "...",
      "question_type": "temporal-reasoning",
      "backend": "sonzai",
      "ranked_session_ids": ["s023", "s011", ...],
      "recall_at_5": 1.0, "ndcg_at_5": 0.82,
      "agent_answer": "...",
      "qa_correct": true, "qa_rationale": "...",
      "answer_session_ids": ["s023"],
      "question": "...", "answer": "...",
      "extra": {...}    # backend-specific diagnostics
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
from .backends import BackendResult
from .backends import mempalace as mempalace_backend
from .backends import sonzai as sonzai_backend
from .dataset import LongMemEvalQuestion, load_questions, resolve_dataset_path
from .scoring import fact_ndcg_at_k, fact_recall_at_k, ndcg_at_k, recall_at_k

logger = logging.getLogger("benchmarks.longmemeval")


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


async def _score_and_serialize(
    q: LongMemEvalQuestion,
    br: BackendResult,
    *,
    backend: str,
    judge: GeminiJudge | None,
    mode: str,
) -> dict:
    row: dict = {
        "question_id": q.question_id,
        "question_type": q.question_type,
        "backend": backend,
        "question": q.question,
        "answer": q.answer,
        "answer_session_ids": q.answer_session_ids,
        "ranked_session_ids": br.ranked_session_ids,
        "ranked_fact_texts": br.ranked_fact_texts[:10],  # cap for JSONL size
        "agent_answer": br.agent_answer,
        "extra": br.extra,
    }

    if mode in {"retrieval", "both"}:
        if br.ranked_session_ids:
            row["session_recall_at_5"] = recall_at_k(
                br.ranked_session_ids, q.answer_session_ids, 5
            )
            row["session_ndcg_at_5"] = ndcg_at_k(
                br.ranked_session_ids, q.answer_session_ids, 5
            )
        if br.ranked_fact_texts:
            row["fact_recall_at_5"] = fact_recall_at_k(br.ranked_fact_texts, q.answer, 5)
            row["fact_ndcg_at_5"] = fact_ndcg_at_k(br.ranked_fact_texts, q.answer, 5)

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
        "ranked_session_ids": [],
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

    def _avg(key: str) -> float | None:
        vals = [r[key] for r in rows if key in r]
        return sum(vals) / len(vals) if vals else None

    for key in ("session_recall_at_5", "session_ndcg_at_5", "fact_recall_at_5", "fact_ndcg_at_5"):
        avg = _avg(key)
        if avg is not None:
            summary[key] = avg
    if qa_rows:
        summary["qa_accuracy"] = sum(1 for r in qa_rows if r["qa_correct"]) / len(qa_rows)

    by_type: dict[str, dict[str, float | int]] = {}
    for r in rows:
        t = r["question_type"]
        b = by_type.setdefault(t, {"n": 0, "qa_correct_sum": 0})
        b["n"] += 1
        if r.get("qa_correct") is True:
            b["qa_correct_sum"] += 1
    for t, b in by_type.items():
        if b["n"]:
            b["qa_accuracy"] = b["qa_correct_sum"] / b["n"]
    summary["by_type"] = by_type
    return summary


def _print_summary(summary: dict, *, label: str) -> None:
    if not summary:
        print(f"[{label}] no results")
        return
    print(f"\n=== {label} (n={summary['n']}) ===")
    for key, display in [
        ("session_recall_at_5", "Session R@5"),
        ("session_ndcg_at_5", "Session NDCG@5"),
        ("fact_recall_at_5", "Fact R@5"),
        ("fact_ndcg_at_5", "Fact NDCG@5"),
        ("qa_accuracy", "QA accuracy"),
    ]:
        if key in summary:
            print(f"  {display:<15}: {summary[key]:.3f}")
    print(f"  {'type':<30} {'n':>4} {'QA':>6}")
    for t, b in sorted(summary.get("by_type", {}).items()):
        qa = b.get("qa_accuracy")
        qa_s = f"{qa:.3f}" if qa is not None else "  -  "
        print(f"  {t:<30} {b['n']:>4} {qa_s:>6}")


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

    print("\n### Side-by-side\n")
    print(f"| Metric                 | {label_a:>12} | {label_b:>12} |")
    print("|------------------------|-------------:|-------------:|")
    for k in (
        "n",
        "session_recall_at_5",
        "session_ndcg_at_5",
        "fact_recall_at_5",
        "fact_ndcg_at_5",
        "qa_accuracy",
    ):
        va = sum_a.get(k)
        vb = sum_b.get(k)
        va_s = f"{va:.3f}" if isinstance(va, float) else str(va or "-")
        vb_s = f"{vb:.3f}" if isinstance(vb, float) else str(vb or "-")
        print(f"| {k:<22} | {va_s:>12} | {vb_s:>12} |")


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
