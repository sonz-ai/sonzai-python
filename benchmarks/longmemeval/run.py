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
        choices=["sonzai", "mempalace", "mem0"],
        default="sonzai",
        help="Memory system to evaluate (default: sonzai). 'mem0' uses mem0 "
        "cloud via the mem0ai SDK (requires MEM0_API_KEY).",
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
        "--reuse-agents",
        nargs="?",
        const=str(Path(__file__).parent / "results" / "reuse_agents.json"),
        default=None,
        metavar="PATH",
        help="Sonzai only: persist {question_id → agent_id} after first ingest; "
        "subsequent runs skip ingest + advance_time and reuse the pre-populated "
        "agents. Iteration time drops from ~19 min to ~2 min. Default path: "
        "benchmarks/longmemeval/results/reuse_agents.json. Snapshot slice must "
        "match current --limit / --max-sessions-per-question or it's ignored.",
    )
    p.add_argument(
        "--clear-reused-memory",
        action="store_true",
        help="Sonzai only: when reusing agents, call memory.reset before each "
        "question to wipe stale state. Rarely needed — delete the snapshot "
        "file to force re-ingest instead.",
    )
    p.add_argument(
        "--max-sessions-per-question",
        type=int,
        default=0,
        help="Sonzai only: cap haystack size per question (0 = full). "
        "Answer-bearing sessions are kept preferentially. Use for fast smoke runs.",
    )
    p.add_argument(
        "--question-type",
        default=None,
        help="Filter to a single question_type (e.g. multi-session, "
        "single-session-user, single-session-assistant, single-session-preference, "
        "temporal-reasoning, knowledge-update). Applied AFTER --limit slicing: "
        "if --limit=20 and --question-type=multi-session, you get the first "
        "multi-session questions within the initial 20-row slice. Pass "
        "--limit=0 to search the full 500-row dataset for the subtype.",
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
        nargs="+",
        metavar="FILE",
        help="Compare two or more JSONL result files. Prints per-system headline, "
        "side-by-side R@K (when exactly two files), and the per-question-type QA "
        "breakdown table (text + markdown) so you can paste straight into the README. "
        "Order of files = column order in the table.",
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
    reuse_agents_path: str | None = None,
    clear_reused_memory: bool = False,
    dataset_path_hint: str | None = None,
) -> list[dict]:
    # advance_time runs the full CE worker stack per simulated day and can take
    # minutes per call. sessions/end with wait=true also serializes fact
    # extraction / episode-finalize / dedup through Gemini inside the platform
    # API — observed ~100s tail on prod — so the SDK timeout has to outlast
    # the per-question asyncio ceiling below. 1200s = 20min.
    client = AsyncSonzai(timeout=1200.0)
    sem = asyncio.Semaphore(concurrency)

    # --- Snapshot setup for --reuse-agents ---------------------------------
    # Model: ONE shared agent serves every question (the benchmark's
    # persistent AI persona). Each question gets its own user_id so memory
    # stays isolated per question — matching Sonzai's production (agent_id,
    # user_id) scoping semantics. The snapshot stores the shared agent_id
    # under a reserved ``__shared_agent__`` meta entry plus per-question
    # entries flagged with ``ingested=true`` so we know which users have
    # been populated.
    snapshot = None
    current_slice = None
    snapshot_lock: asyncio.Lock | None = None
    shared_agent_id: str = ""
    SHARED_META_KEY = "__shared_agent__"

    if reuse_agents_path:
        from ..common.agent_reuse import (
            SliceKey,
            dataset_tag,
            load_snapshot,
            new_snapshot,
            save_snapshot,
            should_reuse,
            upsert_agent,
        )

        current_slice = SliceKey(
            benchmark="longmemeval",
            limit=len(questions),
            max_sessions_per_question=max_sessions,
            dataset_tag=dataset_tag(dataset_path_hint),
        )
        loaded = load_snapshot(reuse_agents_path)
        if loaded and loaded.slice.matches(current_slice):
            snapshot = loaded
            meta = loaded.agents.get(SHARED_META_KEY)
            if meta:
                shared_agent_id = meta.agent_id
            logger.info(
                "reuse-agents: loaded snapshot (shared_agent=%s, %d user entries)",
                shared_agent_id or "none", len(loaded.agents) - (1 if meta else 0),
            )
        else:
            if loaded:
                logger.info(
                    "reuse-agents: snapshot slice mismatch — starting fresh. "
                    "expected=%s, found=%s", current_slice, loaded.slice,
                )
            snapshot = new_snapshot(current_slice)
        snapshot_lock = asyncio.Lock()

    # Bootstrap the shared agent. Prefer a pinned agent_id from disk
    # (``shared_agent.json``) — it survives slice changes (different
    # --limit / --max-sessions-per-question) that would invalidate the
    # per-user ingest snapshot. Without this pin, every slice change
    # leaks a fresh agent on the server and leaves orphaned state.
    #
    # Precedence:
    #   1. Snapshot's __shared_agent__ (same slice, already picked one)
    #   2. Pinned agent manifest (cross-slice persistence)
    #   3. Create a new agent with a stable name and pin it
    from ..common.agent_reuse import load_pinned_agent, save_pinned_agent

    bench_results_dir = Path(__file__).parent / "results"

    if not shared_agent_id:
        pinned = load_pinned_agent(bench_results_dir, benchmark="longmemeval")
        if pinned and pinned.agent_id:
            shared_agent_id = pinned.agent_id
            logger.info(
                "reuse-agents: using pinned agent %s (name=%s, created=%s)",
                pinned.agent_id, pinned.name, pinned.created_at,
            )

    # Always call generate-and-create on bootstrap — it's idempotent on the
    # ``name`` key. First invocation expands the description into a full CE
    # profile (Big5, traits, speech, preferences) and returns the new
    # agent_id. Every subsequent call returns the existing agent with no
    # LLM cost. This gives the bench a production-representative agent
    # rather than the thin "create with raw prompt" path we used before.
    #
    # We still write ``shared_agent.json`` after first create so we can
    # surface the pinned ID in reports/logs without a round-trip, but the
    # server is the source of truth.
    # Use the canonical bench agent preset from the SDK. Third-party
    # evaluators can import the same preset
    # (`sonzai.benchmarks.ensure_longmemeval_agent_async`) so their numbers
    # are measured against the same agent configuration as our published
    # ones. Applies a memory-assistant description plus speech_patterns
    # tuned for literal-value recall (normal personality field, available
    # to all users — not a benchmark-only hack).
    from sonzai.benchmarks import (
        BENCHMARK_AGENT_NAME,
        ensure_benchmark_agent_async,
    )

    agent_name = BENCHMARK_AGENT_NAME
    resolved_agent_id, agent_existed = await ensure_benchmark_agent_async(client)
    logger.info(
        "bench: shared agent %s ready (existed=%s, concise-recall speech_patterns applied)",
        resolved_agent_id, agent_existed,
    )
    if shared_agent_id and shared_agent_id != resolved_agent_id:
        logger.info(
            "reuse-agents: pinned agent_id %s differs from server-resolved %s — "
            "updating pin", shared_agent_id, resolved_agent_id,
        )
    shared_agent_id = resolved_agent_id
    logger.info(
        "reuse-agents: shared agent %s (name=%s, existed=%s)",
        shared_agent_id, agent_name, agent_existed,
    )
    save_pinned_agent(
        bench_results_dir,
        benchmark="longmemeval",
        agent_id=shared_agent_id,
        name=agent_name,
    )

    # Also stamp the shared agent into the slice-specific snapshot so
    # reuse-snapshot loads can verify the shared-agent identity matches.
    if snapshot is not None and snapshot_lock is not None and shared_agent_id:
        meta = snapshot.agents.get(SHARED_META_KEY)
        if meta is None or meta.agent_id != shared_agent_id:
            async with snapshot_lock:
                upsert_agent(
                    snapshot,
                    key=SHARED_META_KEY,
                    agent_id=shared_agent_id,
                    user_id="",
                    meta={"role": "shared_agent"},
                )
                save_snapshot(reuse_agents_path, snapshot)

    async def one(q: LongMemEvalQuestion) -> dict:
        async with sem:
            # Under the shared-agent model, the question_id still keys the
            # snapshot — but the entry now only tells us whether THIS user's
            # data is already ingested under the shared agent.
            user_already_ingested = False
            if snapshot is not None and current_slice is not None:
                entry = should_reuse(snapshot, current_slice, q.question_id)
                user_already_ingested = entry is not None and entry.agent_id == shared_agent_id

            try:
                # Per-question hard ceiling. Without it, one stuck chat call
                # (Cloudflare 524 retry storm, server-side stall, judge
                # deadlock on a numeric answer) holds back the asyncio.gather
                # below — we observed runs hung at 99/100 for 12+ minutes
                # waiting on a single task while the other 99 sit idle in
                # memory. 15 minutes is the working ceiling: ingest + N chat
                # turns + session-end (wait=true runs the full CE pipeline
                # synchronously — segmenter + episode-finalize + fact
                # extraction + dedup + side-effect storage, all Gemini-
                # gated) + final QA. Prod tail is ~100s on a bad day so we
                # want headroom without masking truly-hung sessions.
                br = await asyncio.wait_for(
                    sonzai_backend.run_question(
                        client,
                        q,
                        include_qa=(mode in {"qa", "both"}),
                        skip_advance_time=skip_advance_time,
                        max_sessions=max_sessions,
                        existing_agent_id=shared_agent_id,
                        existing_user_id=None,  # backend derives from question_id
                        skip_ingest=user_already_ingested,
                        clear_memory_before_reuse=clear_reused_memory,
                        keep_agent_alive=True,  # never delete the shared agent
                    ),
                    timeout=900.0,
                )
            except asyncio.TimeoutError:
                logger.error("sonzai backend TIMEOUT on %s after 900s", q.question_id)
                return _error_row(q, "sonzai", "per-question timeout (900s)")
            except Exception as e:
                logger.exception("sonzai backend failed on %s", q.question_id)
                return _error_row(q, "sonzai", str(e))

            # After a fresh ingest for this user, persist so future runs
            # with the same slice skip re-ingestion. Writing after every
            # question makes partial progress survivable across crashes.
            if (
                snapshot is not None
                and not user_already_ingested
                and snapshot_lock is not None
            ):
                extra = br.extra or {}
                user_id = str(extra.get("user_id") or "")
                session_ids = list(extra.get("session_ids_ingested") or [])
                if user_id:
                    async with snapshot_lock:
                        upsert_agent(
                            snapshot,
                            key=q.question_id,
                            agent_id=shared_agent_id,
                            user_id=user_id,
                            session_ids=session_ids,
                        )
                        save_snapshot(reuse_agents_path, snapshot)

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
# mem0 backend orchestration (ingest → search via mem0 cloud; QA via Gemini reader)
# ---------------------------------------------------------------------------


