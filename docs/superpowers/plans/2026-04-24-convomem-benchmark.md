# ConvoMem benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `benchmarks/convomem/` — a runner for the Salesforce ConvoMem benchmark that mirrors Supermemory MemoryBench's slice, ingests one `sessions.end` per conversation with a single `advance_time(168h)` flush, and reports QA accuracy per evidence category plus MemScore.

**Architecture:** New package under `benchmarks/convomem/` following the `benchmarks/longmemeval/` layout. Reuses `benchmarks/common/` helpers unchanged. Adds one SDK preset (`ensure_convomem_agent_async`) alongside the existing longmemeval preset.

**Tech Stack:** Python 3.10+, `sonzai` SDK (`AsyncSonzai`), `google-genai` (judge), `tqdm`, `pytest`. Dataset downloads from HuggingFace via `urllib.request`. No new third-party deps.

**Spec:** `docs/superpowers/specs/2026-04-24-convomem-benchmark-design.md`

---

## File Structure

**Create:**
- `benchmarks/convomem/__init__.py`
- `benchmarks/convomem/__main__.py`
- `benchmarks/convomem/dataset.py`
- `benchmarks/convomem/scoring.py`
- `benchmarks/convomem/run.py`
- `benchmarks/convomem/backends/__init__.py`
- `benchmarks/convomem/backends/sonzai.py`
- `benchmarks/convomem/tests/__init__.py`
- `benchmarks/convomem/tests/fixtures/convomem_sample.json`
- `benchmarks/convomem/tests/test_dataset.py`
- `benchmarks/convomem/tests/test_scoring.py`
- `benchmarks/convomem/results/.gitkeep`

**Modify:**
- `src/sonzai/benchmarks.py` — add `CONVOMEM_AGENT_NAME`, `CONVOMEM_AGENT_DESCRIPTION`, `CONVOMEM_SPEECH_PATTERNS`, `ensure_convomem_agent`, `ensure_convomem_agent_async`
- `benchmarks/common/gemini_judge.py` — add `judge_abstention` / `judge_abstention_async` helpers for the abstention category
- `benchmarks/README.md` — add a ConvoMem section mirroring LongMemEval's
- `benchmarks/.gitignore` — add `convomem/results/*.jsonl` with the same allow-list shape as longmemeval

Each task below builds on the previous, in strict TDD order where tests make sense (dataset, scoring, SDK preset) and in plain code-first order where integration is network-gated (backend, CLI).

---

## Task 1: Test fixture for the dataset loader

**Files:**
- Create: `benchmarks/convomem/tests/__init__.py`
- Create: `benchmarks/convomem/tests/fixtures/convomem_sample.json`

- [ ] **Step 1: Create empty `__init__.py`**

Run: `touch benchmarks/convomem/tests/__init__.py`

- [ ] **Step 2: Write the fixture file**

This is a minimal two-item sample that mirrors the HF `batched_000.json` shape —
a JSON list of pre-mixed test cases, each with `evidenceItems` containing one
or more evidence items. The fixture file simulates ONE category; the loader
will read per-category files separately.

Write `benchmarks/convomem/tests/fixtures/convomem_sample.json`:

```json
[
  {
    "evidenceItems": [
      {
        "question": "How many kids do I have?",
        "answer": "3",
        "message_evidences": [
          {"speaker": "User", "text": "I have 3 kids named Emma, Josh, and Lily."}
        ],
        "conversations": [
          {
            "messages": [
              {"speaker": "User", "text": "Morning. Quick thing."},
              {"speaker": "Assistant", "text": "Morning! What's up?"},
              {"speaker": "User", "text": "I have 3 kids named Emma, Josh, and Lily."},
              {"speaker": "Assistant", "text": "Got it — three kids."}
            ]
          },
          {
            "messages": [
              {"speaker": "User", "text": "Unrelated: recipe ideas?"},
              {"speaker": "Assistant", "text": "Sure — what cuisine?"}
            ]
          }
        ]
      },
      {
        "question": "What color do I use for hot leads?",
        "answer": "Green",
        "message_evidences": [
          {"speaker": "User", "text": "I use green for hot leads in my personal spreadsheet."}
        ],
        "conversations": [
          {
            "messages": [
              {"speaker": "User", "text": "I use green for hot leads in my personal spreadsheet."},
              {"speaker": "Assistant", "text": "Nice, clear color coding."}
            ]
          }
        ]
      }
    ]
  }
]
```

- [ ] **Step 3: Commit**

```bash
git add benchmarks/convomem/tests/__init__.py benchmarks/convomem/tests/fixtures/convomem_sample.json
git commit -m "bench(convomem): add dataset fixture for loader tests"
```

---

## Task 2: Dataset loader — failing test first

**Files:**
- Create: `benchmarks/convomem/tests/test_dataset.py`

- [ ] **Step 1: Write the failing test**

Write `benchmarks/convomem/tests/test_dataset.py`:

```python
"""Unit tests for the ConvoMem dataset loader.

No network calls — tests point the loader at a local fixture file via the
``cache_dir`` override.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from benchmarks.convomem.dataset import (
    CATEGORY_SUBFOLDERS,
    ConvoMemQuestion,
    Conversation,
    EvidenceMessage,
    Message,
    load_questions,
)

FIXTURE = Path(__file__).parent / "fixtures" / "convomem_sample.json"


def _populate_cache(cache_dir: Path) -> None:
    """Mirror the cache-dir layout load_questions expects, from a single fixture."""
    for category, subfolder in CATEGORY_SUBFOLDERS.items():
        target_dir = cache_dir / category / subfolder
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIXTURE, target_dir / "batched_000.json")


def test_category_map_has_all_six_categories():
    assert set(CATEGORY_SUBFOLDERS) == {
        "user_evidence",
        "assistant_facts_evidence",
        "changing_evidence",
        "abstention_evidence",
        "preference_evidence",
        "implicit_connection_evidence",
    }
    # Supermemory's map: everything is 1_evidence except changing_evidence.
    assert CATEGORY_SUBFOLDERS["changing_evidence"] == "2_evidence"
    for k, v in CATEGORY_SUBFOLDERS.items():
        if k != "changing_evidence":
            assert v == "1_evidence"


def test_load_all_categories(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path)
    # 6 categories × 2 items per fixture = 12 questions
    assert len(qs) == 12
    cats = {q.question_type for q in qs}
    assert cats == set(CATEGORY_SUBFOLDERS)


def test_question_shape(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, categories=["user_evidence"])
    assert len(qs) == 2
    q = qs[0]
    assert isinstance(q, ConvoMemQuestion)
    assert q.question_type == "user_evidence"
    assert q.question_id == "convomem-user_evidence-0"
    assert q.question == "How many kids do I have?"
    assert q.answer == "3"
    assert q.evidence_messages == [
        EvidenceMessage(speaker="User", text="I have 3 kids named Emma, Josh, and Lily.")
    ]
    assert len(q.conversations) == 2
    assert q.conversations[0].conversation_id == "convomem-user_evidence-0-conv-0"
    first_conv = q.conversations[0]
    assert isinstance(first_conv, Conversation)
    assert first_conv.messages[0] == Message(role="user", content="Morning. Quick thing.")
    # Dataset uses "Assistant"/"User"; loader lowercases to SDK's "assistant"/"user".
    assert first_conv.messages[1].role == "assistant"


def test_question_ids_stable_across_loads(tmp_path: Path):
    _populate_cache(tmp_path)
    a = [q.question_id for q in load_questions(cache_dir=tmp_path)]
    b = [q.question_id for q in load_questions(cache_dir=tmp_path)]
    assert a == b


def test_category_filter(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, categories=["abstention_evidence"])
    assert len(qs) == 2
    assert {q.question_type for q in qs} == {"abstention_evidence"}


def test_limit_slices_across_categories(tmp_path: Path):
    """``limit=6`` must spread across all six categories, one each."""
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, limit=6)
    assert len(qs) == 6
    assert len({q.question_type for q in qs}) == 6


def test_limit_zero_returns_everything(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, limit=0)
    assert len(qs) == 12


def test_unknown_category_raises(tmp_path: Path):
    _populate_cache(tmp_path)
    with pytest.raises(ValueError, match="unknown category"):
        load_questions(cache_dir=tmp_path, categories=["not_a_real_category"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest benchmarks/convomem/tests/test_dataset.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'benchmarks.convomem.dataset'`

- [ ] **Step 3: Commit**

```bash
git add benchmarks/convomem/tests/test_dataset.py
git commit -m "bench(convomem): add failing dataset loader tests"
```

---

## Task 3: Dataset loader — implementation

**Files:**
- Create: `benchmarks/convomem/__init__.py`
- Create: `benchmarks/convomem/dataset.py`

- [ ] **Step 1: Create package `__init__.py`**

Run: `touch benchmarks/convomem/__init__.py`

- [ ] **Step 2: Implement `dataset.py`**

Write `benchmarks/convomem/dataset.py`:

```python
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
```

- [ ] **Step 3: Run test to verify it passes**

Run: `pytest benchmarks/convomem/tests/test_dataset.py -v`
Expected: PASS (8 tests)

- [ ] **Step 4: Commit**

```bash
git add benchmarks/convomem/__init__.py benchmarks/convomem/dataset.py
git commit -m "bench(convomem): implement dataset loader matching Supermemory slice"
```

---

## Task 4: Abstention judge helper — failing test

**Files:**
- Create: `benchmarks/convomem/tests/test_scoring.py`

- [ ] **Step 1: Write the failing test**

Write `benchmarks/convomem/tests/test_scoring.py`:

```python
"""Unit tests for ConvoMem scoring helpers.

The Gemini client is mocked via a dummy judge shim. No network calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from benchmarks.common.gemini_judge import QAVerdict
from benchmarks.convomem.scoring import (
    CATEGORY_ORDER,
    aggregate_summary,
)


@dataclass
class _FakeJudge:
    """Stand-in for GeminiJudge that returns pre-canned verdicts by agent_answer text."""

    canned: dict[str, QAVerdict]

    async def grade_async(self, prompt: str, schema: Any) -> Any:  # noqa: ANN401
        # The abstention prompt embeds the agent_answer; find the matching key.
        for needle, verdict in self.canned.items():
            if needle in prompt:
                return verdict
        return QAVerdict(correct=False, rationale="no canned match")


@pytest.mark.asyncio
async def test_judge_abstention_recognises_decline():
    from benchmarks.common.gemini_judge import judge_abstention_async

    judge = _FakeJudge(canned={
        "I don't have that information": QAVerdict(correct=True, rationale="declined"),
        "His number is 555-1234":          QAVerdict(correct=False, rationale="fabricated"),
    })
    decline = await judge_abstention_async(
        judge,  # type: ignore[arg-type]
        question="What is John's phone number?",
        agent_answer="I don't have that information in our prior conversation.",
    )
    assert decline.correct is True

    fabricated = await judge_abstention_async(
        judge,  # type: ignore[arg-type]
        question="What is John's phone number?",
        agent_answer="His number is 555-1234.",
    )
    assert fabricated.correct is False


def test_category_order_matches_spec():
    assert CATEGORY_ORDER == [
        "user_evidence",
        "assistant_facts_evidence",
        "preference_evidence",
        "changing_evidence",
        "implicit_connection_evidence",
        "abstention_evidence",
    ]


def _row(qid: str, qtype: str, correct: bool, elapsed_ms: int, tokens: int) -> dict:
    return {
        "question_id": qid,
        "question_type": qtype,
        "qa_correct": correct,
        "elapsed_ms": elapsed_ms,
        "extra": {
            "chat_loaded_facts_count": tokens,  # proxy for MemScore context tokens
            "advance_time_calls": 1,
            "consolidation_events": 0,
            "advance_time_failures": 0,
        },
    }


def test_aggregate_summary_basic():
    rows = [
        _row("q1", "user_evidence",              True,  1000, 10),
        _row("q2", "user_evidence",              False, 2000, 12),
        _row("q3", "abstention_evidence",        True,  1500,  8),
    ]
    s = aggregate_summary(rows)
    assert s["n"] == 3
    assert s["qa_accuracy"] == pytest.approx(2 / 3)
    by_type = s["by_type"]
    assert by_type["user_evidence"]["n"] == 2
    assert by_type["user_evidence"]["qa_accuracy"] == pytest.approx(0.5)
    assert by_type["abstention_evidence"]["qa_accuracy"] == pytest.approx(1.0)
    ms = s["memscore"]
    assert ms["accuracy_pct"] == pytest.approx(200 / 3)          # ~66.67
    assert ms["avg_latency_ms"] == pytest.approx(1500)           # mean of 1000,2000,1500
    assert ms["avg_context_tokens"] == pytest.approx(10)         # mean of 10,12,8


def test_aggregate_handles_missing_qa_correct():
    rows = [
        _row("q1", "user_evidence", True, 1000, 10),
        {"question_id": "q2", "question_type": "user_evidence", "elapsed_ms": 500, "extra": {}},
    ]
    s = aggregate_summary(rows)
    # q2 is unscored — counted in n but excluded from qa_accuracy.
    assert s["n"] == 2
    assert s["qa_accuracy"] == pytest.approx(1.0)  # 1 scored, 1 correct
    assert s["by_type"]["user_evidence"]["qa_scored"] == 1
```

- [ ] **Step 2: Install `pytest-asyncio` gate note**

Check whether `pytest-asyncio` is already a dev dep:

Run: `grep -r "pytest-asyncio" pyproject.toml benchmarks/requirements.txt 2>&1 | head -5`

