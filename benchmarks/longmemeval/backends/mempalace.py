"""MemPalace backend for head-to-head comparison.

We drive MemPalace's own ``longmemeval_bench.py`` rather than re-implementing
against their internal API. Using their canonical runner keeps the comparison
as fair as possible — any critique of MemPalace's numbers applies identically
to ours.

Checkout resolution (in order):
  1. ``SONZAI_BENCH_MEMPALACE_DIR`` env var (explicit override).
  2. ``sonzai-sdk/mempalace`` — a sibling clone alongside ``sonzai-python`` at
     the repo root. This is the intended default for local development and
     lets us read the source while running the benchmark against it.
  3. ``$SONZAI_BENCH_CACHE/mempalace`` (or ``~/.cache/sonzai-bench/mempalace``)
     — auto-cloned on first invocation if nothing above exists.

MemPalace's script is invoked once per question set (its ChromaDB index setup
amortizes well). We parse the JSONL it writes and return one ``BackendResult``
per question, carrying:

- ``ranked_items`` (MemPalace's ``retrieval_results.ranked_items``) verbatim,
  so downstream scoring sees identical inputs to MemPalace's internal scorer;
- ``ranked_session_ids`` / ``ranked_fact_texts`` convenience projections;
- ``extra["mempalace_metrics"]`` — MemPalace's own per-question metrics dict,
  reported side-by-side with ours as a parity sanity check.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from pathlib import Path

from ..dataset import LongMemEvalQuestion
from . import BackendResult, RankedItem

logger = logging.getLogger(__name__)

MEMPALACE_REPO = "https://github.com/MemPalace/mempalace.git"

BENCHMARK_SCRIPT = "benchmarks/longmemeval_bench.py"


def _resolve_checkout() -> Path:
    """Pick the MemPalace checkout to run against — prefer the sibling clone."""
    env_override = os.environ.get("SONZAI_BENCH_MEMPALACE_DIR")
    if env_override:
        p = Path(env_override).expanduser()
        if (p / BENCHMARK_SCRIPT).exists():
            return p
        logger.warning("SONZAI_BENCH_MEMPALACE_DIR set but %s missing — falling back", p)

    # sonzai-python/benchmarks/longmemeval/backends/mempalace.py
    #   -> sonzai-python/benchmarks/longmemeval/backends
    #   -> sonzai-python/benchmarks/longmemeval
    #   -> sonzai-python/benchmarks
    #   -> sonzai-python
    #   -> sonzai-sdk  (sibling "mempalace" checkout lives here)
    repo_root = Path(__file__).resolve().parents[4]
    sibling = repo_root / "mempalace"
    if (sibling / BENCHMARK_SCRIPT).exists():
        return sibling

    cache_override = os.environ.get("SONZAI_BENCH_CACHE")
    cache_root = (
        Path(cache_override).expanduser() if cache_override else Path.home() / ".cache" / "sonzai-bench"
    )
    return cache_root / "mempalace"


def _ensure_checkout() -> Path:
    target = _resolve_checkout()
    if (target / BENCHMARK_SCRIPT).exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    if not shutil.which("git"):
        raise RuntimeError(
            "git is required to clone MemPalace for the comparison backend"
        )
    logger.info("Cloning MemPalace into %s", target)
    subprocess.run(
        ["git", "clone", "--depth", "1", MEMPALACE_REPO, str(target)],
        check=True,
    )
    return target


def _run_bench(
    *,
    dataset_path: Path,
    output_path: Path,
    mode: str,
    limit: int,
) -> None:
    checkout = _ensure_checkout()
    script = checkout / BENCHMARK_SCRIPT
    cmd = [
        "python",
        str(script),
        str(dataset_path),
        "--mode",
        mode,
        "--out",
        str(output_path),
    ]
    if limit and limit > 0:
        cmd += ["--limit", str(limit)]
    logger.info("Running MemPalace benchmark: %s", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=checkout)


def _parse_row(
    row: dict,
) -> tuple[list[RankedItem], list[str], list[str], dict]:
    """Extract ranked items, session-id projection, fact-text projection, and metrics."""
    retrieval = row.get("retrieval_results") or {}
    ranked_raw = retrieval.get("ranked_items") or []

    items: list[RankedItem] = []
    sids: list[str] = []
    seen_sids: set[str] = set()
    texts: list[str] = []

    for item in ranked_raw:
        corpus_id = str(item.get("corpus_id") or "")
        text = str(item.get("text") or "")
        timestamp = str(item.get("timestamp") or "")
        items.append(RankedItem(corpus_id=corpus_id, text=text, timestamp=timestamp))
        if corpus_id:
            # Turn ids like "sess_xxx_turn_4" collapse to session ids.
            sid = (
                corpus_id.rsplit("_turn_", 1)[0] if "_turn_" in corpus_id else corpus_id
            )
            if sid not in seen_sids:
                seen_sids.add(sid)
                sids.append(sid)
        if text:
            texts.append(text)

    # Legacy schema fallback (older MemPalace outputs).
    if not sids:
        legacy = list(row.get("ranked_session_ids") or row.get("top_sessions") or [])
        sids = legacy

    return items, sids, texts, (retrieval.get("metrics") or {})


def _parse_results(
    output_path: Path,
) -> dict[str, tuple[list[RankedItem], list[str], list[str], dict]]:
    out: dict[str, tuple[list[RankedItem], list[str], list[str], dict]] = {}
    with open(output_path) as f:
        for line in f:
            row = json.loads(line)
            qid = row.get("question_id") or row.get("qid")
            if not qid:
                continue
            out[qid] = _parse_row(row)
    return out


def run_all(
    questions: list[LongMemEvalQuestion],
    *,
    dataset_path: Path,
    mempalace_mode: str = "raw",
) -> dict[str, BackendResult]:
    """Run MemPalace over the whole question set and return per-question results.

    MemPalace is retrieval-only: ``agent_answer`` is left empty. For QA comparison
    the runner feeds MemPalace's top-k sessions back through a Gemini reader
    (see ``longmemeval/run.py``).
    """
    checkout = _ensure_checkout()
    # Write MemPalace's JSONL alongside the checkout to keep its conventions;
    # the runner only reads the file.
    output_path = checkout / "benchmarks" / f"results_sonzai_parity_{mempalace_mode}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    _run_bench(
        dataset_path=dataset_path,
        output_path=output_path,
        mode=mempalace_mode,
        limit=len(questions) if questions else 0,
    )

    parsed = _parse_results(output_path)
    results: dict[str, BackendResult] = {}
    for q in questions:
        items, sids, texts, mp_metrics = parsed.get(q.question_id, ([], [], [], {}))
        results[q.question_id] = BackendResult(
            ranked_items=items,
            ranked_session_ids=sids,
            ranked_fact_texts=texts,
            agent_answer="",
            extra={
                "mempalace_mode": mempalace_mode,
                "mempalace_checkout": str(checkout),
                "mempalace_metrics": mp_metrics,
            },
        )
    return results