async def _run_mem0_backend(
    questions: list[LongMemEvalQuestion],
    *,
    mode: str,
    judge: GeminiJudge | None,
    concurrency: int,
) -> list[dict]:
    from .backends import mem0 as mem0_backend

    results = await mem0_backend.run_all(questions, concurrency=concurrency)

    sem = asyncio.Semaphore(concurrency)

    async def one(q: LongMemEvalQuestion) -> dict:
        br = results.get(q.question_id, BackendResult())
        if mode in {"qa", "both"} and br.ranked_session_ids and judge is not None:
            async with sem:
                br.agent_answer = await _mempalace_read_answer(
                    judge, question=q, ranked_session_ids=br.ranked_session_ids
                )
        return await _score_and_serialize(q, br, backend="mem0", judge=judge, mode=mode)

    return await tqdm_asyncio.gather(*(one(q) for q in questions), desc="mem0-score")


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


def _metrics_from_row(r: dict) -> dict[str, dict[str, float]]:
    """Extract session/turn metric grids for a row, back-filling from the
    legacy flat schema when the new ``retrieval_results.metrics`` block is
    absent.

    Older result files (pre-parity rewrite) stored only flat top-level keys
    like ``session_recall_at_5`` / ``session_ndcg_at_5`` plus
    ``ranked_session_ids``. We reconstruct the full MemPalace k-grid from
    ``ranked_session_ids`` + ``answer_session_ids`` on the fly so a summary /
    ``--compare`` across mixed-schema files stays consistent.
    """
    metrics = (r.get("retrieval_results") or {}).get("metrics") or {}
    session = metrics.get("session") or {}
    turn = metrics.get("turn") or {}

    # Fast path: new schema already has the grid.
    if session:
        return {"session": dict(session), "turn": dict(turn)}

    # Back-fill: compute from ranked_session_ids + answer_session_ids.
    answer_sids = list(r.get("answer_session_ids") or [])
    ranked_sids = list(r.get("ranked_session_ids") or [])
    if not ranked_sids:
        # Last-ditch: try the ranked_items if populated but metrics weren't.
        items = (r.get("retrieval_results") or {}).get("ranked_items") or []
        ranked_sids = [
            session_id_from_corpus_id(str(it.get("corpus_id") or "")) for it in items
        ]
        ranked_sids = [s for s in ranked_sids if s]

    if not ranked_sids:
        # Preserve any legacy flat keys so they still show up somewhere.
        legacy = {}
        for flat, grid_key in [
            ("session_recall_at_5", "recall_any@5"),
            ("session_ndcg_at_5", "ndcg_any@5"),
        ]:
            if flat in r:
                legacy[grid_key] = float(r[flat])
        return {"session": legacy, "turn": dict(turn)}

    backfilled = {}
    for k in KS:
        backfilled[f"recall_any@{k}"] = recall_any_at_k(ranked_sids, answer_sids, k)
        backfilled[f"recall_all@{k}"] = recall_all_at_k(ranked_sids, answer_sids, k)
        backfilled[f"ndcg_any@{k}"] = ndcg_at_k(ranked_sids, answer_sids, k)
    backfilled["recall_at_g"] = recall_at_g(ranked_sids, answer_sids)
    return {"session": backfilled, "turn": dict(turn)}


