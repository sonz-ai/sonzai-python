"""ConvoMem runner: ingest conversations, judge QA, write JSONL.

Usage::

    # Smoke run — 20 questions (proportionally sliced across all 6 categories)
    python -m benchmarks.convomem --limit 20

    # Full slice
    python -m benchmarks.convomem --limit 0 --concurrency 8

    # No self-learning baseline
    python -m benchmarks.convomem --limit 20 --skip-advance-time

    # Head-to-head compare two JSONLs
    python -m benchmarks.convomem --compare \\
        benchmarks/convomem/results/sonzai_<ts>.jsonl \\
        benchmarks/convomem/results/supermemory_<ts>.jsonl

Concurrency is bounded by ``--concurrency`` over questions. Each question is
fully independent (shared agent, per-question user_id) so parallelism is clean.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path

from sonzai import AsyncSonzai
from sonzai.benchmarks import ensure_convomem_agent_async
from tqdm.asyncio import tqdm_asyncio

from ..common.gemini_judge import (
    DEFAULT_MODEL as DEFAULT_JUDGE_MODEL,
    GeminiJudge,
    judge_abstention_async,
    judge_qa_async,
)
from .backends import BackendResult
from .backends import sonzai as sonzai_backend
from .dataset import CATEGORY_SUBFOLDERS, ConvoMemQuestion, load_questions, resolve_cache_dir
from .scoring import CATEGORY_ORDER, aggregate_summary, format_percent

logger = logging.getLogger("benchmarks.convomem")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.convomem",
        description="Run the Salesforce ConvoMem benchmark against Sonzai.",
    )
    p.add_argument(
        "--backend",
        choices=["sonzai"],
        default="sonzai",
        help="Memory system to evaluate. Only 'sonzai' at launch.",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Questions to evaluate (0 = all). "
             "Sliced proportionally across categories for balanced smoke runs.",
    )
    p.add_argument(
        "--categories",
        default=None,
        help=f"Comma-separated subset of: {','.join(CATEGORY_SUBFOLDERS)}. Default: all six.",
    )
    p.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Max questions in flight concurrently (default 4).",
    )
    p.add_argument(
        "--skip-advance-time",
        action="store_true",
        help="Skip the post-ingest advance_time flush. Produces a baseline "
             "without CE workers — the delta vs normal runs is the measured lift.",
    )
    p.add_argument(
        "--flush-hours",
        type=float,
        default=168.0,
        help="advance_time flush duration after ingest (default 168h = 7d).",
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
        help="Output JSONL path (default: benchmarks/convomem/results/<backend>_<ts>.jsonl).",
    )
    p.add_argument(
        "--compare",
        nargs="+",
        metavar="FILE",
        help="Compare two or more JSONL result files. Prints per-system summary + "
             "per-category QA breakdown. Order of files = column order.",
    )
    p.add_argument(
        "-v", "--verbose", action="count", default=0,
    )
    return p.parse_args(argv)


# ---------------------------------------------------------------------------
# Backend orchestration
# ---------------------------------------------------------------------------


async def _run_sonzai_backend(
    questions: list[ConvoMemQuestion],
    *,
    concurrency: int,
    judge: GeminiJudge,
    skip_advance_time: bool,
    flush_hours: float,
) -> list[dict]:
    # advance_time can take minutes; SDK default 30s is far too short.
    client = AsyncSonzai(timeout=600.0)
    sem = asyncio.Semaphore(concurrency)

    # Shared agent bootstrap — same pattern as longmemeval.
    agent_id, existed = await ensure_convomem_agent_async(client)
    logger.info(
        "convomem: shared agent %s ready (existed=%s)", agent_id, existed,
    )

    async def one(q: ConvoMemQuestion) -> dict:
        async with sem:
            t0 = time.time()
            try:
                br = await asyncio.wait_for(
                    sonzai_backend.run_question(
                        client,
                        q,
                        existing_agent_id=agent_id,
                        skip_advance_time=skip_advance_time,
                        flush_hours=flush_hours,
                    ),
                    timeout=900.0,
                )
            except asyncio.TimeoutError:
                logger.error("sonzai backend TIMEOUT on %s after 900s", q.question_id)
                return _error_row(q, "sonzai", "per-question timeout (900s)", time.time() - t0)
            except Exception as e:
                logger.exception("sonzai backend failed on %s", q.question_id)
                return _error_row(q, "sonzai", str(e), time.time() - t0)

            elapsed_ms = int((time.time() - t0) * 1000)
            return await _score_and_serialize(q, br, backend="sonzai", judge=judge, elapsed_ms=elapsed_ms)

    try:
        rows = await tqdm_asyncio.gather(*(one(q) for q in questions), desc="sonzai")
    finally:
        await client.close()
    return rows


# ---------------------------------------------------------------------------
# Scoring / serialization
# ---------------------------------------------------------------------------


async def _score_and_serialize(
    q: ConvoMemQuestion,
    br: BackendResult,
    *,
    backend: str,
    judge: GeminiJudge,
    elapsed_ms: int,
) -> dict:
    row: dict = {
        "question_id": q.question_id,
        "question_type": q.question_type,
        "backend": backend,
        "question": q.question,
        "answer": q.answer,
        "evidence_messages": [
            {"speaker": m.speaker, "text": m.text} for m in q.evidence_messages
        ],
        "agent_answer": br.agent_answer,
        "elapsed_ms": elapsed_ms,
        "extra": dict(br.extra),
    }

    if br.agent_answer:
        try:
            if q.question_type == "abstention_evidence":
                verdict = await judge_abstention_async(
                    judge,
                    question=q.question,
                    agent_answer=br.agent_answer,
                )
            else:
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


def _error_row(q: ConvoMemQuestion, backend: str, err: str, elapsed_s: float) -> dict:
    return {
        "question_id": q.question_id,
        "question_type": q.question_type,
        "backend": backend,
        "question": q.question,
        "answer": q.answer,
        "evidence_messages": [
            {"speaker": m.speaker, "text": m.text} for m in q.evidence_messages
        ],
        "agent_answer": "",
        "elapsed_ms": int(elapsed_s * 1000),
        "extra": {"error": err},
    }


# ---------------------------------------------------------------------------
# Output + summary
# ---------------------------------------------------------------------------


def _default_output_path(backend: str) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    return results_dir / f"{backend}_{ts}.jsonl"


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def _print_summary(summary: dict, *, label: str) -> None:
    if not summary or summary.get("n") == 0:
        print(f"[{label}] no results")
        return
    print(f"\n=== {label} (n={summary['n']}) ===")
    qa = summary.get("qa_accuracy")
    print(f"  HEADLINE QA: {format_percent(qa)}")

    ms = summary.get("memscore") or {}
    acc = ms.get("accuracy_pct")
    lat = ms.get("avg_latency_ms")
    tok = ms.get("avg_context_tokens")
    mem_parts = []
    if acc is not None: mem_parts.append(f"{acc:.1f}%")
    if lat is not None: mem_parts.append(f"{lat:.0f}ms")
    if tok is not None: mem_parts.append(f"{tok:.0f}tok")
    if mem_parts:
        print(f"  MemScore   : " + " / ".join(mem_parts))

    advance = summary.get("advance_time") or {}
    if advance.get("total_calls"):
        print(
            f"  advance_time : calls={advance['total_calls']}"
            f"  consolidations={advance['total_consolidations']}"
            f"  failures={advance['total_failures']}"
            f"  avg/q={advance['avg_calls']:.1f}"
        )

    by_type = summary.get("by_type") or {}
    if by_type:
        ordered = [t for t in CATEGORY_ORDER if t in by_type]
        ordered += sorted(t for t in by_type if t not in CATEGORY_ORDER)
        print(f"  {'category':<30} {'n':>4} {'scored':>7} {'QA':>8}")
        for t in ordered:
            b = by_type[t]
            qa_s = format_percent(b.get("qa_accuracy"))
            print(f"  {t:<30} {b['n']:>4} {b['qa_scored']:>7} {qa_s:>8}")


def _print_compare_table(summaries: list[dict], labels: list[str]) -> None:
    """Markdown + text per-category breakdown across multiple JSONLs."""
    print("\n### Per-category QA accuracy\n")
    label_w = max(len("Category"), *(len(t) for t in CATEGORY_ORDER + ["Overall"]))
    col_w = max(8, *(len(l) for l in labels))
    head = f"  {'Category':<{label_w}}  " + "  ".join(f"{l:>{col_w}}" for l in labels)
    print(head)
    print("  " + "-" * (len(head) - 2))
    for t in CATEGORY_ORDER:
        cells = []
        for s in summaries:
            v = (s.get("by_type") or {}).get(t, {}).get("qa_accuracy")
            cells.append(f"{format_percent(v):>{col_w}}")
        print(f"  {t:<{label_w}}  " + "  ".join(cells))
    overall = [f"{format_percent(s.get('qa_accuracy')):>{col_w}}" for s in summaries]
    print(f"  {'Overall':<{label_w}}  " + "  ".join(overall))

    # Markdown — paste directly into the README.
    print()
    header = "| Category | " + " | ".join(labels) + " |"
    sep = "|---|" + "|".join(["---:"] * len(labels)) + "|"
    print(header)
    print(sep)
    for t in CATEGORY_ORDER:
        cells = []
        for s in summaries:
            v = (s.get("by_type") or {}).get(t, {}).get("qa_accuracy")
            cells.append(format_percent(v))
        print(f"| {t} | " + " | ".join(cells) + " |")
    overall_md = [f"**{format_percent(s.get('qa_accuracy'))}**" for s in summaries]
    print("| **Overall** | " + " | ".join(overall_md) + " |")


def _compare(files: list[Path]) -> None:
    parsed = []
    for path in files:
        rows = [json.loads(line) for line in open(path)]
        summary = aggregate_summary(rows)
        label = rows[0].get("backend", path.stem) if rows else path.stem
        parsed.append((path, label, rows, summary))

    for _, label, _, summary in parsed:
        _print_summary(summary, label=label)

    summaries = [s for _, _, _, s in parsed]
    labels = [l for _, l, _, _ in parsed]
    _print_compare_table(summaries, labels)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def _amain(args: argparse.Namespace) -> int:
    logging.basicConfig(
        level=logging.WARNING - 10 * min(args.verbose, 2),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.compare:
        if len(args.compare) < 2:
            print("error: --compare requires at least two JSONL files", file=sys.stderr)
            return 2
        _compare([Path(p) for p in args.compare])
        return 0

    if not os.environ.get("SONZAI_API_KEY"):
        print("error: SONZAI_API_KEY must be set", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        print("error: GEMINI_API_KEY must be set for QA judging", file=sys.stderr)
        return 2

    categories = [c.strip() for c in args.categories.split(",")] if args.categories else None
    questions = load_questions(limit=args.limit, categories=categories)
    print(
        f"Loaded {len(questions)} questions from ConvoMem "
        f"(cache: {resolve_cache_dir()}).",
        file=sys.stderr,
    )

    judge = GeminiJudge(model=args.judge_model)

    t0 = time.time()
    rows = await _run_sonzai_backend(
        questions,
        concurrency=args.concurrency,
        judge=judge,
        skip_advance_time=args.skip_advance_time,
        flush_hours=args.flush_hours,
    )
    elapsed = time.time() - t0

    output = args.output or _default_output_path(args.backend)
    _write_jsonl(output, rows)

    summary = aggregate_summary(rows)
    _print_summary(summary, label=args.backend)

    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
