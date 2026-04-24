"""ConvoMem dataset loader with on-demand HuggingFace download.

Source: https://huggingface.co/datasets/Salesforce/ConvoMem
Slice : core_benchmark/pre_mixed_testcases/<category>/<subfolder>/batched_000.json

The loader pulls one ``batched_000.json`` per (category, subfolder) pair,
matching Supermemory MemoryBench's convomem shape so our numbers are directly
comparable. Each batched file is a JSON list of test cases; each test case
carries an ``evidenceItems`` array; each evidence item becomes one
``ConvoMemQuestion`` with multiple ``Conversation``s (the evidence-bearing
conversation plus filler conversations mixed into the test case).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from ..common.dataset_cache import cache_root, ensure_file

HF_BASE = (
    "https://huggingface.co/datasets/Salesforce/ConvoMem/resolve/main/"
    "core_benchmark/pre_mixed_testcases"
)

# Category → evidence-count subfolder. Matches Supermemory's map exactly so
# the question set is reproducible line-for-line against their published
# numbers.
CATEGORY_SUBFOLDERS: dict[str, str] = {
    "user_evidence":                "1_evidence",
    "assistant_facts_evidence":     "1_evidence",
    "changing_evidence":            "2_evidence",
    "abstention_evidence":          "1_evidence",
    "preference_evidence":          "1_evidence",
    "implicit_connection_evidence": "1_evidence",
}

BATCH_FILENAME = "batched_000.json"


@dataclass
class Message:
    role: str       # "user" | "assistant" — lowercased from dataset's "User"/"Assistant"
    content: str


@dataclass
class Conversation:
    conversation_id: str
    messages: list[Message]


@dataclass
class EvidenceMessage:
    speaker: str    # "User" | "Assistant" — preserved casing (for display)
    text: str


@dataclass
class ConvoMemQuestion:
    question_id: str
    question_type: str
    question: str
    answer: str
    evidence_messages: list[EvidenceMessage]
    conversations: list[Conversation]


def _cache_dir(cache_dir: Path | None) -> Path:
    return Path(cache_dir) if cache_dir else (cache_root() / "convomem")


def _ensure_category_file(
    category: str, subfolder: str, cache_dir: Path, download: bool
) -> Path:
    """Return the path to a category's ``batched_000.json``, downloading if needed."""
    target = cache_dir / category / subfolder / BATCH_FILENAME
    if target.exists() and target.stat().st_size > 0:
        return target
    if not download:
        raise FileNotFoundError(
            f"ConvoMem fixture missing: {target} (download disabled)"
        )
    url = f"{HF_BASE}/{category}/{subfolder}/{BATCH_FILENAME}"
    target.parent.mkdir(parents=True, exist_ok=True)
    # ensure_file caches by filename under cache_root(); for per-category
    # caching we bypass it and fetch directly via urllib here.
    import urllib.request
    import shutil as _shutil

    tmp = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(url) as resp:  # noqa: S310 — trusted HF URL
        with open(tmp, "wb") as f:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
    _shutil.move(str(tmp), str(target))
    return target


def _parse_category_file(path: Path, category: str) -> list[ConvoMemQuestion]:
    """Flatten a batched file into ConvoMemQuestions.

    The batched file is a JSON list; each entry has ``evidenceItems``. We
    concatenate evidence items across entries so the per-category index is
    dense and deterministic.
    """
    with open(path) as f:
        raw = json.load(f)

    questions: list[ConvoMemQuestion] = []
    idx = 0
    for test_case in raw:
        for item in test_case.get("evidenceItems", []) or []:
            qid = f"convomem-{category}-{idx}"
            idx += 1
            conversations = []
            for i, conv in enumerate(item.get("conversations") or []):
                messages = [
                    Message(role=m["speaker"].lower(), content=m["text"])
                    for m in (conv.get("messages") or [])
                ]
                conversations.append(
                    Conversation(
                        conversation_id=f"{qid}-conv-{i}",
                        messages=messages,
                    )
                )
            evidence = [
                EvidenceMessage(speaker=m["speaker"], text=m["text"])
                for m in (item.get("message_evidences") or [])
            ]
            questions.append(
                ConvoMemQuestion(
                    question_id=qid,
                    question_type=category,
                    question=str(item.get("question") or ""),
                    answer=str(item.get("answer") or ""),
                    evidence_messages=evidence,
                    conversations=conversations,
                )
            )
    return questions


def load_questions(
    *,
    limit: int = 0,
    categories: list[str] | None = None,
    cache_dir: Path | None = None,
    download: bool = True,
) -> list[ConvoMemQuestion]:
    """Load ConvoMem questions, downloading category batches as needed.

    ``limit=0`` returns everything. Otherwise the limit is **sliced
    proportionally across the requested categories** so smoke runs hit all
    six evidence types — important because the categories test different
    capabilities and a naive truncation would bias toward whichever
    category sorts first.

    ``categories=None`` loads all six. Explicit list filters; unknown names
    raise ``ValueError``.

    ``cache_dir`` overrides the default ``~/.cache/sonzai-bench/convomem/``
    root. Used by tests to point at a fixture tree.

    ``download=False`` turns off the HuggingFace fetch — useful in tests that
    pre-populate ``cache_dir`` from fixtures.
    """
    cats = list(categories) if categories else list(CATEGORY_SUBFOLDERS)
    unknown = [c for c in cats if c not in CATEGORY_SUBFOLDERS]
    if unknown:
        raise ValueError(f"unknown category: {unknown[0]}")

    root = _cache_dir(cache_dir)
    per_cat: dict[str, list[ConvoMemQuestion]] = {}
    for cat in cats:
        path = _ensure_category_file(
            cat, CATEGORY_SUBFOLDERS[cat], root, download=download
        )
        per_cat[cat] = _parse_category_file(path, cat)

    if limit <= 0:
        # Preserve category order from CATEGORY_SUBFOLDERS for reproducibility.
        return [q for cat in cats for q in per_cat[cat]]

    # Proportional slice: floor(limit/n), distribute remainder to first cats.
    base, extra = divmod(limit, len(cats))
    out: list[ConvoMemQuestion] = []
    for i, cat in enumerate(cats):
        take = base + (1 if i < extra else 0)
        out.extend(per_cat[cat][:take])
    return out


def resolve_cache_dir(cache_dir: str | Path | None = None) -> Path:
    """Return the resolved cache directory — used by `__main__` for logging."""
    return _cache_dir(Path(cache_dir) if cache_dir else None)