def _summarize(rows: list[dict]) -> dict:
    if not rows:
        return {}
    n = len(rows)
    qa_rows = [r for r in rows if r.get("qa_correct") is True or r.get("qa_correct") is False]

    summary: dict = {"n": n}

    # Aggregate retrieval metrics across the full k-grid. ``_metrics_from_row``
    # back-fills the legacy flat-key schema so old result files score the
    # same way as new ones — important for side-by-side against MemPalace
    # baselines that predate the rewrite.
    sums: dict[str, dict[str, float]] = {"session": defaultdict(float), "turn": defaultdict(float)}
    counts: dict[str, dict[str, int]] = {"session": defaultdict(int), "turn": defaultdict(int)}
    for r in rows:
        metrics = _metrics_from_row(r)
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

    # Per-type breakdown — R@G, R@10, R@30, QA accuracy, with a separate
    # track for abstention (``_abs`` question_id suffix). An agent that
    # correctly says "I don't know" on unanswerable questions should not
    # have that credit merged into its category's "answerable" score —
    # the published LongMemEval paper reports them as separate metrics.
    by_type: dict[str, dict] = {}
    for r in rows:
        t = r["question_type"]
        qid = r.get("question_id", "")
        is_abs = _is_abstention(qid)
        bucket = by_type.setdefault(
            t,
            {
                "n": 0,
                "qa_scored": 0,         # rows where qa_correct is True/False (i.e., QA actually attempted)
                "qa_correct_sum": 0,
                # Abstention split — tracked separately so the category's
                # main qa_accuracy reflects "answerable" performance only.
                "n_abs": 0,
                "qa_scored_abs": 0,
                "qa_correct_abs": 0,
                "n_ans": 0,
                "qa_scored_ans": 0,
                "qa_correct_ans": 0,
                "rg_sum": 0.0,
                "r10_sum": 0.0,
                "r30_sum": 0.0,
            },
        )
        bucket["n"] += 1
        if is_abs:
            bucket["n_abs"] += 1
        else:
            bucket["n_ans"] += 1
        # Track QA scored separately from totals so retrieval-only runs report
        # qa_accuracy=None per type (rendered as "-") instead of a misleading
        # 0.00% (which falsely implies "tried QA, got everything wrong").
        qc = r.get("qa_correct")
        if qc is True or qc is False:
            bucket["qa_scored"] += 1
            if qc is True:
                bucket["qa_correct_sum"] += 1
            if is_abs:
                bucket["qa_scored_abs"] += 1
                if qc is True:
                    bucket["qa_correct_abs"] += 1
            else:
                bucket["qa_scored_ans"] += 1
                if qc is True:
                    bucket["qa_correct_ans"] += 1
        session_metrics = _metrics_from_row(r).get("session") or {}
        bucket["rg_sum"] += float(session_metrics.get("recall_at_g", 0.0))
        bucket["r10_sum"] += float(session_metrics.get("recall_any@10", 0.0))
        bucket["r30_sum"] += float(session_metrics.get("recall_any@30", 0.0))
    for t, b in by_type.items():
        if b["n"]:
            # qa_accuracy (the display number in the main category table)
            # reflects ANSWERABLE questions only — matches the published
            # LongMemEval headline per category. Abstention is carried
            # alongside as its own field. None signals "no QA scored"
            # (rendered as "-") not "0% correct".
            b["qa_accuracy"] = (
                (b["qa_correct_ans"] / b["qa_scored_ans"]) if b["qa_scored_ans"] else None
            )
            b["qa_accuracy_abs"] = (
                (b["qa_correct_abs"] / b["qa_scored_abs"]) if b["qa_scored_abs"] else None
            )
            # Combined "all questions" view — useful for the single
            # headline QA number that cuts across answerable + abstention.
            b["qa_accuracy_combined"] = (
                (b["qa_correct_sum"] / b["qa_scored"]) if b["qa_scored"] else None
            )
            b["recall_at_g"] = b["rg_sum"] / b["n"]
            b["recall_any@10"] = b["r10_sum"] / b["n"]
            b["recall_any@30"] = b["r30_sum"] / b["n"]
    summary["by_type"] = by_type

    # Capability-level roll-up — the five core memory capabilities defined
    # in the LongMemEval paper. Computed by re-aggregating per-row QA
    # verdicts into capability buckets via _QA_CAPABILITY_MAP, so the
    # numbers are exact (not averages of per-category averages which
    # would weight each category equally regardless of size).
    by_capability: dict[str, dict] = {}
    abs_scored_total = 0
    abs_correct_total = 0
    for r in rows:
        t = r["question_type"]
        capability = _QA_CAPABILITY_MAP.get(t)
        if capability is None:
            continue
        is_abs = _is_abstention(r.get("question_id", ""))
        cap = by_capability.setdefault(
            capability,
            {"n": 0, "qa_scored_ans": 0, "qa_correct_ans": 0, "n_ans": 0, "n_abs": 0},
        )
        cap["n"] += 1
        if is_abs:
            cap["n_abs"] += 1
        else:
            cap["n_ans"] += 1
        qc = r.get("qa_correct")
        if (qc is True or qc is False):
            if is_abs:
                abs_scored_total += 1
                if qc is True:
                    abs_correct_total += 1
            else:
                cap["qa_scored_ans"] += 1
                if qc is True:
                    cap["qa_correct_ans"] += 1
    for capability, c in by_capability.items():
        c["qa_accuracy"] = (
            (c["qa_correct_ans"] / c["qa_scored_ans"]) if c["qa_scored_ans"] else None
        )
    # Abstention is capability #5 — measured across all categories, so
    # it's a single number not a per-category column.
    summary["by_capability"] = by_capability
    summary["abstention_accuracy"] = (
        (abs_correct_total / abs_scored_total) if abs_scored_total else None
    )
    summary["abstention_n"] = abs_scored_total

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
        # Detailed per-type table — retrieval + QA columns side-by-side.
        # Sorted by canonical published order (matches Supermemory/Zep
        # comparison shape) with any unexpected types appended alphabetically.
        ordered = [t for t in _QA_TYPE_ORDER if t in by_type]
        ordered += sorted(t for t in by_type if t not in _QA_TYPE_ORDER)
        print(
            f"  {'type':<30} {'n':>4} {'R@G':>6} {'R@10':>6} {'R@30':>6} {'QA':>6}"
        )
        for t in ordered:
            b = by_type[t]
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


