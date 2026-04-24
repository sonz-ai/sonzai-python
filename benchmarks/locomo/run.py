"""LoCoMo benchmark runner: ingest samples, answer QAs, score, write JSONL.

Same layout philosophy as benchmarks/longmemeval/run.py:
- Argparse CLI driving three modes (backend sonzai, backend mem0, compare)
- Asyncio with bounded concurrency — sample-level pool + QA-level pool
- JSONL output one row per (sample, qa) for downstream aggregation

The Sonzai backend uses /process for ingest and Gemini for reader+judge.
The mem0 backend uses their MemoryClient for ingest+search and shares our
reader+judge so the comparison isolates the memory layer.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path

from sonzai import AsyncSonzai
from tqdm.asyncio import tqdm_asyncio

from ..common.gemini_judge import (
    DEFAULT_MODEL as DEFAULT_JUDGE_MODEL,
    GeminiJudge,
    judge_locomo_async,
)
from .backends import LocomoBackendResult, RankedMemoryItem
from .dataset import LocomoQA, LocomoSample, load_samples
from .scoring import (
    aggregate_rows,
    evidence_to_session_ids,
    retrieval_metrics_grid,
    token_f1,
)

logger = logging.getLogger("benchmarks.locomo")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.locomo",
        description="Run the LoCoMo benchmark against Sonzai or mem0.",
    )
    p.add_argument("--backend", choices=["sonzai", "mem0"], default="sonzai")
    p.add_argument("--limit", type=int, default=2)
    p.add_argument("--concurrency", type=int, default=2)
    p.add_argument("--top-k", type=int, default=30)
    p.add_argument("--ingest-batch-size", type=int, default=2,
                   help="Batch size for /process calls (default 2, matches mem0; 0 = whole-session).")
    p.add_argument("--skip-advance-time", action="store_true",
                   help="Sonzai only: skip advance_time between sessions (no-self-learning baseline).")
    p.add_argument("--include-adversarial", action="store_true",
                   help="Include category-5 questions (filtered by default to match mem0).")
    p.add_argument("--reuse-agents", nargs="?",
                   const=str(Path(__file__).parent / "results" / "reuse_agents.json"),
                   default=None, metavar="PATH",
                   help="Sonzai only: persist {sample_id → ingest-state} so subsequent runs skip ingest.")
    p.add_argument("--clear-reused-memory", action="store_true",
                   help="Sonzai only: memory.reset before reuse (rarely needed).")
    p.add_argument("--mode", choices=["retrieval", "qa", "both"], default="both")
    p.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    p.add_argument("--dataset-path", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--compare", nargs="+", metavar="FILE", default=None)
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args(argv)


def _default_output_path(backend: str) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    return Path(__file__).parent / "results" / f"{backend}_{ts}.jsonl"


# ---------------------------------------------------------------------------
# Per-question scoring + serialisation
# ---------------------------------------------------------------------------


def _score_row(
    sample: LocomoSample, qa: LocomoQA, qa_index: int, br: LocomoBackendResult,
    *, backend: str, llm_correct: "bool | None", llm_rationale: str,
) -> dict:
    evidence_sids = evidence_to_session_ids(qa.evidence)
    retrieval = retrieval_metrics_grid(br.retrieved_session_ids, evidence_sids)
    return {
        "sample_id": sample.sample_id,
        "qa_index": qa_index,
        "question": qa.question,
        "gold_answer": qa.answer,
        "category": qa.category,
        "evidence": qa.evidence,
        "generated_answer": br.agent_answer,
        "llm_correct": llm_correct,
        "llm_rationale": llm_rationale,
        "token_f1": token_f1(br.agent_answer, qa.answer),
        "speaker_a_memories": [_item_to_json(m) for m in br.speaker_a_memories],
        "speaker_b_memories": [_item_to_json(m) for m in br.speaker_b_memories],
        "retrieval": retrieval,
        "retrieved_session_ids": br.retrieved_session_ids,
        "backend": backend,
        "extra": br.extra or {},
    }


def _item_to_json(m: RankedMemoryItem) -> dict:
    return {
        "memory_id": m.memory_id,
        "text": m.text,
        "timestamp": m.timestamp,
        "score": m.score,
        "session_id": m.session_id,
    }


# ---------------------------------------------------------------------------
# Sonzai backend orchestration
# ---------------------------------------------------------------------------


async def _run_sonzai(
    samples: list[LocomoSample],
    *,
    concurrency: int, mode: str, judge: "GeminiJudge | None",
    top_k: int, ingest_batch_size: int, skip_advance_time: bool,
    include_adversarial: bool,
    reuse_agents_path: "str | None", clear_reused_memory: bool,
) -> list[dict]:
    from .backends import sonzai as sb
    from ..common.agent_reuse import (
        SliceKey, load_snapshot, new_snapshot, save_snapshot,
        should_reuse, upsert_agent,
    )
    from sonzai.benchmarks import ensure_benchmark_agent_async

    client = AsyncSonzai(timeout=600.0)
    try:
        shared_agent_id, existed = await ensure_benchmark_agent_async(client)
        logger.info("bench agent: %s (existed=%s)", shared_agent_id, existed)

        snapshot = None
        snapshot_lock: "asyncio.Lock | None" = None
        current_slice = None
        if reuse_agents_path:
            current_slice = SliceKey(benchmark="locomo", limit=len(samples))
            loaded = load_snapshot(reuse_agents_path)
            snapshot = loaded if (loaded and loaded.slice.matches(current_slice)) else new_snapshot(current_slice)
            snapshot_lock = asyncio.Lock()

        sem_sample = asyncio.Semaphore(concurrency)

        async def _one_sample(sample: LocomoSample) -> list[dict]:
            async with sem_sample:
                already_ingested = False
                if snapshot is not None and current_slice is not None:
                    entry = should_reuse(snapshot, current_slice, sample.sample_id)
                    already_ingested = entry is not None and entry.agent_id == shared_agent_id

                ingest_diag: dict = {}
                if not already_ingested:
                    ingest_diag = await sb.ingest_sample(
                        client, sample,
                        shared_agent_id=shared_agent_id,
                        ingest_batch_size=ingest_batch_size,
                        skip_advance_time=skip_advance_time,
                        clear_before=True,
                    )
                    if snapshot is not None and snapshot_lock is not None:
                        async with snapshot_lock:
                            upsert_agent(
                                snapshot, key=sample.sample_id,
                                agent_id=shared_agent_id,
                                user_id=f"lc-{sample.sample_id}-a",
                                session_ids=[f"session_{s.index}" for s in sample.sessions],
                            )
                            save_snapshot(reuse_agents_path, snapshot)
                elif clear_reused_memory:
                    ingest_diag = await sb.ingest_sample(
                        client, sample,
                        shared_agent_id=shared_agent_id,
                        ingest_batch_size=ingest_batch_size,
                        skip_advance_time=skip_advance_time,
                        clear_before=True,
                    )

                qa_pairs = [(qi, qa) for qi, qa in enumerate(sample.qa)
                            if include_adversarial or qa.category != 5]

                async def _one_qa(qi: int, qa: LocomoQA) -> dict:
                    br = await sb.answer_one_qa(
                        client, sample, qa.question,
                        shared_agent_id=shared_agent_id, top_k=top_k, reader=judge,
                    )
                    if qa_pairs and qi == qa_pairs[0][0]:
                        br.extra = dict(br.extra or {})
                        br.extra.update(ingest_diag)

                    llm_correct: "bool | None" = None
                    llm_rationale = ""
                    if mode in {"qa", "both"} and judge is not None:
                        try:
                            verdict = await judge_locomo_async(
                                judge, question=qa.question,
                                gold_answer=qa.answer, generated_answer=br.agent_answer,
                            )
                            llm_correct = verdict.label.upper() == "CORRECT"
                        except Exception as e:
                            logger.warning("judge failed: %s", e)

                    return _score_row(
                        sample, qa, qi, br,
                        backend="sonzai", llm_correct=llm_correct, llm_rationale=llm_rationale,
                    )

                rows = await asyncio.gather(*(_one_qa(qi, qa) for qi, qa in qa_pairs))
                return rows

        per_sample = await tqdm_asyncio.gather(*(_one_sample(s) for s in samples), desc="sonzai")
        return [row for batch in per_sample for row in batch]
    finally:
        await client.close()


# ---------------------------------------------------------------------------
# mem0 backend orchestration
# ---------------------------------------------------------------------------


async def _run_mem0(
    samples: list[LocomoSample],
    *,
    concurrency: int, mode: str, judge: "GeminiJudge | None",
    top_k: int, ingest_batch_size: int, include_adversarial: bool,
) -> list[dict]:
    from .backends import mem0 as mb

    mem0_client = mb.build_client()
    sem_sample = asyncio.Semaphore(concurrency)

    async def _one_sample(sample: LocomoSample) -> list[dict]:
        async with sem_sample:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: mb.ingest_sample_sync(
                    mem0_client, sample, ingest_batch_size=ingest_batch_size,
                ),
            )

            qa_pairs = [(qi, qa) for qi, qa in enumerate(sample.qa)
                        if include_adversarial or qa.category != 5]

            async def _one_qa(qi: int, qa: LocomoQA) -> dict:
                br = await mb.answer_one_qa(
                    mem0_client, sample, qa.question, top_k=top_k, reader=judge,
                )
                llm_correct: "bool | None" = None
                llm_rationale = ""
                if mode in {"qa", "both"} and judge is not None:
                    try:
                        verdict = await judge_locomo_async(
                            judge, question=qa.question,
                            gold_answer=qa.answer, generated_answer=br.agent_answer,
                        )
                        llm_correct = verdict.label.upper() == "CORRECT"
                    except Exception as e:
                        logger.warning("judge failed: %s", e)
                return _score_row(
                    sample, qa, qi, br,
                    backend="mem0", llm_correct=llm_correct, llm_rationale=llm_rationale,
                )

            return await asyncio.gather(*(_one_qa(qi, qa) for qi, qa in qa_pairs))

    per_sample = await tqdm_asyncio.gather(*(_one_sample(s) for s in samples), desc="mem0")
    return [row for batch in per_sample for row in batch]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _write_jsonl(rows: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _print_summary(rows: list[dict]) -> None:
    agg = aggregate_rows(rows)
    print("\n=== LoCoMo summary ===")
    for cat in sorted(agg["per_category"].keys()):
        m = agg["per_category"][cat]
        print(f"  category {cat}: n={m['n']} LLM-judge={m['llm_accuracy']:.3f} "
              f"token-F1={m['token_f1']:.3f} "
              f"R@5={m.get('recall_any@5', 0):.3f} R@10={m.get('recall_any@10', 0):.3f}")
    o = agg["overall"]
    print(f"  OVERALL:    n={o['n']} LLM-judge={o['llm_accuracy']:.3f} "
          f"token-F1={o['token_f1']:.3f} R@5={o.get('recall_any@5', 0):.3f}")


def main(argv: "list[str] | None" = None) -> int:
    args = _parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose >= 2 else (logging.INFO if args.verbose else logging.WARNING),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.compare:
        from .compare import main as compare_main
        return compare_main(args.compare)

    samples = load_samples(limit=args.limit, path=args.dataset_path)
    if not samples:
        print("no samples loaded", file=sys.stderr)
        return 1

    judge: "GeminiJudge | None" = None
    if args.mode in {"qa", "both"}:
        judge = GeminiJudge(model=args.judge_model)

    out = args.output or _default_output_path(args.backend)

    if args.backend == "sonzai":
        rows = asyncio.run(_run_sonzai(
            samples,
            concurrency=args.concurrency,
            mode=args.mode,
            judge=judge,
            top_k=args.top_k,
            ingest_batch_size=args.ingest_batch_size,
            skip_advance_time=args.skip_advance_time,
            include_adversarial=args.include_adversarial,
            reuse_agents_path=args.reuse_agents,
            clear_reused_memory=args.clear_reused_memory,
        ))
    elif args.backend == "mem0":
        rows = asyncio.run(_run_mem0(
            samples,
            concurrency=args.concurrency,
            mode=args.mode,
            judge=judge,
            top_k=args.top_k,
            ingest_batch_size=args.ingest_batch_size,
            include_adversarial=args.include_adversarial,
        ))
    else:
        print(f"unknown backend: {args.backend}", file=sys.stderr)
        return 2

    _write_jsonl(rows, out)
    print(f"wrote {len(rows)} rows to {out}")
    _print_summary(rows)
    return 0
