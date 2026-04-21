"""MemPalace backend for head-to-head comparison.

We drive MemPalace's own ``longmemeval_bench.py`` script rather than
re-implementing against their internal API. Using their canonical runner keeps
the comparison as fair as possible — any critique of MemPalace's numbers
applies identically to ours.

The script is invoked once over the whole question set (not per-question —
their runner amortizes ChromaDB index setup). We parse the JSONL it writes and
return ``BackendResult`` per question.

Setup (one-time)::

    git clone https://github.com/MemPalace/mempalace.git \\
        ~/.cache/sonzai-bench/mempalace
    pip install -e ~/.cache/sonzai-bench/mempalace[dev]

The runner will do the clone automatically on first invocation if missing.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
from pathlib import Path

from ..dataset import LongMemEvalQuestion
from . import BackendResult

logger = logging.getLogger(__name__)

MEMPALACE_REPO = "https://github.com/MemPalace/mempalace.git"

BENCHMARK_SCRIPT = "benchmarks/longmemeval_bench.py"


def _cache_dir() -> Path:
    override = os.environ.get("SONZAI_BENCH_CACHE")
    root = Path(override).expanduser() if override else Path.home() / ".cache" / "sonzai-bench"
    return root / "mempalace"


def _ensure_checkout() -> Path:
    target = _cache_dir()
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


def _parse_results(output_path: Path) -> dict[str, tuple[list[str], list[str]]]:
    """Parse MemPalace JSONL into ``{question_id: (session_ids, fact_texts)}``.

    MemPalace's output schema (v3.x): each row has ``retrieval_results`` with
    ``ranked_items[]`` where each item carries ``corpus_id`` (= session id at
    the default session-granularity) and ``text``. We mirror both so the
    downstream scoring can do session-level recall AND fact-level recall
    over the same MemPalace output.
    """
    out: dict[str, tuple[list[str], list[str]]] = {}
    with open(output_path) as f:
        for line in f:
            row = json.loads(line)
            qid = row.get("question_id") or row.get("qid")
            if not qid:
                continue
            retrieval = row.get("retrieval_results") or {}
            ranked_items = retrieval.get("ranked_items") or []
            sids: list[str] = []
            texts: list[str] = []
            seen_sids: set[str] = set()
            for item in ranked_items:
                sid = item.get("corpus_id") or ""
                if sid and sid not in seen_sids:
                    seen_sids.add(sid)
                    sids.append(sid)
                text = item.get("text") or ""
                if text:
                    texts.append(text)
            # Legacy fallbacks for earlier MemPalace output schemas.
            if not sids:
                sids = list(row.get("ranked_session_ids") or row.get("top_sessions") or [])
            out[qid] = (sids, texts)
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
    output_path = _cache_dir() / f"results_{mempalace_mode}.jsonl"
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
        sids, texts = parsed.get(q.question_id, ([], []))
        results[q.question_id] = BackendResult(
            ranked_session_ids=sids,
            ranked_fact_texts=texts,
            agent_answer="",
            extra={"mempalace_mode": mempalace_mode},
        )
    return results