# LongMemEval-S dataset schema (per the paper + the published leaderboards):
#
#   500 questions across 6 categories and 5 core memory capabilities:
#
#   Capability 1 — Information Extraction (accurately extract + store facts)
#     - single-session-user        70 Q   (literal user context, single session)
#     - single-session-assistant   56 Q   (literal assistant context, single session)
#     - single-session-preference  30 Q   (implicit user preferences)
#
#   Capability 2 — Multi-Session Reasoning (synthesise across sessions)
#     - multi-session             133 Q
#
#   Capability 3 — Knowledge Update (newer info supersedes older)
#     - knowledge-update           78 Q
#
#   Capability 4 — Temporal Reasoning (sequence, intervals, relative times)
#     - temporal-reasoning        133 Q
#
#   Capability 5 — Abstaining on Unanswerable Questions (say "I don't know")
#     - Cuts across ALL categories: 30 questions marked with an "_abs"
#       suffix on question_id. These are scored separately as abstention
#       accuracy so the overall category score isn't confounded.
#
# _QA_TYPE_ORDER fixes the display order to match the canonical published
# comparison tables (Supermemory vs Zep vs Full-context etc.). Any future
# dataset additions get appended alphabetically rather than silently dropped.
_QA_TYPE_ORDER = [
    "single-session-user",
    "single-session-assistant",
    "single-session-preference",
    "knowledge-update",
    "temporal-reasoning",
    "multi-session",
]