Expected: already present (longmemeval's tests use `async def`). If missing, add it before running the test.

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest benchmarks/convomem/tests/test_scoring.py -v`
Expected: FAIL with `ImportError: cannot import name 'CATEGORY_ORDER' from 'benchmarks.convomem.scoring'` (or similar — module doesn't exist yet)

- [ ] **Step 4: Commit**

```bash
git add benchmarks/convomem/tests/test_scoring.py
git commit -m "bench(convomem): add failing tests for abstention judge + aggregation"
```

---

## Task 5: Abstention judge helper — implementation

**Files:**
- Modify: `benchmarks/common/gemini_judge.py` (append new helpers at the end, do not touch existing functions)

- [ ] **Step 1: Append abstention helpers to `gemini_judge.py`**

Open `benchmarks/common/gemini_judge.py` and append at the end of the file
(after the existing SOTOPIA helpers — do not modify anything above):

```python


# ---------------------------------------------------------------------------
# ConvoMem abstention rubric — "correct iff the agent declines to answer"
# ---------------------------------------------------------------------------

_ABSTENTION_PROMPT = """You are grading whether an AI assistant CORRECTLY ABSTAINED
from answering a question. The question is designed to be UNANSWERABLE from the
conversation history — no evidence has been provided.

Question:
{question}

Assistant's answer:
{agent_answer}

The assistant's answer is CORRECT if it clearly declines to answer, says it
doesn't have the information, says the topic was not mentioned, or otherwise
acknowledges the absence of relevant context. Examples of correct abstention:

- "I don't have that information."
- "You didn't mention that in our conversation."
- "I'm not sure — I don't recall a prior discussion of this."
- "I can't answer that without more context."

The answer is INCORRECT if it fabricates details, guesses, or invents a
specific answer as though it were known.

Respond with JSON matching this schema:
{{"correct": <bool>, "rationale": "<one short sentence>"}}
"""


def judge_abstention(
    judge: GeminiJudge, *, question: str, agent_answer: str
) -> QAVerdict:
    return judge.grade(
        _ABSTENTION_PROMPT.format(
            question=question.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )


async def judge_abstention_async(
    judge: GeminiJudge, *, question: str, agent_answer: str
) -> QAVerdict:
    return await judge.grade_async(
        _ABSTENTION_PROMPT.format(
            question=question.strip(),
            agent_answer=agent_answer.strip() or "[no answer]",
        ),
        QAVerdict,
    )
```

- [ ] **Step 2: Verify no pre-existing tests broke**

Run: `pytest benchmarks/longmemeval/tests/ -v`
Expected: all existing longmemeval tests still pass (we only appended new
functions; existing behavior is untouched).

- [ ] **Step 3: Commit**

```bash
git add benchmarks/common/gemini_judge.py
git commit -m "bench(common): add judge_abstention helper for ConvoMem"
```

---

## Task 6: Scoring module — implementation

**Files:**
- Create: `benchmarks/convomem/scoring.py`

- [ ] **Step 1: Implement `scoring.py`**

Write `benchmarks/convomem/scoring.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it passes**

Run: `pytest benchmarks/convomem/tests/test_scoring.py -v`
Expected: PASS (4 tests)

- [ ] **Step 3: Commit**

```bash
git add benchmarks/convomem/scoring.py
git commit -m "bench(convomem): implement per-category QA + MemScore aggregation"
```

---

## Task 7: SDK preset — `ensure_convomem_agent_async`

**Files:**
- Modify: `src/sonzai/benchmarks.py`

- [ ] **Step 1: Add preset constants and helpers**

Open `src/sonzai/benchmarks.py`. Locate the `__all__` list near the top and
extend it to expose the new symbols (keep existing entries; add four new):

```python
__all__ = [
    "LONGMEMEVAL_AGENT_NAME",
    "LONGMEMEVAL_AGENT_DESCRIPTION",
    "LONGMEMEVAL_SPEECH_PATTERNS",
    "ensure_longmemeval_agent",
    "ensure_longmemeval_agent_async",
    "CONVOMEM_AGENT_NAME",
    "CONVOMEM_AGENT_DESCRIPTION",
    "CONVOMEM_SPEECH_PATTERNS",
    "ensure_convomem_agent",
    "ensure_convomem_agent_async",
]
```

Then, at the end of the file (after the existing `_unpack_generate_create_response`
helper), append:

```python


# ---------------------------------------------------------------------------
# ConvoMem preset
# ---------------------------------------------------------------------------
#
# Same idea as the LongMemEval preset: one canonical agent so third-party
# evaluators measure against the same configuration we publish against.
# ConvoMem's six evidence categories mostly want literal-value recall (user
# facts, assistant facts, changing facts) with correct abstention behavior
# on the unanswerable category. The longmemeval speech pattern — "answer
# with the literal value first" — also serves ConvoMem well; abstention is
# a capability of the underlying model, nudged (not forced) by the voice.

CONVOMEM_AGENT_NAME = "sonzai-bench-convomem"

CONVOMEM_AGENT_DESCRIPTION = (
    "A helpful AI assistant that maintains a rich long-term memory of the "
    "user across many conversations. Remembers user-stated facts, its own "
    "prior statements, evolving preferences, and multi-hop connections. "
    "Answers factual recall questions with the specific value first, and "
    "declines clearly when the topic was never discussed."
)

CONVOMEM_SPEECH_PATTERNS: list[str] = [
    "Answers recall questions with the literal value first — a number, "
    "name, date, or short phrase — before any optional context.",
]


def ensure_convomem_agent(
    client: "Sonzai",
    *,
    name: str = CONVOMEM_AGENT_NAME,
    description: str = CONVOMEM_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Create or return the canonical ConvoMem benchmark agent (sync).

    Behavior mirrors :func:`ensure_longmemeval_agent` exactly — idempotent,
    keyed by ``name`` server-side, speech_patterns re-applied on every call.
    """
    sp = speech_patterns if speech_patterns is not None else CONVOMEM_SPEECH_PATTERNS
    agent_id, existed = _generate_and_create_sync(client, name=name, description=description)
    try:
        client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed


async def ensure_convomem_agent_async(
    client: "AsyncSonzai",
    *,
    name: str = CONVOMEM_AGENT_NAME,
    description: str = CONVOMEM_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Async variant of :func:`ensure_convomem_agent`."""
    sp = speech_patterns if speech_patterns is not None else CONVOMEM_SPEECH_PATTERNS
    agent_id, existed = await _generate_and_create_async(
        client, name=name, description=description
    )
    try:
        await client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed
```

- [ ] **Step 2: Verify imports still work and no existing tests broke**

Run: `python -c "from sonzai.benchmarks import ensure_convomem_agent_async, CONVOMEM_AGENT_NAME; print(CONVOMEM_AGENT_NAME)"`
Expected output: `sonzai-bench-convomem`

Run: `pytest tests/ -k "benchmarks" -v 2>&1 | head -30`
Expected: existing SDK tests still pass (no regressions).

- [ ] **Step 3: Commit**

```bash
git add src/sonzai/benchmarks.py
git commit -m "sdk: add ensure_convomem_agent preset for ConvoMem benchmark"
```

---

## Task 8: Backend result dataclass

**Files:**
- Create: `benchmarks/convomem/backends/__init__.py`

- [ ] **Step 1: Implement the minimal backend interface**

Write `benchmarks/convomem/backends/__init__.py`:

```python
"""Memory-system backends for ConvoMem.

Each backend exposes one async function::

    async def run_question(
        client, question, *, include_qa: bool = True, ...
    ) -> BackendResult

ConvoMem doesn't grade retrieval — ground truth is message-level, not
session-level. So the BackendResult is deliberately thinner than
longmemeval's: an ``agent_answer`` for QA judging, plus diagnostic fields
for stored-fact counts and CE-worker activity.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BackendResult:
    # The agent's free-text answer to the question (for QA scoring).
    # Empty string means the backend doesn't support end-to-end QA.
    agent_answer: str = ""

    # Ranked memory.search hits — diagnostic only. Useful for debugging
    # "retrieval found it, chat didn't surface it" vs "retrieval missed it"
    # without being a scored metric.
    ranked_fact_texts: list[str] = field(default_factory=list)

    # Per-backend diagnostics — serialized into the JSONL output unchanged.
    extra: dict[str, object] = field(default_factory=dict)
```

- [ ] **Step 2: Commit**

```bash
git add benchmarks/convomem/backends/__init__.py
git commit -m "bench(convomem): add BackendResult dataclass"
```

---

## Task 9: Sonzai backend — `run_question`

**Files:**
- Create: `benchmarks/convomem/backends/sonzai.py`

- [ ] **Step 1: Implement the backend**

Write `benchmarks/convomem/backends/sonzai.py`:

```python
"""Sonzai backend for ConvoMem.

Flow per question:

1. Reuse the shared ConvoMem agent (pinned via ``ensure_convomem_agent_async``).
2. Derive ``user_id`` from ``question_id`` so memory stays isolated per-question
   under the shared agent — same model longmemeval uses.
3. For each conversation in ``question.conversations``:
   - ``sessions.start`` with a deterministic session_id.
   - ``sessions.end(messages=..., wait=True)`` — feed the canned transcript
     into the CE pipeline for fact extraction, synchronously. No per-message
     generation; we're testing memory, not chat.
   - **No** ``advance_time`` between conversations. ConvoMem has no dates;
     forcing gaps would be synthetic overhead.
4. **Single flush:** one ``advance_time(168h)`` after all conversations
   are ingested. That catches daily consolidation plus the ``sessionCount
   % 7 == 0`` weekly gate without paying the per-conversation advance-time
   cost (each call takes 1-5 minutes).
5. ``memory.search`` — diagnostic, not scored.
6. ``agents.chat`` — the headline QA path. SSE-stream consumed directly so
   we capture ``context_ready.loaded_facts`` for the MemScore context-token
   proxy.
"""

from __future__ import annotations

import logging
from sonzai import AsyncSonzai

from ...common.sdk_extras import async_memory, async_sessions, clear_agent_memory_async
from ...common.workbench_compat import advance_time_chunked_async
from ..dataset import ConvoMemQuestion, Conversation
from . import BackendResult

logger = logging.getLogger(__name__)

# Single post-ingest flush. 168h = 7 simulated days — catches daily
# consolidation + the sessionCount % 7 weekly gate.
DEFAULT_FLUSH_HOURS = 168.0

# Agent-metadata fact IDs follow a deterministic suffix pattern. We filter
# them from ranked_fact_texts for diagnostic clarity — same filter
# longmemeval applies. Not scored, but keeps the diagnostic clean.
_META_MARKERS = (":comm_style", ":side_effect:", ":interest:")


def _is_metadata_fact(fact_id: str) -> bool:
    return any(m in fact_id for m in _META_MARKERS)


async def _replay_conversation(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    conv: Conversation,
) -> None:
    """Feed one ConvoMem conversation into Sonzai via sessions.end(wait=True)."""
    sessions = async_sessions(client)
    await sessions.start(
        agent_id=agent_id, user_id=user_id, session_id=conv.conversation_id,
    )
    await sessions.end(
        agent_id=agent_id,
        user_id=user_id,
        session_id=conv.conversation_id,
        total_messages=len(conv.messages),
        messages=[{"role": m.role, "content": m.content} for m in conv.messages],
        wait=True,
    )


async def _retrieve(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    question: str,
    limit: int,
) -> list[str]:
    """Run memory.search — diagnostic only, not scored against ground truth."""
    memory = async_memory(client)
    results = await memory.search(
        agent_id=agent_id, user_id=user_id, query=question, limit=limit,
    )
    return [
        r.content
        for r in results.results
        if r.content and not _is_metadata_fact(r.fact_id)
    ]


async def _ask_question(
    client: AsyncSonzai, *, agent_id: str, user_id: str, question: str,
) -> tuple[str, dict]:
    """Consume the /chat SSE stream directly so we can capture context_ready.

    Diagnostics captured::

        {
          "loaded_facts_count": int,
          "loaded_facts_preview": [first 5 fact texts, 200 chars each],
          "loaded_facts_texts":   [all loaded fact texts, 300 chars each],
          "build_duration_ms":    int,
        }
    """
    from sonzai.types import ChatStreamEvent

    content_parts: list[str] = []
    diag: dict = {}
    try:
        async for event in client._http.stream_sse(  # type: ignore[attr-defined]
            "POST",
            f"/api/v1/agents/{agent_id}/chat",
            json_data={
                "messages": [{"role": "user", "content": question}],
                "user_id": user_id,
            },
        ):
            etype = str(event.get("type") or "")
            if etype == "context_ready":
                enriched = event.get("enriched_context") or {}
                loaded = list(enriched.get("loaded_facts") or enriched.get("LoadedFacts") or [])
                texts = [
                    str(f.get("atomic_text") or f.get("AtomicText") or "")
                    for f in loaded
                    if isinstance(f, dict)
                ]
                diag["loaded_facts_count"] = len(loaded)
                diag["loaded_facts_preview"] = [t[:200] for t in texts[:5]]
                diag["loaded_facts_texts"] = [t[:300] for t in texts]
                if "build_duration_ms" in event:
                    diag["build_duration_ms"] = int(event["build_duration_ms"])
            else:
                try:
                    parsed = ChatStreamEvent.model_validate(event)
                except Exception:
                    parsed = None
                if parsed and parsed.content:
                    content_parts.append(str(parsed.content))
    except Exception as e:
        logger.debug("_ask_question stream failed, falling back to non-stream: %s", e)
        resp = await client.agents.chat(
            agent_id=agent_id,
            user_id=user_id,
            messages=[{"role": "user", "content": question}],
        )
        return getattr(resp, "content", "") or "", diag

    return "".join(content_parts), diag


async def run_question(
    client: AsyncSonzai,
    question: ConvoMemQuestion,
    *,
    existing_agent_id: str,
    existing_user_id: str | None = None,
    include_qa: bool = True,
    skip_advance_time: bool = False,
    skip_ingest: bool = False,
    clear_memory_before_reuse: bool = False,
    flush_hours: float = DEFAULT_FLUSH_HOURS,
    retrieval_limit: int = 50,
) -> BackendResult:
    """Run one ConvoMem question end-to-end against Sonzai.

    ``existing_agent_id`` is the shared ConvoMem agent (see
    :func:`sonzai.benchmarks.ensure_convomem_agent_async`). Each question
    scopes its memory under a deterministic per-question ``user_id``.

    ``skip_advance_time=True`` → pure session-end path (no CE worker sim).
    Produces a baseline; the delta vs a normal run is the measured lift.

    ``skip_ingest=True`` (reuse mode) → retrieval + QA only, assumes the
    agent/user pair was populated in a prior run. Controlled by the
    orchestrator via ``--reuse-agents``.
    """
    user_id = existing_user_id or f"convomem-user-{question.question_id[:16]}"
    agent_id = str(existing_agent_id)

    advance_calls = 0
    consolidation_events = 0
    advance_failures = 0

    # Idempotency: wipe prior-run memory for this (agent, user) before
    # re-ingesting, so rerunning the bench with the same question_id lands
    # on a clean state. Skipped in reuse mode unless explicitly asked for.
    if not skip_ingest:
        await clear_agent_memory_async(client, agent_id=agent_id, user_id=user_id)
    elif clear_memory_before_reuse:
        await clear_agent_memory_async(client, agent_id=agent_id, user_id=user_id)

    # ── Ingest ───────────────────────────────────────────────────────────
    if not skip_ingest:
        for conv in question.conversations:
            await _replay_conversation(
                client, agent_id=agent_id, user_id=user_id, conv=conv,
            )

    # ── Single flush ────────────────────────────────────────────────────
    if not skip_ingest and not skip_advance_time and flush_hours > 0:
        try:
            results = await advance_time_chunked_async(
                client, agent_id=agent_id, user_id=user_id, total_hours=flush_hours,
            )
            advance_calls = len(results)
            consolidation_events = sum(1 for r in results if r.consolidation_ran)
        except Exception as e:
            advance_failures += 1
            logger.warning(
                "advance_time(%s, %.1fh) failed (non-fatal): %s",
                agent_id, flush_hours, e,
            )

    # ── Retrieval (diagnostic) ──────────────────────────────────────────
    ranked_facts: list[str] = []
    try:
        ranked_facts = await _retrieve(
            client,
            agent_id=agent_id,
            user_id=user_id,
            question=question.question,
            limit=retrieval_limit,
        )
    except Exception as e:
        logger.debug("memory.search failed (diagnostic only): %s", e)

    # ── QA (headline) ───────────────────────────────────────────────────
    agent_answer = ""
    chat_diag: dict = {}
    if include_qa:
        agent_answer, chat_diag = await _ask_question(
            client, agent_id=agent_id, user_id=user_id, question=question.question,
        )

    # Stored-fact count diagnostic.
    facts_stored = 0
    facts_sample: list[str] = []
    try:
        memory = async_memory(client)
        fact_list = await memory.list_facts(
            agent_id=agent_id, user_id=user_id, limit=500
        )
        facts_stored = len(fact_list.facts)
        facts_sample = [f.content for f in fact_list.facts[:5]]
    except Exception as e:
        logger.debug("memory.list_facts diagnostic failed: %s", e)

    return BackendResult(
        agent_answer=agent_answer,
        ranked_fact_texts=ranked_facts,
        extra={
            "agent_id": agent_id,
            "user_id": user_id,
            "reused_agent": skip_ingest,
            "conversations_ingested": 0 if skip_ingest else len(question.conversations),
            "advance_time_calls": advance_calls,
            "advance_time_failures": advance_failures,
            "consolidation_events": consolidation_events,
            "skip_advance_time": skip_advance_time,
            "facts_retrieved": len(ranked_facts),
            "facts_stored": facts_stored,
            "facts_sample": facts_sample,
            **({f"chat_{k}": v for k, v in chat_diag.items()} if chat_diag else {}),
        },
    )
```

- [ ] **Step 2: Import smoke check**

Run: `python -c "from benchmarks.convomem.backends.sonzai import run_question; print('ok')"`
Expected output: `ok`

- [ ] **Step 3: Commit**

```bash
git add benchmarks/convomem/backends/sonzai.py
git commit -m "bench(convomem): Sonzai backend — per-conv ingest + single flush"
```

---

## Task 10: CLI orchestrator `run.py`

**Files:**
- Create: `benchmarks/convomem/run.py`

- [ ] **Step 1: Implement the orchestrator**

Write `benchmarks/convomem/run.py`:

```python
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
```

- [ ] **Step 2: Import smoke check**

Run: `python -c "from benchmarks.convomem.run import main; print('ok')"`
Expected output: `ok`

- [ ] **Step 3: Help-text smoke check**

Run: `python -m benchmarks.convomem --help 2>&1 | head -30`
Expected: argparse help with `--backend`, `--limit`, `--categories`, `--skip-advance-time`, `--compare`.

- [ ] **Step 4: Commit**

```bash
git add benchmarks/convomem/run.py
git commit -m "bench(convomem): CLI orchestrator with --compare and MemScore output"
```

---

## Task 11: `__main__.py` entry shim

**Files:**
- Create: `benchmarks/convomem/__main__.py`
- Create: `benchmarks/convomem/results/.gitkeep`

- [ ] **Step 1: Write `__main__.py`**

Write `benchmarks/convomem/__main__.py`:

```python
"""``python -m benchmarks.convomem`` entry point."""
from .run import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Create results directory placeholder**

Run: `touch benchmarks/convomem/results/.gitkeep`

- [ ] **Step 3: End-to-end help smoke check**

Run: `python -m benchmarks.convomem --help`
Expected: argparse help prints successfully.

- [ ] **Step 4: Commit**

```bash
git add benchmarks/convomem/__main__.py benchmarks/convomem/results/.gitkeep
git commit -m "bench(convomem): wire python -m entry point"
```

---

## Task 12: gitignore — iteration runs vs published receipts

**Files:**
- Modify: `benchmarks/.gitignore`

- [ ] **Step 1: Inspect existing ignore shape**

Run: `cat benchmarks/.gitignore`
Expected: shows per-benchmark rules for longmemeval and sotopia — iteration
runs gitignored, published receipts allow-listed.

- [ ] **Step 2: Append ConvoMem rules matching the existing shape**

Open `benchmarks/.gitignore` and append (adapt the exact phrasing to match
whatever shape the existing rules use — the point is to gitignore
`benchmarks/convomem/results/*.jsonl` by default and let headline receipts
be explicitly re-added via `!`):

```
# ConvoMem — iteration runs gitignored; published receipts allow-listed below
benchmarks/convomem/results/*.jsonl
benchmarks/convomem/results/*.png
# (add `!benchmarks/convomem/results/<headline>.jsonl` lines as receipts ship)
```

- [ ] **Step 3: Verify nothing accidentally got untracked**

Run: `git status --short benchmarks/convomem/ 2>&1 | head`
Expected: only intentionally-tracked files (source + `.gitkeep`) shown; no
JSONL iteration outputs.

- [ ] **Step 4: Commit**

```bash
git add benchmarks/.gitignore
git commit -m "bench(convomem): gitignore iteration runs under results/"
```

---

## Task 13: README — ConvoMem section

**Files:**
- Modify: `benchmarks/README.md`

- [ ] **Step 1: Append a ConvoMem section to the README**

Open `benchmarks/README.md`, locate the SOTOPIA section, and add a new
section after it (before "Cost and time"):

````markdown
## ConvoMem

[ConvoMem](https://github.com/SalesforceAIResearch/ConvoMem) (Salesforce,
2025) tests conversational memory across **six evidence categories**:
user facts, assistant facts, changing facts, abstention, preferences, and
implicit connections.

We mirror [Supermemory MemoryBench](https://github.com/supermemoryai/memorybench)'s
slice exactly — one `batched_000.json` per category from the HuggingFace
dataset — so numbers compare line-for-line against their published
leaderboard entry.

### Running it yourself

```bash
# Smoke run — 20 questions proportionally sliced across all 6 categories
python -m benchmarks.convomem --limit 20

# Full Supermemory slice (all batched_000.json items across 6 categories)
python -m benchmarks.convomem --limit 0 --concurrency 8

# Baseline without self-learning (delta = measured CE-worker lift)
python -m benchmarks.convomem --limit 20 --skip-advance-time

# Compare two JSONL result files (head-to-head)
python -m benchmarks.convomem --compare \
    benchmarks/convomem/results/sonzai_<ts>.jsonl \
    benchmarks/convomem/results/<other>_<ts>.jsonl
```

### Methodology — the only call that differs from a normal Sonzai app

ConvoMem's dataset has no timestamps. Per question, the bench replays each
conversation via `sessions.end(messages=<transcript>, wait=True)` — one call
per conversation, back-to-back. After all N conversations land, **one**
`workbench.advance_time(168h)` flush fires so daily consolidation and the
server-side weekly gate (`sessionCount % 7 == 0`) complete before retrieval.
One advance_time per question, not N — matters because advance_time takes
1–5 minutes per call.

Everything else (`agents.chat`, `memory.search`) hits the same production
endpoints.

### Metrics

- **QA accuracy** — Gemini 3.1 Flash Lite judges each answer against ground
  truth. Abstention category uses a dedicated prompt that rewards correct
  "I don't know" responses and penalizes fabrication.
- **Per-category breakdown** — six rows matching ConvoMem's categories.
- **MemScore** — `accuracy% / avg_latency_ms / avg_context_tokens`, Supermemory-
  compatible triple. Context-tokens is sourced from the chat handler's
  `context_ready.loaded_facts` count, not the raw haystack size.
- **advance_time diagnostics** — total CE-worker calls, consolidations fired,
  failures. Proves self-learning actually ran.
````

- [ ] **Step 2: Verify the markdown renders**

Run: `head -250 benchmarks/README.md | tail -50`
Expected: the new ConvoMem section appears cleanly between SOTOPIA and
the following section.

- [ ] **Step 3: Commit**

```bash
git add benchmarks/README.md
git commit -m "docs(bench): add ConvoMem section to README"
```

---

## Task 14: End-to-end validation against the platform

> **Network-gated.** This task only runs locally when `SONZAI_API_KEY` and
> `GEMINI_API_KEY` are set. Treat it as the "does this actually work"
> acceptance gate before declaring the feature done.

**Files:**
- Touch none; executes the runner against real infrastructure.

- [ ] **Step 1: Confirm env vars**

Run: `test -n "$SONZAI_API_KEY" && test -n "$GEMINI_API_KEY" && echo ok`
Expected: `ok`. If blank: stop, configure `.env`, and re-run.

- [ ] **Step 2: Dataset download check**

Run: `python -c "from benchmarks.convomem.dataset import load_questions; qs = load_questions(limit=6); print(len(qs), qs[0].question_type)"`
Expected: `6 user_evidence` (or whatever the first category is in
`CATEGORY_SUBFOLDERS`). Downloads six `batched_000.json` files on first run.

- [ ] **Step 3: Smoke run (6 questions, one per category, skip advance_time)**

Run: `python -m benchmarks.convomem --limit 6 --skip-advance-time --concurrency 2`
Expected:
- Runs in ~2 minutes (no advance_time).
- Prints a summary table with 6 categories.
- Writes `benchmarks/convomem/results/sonzai_<ts>.jsonl`.
- No crashes.

- [ ] **Step 4: Smoke run with advance_time**

Run: `python -m benchmarks.convomem --limit 6 --concurrency 2`
Expected:
- Runs in ~10–20 minutes (one advance_time per question).
- `advance_time` diagnostics row shows `calls >= 6`, `failures=0`.

- [ ] **Step 5: Self-compare two JSONLs**

Run: `python -m benchmarks.convomem --compare benchmarks/convomem/results/sonzai_*.jsonl`
Expected: per-category breakdown table + markdown table printed for both files.

- [ ] **Step 6: Commit first headline receipt**

If step 4's results look sane, copy the JSONL to a named receipt and
allow-list it in `.gitignore`:

```bash
cp benchmarks/convomem/results/sonzai_<ts>.jsonl \
   benchmarks/convomem/results/headline_sonzai_<ts>.jsonl
```

Add `!benchmarks/convomem/results/headline_sonzai_<ts>.jsonl` to
`benchmarks/.gitignore` under the ConvoMem section.

```bash
git add benchmarks/.gitignore benchmarks/convomem/results/headline_sonzai_<ts>.jsonl
git commit -m "bench(convomem): first headline receipt from smoke run"
```

---

## Self-Review

**1. Spec coverage:** Walking each spec section against tasks —
- §1 file layout → Tasks 1–3, 8–11.
- §2 dataset loader → Tasks 1–3. Category map, proportional slicing, download-by-default all covered.
- §3 Sonzai backend → Tasks 7–9. `ensure_convomem_agent_async`, per-conversation `sessions.end(wait=True)`, single `advance_time(168h)` flush, SSE chat consumption all present.
- §4 scoring → Tasks 4–6, 10. Normal + abstention judges wired per category in `_score_and_serialize`; MemScore aggregation in `aggregate_summary`.
- §5 CLI + compare → Task 10. Every spec flag is in `_parse_args`; compare output has both text and markdown tables.
- §6 tests → Tasks 1, 2, 4. Fixture-based loader + abstention judge + aggregation math tests included; no golden-output tests (deliberately — spec says so).
- Non-goals (full 75k grid, multi-evidence counts, retrieval scoring, supermemory backend) are respected — not implemented.

**2. Placeholder scan:** No TBDs, no "add error handling later", no "similar to Task N". Every code block is complete; every command shows expected output.

**3. Type consistency:**
- `ConvoMemQuestion`, `Conversation`, `Message`, `EvidenceMessage` — defined in Task 3, used identically in Tasks 4, 6, 9, 10.
- `BackendResult(agent_answer, ranked_fact_texts, extra)` — defined in Task 8, consumed in Task 9 (constructs) and Task 10 (`_score_and_serialize` reads `br.agent_answer` and `br.extra`).
- `aggregate_summary` / `format_percent` / `CATEGORY_ORDER` — defined in Task 6, imported in Task 10.
- `judge_abstention_async` / `judge_qa_async` / `GeminiJudge` / `QAVerdict` — `judge_abstention_async` added in Task 5, `judge_qa_async` + friends reused unchanged from existing `gemini_judge.py`.
- `ensure_convomem_agent_async` — defined in Task 7 under `sonzai.benchmarks`, imported in Task 10.
- `CATEGORY_SUBFOLDERS` — defined in Task 3, imported in Tasks 2, 10 for validation and help text.
- `resolve_cache_dir` — defined in Task 3, imported in Task 10 for logging.

No mismatched names or signatures found.

---

Plan complete and saved to `docs/superpowers/plans/2026-04-24-convomem-benchmark.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