# Maps each category → human-readable capability. Used for the secondary
# capability-level roll-up table (5 rows instead of 6).
_QA_CAPABILITY_MAP: dict[str, str] = {
    "single-session-user":       "Information Extraction",
    "single-session-assistant":  "Information Extraction",
    "single-session-preference": "Information Extraction",
    "multi-session":             "Multi-Session Reasoning",
    "knowledge-update":          "Knowledge Update",
    "temporal-reasoning":        "Temporal Reasoning",
}

# Display order for the capability-level table. Matches the paper's
# "five core memory capabilities" ordering.
_QA_CAPABILITY_ORDER = [
    "Information Extraction",
    "Multi-Session Reasoning",
    "Knowledge Update",
    "Temporal Reasoning",
]


def _is_abstention(question_id: str) -> bool:
    """LongMemEval marks unanswerable questions with an ``_abs`` suffix on
    ``question_id``. Used to split the per-category accuracy into
    answerable vs abstention so an agent that correctly says 'I don't
    know' on 30/30 unanswerables doesn't inflate the main category score."""
    return question_id.endswith("_abs")


def _format_pct(v: float | None) -> str:
    """Format a 0..1 accuracy as XX.YY%, or '-' for missing/unscored."""
    if v is None:
        return "-"
    return f"{v * 100:.2f}%"


def _qa_breakdown_rows(summary: dict) -> dict[str, tuple[float | None, int]]:
    """Extract {question_type: (qa_accuracy, n)} from a summary, including
    'Abstention' (cross-category, `_abs` questions only) and 'Overall'.

    Per-category qa_accuracy reflects ANSWERABLE questions only — matches
    the published LongMemEval paper. Abstention is reported as its own row
    so agents that say "I don't know" correctly don't inflate category
    scores and failures on unanswerables don't depress them.
    """
    out: dict[str, tuple[float | None, int]] = {}
    for t, b in (summary.get("by_type") or {}).items():
        # Display qa_accuracy (answerable-only); n is answerable count
        # if available, else total.
        n_display = b.get("n_ans", b.get("n", 0))
        out[t] = (b.get("qa_accuracy"), n_display)
    out["Abstention"] = (
        summary.get("abstention_accuracy"),
        summary.get("abstention_n", 0),
    )
    out["Overall"] = (summary.get("qa_accuracy"), summary.get("n", 0))
    return out


def _print_qa_capability_table(
    summaries: list[dict],
    labels: list[str],
    *,
    fmt: str = "text",
) -> None:
    """Render the capability-level roll-up (5 rows: 4 content capabilities
    + Abstention). Complements the 6-category breakdown — same data
    aggregated to the paper's "core memory capabilities" dimension.

    Formats: ``text`` (aligned) or ``markdown`` (pipe-table)."""
    # Rows = 4 content capabilities + Abstention (cuts across categories)
    rows = list(_QA_CAPABILITY_ORDER) + ["Abstention"]

    def cell(s: dict, row: str) -> str:
        if row == "Abstention":
            return _format_pct(s.get("abstention_accuracy"))
        cap = (s.get("by_capability") or {}).get(row, {})
        return _format_pct(cap.get("qa_accuracy"))

    if fmt == "markdown":
        header = "| Capability | " + " | ".join(labels) + " |"
        sep = "|---|" + "|".join(["---:"] * len(labels)) + "|"
        print(header)
        print(sep)
        for row in rows:
            cells = [cell(s, row) for s in summaries]
            print(f"| {row} | " + " | ".join(cells) + " |")
        # Overall last.
        overall_cells = [
            f"**{_format_pct(s.get('qa_accuracy'))}**" for s in summaries
        ]
        print("| **Overall** | " + " | ".join(overall_cells) + " |")
        return

    label_w = max(len("Capability"), *(len(r) for r in rows + ["Overall"]))
    col_w = max(8, *(len(l) for l in labels))
    head = f"  {'Capability':<{label_w}}  " + "  ".join(f"{l:>{col_w}}" for l in labels)
    print(head)
    print("  " + "-" * (len(head) - 2))
    for row in rows:
        cells = [f"{cell(s, row):>{col_w}}" for s in summaries]
        print(f"  {row:<{label_w}}  " + "  ".join(cells))
    overall = [
        f"{_format_pct(s.get('qa_accuracy')):>{col_w}}" for s in summaries
    ]
    print(f"  {'Overall':<{label_w}}  " + "  ".join(overall))


def _print_qa_breakdown_table(
    summaries: list[dict],
    labels: list[str],
    *,
    fmt: str = "text",
) -> None:
    """Render a per-question-type QA accuracy table comparing N backends.

    Matches the standard LongMemEval comparison shape (rows = question
    types, columns = backends + Overall row at bottom). Two formats:

    - ``text``: aligned columns for the terminal.
    - ``markdown``: pipe-table for pasting into the README directly.
    """
    # Union of types across all summaries, ordered canonically.
    seen: set[str] = set()
    rows: list[str] = []
    for t in _QA_TYPE_ORDER:
        for s in summaries:
            if t in (s.get("by_type") or {}):
                if t not in seen:
                    rows.append(t)
                    seen.add(t)
                break
    # Append any unexpected types alphabetically so dataset additions don't
    # silently drop from the table.
    extras: set[str] = set()
    for s in summaries:
        for t in (s.get("by_type") or {}):
            if t not in seen:
                extras.add(t)
    rows.extend(sorted(extras))

    per_summary = [_qa_breakdown_rows(s) for s in summaries]

    # Abstention row sits BETWEEN the last category and Overall: it's its
    # own measurement (cross-category `_abs` questions), not one of the
    # answerable categories, so placing it next to Overall reads naturally
    # as "here's the abstention capability" alongside the grand total.
    has_abstention = any(ps["Abstention"][0] is not None for ps in per_summary)

    if fmt == "markdown":
        header = "| Category | " + " | ".join(labels) + " |"
        sep = "|---|" + "|".join(["---:"] * len(labels)) + "|"
        print(header)
        print(sep)
        for t in rows:
            cells = []
            for ps in per_summary:
                v, _ = ps.get(t, (None, 0))
                cells.append(_format_pct(v))
            print(f"| {t} | " + " | ".join(cells) + " |")
        if has_abstention:
            cells = [_format_pct(ps["Abstention"][0]) for ps in per_summary]
            print("| _Abstention_ | " + " | ".join(cells) + " |")
        # Overall row last.
        cells = []
        for ps in per_summary:
            v, _ = ps["Overall"]
            cells.append(f"**{_format_pct(v)}**")
        print(f"| **Overall** | " + " | ".join(cells) + " |")
        return

    # Text mode — match the screenshot's right-aligned numeric columns.
    label_w = max(
        len("Category"),
        *(len(t) for t in rows + ["Overall", "Abstention"]),
    )
    col_w = max(8, *(len(l) for l in labels))
    head = f"  {'Category':<{label_w}}  " + "  ".join(f"{l:>{col_w}}" for l in labels)
    print(head)
    print("  " + "-" * (len(head) - 2))
    for t in rows:
        cells = []
        for ps in per_summary:
            v, _ = ps.get(t, (None, 0))
            cells.append(f"{_format_pct(v):>{col_w}}")
        print(f"  {t:<{label_w}}  " + "  ".join(cells))
    if has_abstention:
        cells = [f"{_format_pct(ps['Abstention'][0]):>{col_w}}" for ps in per_summary]
        print(f"  {'Abstention':<{label_w}}  " + "  ".join(cells))
    overall_cells = [
        f"{_format_pct(ps['Overall'][0]):>{col_w}}" for ps in per_summary
    ]
    print(f"  {'Overall':<{label_w}}  " + "  ".join(overall_cells))


def _compare(files: list[Path]) -> None:
    """Compare N JSONL result files. Prints:

      1. Per-system summary block (n, R@G/R@10/R@30, QA, advance_time, etc.)
      2. Side-by-side R@K markdown table (when exactly two files)
      3. Per-question-type QA breakdown — text (terminal) + markdown (README)

    Order of files = column order in the breakdown table.
    """
    parsed = []
    for path in files:
        rows = [json.loads(line) for line in open(path)]
        summary = _summarize(rows)
        label = (
            rows[0].get("backend", path.stem) if rows else path.stem
        )
        parsed.append((path, label, rows, summary))

    for _, label, _, summary in parsed:
        _print_summary(summary, label=label)

    # Pairwise R@K side-by-side only meaningful for exactly 2 backends —
    # the original two-file shape. For 3+ backends we skip this and rely
    # on the per-system summaries above + the QA breakdown table below.
    if len(parsed) == 2:
        _, label_a, _, sum_a = parsed[0]
        _, label_b, _, sum_b = parsed[1]
        print("\n### Side-by-side (session-level)\n")
        print(f"| Metric                 | {label_a:>12} | {label_b:>12} |")
        print("|------------------------|-------------:|-------------:|")
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

    # Per-question-type QA breakdown — the load-bearing table for the README.
    # Matches the published Supermemory/Zep/Full-context comparison shape.
    summaries = [s for _, _, _, s in parsed]
    labels = [l for _, l, _, _ in parsed]

    print("\n### Per-question-type QA accuracy\n")
    _print_qa_breakdown_table(summaries, labels, fmt="text")
    print()
    _print_qa_breakdown_table(summaries, labels, fmt="markdown")

    # Secondary roll-up: the five core memory capabilities from the
    # LongMemEval paper. Same data, collapsed from 6 categories to 5
    # capabilities (Information Extraction, Multi-Session Reasoning,
    # Knowledge Update, Temporal Reasoning) + Abstention as the fifth.
    if any((s.get("by_capability") or {}) for s in summaries):
        print("\n### By memory capability (LongMemEval paper grouping)\n")
        _print_qa_capability_table(summaries, labels, fmt="text")
        print()
        _print_qa_capability_table(summaries, labels, fmt="markdown")


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

    if not os.environ.get("SONZAI_API_KEY") and args.backend == "sonzai":
        print("error: SONZAI_API_KEY must be set for the sonzai backend", file=sys.stderr)
        return 2
    if not os.environ.get("MEM0_API_KEY") and args.backend == "mem0":
        print("error: MEM0_API_KEY must be set for --backend mem0", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY") and args.mode in {"qa", "both"}:
        print("error: GEMINI_API_KEY must be set for QA scoring", file=sys.stderr)
        return 2

    dataset_path = resolve_dataset_path(str(args.dataset_path) if args.dataset_path else None)
    # When --question-type is set, load the full dataset first so the subtype
    # filter sees every candidate row; then re-slice to --limit so the filter
    # result respects the requested size. Without this, --limit would cut off
    # subtypes that don't appear in the first N rows of the shuffled file.
    load_limit = 0 if args.question_type else args.limit
    questions = load_questions(limit=load_limit, path=str(dataset_path))
    if args.question_type:
        before = len(questions)
        questions = [q for q in questions if q.question_type == args.question_type]
        print(
            f"Filtered to question_type={args.question_type}: "
            f"{len(questions)} of {before} kept.",
            file=sys.stderr,
        )
        if args.limit and len(questions) > args.limit:
            questions = questions[: args.limit]
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
            reuse_agents_path=args.reuse_agents,
            clear_reused_memory=args.clear_reused_memory,
            dataset_path_hint=str(args.dataset_path) if args.dataset_path else None,
        )
    elif args.backend == "mem0":
        rows = await _run_mem0_backend(
            questions,
            mode=args.mode,
            judge=judge,
            concurrency=min(args.concurrency, 2),
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

    # Per-question-type QA breakdown — always emitted when QA was scored
    # so the numbers are ready to paste into the README without a second
    # tool invocation. Matches the published Supermemory/Zep comparison shape.
    by_type = summary.get("by_type") or {}
    if any(b.get("qa_accuracy") is not None for b in by_type.values()) or summary.get("abstention_accuracy") is not None:
        print("\n### Per-question-type QA accuracy\n")
        _print_qa_breakdown_table([summary], [args.backend], fmt="text")
        print()
        _print_qa_breakdown_table([summary], [args.backend], fmt="markdown")

        # Capability roll-up (5 capabilities from the LongMemEval paper).
        if (summary.get("by_capability") or {}):
            print("\n### By memory capability\n")
            _print_qa_capability_table([summary], [args.backend], fmt="text")
            print()
            _print_qa_capability_table([summary], [args.backend], fmt="markdown")

    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
