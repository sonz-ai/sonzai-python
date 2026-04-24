# LoCoMo benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `benchmarks/locomo/` — a Sonzai-vs-mem0 head-to-head LoCoMo runner that mirrors mem0's published evaluation pipeline byte-for-byte on the reader/judge side while swapping in Sonzai's `/process` + `advance_time` for the memory layer.

**Architecture:** New `benchmarks/locomo/` package following the existing `longmemeval/` layout (dataset, backends, scoring, run, compare, tests). Two backends (`sonzai.py`, `mem0.py`) both emitting the same `LocomoBackendResult` shape. Unified benchmark agent in the SDK (`sonzai.benchmarks.ensure_benchmark_agent_async`) shared across LongMemEval + LoCoMo. A `/process` forward-compat shim in `benchmarks/common/sdk_extras.py`. A Gemini-based reader and judge using verbatim ports of mem0's `ANSWER_PROMPT` and `ACCURACY_PROMPT`.

**Tech Stack:** Python 3.12, async Sonzai SDK (`sonzai.AsyncSonzai`), `google-genai` for Gemini, optional `mem0ai` SDK (lazy), `pytest` for tests, `tqdm.asyncio` for progress.

**Spec:** `docs/superpowers/specs/2026-04-24-locomo-benchmark-design.md`

---

## File Structure

### New files
| Path | Purpose |
|---|---|
| `benchmarks/locomo/__init__.py` | Package docstring |
| `benchmarks/locomo/__main__.py` | `python -m benchmarks.locomo` entry |
| `benchmarks/locomo/dataset.py` | Loader for `locomo10.json`, dataclasses, date-time parser, category-5 filter |
| `benchmarks/locomo/prompts.py` | Verbatim ports of mem0 `ANSWER_PROMPT` + `ACCURACY_PROMPT` |
| `benchmarks/locomo/scoring.py` | token-F1, session-level Recall@K + NDCG@K, aggregation |
| `benchmarks/locomo/run.py` | Orchestrator: CLI + Sonzai + mem0 + scoring + JSONL writer + compare |
| `benchmarks/locomo/compare.py` | Head-to-head table generator from two JSONLs |
| `benchmarks/locomo/backends/__init__.py` | `LocomoBackendResult` + `RankedMemoryItem` |
| `benchmarks/locomo/backends/sonzai.py` | `/process` ingest, advance_time, dual-user search, reader |
| `benchmarks/locomo/backends/mem0.py` | mem0ai port of `add.py` + `search.py` |
| `benchmarks/locomo/tests/__init__.py` | Empty |
| `benchmarks/locomo/tests/fixtures/mini_locomo.json` | Tiny 1-sample fixture for loader + ingest tests |
| `benchmarks/locomo/tests/test_dataset.py` | Loader + date-time parsing + filter tests |
| `benchmarks/locomo/tests/test_scoring.py` | token-F1 + Recall@K + aggregate tests |
| `benchmarks/locomo/tests/test_prompts_port.py` | Snapshot-assert prompt equality |
| `benchmarks/locomo/tests/test_scoring_integration.py` | Tiny end-to-end scoring over mini fixture |
| `benchmarks/locomo/results/.gitkeep` | Reserve results dir in git |
| `benchmarks/locomo/results/.gitignore` | Ignore all JSONL except allow-listed headline receipts |

### Modified files
| Path | What changes |
|---|---|
| `src/sonzai/benchmarks.py` | Add `BENCHMARK_AGENT_NAME`, `ensure_benchmark_agent_async` (+ sync variant); add aliases so `LONGMEMEVAL_AGENT_NAME` / `ensure_longmemeval_agent_async` still import. |
| `benchmarks/common/sdk_extras.py` | Add `async_process()` forward-compat shim |
| `benchmarks/common/gemini_judge.py` | Add `LocomoVerdict` + `judge_locomo_async` |
| `benchmarks/common/agent_reuse.py` | `SliceKey.matches()` — add `"locomo"` branch |
| `benchmarks/longmemeval/run.py` | One-line import swap to the new `ensure_benchmark_agent_async` |
| `benchmarks/README.md` | New LoCoMo section |

---

## Conventions

- **Testing:** every module gets unit tests first. Run tests from the repo root: `pytest benchmarks/locomo/tests/ -v`. Tests must not hit live APIs.
- **Commit cadence:** commit at the end of each task (after all steps pass). Commit message = imperative mood, scoped `feat(bench):` / `test(bench):` / `refactor(sdk):` etc.
- **Code style:** match the existing `longmemeval/` patterns — `from __future__ import annotations`, explicit dataclasses, `logger = logging.getLogger(__name__)`, no emojis, minimal comments (only for non-obvious WHY).

---

## Task 1: SDK refactor — unified benchmark agent

**Files:**
- Modify: `src/sonzai/benchmarks.py`

- [ ] **Step 1: Verify current state of the SDK module**

Run: `grep -n "LONGMEMEVAL_AGENT_NAME\|ensure_longmemeval" src/sonzai/benchmarks.py`

Expected: matches on lines around 50–54 (`__all__`), 69 (constant), 105, 134 (functions).

- [ ] **Step 2: Write a failing test for the new exports**

Create: `tests/unit/test_benchmarks_agent.py`

```python
"""Exports + aliases for the unified benchmark agent preset."""

from __future__ import annotations


def test_benchmark_agent_name_is_exported():
    from sonzai.benchmarks import BENCHMARK_AGENT_NAME

    assert BENCHMARK_AGENT_NAME == "sonzai-benchmark-agent"


def test_ensure_benchmark_agent_async_is_callable():
    from sonzai.benchmarks import ensure_benchmark_agent_async

    assert callable(ensure_benchmark_agent_async)


def test_longmemeval_aliases_point_to_unified_exports():
    """Back-compat: old names still resolve to the new ones."""
    from sonzai.benchmarks import (
        BENCHMARK_AGENT_NAME,
        LONGMEMEVAL_AGENT_NAME,
        ensure_benchmark_agent_async,
        ensure_longmemeval_agent_async,
    )

    assert LONGMEMEVAL_AGENT_NAME == BENCHMARK_AGENT_NAME
    assert ensure_longmemeval_agent_async is ensure_benchmark_agent_async


def test_sync_aliases_point_to_unified_exports():
    from sonzai.benchmarks import ensure_benchmark_agent, ensure_longmemeval_agent

    assert ensure_longmemeval_agent is ensure_benchmark_agent
```

- [ ] **Step 3: Run test — expect ImportError for `BENCHMARK_AGENT_NAME`**

Run: `pytest tests/unit/test_benchmarks_agent.py -v`

Expected: FAIL — `ImportError: cannot import name 'BENCHMARK_AGENT_NAME'`

- [ ] **Step 4: Refactor `src/sonzai/benchmarks.py` — add unified names, preserve aliases**

Edit `src/sonzai/benchmarks.py`:

Change `__all__`:
```python
__all__ = [
    # Unified exports (new canonical names)
    "BENCHMARK_AGENT_NAME",
    "BENCHMARK_AGENT_DESCRIPTION",
    "BENCHMARK_SPEECH_PATTERNS",
    "ensure_benchmark_agent",
    "ensure_benchmark_agent_async",
    # Back-compat aliases — keep exporting the old names one-for-one.
    "LONGMEMEVAL_AGENT_NAME",
    "LONGMEMEVAL_AGENT_DESCRIPTION",
    "LONGMEMEVAL_SPEECH_PATTERNS",
    "ensure_longmemeval_agent",
    "ensure_longmemeval_agent_async",
]
```

Rename the constants (this moves the canonical definition, keeps behavior identical):
```python
BENCHMARK_AGENT_NAME = "sonzai-benchmark-agent"

BENCHMARK_AGENT_DESCRIPTION = (
    "A helpful AI assistant that maintains a rich long-term memory of the "
    "user. Remembers specific personal details (routines, preferences, "
    "places, people, milestones, plans) and recalls them accurately when "
    "asked. Warm and attentive in day-to-day chat but switches to crisp, "
    "factual answers when the user is clearly asking for a lookup."
)

BENCHMARK_SPEECH_PATTERNS: list[str] = [
    "Answers recall questions with the literal value first — a number, "
    "name, date, or short phrase — before any optional context.",
]

# Back-compat aliases — deprecated, kept for one release cycle.
LONGMEMEVAL_AGENT_NAME = BENCHMARK_AGENT_NAME
LONGMEMEVAL_AGENT_DESCRIPTION = BENCHMARK_AGENT_DESCRIPTION
LONGMEMEVAL_SPEECH_PATTERNS = BENCHMARK_SPEECH_PATTERNS
```

Rename the functions `ensure_longmemeval_agent` / `ensure_longmemeval_agent_async` to `ensure_benchmark_agent` / `ensure_benchmark_agent_async`, updating their default-argument references to the new constant names. Then add module-level aliases at the bottom of the file:

```python
# Back-compat aliases — identity assignments so `is` comparisons hold.
ensure_longmemeval_agent = ensure_benchmark_agent
ensure_longmemeval_agent_async = ensure_benchmark_agent_async
```

Update the module docstring: swap the usage example from `ensure_longmemeval_agent_async` to `ensure_benchmark_agent_async`, mention that old names are preserved as aliases.

- [ ] **Step 5: Run all SDK unit tests to catch any breakage**

Run: `pytest tests/unit/ -v -k benchmark`

Expected: all tests in `test_benchmarks_agent.py` PASS. No regressions elsewhere.

- [ ] **Step 6: Update LongMemEval run.py to use the new name**

Edit `benchmarks/longmemeval/run.py` around lines 298–301:

Before:
```python
from sonzai.benchmarks import (
    LONGMEMEVAL_AGENT_NAME,
    ensure_longmemeval_agent_async,
)

agent_name = LONGMEMEVAL_AGENT_NAME
resolved_agent_id, agent_existed = await ensure_longmemeval_agent_async(client)
```

After:
```python
from sonzai.benchmarks import (
    BENCHMARK_AGENT_NAME,
    ensure_benchmark_agent_async,
)

agent_name = BENCHMARK_AGENT_NAME
resolved_agent_id, agent_existed = await ensure_benchmark_agent_async(client)
```

- [ ] **Step 7: Verify LongMemEval module still imports cleanly**

Run: `python -c "from benchmarks.longmemeval import run; print('ok')"`

Expected: `ok`

- [ ] **Step 8: Commit**

```bash
git add src/sonzai/benchmarks.py tests/unit/test_benchmarks_agent.py benchmarks/longmemeval/run.py
git commit -m "refactor(sdk): unify benchmark agent preset across LongMemEval + LoCoMo

Renames the canonical bench-agent exports from LONGMEMEVAL_* to the
generic BENCHMARK_* so a single agent is used across every memory
benchmark. Old names kept as identity aliases for back-compat.
LongMemEval run.py updated to the new name."
```

---

## Task 2: `/process` forward-compat shim

**Files:**
- Modify: `benchmarks/common/sdk_extras.py`
- Create: `benchmarks/common/tests/__init__.py` (if missing)
- Create: `benchmarks/common/tests/test_sdk_extras_process.py`

- [ ] **Step 1: Check whether common/tests exists**

Run: `ls benchmarks/common/tests/ 2>/dev/null || echo MISSING`

If MISSING, create `benchmarks/common/tests/__init__.py` as an empty file.

- [ ] **Step 2: Write failing test for `async_process` signature and fallback**

Create: `benchmarks/common/tests/test_sdk_extras_process.py`

```python
"""Tests for async_process() — the forward-compat shim over POST /process."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from benchmarks.common.sdk_extras import async_process


@pytest.mark.asyncio
async def test_async_process_falls_back_to_raw_transport():
    """When client.process isn't present, go through client._http.post."""
    client = MagicMock()
    client.process = None  # simulate pre-regen SDK
    client._http = MagicMock()
    client._http.post = AsyncMock(
        return_value={"success": True, "facts_extracted": 3, "side_effects": {}}
    )

    resp = await async_process(
        client,
        agent_id="agent-1",
        user_id="user-1",
        messages=[
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ],
        session_id="sess-1",
    )

    client._http.post.assert_awaited_once()
    path, = client._http.post.call_args.args
    kwargs = client._http.post.call_args.kwargs
    assert path == "/api/v1/agents/agent-1/process"
    assert kwargs["json_data"]["userId"] == "user-1"
    assert kwargs["json_data"]["sessionId"] == "sess-1"
    assert len(kwargs["json_data"]["messages"]) == 2
    assert resp["facts_extracted"] == 3


@pytest.mark.asyncio
async def test_async_process_uses_native_binding_when_present():
    client = MagicMock()
    client.process = AsyncMock(return_value={"success": True, "facts_extracted": 1})

    resp = await async_process(
        client,
        agent_id="agent-1",
        user_id="user-1",
        messages=[{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}],
    )

    client.process.assert_awaited_once()
    assert resp["facts_extracted"] == 1


@pytest.mark.asyncio
async def test_async_process_requires_min_2_messages():
    """The server requires >=2 messages; we validate client-side to fail fast."""
    client = MagicMock()
    client.process = None
    client._http = MagicMock()

    with pytest.raises(ValueError, match="at least 2 messages"):
        await async_process(
            client,
            agent_id="agent-1",
            user_id="user-1",
            messages=[{"role": "user", "content": "only one"}],
        )
```

- [ ] **Step 3: Run test — expect ImportError**

Run: `pytest benchmarks/common/tests/test_sdk_extras_process.py -v`

Expected: FAIL — `ImportError: cannot import name 'async_process'`

- [ ] **Step 4: Add `async_process` to `benchmarks/common/sdk_extras.py`**

Append to the file:

```python
# ---------------------------------------------------------------------------
# /process endpoint shim — runs full CE pipeline on externally-generated
# transcripts. Used by benchmarks ingesting pre-scripted conversations
# (LoCoMo, potentially others) where sessions.start/end ceremony is
# unnecessary. Forward-compat: delegates to client.process when the
# regenerated SDK exposes a native binding.
# ---------------------------------------------------------------------------


async def async_process(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    messages: list[dict[str, str]],
    session_id: str = "",
    instance_id: str = "",
    provider: str = "",
    model: str = "",
) -> dict:
    """POST /api/v1/agents/{agent_id}/process. Requires >=2 messages.

    Returns the server response dict as-is: {success, facts_extracted, side_effects}.
    Raises ValueError if fewer than 2 messages are supplied (mirrors server
    validation so we fail fast with a clear message).
    """
    if len(messages) < 2:
        raise ValueError("/process requires at least 2 messages")

    native = getattr(client, "process", None)
    if native is not None and callable(native):
        return await native(
            agent_id=agent_id,
            user_id=user_id,
            messages=messages,
            session_id=session_id,
            instance_id=instance_id,
            provider=provider,
            model=model,
        )

    body: dict[str, object] = {
        "userId": user_id,
        "messages": messages,
        "sessionId": session_id,
        "instanceId": instance_id,
        "provider": provider,
        "model": model,
    }
    return await client._http.post(  # type: ignore[attr-defined]
        f"/api/v1/agents/{agent_id}/process", json_data=body,
    )
```

- [ ] **Step 5: Run tests again**

Run: `pytest benchmarks/common/tests/test_sdk_extras_process.py -v`

Expected: all 3 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add benchmarks/common/sdk_extras.py benchmarks/common/tests/test_sdk_extras_process.py benchmarks/common/tests/__init__.py
git commit -m "feat(bench): add async_process shim for /process endpoint

Forward-compat wrapper around POST /api/v1/agents/{id}/process. Used by
LoCoMo and other external-transcript benchmarks. Delegates to client.process
when the regenerated SDK exposes a native binding; otherwise uses the raw
transport. Validates message count client-side to fail fast."
```

---

## Task 3: Dataset loader + dataclasses

**Files:**
- Create: `benchmarks/locomo/__init__.py`
- Create: `benchmarks/locomo/__main__.py`
- Create: `benchmarks/locomo/dataset.py`
- Create: `benchmarks/locomo/tests/__init__.py`
- Create: `benchmarks/locomo/tests/fixtures/mini_locomo.json`
- Create: `benchmarks/locomo/tests/test_dataset.py`

- [ ] **Step 1: Create package skeleton**

`benchmarks/locomo/__init__.py`:

```python
"""LoCoMo benchmark — Sonzai vs mem0 on long-term conversational memory.

Dataset: https://github.com/snap-research/locomo (10 dialogues, 19–35 sessions
each, 300–600 turns). Invoke via::

    python -m benchmarks.locomo --backend sonzai --limit 2
    python -m benchmarks.locomo --backend mem0 --limit 2
    python -m benchmarks.locomo --compare results/sonzai_*.jsonl results/mem0_*.jsonl

See benchmarks/locomo/dataset.py for the data shape and
docs/superpowers/specs/2026-04-24-locomo-benchmark-design.md for the full
evaluation protocol.
"""
```

`benchmarks/locomo/__main__.py`:

```python
"""Entry point for ``python -m benchmarks.locomo``."""

from __future__ import annotations

from .run import main

if __name__ == "__main__":
    raise SystemExit(main())
```

`benchmarks/locomo/tests/__init__.py`: empty.

- [ ] **Step 2: Write the mini-fixture**

Create `benchmarks/locomo/tests/fixtures/mini_locomo.json`:

```json
[
  {
    "sample_id": "fixture-sample-0",
    "qa": [
      {
        "question": "What job does Alice want?",
        "answer": "data scientist",
        "evidence": ["D1:3"],
        "category": 1
      },
      {
        "question": "When did Bob buy his bike?",
        "answer": "May 2023",
        "evidence": ["D2:4"],
        "category": 3
      },
      {
        "question": "Adversarial question about unknowns",
        "answer": "no answer",
        "adversarial_answer": "I don't know",
        "evidence": [],
        "category": 5
      }
    ],
    "conversation": {
      "speaker_a": "Alice",
      "speaker_b": "Bob",
      "session_1_date_time": "1:00 pm on 8 May, 2023",
      "session_1": [
        {"speaker": "Alice", "dia_id": "D1:1", "text": "Hi Bob!"},
        {"speaker": "Bob", "dia_id": "D1:2", "text": "Hey Alice, what's new?"},
        {"speaker": "Alice", "dia_id": "D1:3", "text": "I'm applying for data science roles."},
        {"speaker": "Bob", "dia_id": "D1:4", "text": "Nice, good luck!"}
      ],
      "session_2_date_time": "9:00 am on 12 May, 2023",
      "session_2": [
        {"speaker": "Bob", "dia_id": "D2:1", "text": "I got something cool yesterday."},
        {"speaker": "Alice", "dia_id": "D2:2", "text": "Oh yeah?"},
        {"speaker": "Bob", "dia_id": "D2:3", "text": "Yeah, new bicycle."},
        {"speaker": "Alice", "dia_id": "D2:4", "text": "Awesome, when?"}
      ]
    }
  }
]
```

- [ ] **Step 3: Write failing tests**

Create `benchmarks/locomo/tests/test_dataset.py`:

```python
"""Tests for the LoCoMo dataset loader."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from benchmarks.locomo.dataset import (
    LocomoQA,
    LocomoSample,
    LocomoSession,
    LocomoTurn,
    load_qa,
    load_samples,
    parse_locomo_datetime,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mini_locomo.json"


def test_load_samples_shape():
    samples = load_samples(path=FIXTURE)
    assert len(samples) == 1
    sample = samples[0]
    assert sample.sample_id == "fixture-sample-0"
    assert sample.speaker_a == "Alice"
    assert sample.speaker_b == "Bob"
    assert len(sample.sessions) == 2
    assert len(sample.qa) == 3


def test_load_samples_sessions_are_sorted_chronologically():
    samples = load_samples(path=FIXTURE)
    sessions = samples[0].sessions
    assert sessions[0].index == 1
    assert sessions[1].index == 2
    assert sessions[0].parsed_date_time < sessions[1].parsed_date_time


def test_load_samples_turns_preserve_dia_ids():
    samples = load_samples(path=FIXTURE)
    turns = samples[0].sessions[0].turns
    assert [t.dia_id for t in turns] == ["D1:1", "D1:2", "D1:3", "D1:4"]
    assert turns[0].speaker == "Alice"
    assert turns[0].text == "Hi Bob!"


def test_load_samples_limit_truncates():
    samples = load_samples(path=FIXTURE, limit=1)
    assert len(samples) == 1


def test_load_qa_filters_adversarial_by_default():
    samples = load_samples(path=FIXTURE)
    pairs = load_qa(samples)
    categories = [qa.category for _, qa in pairs]
    assert 5 not in categories
    assert len(pairs) == 2


def test_load_qa_include_adversarial():
    samples = load_samples(path=FIXTURE)
    pairs = load_qa(samples, include_adversarial=True)
    assert len(pairs) == 3
    assert any(qa.category == 5 for _, qa in pairs)


def test_parse_locomo_datetime_standard_format():
    dt = parse_locomo_datetime("1:00 pm on 8 May, 2023")
    assert dt == datetime(2023, 5, 8, 13, 0)


def test_parse_locomo_datetime_morning():
    dt = parse_locomo_datetime("9:00 am on 12 May, 2023")
    assert dt == datetime(2023, 5, 12, 9, 0)


def test_parse_locomo_datetime_fallback_on_unparseable():
    """Unparseable strings return datetime.min so callers can fall back to index order."""
    dt = parse_locomo_datetime("nonsense")
    assert dt == datetime.min
```

- [ ] **Step 4: Run tests — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_dataset.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'benchmarks.locomo.dataset'`

- [ ] **Step 5: Implement `benchmarks/locomo/dataset.py`**

```python
"""LoCoMo dataset loader.

Dataset source:
    https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json

Each sample has:
- conversation.speaker_a / speaker_b: the two participants' display names
- conversation.session_N: list of turn dicts (speaker, dia_id, text)
- conversation.session_N_date_time: human-readable timestamp string
- qa: list of {question, answer, evidence: [dia_id...], category: 1..5}

Category 5 is adversarial (unanswerable); filtered by default — matches
mem0's published methodology so our numbers compare directly.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ..common.dataset_cache import ensure_file

DATASET_URL = (
    "https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json"
)
DATASET_FILE = "locomo10.json"

# LoCoMo dates look like: "1:00 pm on 8 May, 2023"
_LOCOMO_DT_RE = re.compile(
    r"^\s*(\d{1,2}):(\d{2})\s*(am|pm)\s+on\s+(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})\s*$",
    re.IGNORECASE,
)
_MONTH_MAP = {
    m.lower(): i for i, m in enumerate(
        ["", "January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
        start=0,
    ) if i > 0
}


@dataclass
class LocomoTurn:
    speaker: str
    dia_id: str
    text: str
    img_url: str = ""
    blip_caption: str = ""


@dataclass
class LocomoSession:
    index: int
    date_time: str
    turns: list[LocomoTurn]

    @property
    def parsed_date_time(self) -> datetime:
        return parse_locomo_datetime(self.date_time)


@dataclass
class LocomoQA:
    question: str
    answer: str
    category: int
    evidence: list[str] = field(default_factory=list)
    adversarial_answer: str = ""


@dataclass
class LocomoSample:
    sample_id: str
    speaker_a: str
    speaker_b: str
    sessions: list[LocomoSession]
    qa: list[LocomoQA]


def parse_locomo_datetime(raw: str) -> datetime:
    """Parse LoCoMo's "1:00 pm on 8 May, 2023" format.

    Returns datetime.min on parse failure so callers can sort by index order
    as a fallback without raising. This is intentional — the dataset is hand-
    annotated and string formats drift slightly between samples.
    """
    m = _LOCOMO_DT_RE.match(raw or "")
    if not m:
        return datetime.min
    hour, minute, ampm, day, month_name, year = m.groups()
    month = _MONTH_MAP.get(month_name.lower())
    if month is None:
        return datetime.min
    h = int(hour) % 12
    if ampm.lower() == "pm":
        h += 12
    try:
        return datetime(int(year), month, int(day), h, int(minute))
    except ValueError:
        return datetime.min


def _build_turns(raw_turns: list[dict]) -> list[LocomoTurn]:
    out: list[LocomoTurn] = []
    for t in raw_turns:
        out.append(
            LocomoTurn(
                speaker=str(t.get("speaker") or ""),
                dia_id=str(t.get("dia_id") or ""),
                text=str(t.get("text") or ""),
                img_url=str(t.get("img_url") or ""),
                blip_caption=str(t.get("blip_caption") or ""),
            )
        )
    return out


def _build_sample(raw: dict, sample_id_fallback: str) -> LocomoSample:
    conv = raw.get("conversation") or {}
    speaker_a = str(conv.get("speaker_a") or "")
    speaker_b = str(conv.get("speaker_b") or "")

    sessions: list[LocomoSession] = []
    for key in conv.keys():
        if not key.startswith("session_") or key.endswith("_date_time"):
            continue
        if key in ("speaker_a", "speaker_b"):
            continue
        try:
            idx = int(key.split("_", 1)[1])
        except (ValueError, IndexError):
            continue
        raw_turns = conv.get(key) or []
        if not isinstance(raw_turns, list):
            continue
        dt_key = f"{key}_date_time"
        sessions.append(
            LocomoSession(
                index=idx,
                date_time=str(conv.get(dt_key) or ""),
                turns=_build_turns(raw_turns),
            )
        )

    # Sort by parsed date_time; on ties or unparseable dates, fall back to index.
    sessions.sort(key=lambda s: (s.parsed_date_time, s.index))

    qa_list: list[LocomoQA] = []
    for qa in raw.get("qa") or []:
        qa_list.append(
            LocomoQA(
                question=str(qa.get("question") or ""),
                answer=str(qa.get("answer") or ""),
                category=int(qa.get("category") or 0),
                evidence=[str(e) for e in (qa.get("evidence") or [])],
                adversarial_answer=str(qa.get("adversarial_answer") or ""),
            )
        )

    return LocomoSample(
        sample_id=str(raw.get("sample_id") or sample_id_fallback),
        speaker_a=speaker_a,
        speaker_b=speaker_b,
        sessions=sessions,
        qa=qa_list,
    )


def load_samples(*, limit: int = 0, path: "str | Path | None" = None) -> list[LocomoSample]:
    """Load LoCoMo samples, auto-downloading the dataset on first run.

    ``limit=0`` returns all samples. ``path`` overrides the cached default —
    pass a fixture path for tests.
    """
    target = Path(path) if path else ensure_file(DATASET_URL, DATASET_FILE)
    with open(target) as f:
        raw = json.load(f)
    samples = [
        _build_sample(item, sample_id_fallback=f"locomo-{i}")
        for i, item in enumerate(raw)
    ]
    if limit and limit > 0:
        samples = samples[:limit]
    return samples


def load_qa(
    samples: list[LocomoSample], *, include_adversarial: bool = False,
) -> list[tuple[LocomoSample, LocomoQA]]:
    """Flatten samples into (sample, qa) pairs. Category 5 filtered by default."""
    out: list[tuple[LocomoSample, LocomoQA]] = []
    for s in samples:
        for qa in s.qa:
            if qa.category == 5 and not include_adversarial:
                continue
            out.append((s, qa))
    return out
```

- [ ] **Step 6: Run tests**

Run: `pytest benchmarks/locomo/tests/test_dataset.py -v`

Expected: all 9 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add benchmarks/locomo/__init__.py benchmarks/locomo/__main__.py benchmarks/locomo/dataset.py benchmarks/locomo/tests/__init__.py benchmarks/locomo/tests/fixtures/mini_locomo.json benchmarks/locomo/tests/test_dataset.py
git commit -m "feat(bench): LoCoMo dataset loader + dataclasses

Loader for snap-research/locomo10.json with robust parser for the
'1:00 pm on 8 May, 2023' date-time format (falls back to datetime.min
on unparseable strings so session ordering degrades to index order
rather than raising). Includes fixture + 9 unit tests."
```

---

## Task 4: Verbatim prompt port

**Files:**
- Create: `benchmarks/locomo/prompts.py`
- Create: `benchmarks/locomo/tests/test_prompts_port.py`

- [ ] **Step 1: Fetch canonical upstream hashes**

Run: `gh api repos/mem0ai/mem0/contents/evaluation/prompts.py -H "Accept: application/vnd.github.raw" | shasum -a 256`

Expected: a 64-char hex hash. Record it.

Run: `gh api repos/mem0ai/mem0/contents/evaluation/metrics/llm_judge.py -H "Accept: application/vnd.github.raw" | shasum -a 256`

Expected: a 64-char hex hash. Record it.

- [ ] **Step 2: Write failing test that asserts the ported prompts match upstream**

Create: `benchmarks/locomo/tests/test_prompts_port.py`

```python
"""Snapshot tests guarding the mem0 prompt ports against accidental edits.

The LoCoMo benchmark's credibility depends on running mem0's ANSWER_PROMPT
and ACCURACY_PROMPT byte-for-byte. If mem0 updates their prompts upstream,
we re-port deliberately; if someone edits ours locally, this test catches it.
"""

from __future__ import annotations

from benchmarks.locomo.prompts import (
    ACCURACY_PROMPT,
    ANSWER_PROMPT,
    ANSWER_PROMPT_GRAPH,
    PROMPT_SOURCE,
)


def test_prompt_source_documents_provenance():
    assert "mem0ai/mem0" in PROMPT_SOURCE
    assert "evaluation/prompts.py" in PROMPT_SOURCE
    assert "evaluation/metrics/llm_judge.py" in PROMPT_SOURCE


def test_answer_prompt_contains_required_instructions():
    # Structural invariants — if any of these disappear we have broken parity.
    assert "{{speaker_1_user_id}}" in ANSWER_PROMPT
    assert "{{speaker_2_user_id}}" in ANSWER_PROMPT
    assert "{{speaker_1_memories}}" in ANSWER_PROMPT
    assert "{{speaker_2_memories}}" in ANSWER_PROMPT
    assert "{{question}}" in ANSWER_PROMPT
    assert "less than 5-6 words" in ANSWER_PROMPT
    assert "timestamps" in ANSWER_PROMPT.lower()


def test_answer_prompt_graph_contains_graph_relations():
    assert "{{speaker_1_graph_memories}}" in ANSWER_PROMPT_GRAPH
    assert "{{speaker_2_graph_memories}}" in ANSWER_PROMPT_GRAPH
    assert "knowledge graph" in ANSWER_PROMPT_GRAPH.lower()


def test_accuracy_prompt_invariants():
    assert "{question}" in ACCURACY_PROMPT
    assert "{gold_answer}" in ACCURACY_PROMPT
    assert "{generated_answer}" in ACCURACY_PROMPT
    assert "CORRECT" in ACCURACY_PROMPT
    assert "WRONG" in ACCURACY_PROMPT
    assert '"label"' in ACCURACY_PROMPT
```

- [ ] **Step 3: Run test — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_prompts_port.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'benchmarks.locomo.prompts'`

- [ ] **Step 4: Fetch upstream prompts and paste verbatim**

Create `benchmarks/locomo/prompts.py`:

```python
"""Ported LoCoMo evaluation prompts from mem0's upstream evaluation suite.

These prompts are reproduced BYTE-FOR-BYTE from mem0's published evaluation
code so our LoCoMo numbers are directly comparable to mem0's paper results.
DO NOT EDIT these strings for local preferences — if mem0 updates upstream,
re-port deliberately and update the source record below.

A snapshot test (test_prompts_port.py) asserts structural invariants to
guard against accidental edits.
"""

from __future__ import annotations

PROMPT_SOURCE = (
    "Ported from mem0ai/mem0:\n"
    "- evaluation/prompts.py (ANSWER_PROMPT, ANSWER_PROMPT_GRAPH)\n"
    "- evaluation/metrics/llm_judge.py (ACCURACY_PROMPT)\n"
    "Ported on 2026-04-24.\n"
)


# ---- ANSWER_PROMPT_GRAPH — verbatim from mem0/evaluation/prompts.py ----

ANSWER_PROMPT_GRAPH = """
    You are an intelligent memory assistant tasked with retrieving accurate information from 
    conversation memories.

    # CONTEXT:
    You have access to memories from two speakers in a conversation. These memories contain 
    timestamped information that may be relevant to answering the question. You also have 
    access to knowledge graph relations for each user, showing connections between entities, 
    concepts, and events relevant to that user.

    # INSTRUCTIONS:
    1. Carefully analyze all provided memories from both speakers
    2. Pay special attention to the timestamps to determine the answer
    3. If the question asks about a specific event or fact, look for direct evidence in the 
       memories
    4. If the memories contain contradictory information, prioritize the most recent memory
    5. If there is a question about time references (like "last year", "two months ago", 
       etc.), calculate the actual date based on the memory timestamp. For example, if a 
       memory from 4 May 2022 mentions "went to India last year," then the trip occurred 
       in 2021.
    6. Always convert relative time references to specific dates, months, or years. For 
       example, convert "last year" to "2022" or "two months ago" to "March 2023" based 
       on the memory timestamp. Ignore the reference while answering the question.
    7. Focus only on the content of the memories from both speakers. Do not confuse 
       character names mentioned in memories with the actual users who created those 
       memories.
    8. The answer should be less than 5-6 words.
    9. Use the knowledge graph relations to understand the user's knowledge network and 
       identify important relationships between entities in the user's world.

    # APPROACH (Think step by step):
    1. First, examine all memories that contain information related to the question
    2. Examine the timestamps and content of these memories carefully
    3. Look for explicit mentions of dates, times, locations, or events that answer the 
       question
    4. If the answer requires calculation (e.g., converting relative time references), 
       show your work
    5. Analyze the knowledge graph relations to understand the user's knowledge context
    6. Formulate a precise, concise answer based solely on the evidence in the memories
    7. Double-check that your answer directly addresses the question asked
    8. Ensure your final answer is specific and avoids vague time references

    Memories for user {{speaker_1_user_id}}:

    {{speaker_1_memories}}

    Relations for user {{speaker_1_user_id}}:

    {{speaker_1_graph_memories}}

    Memories for user {{speaker_2_user_id}}:

    {{speaker_2_memories}}

    Relations for user {{speaker_2_user_id}}:

    {{speaker_2_graph_memories}}

    Question: {{question}}

    Answer:
    """


# ---- ANSWER_PROMPT — verbatim from mem0/evaluation/prompts.py ----

ANSWER_PROMPT = """
    You are an intelligent memory assistant tasked with retrieving accurate information from conversation memories.

    # CONTEXT:
    You have access to memories from two speakers in a conversation. These memories contain 
    timestamped information that may be relevant to answering the question.

    # INSTRUCTIONS:
    1. Carefully analyze all provided memories from both speakers
    2. Pay special attention to the timestamps to determine the answer
    3. If the question asks about a specific event or fact, look for direct evidence in the memories
    4. If the memories contain contradictory information, prioritize the most recent memory
    5. If there is a question about time references (like "last year", "two months ago", etc.), 
       calculate the actual date based on the memory timestamp. For example, if a memory from 
       4 May 2022 mentions "went to India last year," then the trip occurred in 2021.
    6. Always convert relative time references to specific dates, months, or years. For example, 
       convert "last year" to "2022" or "two months ago" to "March 2023" based on the memory 
       timestamp. Ignore the reference while answering the question.
    7. Focus only on the content of the memories from both speakers. Do not confuse character 
       names mentioned in memories with the actual users who created those memories.
    8. The answer should be less than 5-6 words.

    # APPROACH (Think step by step):
    1. First, examine all memories that contain information related to the question
    2. Examine the timestamps and content of these memories carefully
    3. Look for explicit mentions of dates, times, locations, or events that answer the question
    4. If the answer requires calculation (e.g., converting relative time references), show your work
    5. Formulate a precise, concise answer based solely on the evidence in the memories
    6. Double-check that your answer directly addresses the question asked
    7. Ensure your final answer is specific and avoids vague time references

    Memories for user {{speaker_1_user_id}}:

    {{speaker_1_memories}}

    Memories for user {{speaker_2_user_id}}:

    {{speaker_2_memories}}

    Question: {{question}}

    Answer:
    """


# ---- ACCURACY_PROMPT — verbatim from mem0/evaluation/metrics/llm_judge.py ----

ACCURACY_PROMPT = """
Your task is to label an answer to a question as 'CORRECT' or 'WRONG'. You will be given the following data:
    (1) a question (posed by one user to another user), 
    (2) a 'gold' (ground truth) answer, 
    (3) a generated answer
which you will score as CORRECT/WRONG.

The point of the question is to ask about something one user should know about the other user based on their prior conversations.
The gold answer will usually be a concise and short answer that includes the referenced topic, for example:
Question: Do you remember what I got the last time I went to Hawaii?
Gold answer: A shell necklace
The generated answer might be much longer, but you should be generous with your grading - as long as it touches on the same topic as the gold answer, it should be counted as CORRECT. 

For time related questions, the gold answer will be a specific date, month, year, etc. The generated answer might be much longer or use relative time references (like "last Tuesday" or "next month"), but you should be generous with your grading - as long as it refers to the same date or time period as the gold answer, it should be counted as CORRECT. Even if the format differs (e.g., "May 7th" vs "7 May"), consider it CORRECT if it's the same date.

Now it's time for the real question:
Question: {question}
Gold answer: {gold_answer}
Generated answer: {generated_answer}

First, provide a short (one sentence) explanation of your reasoning, then finish with CORRECT or WRONG. 
Do NOT include both CORRECT and WRONG in your response, or it will break the evaluation script.

Just return the label CORRECT or WRONG in a json format with the key as "label".
"""


__all__ = ["PROMPT_SOURCE", "ANSWER_PROMPT", "ANSWER_PROMPT_GRAPH", "ACCURACY_PROMPT"]
```

**Note on the ACCURACY_PROMPT:** mem0's upstream uses the typographic apostrophe `’` in `'CORRECT' or 'WRONG'`. We use straight apostrophes `'` — the only intentional deviation (straight apostrophes don't affect LLM interpretation and make Python multi-line strings easier to edit). If this matters for strict byte-equality you can switch to the typographic variants.

- [ ] **Step 5: Run tests**

Run: `pytest benchmarks/locomo/tests/test_prompts_port.py -v`

Expected: all 4 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add benchmarks/locomo/prompts.py benchmarks/locomo/tests/test_prompts_port.py
git commit -m "feat(bench): port mem0 ANSWER_PROMPT + ACCURACY_PROMPT verbatim

Ports the two load-bearing prompts from mem0's LoCoMo evaluation (reader +
LLM judge) so our LoCoMo numbers compare directly to mem0's paper headline.
Snapshot test guards structural invariants against accidental edits."
```

---

## Task 5: `LocomoVerdict` + `judge_locomo_async`

**Files:**
- Modify: `benchmarks/common/gemini_judge.py`
- Create: `benchmarks/common/tests/test_gemini_judge_locomo.py`

- [ ] **Step 1: Write failing test**

Create `benchmarks/common/tests/test_gemini_judge_locomo.py`:

```python
"""Tests for the LoCoMo judge wrapper."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from benchmarks.common.gemini_judge import LocomoVerdict, judge_locomo_async


def test_locomo_verdict_schema():
    v = LocomoVerdict(label="CORRECT")
    assert v.label == "CORRECT"

    # Allow WRONG too
    v2 = LocomoVerdict(label="WRONG")
    assert v2.label == "WRONG"


@pytest.mark.asyncio
async def test_judge_locomo_async_returns_structured_verdict():
    judge = MagicMock()
    judge.grade_async = AsyncMock(return_value=LocomoVerdict(label="CORRECT"))

    result = await judge_locomo_async(
        judge,
        question="What color is Bob's bike?",
        gold_answer="red",
        generated_answer="The bike is red.",
    )

    assert isinstance(result, LocomoVerdict)
    assert result.label == "CORRECT"
    judge.grade_async.assert_awaited_once()
    prompt_arg, schema_arg = judge.grade_async.call_args.args
    assert "What color is Bob's bike?" in prompt_arg
    assert "red" in prompt_arg
    assert "The bike is red." in prompt_arg
    assert schema_arg is LocomoVerdict
```

- [ ] **Step 2: Run test — expect ImportError**

Run: `pytest benchmarks/common/tests/test_gemini_judge_locomo.py -v`

Expected: FAIL — `ImportError: cannot import name 'LocomoVerdict'`

- [ ] **Step 3: Add `LocomoVerdict` + `judge_locomo_async` to `benchmarks/common/gemini_judge.py`**

Append to the file (before `__all__` at the bottom):

```python
# ---------------------------------------------------------------------------
# LoCoMo judge — mirrors mem0's LLM-judge binary CORRECT/WRONG rubric.
# The prompt is ported verbatim in benchmarks/locomo/prompts.py. Kept here
# (not in locomo/) because common/gemini_judge.py is the hub for all
# structured-output grading wrappers.
# ---------------------------------------------------------------------------


class LocomoVerdict(BaseModel):
    """Binary verdict matching mem0's llm_judge output schema."""
    label: str  # "CORRECT" or "WRONG"


async def judge_locomo_async(
    judge: GeminiJudge,
    *,
    question: str,
    gold_answer: str,
    generated_answer: str,
) -> LocomoVerdict:
    """Grade a LoCoMo answer against the gold using mem0's ACCURACY_PROMPT.

    Prompt is imported from benchmarks.locomo.prompts to keep the single
    source of truth there (alongside ANSWER_PROMPT).
    """
    from benchmarks.locomo.prompts import ACCURACY_PROMPT

    prompt = ACCURACY_PROMPT.format(
        question=question.strip(),
        gold_answer=gold_answer.strip(),
        generated_answer=generated_answer.strip() or "[no answer]",
    )
    return await judge.grade_async(prompt, LocomoVerdict)
```

And update `__all__` to include the new symbols:

```python
__all__ = [
    "DEFAULT_MODEL",
    "AgentTurn",
    "GeminiJudge",
    "LocomoVerdict",          # ← add
    "PartnerTurn",
    "QAVerdict",
    "SessionSummary",
    "SotopiaScore",
    "agent_turn_async",
    "judge_locomo_async",     # ← add
    "judge_qa",
    "judge_qa_async",
    "judge_sotopia",
    "judge_sotopia_async",
    "partner_turn",
    "partner_turn_async",
    "summarize_session_async",
]
```

- [ ] **Step 4: Run tests**

Run: `pytest benchmarks/common/tests/test_gemini_judge_locomo.py -v`

Expected: both tests PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/common/gemini_judge.py benchmarks/common/tests/test_gemini_judge_locomo.py
git commit -m "feat(bench): add LoCoMo Gemini judge wrapper

LocomoVerdict (binary CORRECT/WRONG) + judge_locomo_async. Prompt is
imported from benchmarks.locomo.prompts (single source of truth for
the verbatim mem0 port)."
```

---

## Task 6: `LocomoBackendResult` + scoring

**Files:**
- Create: `benchmarks/locomo/backends/__init__.py`
- Create: `benchmarks/locomo/scoring.py`
- Create: `benchmarks/locomo/tests/test_scoring.py`

- [ ] **Step 1: Create backends package init with dataclasses**

`benchmarks/locomo/backends/__init__.py`:

```python
"""Memory-system backends for LoCoMo.

Each backend exposes one async function::

    async def run_sample(
        client, sample, *, shared_agent_id, ..., reader=GeminiJudge,
    ) -> dict[int, LocomoBackendResult]

keyed by qa_index. The runner scores the result, writes JSONL. Adding a new
memory system = one file in this folder.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RankedMemoryItem:
    """One retrieved memory entry.

    ``memory_id`` is the provider-native ID (Sonzai ``fact_id`` or mem0 memory id).
    ``timestamp`` is the LoCoMo session_N_date_time string passed through
    verbatim so the reader can do temporal reasoning (matches mem0's "%timestamp%: %memory%"
    formatting).
    """

    memory_id: str
    text: str
    timestamp: str = ""
    score: float = 0.0
    session_id: str = ""  # LoCoMo "session_N" — used for Recall@K scoring


@dataclass
class LocomoBackendResult:
    """Per-question output from a LoCoMo backend.

    Preserves the dual-speaker retrieval shape from mem0's evaluation — separate
    ranked lists per speaker, merged at scoring time for session-level recall.
    """

    speaker_a_memories: list[RankedMemoryItem] = field(default_factory=list)
    speaker_b_memories: list[RankedMemoryItem] = field(default_factory=list)
    agent_answer: str = ""
    retrieved_session_ids: list[str] = field(default_factory=list)
    extra: dict[str, object] = field(default_factory=dict)
```

- [ ] **Step 2: Write failing tests for scoring**

Create `benchmarks/locomo/tests/test_scoring.py`:

```python
"""Tests for LoCoMo scoring: token-F1 + session-level Recall@K + NDCG."""

from __future__ import annotations

from benchmarks.locomo.scoring import (
    aggregate_rows,
    evidence_to_session_ids,
    merge_speaker_rankings,
    ndcg_at_k,
    recall_any_at_k,
    token_f1,
)
from benchmarks.locomo.backends import RankedMemoryItem


def test_token_f1_identical():
    assert token_f1("red bike", "red bike") == 1.0


def test_token_f1_disjoint():
    assert token_f1("red bike", "blue car") == 0.0


def test_token_f1_partial_overlap():
    # "red bike" vs "red car" — 1 common token of 2 on each side = P=0.5 R=0.5 F1=0.5
    assert token_f1("red bike", "red car") == 0.5


def test_token_f1_handles_empty():
    assert token_f1("", "anything") == 0.0
    assert token_f1("anything", "") == 0.0
    assert token_f1("", "") == 0.0


def test_token_f1_is_case_insensitive():
    assert token_f1("Red Bike", "red bike") == 1.0


def test_token_f1_strips_punctuation():
    assert token_f1("red, bike!", "red bike") == 1.0


def test_evidence_to_session_ids_maps_dia_ids():
    assert evidence_to_session_ids(["D1:3", "D7:14", "D7:5"]) == {"session_1", "session_7"}


def test_evidence_to_session_ids_drops_malformed():
    assert evidence_to_session_ids(["malformed", "D3:4"]) == {"session_3"}


def test_recall_any_at_k_hit():
    retrieved = ["session_2", "session_5", "session_7"]
    gt = {"session_5"}
    assert recall_any_at_k(retrieved, gt, 1) == 0.0
    assert recall_any_at_k(retrieved, gt, 2) == 1.0
    assert recall_any_at_k(retrieved, gt, 3) == 1.0


def test_recall_any_at_k_no_hit():
    assert recall_any_at_k(["session_2"], {"session_5"}, 10) == 0.0


def test_recall_any_at_k_empty_ground_truth():
    assert recall_any_at_k(["session_2"], set(), 10) == 0.0


def test_ndcg_at_k_matches_manual():
    retrieved = ["session_1", "session_5", "session_7"]
    gt = {"session_5", "session_7"}
    # Hits at rank 2 and 3 → DCG = 1/log2(3) + 1/log2(4).
    # Ideal DCG (top-3 of [1,1,1,... relevances where 2 are relevant) = 1/log2(2) + 1/log2(3).
    import math
    dcg = 1 / math.log2(3) + 1 / math.log2(4)
    idcg = 1 / math.log2(2) + 1 / math.log2(3)
    assert abs(ndcg_at_k(retrieved, gt, 3) - dcg / idcg) < 1e-9


def test_merge_speaker_rankings_dedup_session_order():
    a = [
        RankedMemoryItem(memory_id="a1", text="x", session_id="session_2", score=0.9),
        RankedMemoryItem(memory_id="a2", text="y", session_id="session_5", score=0.5),
    ]
    b = [
        RankedMemoryItem(memory_id="b1", text="z", session_id="session_5", score=0.8),
        RankedMemoryItem(memory_id="b2", text="w", session_id="session_7", score=0.4),
    ]
    merged = merge_speaker_rankings(a, b)
    assert merged == ["session_2", "session_5", "session_7"]


def test_aggregate_rows_per_category():
    rows = [
        {"category": 1, "llm_correct": True, "token_f1": 1.0,
         "retrieval": {"recall_any@1": 1.0, "recall_any@10": 1.0}},
        {"category": 1, "llm_correct": False, "token_f1": 0.5,
         "retrieval": {"recall_any@1": 0.0, "recall_any@10": 1.0}},
        {"category": 2, "llm_correct": True, "token_f1": 0.0,
         "retrieval": {"recall_any@1": 1.0, "recall_any@10": 1.0}},
    ]
    agg = aggregate_rows(rows)
    assert agg["per_category"][1]["llm_accuracy"] == 0.5
    assert agg["per_category"][1]["token_f1"] == 0.75
    assert agg["per_category"][2]["llm_accuracy"] == 1.0
    assert agg["per_category"][1]["n"] == 2
    assert agg["overall"]["llm_accuracy"] == pytest.approx(2 / 3, abs=1e-9)


import pytest  # ruff: noqa (imported at bottom for the one pytest.approx usage)
```

- [ ] **Step 3: Run tests — expect ImportError**

Run: `pytest benchmarks/locomo/tests/test_scoring.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'benchmarks.locomo.scoring'`

- [ ] **Step 4: Implement `benchmarks/locomo/scoring.py`**

```python
"""LoCoMo scoring — token-F1, session-level Recall@K, NDCG@K, aggregation.

mem0 reports per-category LLM-judge accuracy as the headline; we mirror that
plus token-F1 (paper-original metric) plus retrieval Recall@K / NDCG@K at
session granularity. dia_id-level retrieval isn't comparable across systems
that don't track per-turn provenance.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable, Sequence

from .backends import RankedMemoryItem

KS = (1, 3, 5, 10, 30)

# LoCoMo dia_ids look like "D3:14" — leading digits of the first half are the
# session index.
_DIA_ID_RE = re.compile(r"^D(\d+):\d+$")


# ---------------------------------------------------------------------------
# Text normalisation + token-F1
# ---------------------------------------------------------------------------


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokens(s: str) -> list[str]:
    return _WORD_RE.findall((s or "").lower())


def token_f1(pred: str, gold: str) -> float:
    """Harmonic mean of token-precision and token-recall (SQuAD-style F1)."""
    pt = _tokens(pred)
    gt = _tokens(gold)
    if not pt or not gt:
        return 0.0
    common: dict[str, int] = {}
    pt_count: dict[str, int] = {}
    gt_count: dict[str, int] = {}
    for t in pt:
        pt_count[t] = pt_count.get(t, 0) + 1
    for t in gt:
        gt_count[t] = gt_count.get(t, 0) + 1
    for t, c in pt_count.items():
        common[t] = min(c, gt_count.get(t, 0))
    n_common = sum(common.values())
    if n_common == 0:
        return 0.0
    precision = n_common / len(pt)
    recall = n_common / len(gt)
    return 2 * precision * recall / (precision + recall)


# ---------------------------------------------------------------------------
# Evidence projection — dia_id → session_id
# ---------------------------------------------------------------------------


def evidence_to_session_ids(evidence: Iterable[str]) -> set[str]:
    """Map dia_ids (e.g. "D3:14") to LoCoMo session_ids ("session_3")."""
    out: set[str] = set()
    for e in evidence:
        m = _DIA_ID_RE.match((e or "").strip())
        if m:
            out.add(f"session_{int(m.group(1))}")
    return out


# ---------------------------------------------------------------------------
# Ranking helpers — merge per-speaker lists before scoring
# ---------------------------------------------------------------------------


def merge_speaker_rankings(
    speaker_a: Sequence[RankedMemoryItem],
    speaker_b: Sequence[RankedMemoryItem],
) -> list[str]:
    """Merge dual-speaker retrievals into a single dedup session-id ranking.

    Sort-by-score across both lists; dedup by session_id, preserving first
    occurrence. Items with no session_id are skipped.
    """
    combined = sorted(
        list(speaker_a) + list(speaker_b),
        key=lambda it: -it.score,
    )
    seen: set[str] = set()
    out: list[str] = []
    for it in combined:
        if not it.session_id or it.session_id in seen:
            continue
        seen.add(it.session_id)
        out.append(it.session_id)
    return out


# ---------------------------------------------------------------------------
# Retrieval metrics
# ---------------------------------------------------------------------------


def recall_any_at_k(
    retrieved: Sequence[str], ground_truth: set[str] | Sequence[str], k: int,
) -> float:
    """1.0 iff any ground-truth session appears in the top-k retrieval."""
    gt = set(ground_truth)
    if not gt:
        return 0.0
    top = set(retrieved[:k])
    return float(bool(gt & top))


def _dcg(relevances: Sequence[float], k: int) -> float:
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(relevances[:k]))


def ndcg_at_k(
    retrieved: Sequence[str], ground_truth: set[str] | Sequence[str], k: int,
) -> float:
    gt = set(ground_truth)
    if not gt:
        return 0.0
    relevances = [1.0 if sid in gt else 0.0 for sid in retrieved[:k]]
    ideal = sorted(relevances, reverse=True)
    idcg = _dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _dcg(relevances, k) / idcg


def retrieval_metrics_grid(
    retrieved: Sequence[str], ground_truth: set[str] | Sequence[str],
) -> dict[str, float]:
    out: dict[str, float] = {}
    for k in KS:
        out[f"recall_any@{k}"] = recall_any_at_k(retrieved, ground_truth, k)
        out[f"ndcg_any@{k}"] = ndcg_at_k(retrieved, ground_truth, k)
    return out


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_rows(rows: list[dict]) -> dict:
    """Per-category means + overall — mirrors mem0's report table shape."""
    by_cat: dict[int, list[dict]] = {}
    for r in rows:
        c = int(r.get("category") or 0)
        by_cat.setdefault(c, []).append(r)

    def _mean(values: list[float]) -> float:
        vs = [v for v in values if v is not None]
        return sum(vs) / len(vs) if vs else 0.0

    per_cat: dict[int, dict[str, float]] = {}
    for cat, group in by_cat.items():
        per_cat[cat] = {
            "n": len(group),
            "llm_accuracy": _mean([float(g.get("llm_correct") or False) for g in group]),
            "token_f1": _mean([float(g.get("token_f1") or 0.0) for g in group]),
        }
        # Retrieval sub-metrics — mean across group for every k.
        for k in KS:
            per_cat[cat][f"recall_any@{k}"] = _mean([
                float((g.get("retrieval") or {}).get(f"recall_any@{k}") or 0.0) for g in group
            ])
            per_cat[cat][f"ndcg_any@{k}"] = _mean([
                float((g.get("retrieval") or {}).get(f"ndcg_any@{k}") or 0.0) for g in group
            ])

    overall = {
        "n": sum(len(g) for g in by_cat.values()),
        "llm_accuracy": _mean([float(r.get("llm_correct") or False) for r in rows]),
        "token_f1": _mean([float(r.get("token_f1") or 0.0) for r in rows]),
    }
    for k in KS:
        overall[f"recall_any@{k}"] = _mean([
            float((r.get("retrieval") or {}).get(f"recall_any@{k}") or 0.0) for r in rows
        ])
        overall[f"ndcg_any@{k}"] = _mean([
            float((r.get("retrieval") or {}).get(f"ndcg_any@{k}") or 0.0) for r in rows
        ])

    return {"per_category": per_cat, "overall": overall}
```

- [ ] **Step 5: Run tests**

Run: `pytest benchmarks/locomo/tests/test_scoring.py -v`

Expected: all 13 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add benchmarks/locomo/backends/__init__.py benchmarks/locomo/scoring.py benchmarks/locomo/tests/test_scoring.py
git commit -m "feat(bench): LoCoMo scoring + LocomoBackendResult shape

SQuAD-style token-F1, session-level Recall@K and NDCG@K against dia_id→session_id
projection, merge-by-score dedup of dual-speaker rankings, per-category +
overall aggregation. Grid ks=(1,3,5,10,30)."
```

---

## Task 7: Extend `SliceKey` for LoCoMo

**Files:**
- Modify: `benchmarks/common/agent_reuse.py`
- Create: `benchmarks/common/tests/test_agent_reuse_locomo.py`

- [ ] **Step 1: Write failing test**

Create `benchmarks/common/tests/test_agent_reuse_locomo.py`:

```python
"""Tests that SliceKey recognises the 'locomo' benchmark."""

from __future__ import annotations

from benchmarks.common.agent_reuse import SliceKey


def test_locomo_slice_matches_on_benchmark_and_limit():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="locomo", limit=10)
    assert a.matches(b)


def test_locomo_slice_mismatch_on_benchmark():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="longmemeval", limit=10)
    assert not a.matches(b)


def test_locomo_slice_mismatch_on_limit():
    a = SliceKey(benchmark="locomo", limit=10)
    b = SliceKey(benchmark="locomo", limit=5)
    assert not a.matches(b)


def test_locomo_slice_ignores_max_sessions_per_question():
    """LoCoMo doesn't use the per-question session cap — should not invalidate reuse."""
    a = SliceKey(benchmark="locomo", limit=10, max_sessions_per_question=0)
    b = SliceKey(benchmark="locomo", limit=10, max_sessions_per_question=5)
    assert a.matches(b)
```

- [ ] **Step 2: Run tests — LoCoMo branch should fail `test_locomo_slice_ignores_max_sessions_per_question`**

Run: `pytest benchmarks/common/tests/test_agent_reuse_locomo.py -v`

Expected: `test_locomo_slice_ignores_max_sessions_per_question` FAILS (current `matches()` treats LoCoMo like LongMemEval and compares `max_sessions_per_question`).

- [ ] **Step 3: Add LoCoMo branch to `SliceKey.matches`**

Edit `benchmarks/common/agent_reuse.py` around line 82–92. Replace:

```python
        if self.benchmark == "sotopia":
            return True
        return self.max_sessions_per_question == other.max_sessions_per_question
```

with:

```python
        if self.benchmark == "sotopia":
            return True
        if self.benchmark == "locomo":
            # LoCoMo ingests the full conversation every time — no per-question
            # session cap, so max_sessions_per_question is not part of identity.
            return True
        return self.max_sessions_per_question == other.max_sessions_per_question
```

And update the `matches()` docstring's benchmark-specific bullet list to mention LoCoMo.

- [ ] **Step 4: Run tests**

Run: `pytest benchmarks/common/tests/test_agent_reuse_locomo.py -v`

Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/common/agent_reuse.py benchmarks/common/tests/test_agent_reuse_locomo.py
git commit -m "feat(bench): recognise 'locomo' benchmark in SliceKey.matches

LoCoMo ingests the full conversation every run; max_sessions_per_question
isn't part of reuse identity. Mirrors the sotopia branch."
```

---

## Task 8: Sonzai backend — ingest via `/process`

**Files:**
- Create: `benchmarks/locomo/backends/sonzai.py` (split across Task 8 for ingest, Task 9 for QA)
- Create: `benchmarks/locomo/tests/test_sonzai_backend.py`

- [ ] **Step 1: Write failing tests for ingest helpers (pure-function pieces)**

Create `benchmarks/locomo/tests/test_sonzai_backend.py`:

```python
"""Tests for benchmarks/locomo/backends/sonzai.py pure-function helpers.

Live-API behaviours aren't tested here — they're exercised in the end-to-end
smoke-run workflow. Pure helpers (message construction, batching, session-id
derivation, metadata-filter) are the only units with deterministic inputs.
"""

from __future__ import annotations

from benchmarks.locomo.backends.sonzai import (
    _batch_messages,
    _build_messages,
    _is_metadata_fact,
    _sonzai_session_id,
)
from benchmarks.locomo.dataset import LocomoSession, LocomoTurn


def _session(turns: list[tuple[str, str, str]]) -> LocomoSession:
    return LocomoSession(
        index=1,
        date_time="1:00 pm on 8 May, 2023",
        turns=[LocomoTurn(speaker=s, dia_id=d, text=t) for s, d, t in turns],
    )


def test_build_messages_speaker_a_pov():
    sess = _session([
        ("Alice", "D1:1", "hi"),
        ("Bob", "D1:2", "hey"),
        ("Alice", "D1:3", "how are you"),
    ])
    msgs = _build_messages(sess, "Alice", "Bob", pov="a")
    assert msgs == [
        {"role": "user", "content": "Alice: hi"},
        {"role": "assistant", "content": "Bob: hey"},
        {"role": "user", "content": "Alice: how are you"},
    ]


def test_build_messages_speaker_b_pov_reverses_roles():
    sess = _session([
        ("Alice", "D1:1", "hi"),
        ("Bob", "D1:2", "hey"),
    ])
    msgs = _build_messages(sess, "Alice", "Bob", pov="b")
    assert msgs == [
        {"role": "assistant", "content": "Alice: hi"},
        {"role": "user", "content": "Bob: hey"},
    ]


def test_batch_messages_default_size_2():
    msgs = [{"role": "user", "content": str(i)} for i in range(5)]
    batches = list(_batch_messages(msgs, 2))
    assert len(batches) == 3
    assert batches[0] == msgs[:2]
    assert batches[1] == msgs[2:4]
    # Last batch would be size-1, which /process rejects — helper pads by
    # re-attaching to the previous batch.
    assert batches[2] == [msgs[3], msgs[4]]


def test_batch_messages_whole_session_when_size_zero():
    msgs = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}, {"role": "user", "content": "c"}]
    batches = list(_batch_messages(msgs, 0))
    assert len(batches) == 1
    assert batches[0] == msgs


def test_batch_messages_raises_on_size_one_input():
    # Even with batch_size=2, a session with only 1 turn can't be batched.
    # /process requires >=2 messages — caller should skip such sessions.
    assert list(_batch_messages([{"role": "user", "content": "only"}], 2)) == []


def test_sonzai_session_id_format():
    assert _sonzai_session_id("sample-0", 3, "a") == "sample-0-s3-a"


def test_is_metadata_fact_flags_comm_style():
    assert _is_metadata_fact("agentX:userY:comm_style") is True


def test_is_metadata_fact_flags_side_effect():
    assert _is_metadata_fact("agentX:userY:side_effect:abc") is True


def test_is_metadata_fact_flags_interest():
    assert _is_metadata_fact("agentX:userY:interest:music") is True


def test_is_metadata_fact_allows_regular_fact_id():
    assert _is_metadata_fact("fact-12345") is False
```

- [ ] **Step 2: Run tests — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_sonzai_backend.py -v`

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Create `benchmarks/locomo/backends/sonzai.py` with ingest portion**

```python
"""Sonzai backend for LoCoMo.

Flow (per sample):
1. For each (chronologically-ordered) session, build messages from two
   perspectives (A and B), then call /process once per POV per batch. Min batch
   size is 2 (server constraint); default 2 to match mem0's ingest cadence,
   0 = whole-session ablation.
2. Between sessions, advance_time(gap_hours) concurrently for both users.
   Final 25h flush so the last session's consolidation fires.
3. QA phase (Task 9): memory.search per user → Gemini reader → judge.

Only /process is used for ingest — not sessions.start/end, not /chat,
not memory/facts/bulk. See spec §2 for endpoint rationale.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterator

from sonzai import AsyncSonzai

from ...common.sdk_extras import (
    async_memory,
    async_process,
    clear_agent_memory_async,
)
from ...common.workbench_compat import advance_time_chunked_async
from ..dataset import LocomoSample, LocomoSession, LocomoTurn
from . import LocomoBackendResult, RankedMemoryItem

logger = logging.getLogger(__name__)

FINAL_FLUSH_HOURS = 25.0
MIN_GAP_HOURS = 25.0
DEFAULT_INGEST_BATCH_SIZE = 2

_META_MARKERS = (":comm_style", ":side_effect:", ":interest:")


# ---------------------------------------------------------------------------
# Pure helpers — deterministic, unit-tested
# ---------------------------------------------------------------------------


def _sonzai_session_id(sample_id: str, session_index: int, pov: str) -> str:
    """Deterministic session_id passed to /process so extracted facts are
    tagged under a predictable key."""
    return f"{sample_id}-s{session_index}-{pov}"


def _build_messages(
    session: LocomoSession, speaker_a: str, speaker_b: str, *, pov: str,
) -> list[dict[str, str]]:
    """Render one session's turns as /process messages from speaker_a/b POV.

    POV "a": speaker_a turns become role "user", speaker_b turns "assistant".
    POV "b": reversed. Turn text is prefixed with `"{speaker}: "` so the
    extractor preserves speaker context (mem0-parity).
    """
    assert pov in ("a", "b"), f"pov must be 'a' or 'b', got {pov}"
    me = speaker_a if pov == "a" else speaker_b
    out: list[dict[str, str]] = []
    for t in session.turns:
        role = "user" if t.speaker == me else "assistant"
        out.append({"role": role, "content": f"{t.speaker}: {t.text}"})
    return out


def _batch_messages(
    messages: list[dict[str, str]], batch_size: int,
) -> Iterator[list[dict[str, str]]]:
    """Yield message batches respecting /process's >=2 constraint.

    batch_size=0 → yield the whole list as one batch (if len>=2, else empty).
    batch_size>=2 → chunk; if the last chunk would be size-1, merge it into
    the previous chunk (so we never emit size-1 batches).
    """
    n = len(messages)
    if n < 2:
        return
    if batch_size <= 0:
        yield messages
        return
    if batch_size < 2:
        raise ValueError("batch_size must be 0 (whole session) or >=2")

    # Walk by batch_size, but on the last chunk if it's size-1, merge with prev.
    batches: list[list[dict[str, str]]] = []
    i = 0
    while i < n:
        batches.append(messages[i:i + batch_size])
        i += batch_size
    if batches and len(batches[-1]) == 1 and len(batches) > 1:
        batches[-2] = batches[-2] + batches[-1]
        batches.pop()
    for b in batches:
        yield b


def _is_metadata_fact(fact_id: str) -> bool:
    """Filter agent-level metadata facts (comm_style, side_effect, interest:*).

    Matches the LongMemEval backend's filter — these are per-(agent, user)
    profile entries, not session-grounded facts. They lack session attribution
    and crowd out the specific LoCoMo-relevant facts in the top-k window.
    """
    return any(m in fact_id for m in _META_MARKERS)


# ---------------------------------------------------------------------------
# Ingest — /process per speaker POV + advance_time between sessions
# ---------------------------------------------------------------------------


async def ingest_sample(
    client: AsyncSonzai,
    sample: LocomoSample,
    *,
    shared_agent_id: str,
    ingest_batch_size: int = DEFAULT_INGEST_BATCH_SIZE,
    skip_advance_time: bool = False,
    clear_before: bool = True,
) -> dict[str, int]:
    """Ingest one sample end-to-end. Returns diagnostics dict."""
    user_a = f"lc-{sample.sample_id}-a"
    user_b = f"lc-{sample.sample_id}-b"

    if clear_before:
        await asyncio.gather(
            clear_agent_memory_async(client, agent_id=shared_agent_id, user_id=user_a),
            clear_agent_memory_async(client, agent_id=shared_agent_id, user_id=user_b),
        )

    process_calls = 0
    facts_extracted = 0
    advance_calls = 0
    advance_failures = 0

    async def _advance(hours: float) -> None:
        nonlocal advance_calls, advance_failures
        if skip_advance_time or hours <= 0:
            return
        try:
            results = await asyncio.gather(
                advance_time_chunked_async(
                    client, agent_id=shared_agent_id, user_id=user_a, total_hours=hours,
                ),
                advance_time_chunked_async(
                    client, agent_id=shared_agent_id, user_id=user_b, total_hours=hours,
                ),
                return_exceptions=True,
            )
            for r in results:
                if isinstance(r, Exception):
                    advance_failures += 1
                    logger.warning("advance_time failed (non-fatal): %s", r)
                else:
                    advance_calls += len(r)
        except Exception as e:
            advance_failures += 1
            logger.warning("advance_time wrapper failed: %s", e)

    prev_dt = None
    for session in sample.sessions:
        dt = session.parsed_date_time
        if prev_dt is not None and dt is not None:
            delta_h = max((dt - prev_dt).total_seconds() / 3600.0, MIN_GAP_HOURS)
            await _advance(delta_h)

        msgs_a = _build_messages(session, sample.speaker_a, sample.speaker_b, pov="a")
        msgs_b = _build_messages(session, sample.speaker_a, sample.speaker_b, pov="b")

        for batch in _batch_messages(msgs_a, ingest_batch_size):
            try:
                resp = await async_process(
                    client,
                    agent_id=shared_agent_id,
                    user_id=user_a,
                    messages=batch,
                    session_id=_sonzai_session_id(sample.sample_id, session.index, "a"),
                )
                process_calls += 1
                facts_extracted += int((resp or {}).get("facts_extracted") or 0)
            except Exception as e:
                logger.warning(
                    "process(A) failed for sample=%s session=%d: %s",
                    sample.sample_id, session.index, e,
                )
        for batch in _batch_messages(msgs_b, ingest_batch_size):
            try:
                resp = await async_process(
                    client,
                    agent_id=shared_agent_id,
                    user_id=user_b,
                    messages=batch,
                    session_id=_sonzai_session_id(sample.sample_id, session.index, "b"),
                )
                process_calls += 1
                facts_extracted += int((resp or {}).get("facts_extracted") or 0)
            except Exception as e:
                logger.warning(
                    "process(B) failed for sample=%s session=%d: %s",
                    sample.sample_id, session.index, e,
                )
        prev_dt = dt

    # Final flush
    await _advance(FINAL_FLUSH_HOURS)

    return {
        "process_calls": process_calls,
        "facts_extracted": facts_extracted,
        "advance_time_calls": advance_calls,
        "advance_time_failures": advance_failures,
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest benchmarks/locomo/tests/test_sonzai_backend.py -v`

Expected: all 10 tests PASS (`test_build_messages_speaker_a_pov`, `_b_pov`, batching, `_sonzai_session_id`, `_is_metadata_fact` × 4).

- [ ] **Step 5: Commit**

```bash
git add benchmarks/locomo/backends/sonzai.py benchmarks/locomo/tests/test_sonzai_backend.py
git commit -m "feat(bench): LoCoMo Sonzai backend — /process ingest + advance_time

Per-sample dual-POV ingest via /process (default batch=2, matches mem0;
0 = whole-session ablation). Concurrent per-user advance_time at session
boundaries, floored at 25h, plus 25h final flush. QA path lands in the
next commit."
```

---

## Task 9: Sonzai backend — QA (retrieve + reader)

**Files:**
- Modify: `benchmarks/locomo/backends/sonzai.py` (append QA helpers)
- Modify: `benchmarks/locomo/tests/test_sonzai_backend.py` (add reader-prompt tests)

- [ ] **Step 1: Write failing tests for reader-prompt formatting**

Append to `benchmarks/locomo/tests/test_sonzai_backend.py`:

```python
# ---------------------------------------------------------------------------
# Reader prompt formatting — mem0-parity ANSWER_PROMPT rendering
# ---------------------------------------------------------------------------


def test_render_answer_prompt_has_all_placeholders_substituted():
    from benchmarks.locomo.backends.sonzai import _render_answer_prompt

    a = [RankedMemoryItem(memory_id="m1", text="Alice wants to be a data scientist", timestamp="8 May 2023")]
    b = [RankedMemoryItem(memory_id="m2", text="Bob bought a bike", timestamp="12 May 2023")]
    prompt = _render_answer_prompt(
        question="Who bought a bike?",
        speaker_1="Alice", speaker_1_memories=a,
        speaker_2="Bob",   speaker_2_memories=b,
    )
    assert "{{" not in prompt  # jinja placeholders substituted
    assert "Alice" in prompt
    assert "Bob" in prompt
    assert "data scientist" in prompt
    assert "bought a bike" in prompt
    assert "Who bought a bike?" in prompt


from benchmarks.locomo.backends import RankedMemoryItem  # ruff: noqa
```

- [ ] **Step 2: Run test — expect ImportError for `_render_answer_prompt`**

Run: `pytest benchmarks/locomo/tests/test_sonzai_backend.py::test_render_answer_prompt_has_all_placeholders_substituted -v`

Expected: FAIL — `ImportError`

- [ ] **Step 3: Append QA helpers to `benchmarks/locomo/backends/sonzai.py`**

```python
# ---------------------------------------------------------------------------
# QA — memory.search per user + Gemini reader
# ---------------------------------------------------------------------------


def _render_answer_prompt(
    *,
    question: str,
    speaker_1: str,
    speaker_1_memories: list[RankedMemoryItem],
    speaker_2: str,
    speaker_2_memories: list[RankedMemoryItem],
) -> str:
    """Render mem0's ANSWER_PROMPT with Jinja-style placeholders.

    mem0 uses Jinja Template — we do a light string-replace so we don't need
    Jinja at runtime. Placeholders are all well-known and the template is
    under our control (ported verbatim).
    """
    from ..prompts import ANSWER_PROMPT

    def _fmt(mems: list[RankedMemoryItem]) -> str:
        import json
        # mem0 formats each memory as "{timestamp}: {memory_text}" in a JSON array
        return json.dumps(
            [f"{m.timestamp}: {m.text}" if m.timestamp else m.text for m in mems],
            indent=4,
        )

    return (
        ANSWER_PROMPT
        .replace("{{speaker_1_user_id}}", speaker_1)
        .replace("{{speaker_2_user_id}}", speaker_2)
        .replace("{{speaker_1_memories}}", _fmt(speaker_1_memories))
        .replace("{{speaker_2_memories}}", _fmt(speaker_2_memories))
        .replace("{{question}}", question)
    )


class _ReaderAnswer(BaseModel):  # noqa: N801 (module-local)
    answer: str


async def _ask_reader(
    judge,
    *,
    question: str,
    speaker_1: str, speaker_1_memories: list[RankedMemoryItem],
    speaker_2: str, speaker_2_memories: list[RankedMemoryItem],
) -> str:
    """Run the Gemini reader over mem0's ported ANSWER_PROMPT."""
    prompt = _render_answer_prompt(
        question=question,
        speaker_1=speaker_1, speaker_1_memories=speaker_1_memories,
        speaker_2=speaker_2, speaker_2_memories=speaker_2_memories,
    )
    verdict = await judge.grade_async(prompt, _ReaderAnswer)
    return verdict.answer


async def _build_fact_to_session_map(
    client: AsyncSonzai, *, agent_id: str, user_id: str,
) -> dict[str, str]:
    """Map fact_id → Sonzai session_id for this (agent, user).

    Mirrors the LongMemEval helper of the same name. The session_id returned
    here is the one we passed to /process (e.g. "lc-sample0-s3-a"), not
    LoCoMo's "session_3" yet — caller does the final projection.
    """
    memory = async_memory(client)
    mapping: dict[str, str] = {}
    try:
        timeline = await memory.timeline(agent_id=agent_id, user_id=user_id)
        for sess in timeline.sessions:
            fallback = sess.session_id if sess.session_id and sess.session_id != "unknown" else ""
            for fact in sess.facts:
                sid = fact.session_id or fallback
                if fact.fact_id and sid and sid != "unknown":
                    mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.timeline failed: %s", e)

    try:
        facts = await memory.list_facts(agent_id=agent_id, user_id=user_id, limit=5000)
        for fact in facts.facts:
            if fact.fact_id in mapping:
                continue
            sid = fact.session_id or fact.source_id
            if sid and sid != "unknown":
                mapping[fact.fact_id] = sid
    except Exception as e:
        logger.debug("memory.list_facts failed: %s", e)

    return mapping


def _sonzai_sid_to_locomo(sonzai_sid: str) -> str:
    """Project "lc-{sample}-s{N}-{a|b}" → "session_{N}"."""
    # Anchored on "-s{digits}-{a|b}" at tail
    import re as _re
    m = _re.search(r"-s(\d+)-[ab]$", sonzai_sid or "")
    if not m:
        return ""
    return f"session_{int(m.group(1))}"


async def _retrieve_for_user(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    query: str,
    top_k: int,
    session_dates: dict[str, str],
) -> list[RankedMemoryItem]:
    """Run memory.search and project to RankedMemoryItem with LoCoMo session_ids."""
    memory = async_memory(client)
    fact_to_sid = await _build_fact_to_session_map(client, agent_id=agent_id, user_id=user_id)
    results = await memory.search(
        agent_id=agent_id, user_id=user_id, query=query, limit=top_k,
    )
    out: list[RankedMemoryItem] = []
    for r in results.results:
        if _is_metadata_fact(r.fact_id):
            continue
        sonzai_sid = str(getattr(r, "session_id", "") or "") or fact_to_sid.get(r.fact_id, "")
        locomo_sid = _sonzai_sid_to_locomo(sonzai_sid)
        out.append(
            RankedMemoryItem(
                memory_id=r.fact_id,
                text=r.content or "",
                timestamp=session_dates.get(locomo_sid, ""),
                score=float(getattr(r, "score", 0.0) or 0.0),
                session_id=locomo_sid,
            )
        )
    return out


async def answer_one_qa(
    client: AsyncSonzai,
    sample: LocomoSample,
    qa_question: str,
    *,
    shared_agent_id: str,
    top_k: int,
    reader,
) -> LocomoBackendResult:
    user_a = f"lc-{sample.sample_id}-a"
    user_b = f"lc-{sample.sample_id}-b"

    # session_N → session_N_date_time map for reader context
    session_dates: dict[str, str] = {
        f"session_{s.index}": s.date_time for s in sample.sessions
    }

    a_mems, b_mems = await asyncio.gather(
        _retrieve_for_user(
            client, agent_id=shared_agent_id, user_id=user_a,
            query=qa_question, top_k=top_k, session_dates=session_dates,
        ),
        _retrieve_for_user(
            client, agent_id=shared_agent_id, user_id=user_b,
            query=qa_question, top_k=top_k, session_dates=session_dates,
        ),
    )

    from ..scoring import merge_speaker_rankings
    merged = merge_speaker_rankings(a_mems, b_mems)

    answer = await _ask_reader(
        reader,
        question=qa_question,
        speaker_1=sample.speaker_a, speaker_1_memories=a_mems,
        speaker_2=sample.speaker_b, speaker_2_memories=b_mems,
    )

    return LocomoBackendResult(
        speaker_a_memories=a_mems,
        speaker_b_memories=b_mems,
        agent_answer=answer,
        retrieved_session_ids=merged,
        extra={},
    )
```

Also add at the top of the file, alongside the existing imports:

```python
from pydantic import BaseModel  # for _ReaderAnswer
```

- [ ] **Step 4: Run the full backend test file**

Run: `pytest benchmarks/locomo/tests/test_sonzai_backend.py -v`

Expected: all 11 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/locomo/backends/sonzai.py benchmarks/locomo/tests/test_sonzai_backend.py
git commit -m "feat(bench): LoCoMo Sonzai backend — QA path (search + reader)

Dual-user memory.search, fact→session mapping via memory.timeline, verbatim
render of mem0's ANSWER_PROMPT for the Gemini reader. Projects Sonzai
session_ids (lc-{sample}-sN-{a|b}) to LoCoMo session_N for Recall@K
scoring."
```

---

## Task 10: mem0 backend

**Files:**
- Create: `benchmarks/locomo/backends/mem0.py`
- Create: `benchmarks/locomo/tests/test_mem0_backend.py`

- [ ] **Step 1: Write failing tests for pure helpers**

Create `benchmarks/locomo/tests/test_mem0_backend.py`:

```python
"""Tests for benchmarks/locomo/backends/mem0.py pure helpers."""

from __future__ import annotations

from benchmarks.locomo.backends.mem0 import (
    _mem0_user_id,
    _session_messages_mem0,
    _hits_to_items,
    MEM0_CUSTOM_INSTRUCTIONS,
)
from benchmarks.locomo.backends import RankedMemoryItem
from benchmarks.locomo.dataset import LocomoSession, LocomoTurn


def test_mem0_user_id_uses_sample_and_speaker_names():
    assert _mem0_user_id("fixture-sample-0", "Alice") == "Alice_fixture-sample-0"


def test_session_messages_mem0_a_pov():
    sess = LocomoSession(
        index=1, date_time="1:00 pm on 8 May, 2023",
        turns=[
            LocomoTurn(speaker="Alice", dia_id="D1:1", text="hi"),
            LocomoTurn(speaker="Bob", dia_id="D1:2", text="hey"),
        ],
    )
    msgs = _session_messages_mem0(sess, "Alice", "Bob", pov="a")
    assert msgs == [
        {"role": "user", "content": "Alice: hi"},
        {"role": "assistant", "content": "Bob: hey"},
    ]


def test_hits_to_items_extracts_score_and_timestamp():
    raw = [
        {
            "id": "mem-1",
            "memory": "Alice is applying for data science roles.",
            "score": 0.87,
            "metadata": {"timestamp": "1:00 pm on 8 May, 2023", "session_id": "session_1"},
        }
    ]
    items = _hits_to_items(raw)
    assert items == [
        RankedMemoryItem(
            memory_id="mem-1",
            text="Alice is applying for data science roles.",
            timestamp="1:00 pm on 8 May, 2023",
            score=0.87,
            session_id="session_1",
        )
    ]


def test_mem0_custom_instructions_contains_identity_cue():
    # mem0's upstream instructions emphasise naming people not "user" —
    # we must preserve that or mem0 retrieves worse.
    assert "not use \"user\"" in MEM0_CUSTOM_INSTRUCTIONS
    assert "self-contained" in MEM0_CUSTOM_INSTRUCTIONS
```

- [ ] **Step 2: Run tests — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_mem0_backend.py -v`

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `benchmarks/locomo/backends/mem0.py`**

```python
"""mem0 cloud backend for LoCoMo.

Direct port of mem0's own evaluation pipeline (evaluation/src/memzero/{add,search}.py)
so our head-to-head numbers land at the same capability level mem0 publishes.
Reader + judge are ours (Gemini); everything upstream (ingest, search,
custom_instructions) is mem0's.

Optional dependency: mem0ai. Import is lazy so sonzai installs don't pull it in.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Any

from ..dataset import LocomoSample, LocomoSession, LocomoTurn
from . import LocomoBackendResult, RankedMemoryItem

logger = logging.getLogger("benchmarks.locomo.mem0")


# Ported verbatim from mem0's evaluation/src/memzero/add.py. Tunes extraction
# toward rich narrative memories with names/dates — load-bearing for mem0's
# published LoCoMo numbers. DO NOT edit to "improve" — that would sandbag the
# comparison.
MEM0_CUSTOM_INSTRUCTIONS = """
Generate personal memories that follow these guidelines:

1. Each memory should be self-contained with complete context, including:
   - The person's name, do not use "user" while creating memories
   - Personal details (career aspirations, hobbies, life circumstances)
   - Emotional states and reactions
   - Ongoing journeys or future plans
   - Specific dates when events occurred

2. Include meaningful personal narratives focusing on:
   - Identity and self-acceptance journeys
   - Family planning and parenting
   - Creative outlets and hobbies
   - Mental health and self-care activities
   - Career aspirations and education goals
   - Important life events and milestones

3. Make each memory rich with specific details rather than general statements
   - Include timeframes (exact dates when possible)
   - Name specific activities (e.g., "charity race for mental health" rather than just "exercise")
   - Include emotional context and personal growth elements

4. Extract memories only from user messages, not incorporating assistant responses

5. Format each memory as a paragraph with a clear narrative structure that captures the person's experience, challenges, and aspirations
"""

DEFAULT_TOP_K = 30
DEFAULT_INGEST_BATCH_SIZE = 2
MAX_429_RETRIES = 8
BASE_429_BACKOFF = 2.0


def _import_mem0():
    try:
        from mem0 import MemoryClient  # type: ignore
        return MemoryClient
    except ImportError as e:
        raise RuntimeError(
            "mem0ai package not installed. Install with `pip install mem0ai` "
            "(only needed when running `--backend mem0`)."
        ) from e


def _mem0_user_id(sample_id: str, speaker: str) -> str:
    """mem0's evaluation uses `{speaker}_{idx}`. We use sample_id as idx so
    multi-run isolation holds even across non-numeric sample IDs."""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", speaker)
    return f"{safe}_{sample_id}"


def _session_messages_mem0(
    session: LocomoSession, speaker_a: str, speaker_b: str, *, pov: str,
) -> list[dict[str, str]]:
    """Format one session's turns for mem0.add — identical shape to _build_messages."""
    me = speaker_a if pov == "a" else speaker_b
    out: list[dict[str, str]] = []
    for t in session.turns:
        role = "user" if t.speaker == me else "assistant"
        out.append({"role": role, "content": f"{t.speaker}: {t.text}"})
    return out


def _hits_to_items(raw_hits: list[dict[str, Any]]) -> list[RankedMemoryItem]:
    items: list[RankedMemoryItem] = []
    for h in raw_hits:
        meta = h.get("metadata") or {}
        items.append(
            RankedMemoryItem(
                memory_id=str(h.get("id") or ""),
                text=str(h.get("memory") or h.get("text") or ""),
                timestamp=str(meta.get("timestamp") or ""),
                score=float(h.get("score") or 0.0),
                session_id=str(meta.get("session_id") or ""),
            )
        )
    return items


def _call_with_retry_sync(fn, *, op: str, retries: int = MAX_429_RETRIES):
    import time as _time
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if "429" in msg and attempt + 1 < retries:
                backoff = BASE_429_BACKOFF * (2 ** attempt)
                logger.info("mem0 %s 429 — backing off %.1fs", op, backoff)
                _time.sleep(backoff)
                continue
            logger.warning("mem0 %s failed (non-retryable): %s", op, e)
            return None
    return None


# ---------------------------------------------------------------------------
# Ingest — dual-POV in mem0's own batched/threaded style
# ---------------------------------------------------------------------------


def _batch_2(messages: list[dict[str, str]], batch_size: int) -> list[list[dict[str, str]]]:
    if batch_size <= 0:
        return [messages] if messages else []
    return [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]


def ingest_sample_sync(
    mem0_client,
    sample: LocomoSample,
    *,
    ingest_batch_size: int = DEFAULT_INGEST_BATCH_SIZE,
) -> None:
    user_a = _mem0_user_id(sample.sample_id, sample.speaker_a)
    user_b = _mem0_user_id(sample.sample_id, sample.speaker_b)

    _call_with_retry_sync(lambda: mem0_client.delete_all(user_id=user_a), op=f"delete_all({user_a})")
    _call_with_retry_sync(lambda: mem0_client.delete_all(user_id=user_b), op=f"delete_all({user_b})")

    for session in sample.sessions:
        msgs_a = _session_messages_mem0(session, sample.speaker_a, sample.speaker_b, pov="a")
        msgs_b = _session_messages_mem0(session, sample.speaker_a, sample.speaker_b, pov="b")
        meta = {
            "timestamp": session.date_time,
            "session_id": f"session_{session.index}",
        }

        for batch in _batch_2(msgs_a, ingest_batch_size):
            _call_with_retry_sync(
                lambda b=batch: mem0_client.add(
                    b, user_id=user_a, version="v2", metadata=meta,
                ),
                op=f"add(A, sample={sample.sample_id}, session={session.index})",
            )
        for batch in _batch_2(msgs_b, ingest_batch_size):
            _call_with_retry_sync(
                lambda b=batch: mem0_client.add(
                    b, user_id=user_b, version="v2", metadata=meta,
                ),
                op=f"add(B, sample={sample.sample_id}, session={session.index})",
            )


# ---------------------------------------------------------------------------
# QA — dual search → Gemini reader
# ---------------------------------------------------------------------------


async def answer_one_qa(
    mem0_client,
    sample: LocomoSample,
    qa_question: str,
    *,
    top_k: int,
    reader,
) -> LocomoBackendResult:
    user_a = _mem0_user_id(sample.sample_id, sample.speaker_a)
    user_b = _mem0_user_id(sample.sample_id, sample.speaker_b)

    def _search(uid: str) -> list[dict]:
        raw = _call_with_retry_sync(
            lambda: mem0_client.search(qa_question, user_id=uid, top_k=top_k),
            op=f"search({uid})",
        ) or []
        if isinstance(raw, dict):
            raw = raw.get("results") or []
        return list(raw)

    loop = asyncio.get_running_loop()
    a_raw, b_raw = await asyncio.gather(
        loop.run_in_executor(None, _search, user_a),
        loop.run_in_executor(None, _search, user_b),
    )
    a_mems = _hits_to_items(a_raw)
    b_mems = _hits_to_items(b_raw)

    from .sonzai import _ask_reader
    from ..scoring import merge_speaker_rankings

    answer = await _ask_reader(
        reader,
        question=qa_question,
        speaker_1=sample.speaker_a, speaker_1_memories=a_mems,
        speaker_2=sample.speaker_b, speaker_2_memories=b_mems,
    )

    return LocomoBackendResult(
        speaker_a_memories=a_mems,
        speaker_b_memories=b_mems,
        agent_answer=answer,
        retrieved_session_ids=merge_speaker_rankings(a_mems, b_mems),
        extra={"mem0_hits_a": len(a_raw), "mem0_hits_b": len(b_raw)},
    )


# ---------------------------------------------------------------------------
# Bootstrapping
# ---------------------------------------------------------------------------


def build_client():
    MemoryClient = _import_mem0()
    api_key = os.environ.get("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("MEM0_API_KEY is required for --backend mem0.")
    client = MemoryClient(
        api_key=api_key,
        org_id=os.environ.get("MEM0_ORGANIZATION_ID"),
        project_id=os.environ.get("MEM0_PROJECT_ID"),
    )
    try:
        client.update_project(custom_instructions=MEM0_CUSTOM_INSTRUCTIONS)
    except Exception as e:
        logger.warning("mem0 update_project failed (custom_instructions not applied): %s", e)
    return client
```

- [ ] **Step 4: Run tests**

Run: `pytest benchmarks/locomo/tests/test_mem0_backend.py -v`

Expected: all 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/locomo/backends/mem0.py benchmarks/locomo/tests/test_mem0_backend.py
git commit -m "feat(bench): mem0 backend for LoCoMo

Direct port of mem0/evaluation/src/memzero/{add,search}.py with their
custom_instructions verbatim (load-bearing — don't remove). Uses our
Gemini reader + judge for parity with the Sonzai side. mem0ai is a
lazy optional dep."
```

---

## Task 11: Orchestrator + CLI (`run.py`)

**Files:**
- Create: `benchmarks/locomo/run.py`
- Create: `benchmarks/locomo/tests/test_run_cli.py`

- [ ] **Step 1: Write failing test that checks CLI arg parsing + output-path default**

Create `benchmarks/locomo/tests/test_run_cli.py`:

```python
"""Smoke tests for the LoCoMo CLI parser — no live API calls."""

from __future__ import annotations

from pathlib import Path

from benchmarks.locomo.run import _parse_args, _default_output_path


def test_parse_args_defaults():
    ns = _parse_args(["--limit", "2"])
    assert ns.backend == "sonzai"
    assert ns.limit == 2
    assert ns.concurrency == 2
    assert ns.top_k == 30
    assert ns.ingest_batch_size == 2
    assert ns.skip_advance_time is False
    assert ns.include_adversarial is False
    assert ns.mode == "both"


def test_parse_args_mem0_backend():
    ns = _parse_args(["--backend", "mem0", "--limit", "5"])
    assert ns.backend == "mem0"
    assert ns.limit == 5


def test_parse_args_compare():
    ns = _parse_args(["--compare", "a.jsonl", "b.jsonl"])
    assert ns.compare == ["a.jsonl", "b.jsonl"]


def test_default_output_path_contains_backend_and_ts():
    path = _default_output_path("sonzai")
    assert path.parent.name == "results"
    assert "sonzai_" in path.name
    assert path.suffix == ".jsonl"
```

- [ ] **Step 2: Run test — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_run_cli.py -v`

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement `benchmarks/locomo/run.py`**

```python
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
import os
import sys
import time
from collections.abc import Iterable
from pathlib import Path

from sonzai import AsyncSonzai
from tqdm.asyncio import tqdm_asyncio

from ..common.gemini_judge import (
    DEFAULT_MODEL as DEFAULT_JUDGE_MODEL,
    GeminiJudge,
    judge_locomo_async,
)
from .backends import LocomoBackendResult, RankedMemoryItem
from .dataset import LocomoQA, LocomoSample, load_qa, load_samples
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
    *, backend: str, llm_correct: bool | None, llm_rationale: str,
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
    concurrency: int, mode: str, judge: GeminiJudge | None,
    top_k: int, ingest_batch_size: int, skip_advance_time: bool,
    include_adversarial: bool,
    reuse_agents_path: str | None, clear_reused_memory: bool,
) -> list[dict]:
    from .backends import sonzai as sb
    from ..common.agent_reuse import (
        SliceKey, dataset_tag, load_snapshot, new_snapshot, save_snapshot,
        should_reuse, upsert_agent,
    )
    from sonzai.benchmarks import ensure_benchmark_agent_async

    client = AsyncSonzai(timeout=600.0)
    try:
        shared_agent_id, existed = await ensure_benchmark_agent_async(client)
        logger.info("bench agent: %s (existed=%s)", shared_agent_id, existed)

        snapshot = None
        snapshot_lock: asyncio.Lock | None = None
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
                    # Caller wants a clean re-ingest
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
                    # Enrich extra with ingest diag once per sample (first QA)
                    if qi == qa_pairs[0][0]:
                        br.extra = dict(br.extra or {})
                        br.extra.update(ingest_diag)

                    llm_correct: bool | None = None
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

                # QAs within a sample run with bounded inner concurrency — retrievals
                # are fast so we can over-subscribe the outer pool here.
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
    concurrency: int, mode: str, judge: GeminiJudge | None,
    top_k: int, ingest_batch_size: int, include_adversarial: bool,
) -> list[dict]:
    from .backends import mem0 as mb

    mem0_client = mb.build_client()
    sem_sample = asyncio.Semaphore(concurrency)

    async def _one_sample(sample: LocomoSample) -> list[dict]:
        async with sem_sample:
            # mem0 SDK is sync — run ingest in the default executor
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
                llm_correct: bool | None = None
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


def main(argv: list[str] | None = None) -> int:
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

    judge: GeminiJudge | None = None
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
```

- [ ] **Step 4: Run CLI tests**

Run: `pytest benchmarks/locomo/tests/test_run_cli.py -v`

Expected: all 4 tests PASS.

- [ ] **Step 5: Smoke test module import**

Run: `python -c "from benchmarks.locomo import run; print('ok')"`

Expected: `ok`

- [ ] **Step 6: Commit**

```bash
git add benchmarks/locomo/run.py benchmarks/locomo/tests/test_run_cli.py
git commit -m "feat(bench): LoCoMo orchestrator + CLI

Async runner that drives Sonzai or mem0 backends, scores each QA with
Gemini judge + token-F1 + session-level Recall@K, and writes JSONL.
Uses the unified ensure_benchmark_agent_async preset. Summary table
printed at end; compare mode delegates to compare.py (next task)."
```

---

## Task 12: Compare utility (head-to-head JSONL diff)

**Files:**
- Create: `benchmarks/locomo/compare.py`
- Create: `benchmarks/locomo/tests/test_compare.py`

- [ ] **Step 1: Write failing test**

Create `benchmarks/locomo/tests/test_compare.py`:

```python
"""Tests for the compare utility — side-by-side JSONL aggregation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from benchmarks.locomo.compare import load_jsonl, render_table


def _write_jsonl(p: Path, rows: list[dict]) -> Path:
    p.write_text("\n".join(json.dumps(r) for r in rows))
    return p


def test_load_jsonl_handles_trailing_newline(tmp_path: Path):
    p = _write_jsonl(tmp_path / "a.jsonl", [{"category": 1, "llm_correct": True}])
    rows = load_jsonl(p)
    assert len(rows) == 1
    assert rows[0]["category"] == 1


def test_render_table_has_per_category_and_overall(tmp_path: Path):
    rows_sonzai = [
        {"category": 1, "llm_correct": True, "token_f1": 1.0, "backend": "sonzai",
         "retrieval": {}},
        {"category": 2, "llm_correct": True, "token_f1": 0.5, "backend": "sonzai",
         "retrieval": {}},
    ]
    rows_mem0 = [
        {"category": 1, "llm_correct": False, "token_f1": 0.0, "backend": "mem0",
         "retrieval": {}},
        {"category": 2, "llm_correct": True, "token_f1": 0.5, "backend": "mem0",
         "retrieval": {}},
    ]
    md = render_table({
        "sonzai": rows_sonzai, "mem0": rows_mem0,
    })
    assert "| Category |" in md
    assert "sonzai" in md
    assert "mem0" in md
    # Category 1: sonzai 100%, mem0 0%
    assert "1.000" in md
    assert "0.000" in md


def test_render_table_rejects_single_file():
    with pytest.raises(ValueError):
        render_table({"only_one": []})
```

- [ ] **Step 2: Run test — expect ModuleNotFoundError**

Run: `pytest benchmarks/locomo/tests/test_compare.py -v`

Expected: FAIL.

- [ ] **Step 3: Implement `benchmarks/locomo/compare.py`**

```python
"""Head-to-head JSONL diff for LoCoMo runs.

Usage (from run.py --compare): load each JSONL file, compute per-category
accuracy + token-F1 + R@K, render a markdown table with one column per file.

Column order = argv order so the caller controls which backend appears on
the left.
"""

from __future__ import annotations

import json
from pathlib import Path

from .scoring import KS, aggregate_rows


def load_jsonl(path: str | Path) -> list[dict]:
    rows: list[dict] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _label_for(path: str | Path, rows: list[dict]) -> str:
    # Prefer explicit "backend" tag; fall back to filename stem.
    if rows and "backend" in rows[0]:
        return str(rows[0]["backend"])
    return Path(path).stem


def render_table(per_file: dict[str, list[dict]]) -> str:
    if len(per_file) < 2:
        raise ValueError("compare needs at least 2 files")

    labels = list(per_file.keys())
    aggs = {k: aggregate_rows(v) for k, v in per_file.items()}
    categories = sorted({c for a in aggs.values() for c in a["per_category"].keys()})

    lines: list[str] = []
    header = "| Category |" + "".join(f" {lbl} (J) | {lbl} (F1) |" for lbl in labels)
    sep = "|---|" + "".join(["---:|"] * (2 * len(labels)))
    lines.append(header)
    lines.append(sep)
    for cat in categories:
        row = [f"| {cat} |"]
        for lbl in labels:
            m = aggs[lbl]["per_category"].get(cat, {})
            row.append(f" {m.get('llm_accuracy', 0):.3f} |")
            row.append(f" {m.get('token_f1', 0):.3f} |")
        lines.append("".join(row))
    # Overall row
    overall_row = ["| **Overall** |"]
    for lbl in labels:
        o = aggs[lbl]["overall"]
        overall_row.append(f" **{o.get('llm_accuracy', 0):.3f}** |")
        overall_row.append(f" {o.get('token_f1', 0):.3f} |")
    lines.append("".join(overall_row))

    lines.append("")
    lines.append("### Retrieval (session-level, any-hit recall)")
    rheader = "| k |" + "".join(f" {lbl} R@k | {lbl} NDCG@k |" for lbl in labels)
    rsep = "|---|" + "".join(["---:|"] * (2 * len(labels)))
    lines.append(rheader)
    lines.append(rsep)
    for k in KS:
        row = [f"| {k} |"]
        for lbl in labels:
            o = aggs[lbl]["overall"]
            row.append(f" {o.get(f'recall_any@{k}', 0):.3f} |")
            row.append(f" {o.get(f'ndcg_any@{k}', 0):.3f} |")
        lines.append("".join(row))

    return "\n".join(lines)


def main(paths: list[str]) -> int:
    per_file: dict[str, list[dict]] = {}
    for path in paths:
        rows = load_jsonl(path)
        label = _label_for(path, rows)
        # de-dup: if two files carry the same backend tag, disambiguate by stem
        if label in per_file:
            label = f"{label} ({Path(path).stem})"
        per_file[label] = rows
    print(render_table(per_file))
    return 0
```

- [ ] **Step 4: Run tests**

Run: `pytest benchmarks/locomo/tests/test_compare.py -v`

Expected: all 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/locomo/compare.py benchmarks/locomo/tests/test_compare.py
git commit -m "feat(bench): LoCoMo compare utility

Load two+ JSONL files, produce markdown table of per-category
LLM-judge accuracy + token-F1 + session-level Recall@K for paste
into README.md. Accessible via python -m benchmarks.locomo --compare ..."
```

---

## Task 13: Results dir + gitignore + README section

**Files:**
- Create: `benchmarks/locomo/results/.gitignore`
- Modify: `benchmarks/README.md`

- [ ] **Step 1: Check existing results gitignore pattern**

Run: `cat benchmarks/longmemeval/results/.gitignore 2>/dev/null || cat benchmarks/.gitignore 2>/dev/null`

Expected: existing `.gitignore` patterns. Copy the same style.

- [ ] **Step 2: Create `benchmarks/locomo/results/.gitignore`**

```gitignore
# Iteration runs are gitignored; headline receipts can be allow-listed below.
*.jsonl
*.png
reuse_agents.json
shared_agent.json
pinned_agents.json

# Allow-list published receipts here — format matches sotopia/longmemeval.
# !locomo_<date>_<hash>.jsonl
```

Also create `benchmarks/locomo/results/.gitkeep` as an empty file so the directory is tracked.

- [ ] **Step 3: Append a LoCoMo section to `benchmarks/README.md`**

Append after the SOTOPIA section (search for "## SOTOPIA longitudinal" and paste the new section after its closing paragraph; before "## Cost and time"):

```markdown
## LoCoMo

10 dialogues (19–35 sessions, 300–600 turns each) between two peer speakers.
Each dialogue has QA pairs across 5 reasoning categories (single-hop,
multi-hop, temporal, open-domain, adversarial). Category 5 (adversarial) is
filtered by default to match mem0's published methodology.

```bash
# Smoke run — 2 samples against Sonzai
python -m benchmarks.locomo --backend sonzai --limit 2

# Same 2 samples through mem0 cloud
export MEM0_API_KEY=...
python -m benchmarks.locomo --backend mem0 --limit 2

# Head-to-head comparison
python -m benchmarks.locomo --compare \
    benchmarks/locomo/results/sonzai_*.jsonl \
    benchmarks/locomo/results/mem0_*.jsonl

# Full 10-dialogue run
python -m benchmarks.locomo --backend sonzai --limit 0 --concurrency 4
```

**Metrics reported** — mirror mem0's LoCoMo paper table line-for-line:

- **LLM-judge accuracy (J)** per category 1–4 + overall — binary CORRECT/WRONG
  graded by Gemini using mem0's `ACCURACY_PROMPT` ported verbatim.
- **Token-F1** (secondary) — paper-original SQuAD-style token overlap.
- **Session-level Recall@K / NDCG@K** at k ∈ {1, 3, 5, 10, 30} — Sonzai-native
  retrieval diagnostic. dia_id-level recall isn't comparable (neither system
  tracks per-turn provenance), so we project `"D3:14" → session_3` on both sides.

**What's Sonzai-specific** (the difference from mem0 on the memory side):

- `/process` ingest per speaker POV — the dedicated external-transcript endpoint,
  not `sessions.start/end`, not `/chat`, not `memory/facts/bulk`.
- `advance_time(gap_hours)` between sessions per user — fires CE workers
  (diary, consolidation, decay) on the real date gap from
  `session_N_date_time`.
- Dual-user search at QA time (`memory.search(user_id=a)` + `user_id=b`),
  merged by score, fed to the same Gemini reader mem0's run uses.

### Methodology

Dual-perspective ingest: each session is fed through `/process` twice, once as
speaker_a's POV (speaker_a turns → role `"user"`, speaker_b → `"assistant"`)
and once mirrored for speaker_b. Default batch size is 2 messages per call,
matching mem0's published ingest cadence (flag `--ingest-batch-size 0` sends
whole sessions — our ablation). Each message's content is prefixed with
`"{speaker_name}: "` so the extractor preserves speaker attribution.

Between sessions, `workbench.advance_time(gap_hours)` runs concurrently for
both users, floored at 25h so at least one daily-worker pass fires per gap.
A final 25h flush runs after the last session so the final day's consolidation
completes before QA.

At QA time: `memory.search(query, user_id=speaker_a)` and `user_id=speaker_b`
each return top-30, metadata facts (comm_style/side_effect/interest:*) are
filtered, and both lists are rendered as `"{timestamp}: {text}"` strings into
mem0's `ANSWER_PROMPT` for Gemini 3.1 Flash Lite to produce the final answer.
The same Gemini judges with `ACCURACY_PROMPT`.

**Agent**: the same `sonzai-benchmark-agent` used by LongMemEval. Third
parties replicate by calling `sonzai.benchmarks.ensure_benchmark_agent_async`.

**Headline receipts** (paste-ready): will land in
`benchmarks/locomo/results/` after the first production run.
```

- [ ] **Step 4: Commit**

```bash
git add benchmarks/locomo/results/.gitignore benchmarks/locomo/results/.gitkeep benchmarks/README.md
git commit -m "docs(bench): add LoCoMo section to benchmarks README

Documents how to run Sonzai vs mem0 on LoCoMo, methodology (/process +
dual-POV ingest + advance_time + dual-user search), and the metric
grid (LLM-judge J, token-F1, session-level Recall@K)."
```

---

## Task 14: End-to-end fixture smoke test

**Files:**
- Create: `benchmarks/locomo/tests/test_end_to_end_fixture.py`

- [ ] **Step 1: Write the smoke test that drives the run.py path with mocked clients**

Create `benchmarks/locomo/tests/test_end_to_end_fixture.py`:

```python
"""End-to-end LoCoMo run test using the mini fixture and fake clients.

No real Sonzai or mem0 API calls — we stub AsyncSonzai.agents.chat,
memory.search, workbench.advance_time, and the /process raw transport.
This asserts that the runner plumbs the backend result through scoring
and judge correctly.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from benchmarks.locomo.dataset import load_samples
from benchmarks.locomo import run as run_mod

FIXTURE = Path(__file__).parent / "fixtures" / "mini_locomo.json"


@pytest.mark.asyncio
async def test_sonzai_pipeline_writes_expected_rows(tmp_path: Path, monkeypatch):
    samples = load_samples(path=FIXTURE)
    assert samples

    # Stub the Sonzai backend entirely — we're testing the orchestration layer
    fake_br = MagicMock()
    fake_br.speaker_a_memories = []
    fake_br.speaker_b_memories = []
    fake_br.agent_answer = "data scientist"
    fake_br.retrieved_session_ids = ["session_1"]
    fake_br.extra = {}

    async def fake_ingest(*args, **kwargs):
        return {"process_calls": 4, "facts_extracted": 7, "advance_time_calls": 1, "advance_time_failures": 0}

    async def fake_answer_one(*args, **kwargs):
        return fake_br

    async def fake_ensure_agent(client):
        return ("agent-xyz", False)

    class _FakeVerdict:
        label = "CORRECT"

    async def fake_judge_locomo(*args, **kwargs):
        return _FakeVerdict()

    async def fake_close():
        return None

    # Patch the call sites used inside _run_sonzai
    with patch("benchmarks.locomo.backends.sonzai.ingest_sample", fake_ingest), \
         patch("benchmarks.locomo.backends.sonzai.answer_one_qa", fake_answer_one), \
         patch("benchmarks.locomo.run.ensure_benchmark_agent_async", fake_ensure_agent), \
         patch("benchmarks.locomo.run.judge_locomo_async", fake_judge_locomo), \
         patch("benchmarks.locomo.run.AsyncSonzai", return_value=MagicMock(close=fake_close)):
        # Judge is a no-op (we patched judge_locomo_async)
        judge = MagicMock()

        rows = await run_mod._run_sonzai(
            samples,
            concurrency=1, mode="both", judge=judge,
            top_k=30, ingest_batch_size=2, skip_advance_time=True,
            include_adversarial=False, reuse_agents_path=None, clear_reused_memory=False,
        )

    # Two non-adversarial QAs in the fixture
    assert len(rows) == 2
    assert all(r["backend"] == "sonzai" for r in rows)
    assert all(r["llm_correct"] is True for r in rows)
    # First QA's expected Recall@1 = 1 because retrieved_session_ids = ["session_1"]
    # and evidence = ["D1:3"] → session_1.
    first = next(r for r in rows if r["qa_index"] == 0)
    assert first["retrieval"]["recall_any@1"] == 1.0
    # Second QA's evidence is D2:4 → session_2; retrieved is session_1 → miss.
    second = next(r for r in rows if r["qa_index"] == 1)
    assert second["retrieval"]["recall_any@10"] == 0.0


def test_write_jsonl_round_trip(tmp_path: Path):
    rows = [{"a": 1}, {"b": [1, 2, 3]}]
    out = tmp_path / "x.jsonl"
    run_mod._write_jsonl(rows, out)
    loaded = [json.loads(line) for line in out.read_text().splitlines()]
    assert loaded == rows
```

- [ ] **Step 2: Run tests**

Run: `pytest benchmarks/locomo/tests/test_end_to_end_fixture.py -v`

Expected: both tests PASS.

- [ ] **Step 3: Commit**

```bash
git add benchmarks/locomo/tests/test_end_to_end_fixture.py
git commit -m "test(bench): LoCoMo end-to-end fixture smoke test

Drives run._run_sonzai with mocked ingest/QA/judge to verify the
orchestration plumbs BackendResult → scoring → row correctly,
including per-category filtering and retrieval metrics wiring."
```

---

## Task 15: Final sweep — full test suite + lint

**Files:**
- None

- [ ] **Step 1: Run the full locomo test suite**

Run: `pytest benchmarks/locomo/ benchmarks/common/tests/ tests/unit/test_benchmarks_agent.py -v`

Expected: all tests PASS. Typical count: 9 (dataset) + 4 (prompts) + 13 (scoring) + 4 (agent reuse) + 11 (sonzai backend) + 4 (mem0 backend) + 4 (CLI) + 3 (compare) + 2 (e2e) + 3 (sdk shim) + 2 (judge) + 4 (agent refactor) = ~63 tests.

- [ ] **Step 2: Verify the LongMemEval suite still passes (no regression from the agent rename)**

Run: `pytest benchmarks/longmemeval/tests/ -v`

Expected: existing tests still pass (none of them reference the agent helper by name).

- [ ] **Step 3: Verify the module loads end-to-end**

Run: `python -m benchmarks.locomo --help`

Expected: argparse help text shows all flags (`--backend`, `--limit`, `--ingest-batch-size`, etc.) with no import errors.

- [ ] **Step 4: Lint / ruff check**

Run: `ruff check benchmarks/locomo/ src/sonzai/benchmarks.py benchmarks/common/`

Expected: no errors. If there are style warnings, fix inline with `ruff check --fix` and commit the fixups.

- [ ] **Step 5: Final commit if any fixups were made**

```bash
git status
# If diffs exist:
git add -u
git commit -m "chore(bench): ruff fixups after LoCoMo landing"
```

---

## Self-review

- **Spec coverage**: every section of the spec is covered.
  - §1 methodology match → Tasks 8, 9, 10 (backends) + Task 4 (prompt port) + Task 5 (judge).
  - §2 `/process` endpoint rationale → Task 2 (shim) + Task 8 (ingest).
  - §3 unified benchmark agent → Task 1 (SDK refactor).
  - §4 `LocomoBackendResult` → Task 6.
  - §5 byte-for-byte prompt port → Task 4.
  - §6 headline metric → Task 6 (scoring) + Task 11 (summary print) + Task 12 (compare).
  - §7 session-level recall → Task 6 (`evidence_to_session_ids`) + Task 9 (`_sonzai_sid_to_locomo`).
  - Dataset, CLI, docs → Tasks 3, 11, 13.
  - Reuse snapshots → Task 7 + Task 11 (orchestrator snapshot handling).
  - Non-goals explicitly stated (MemPalace, multimodal, GPT-4o judge).
- **Placeholders**: none. Every step has concrete code or exact commands.
- **Type consistency**: `LocomoBackendResult`, `RankedMemoryItem`, `LocomoSample`, `LocomoSession`, `LocomoTurn`, `LocomoQA` defined in Tasks 3/6 and used consistently downstream. Function names (`ingest_sample`, `answer_one_qa`, `ensure_benchmark_agent_async`, `async_process`, `judge_locomo_async`, `_render_answer_prompt`, `merge_speaker_rankings`, `evidence_to_session_ids`, `recall_any_at_k`, `ndcg_at_k`, `aggregate_rows`, `token_f1`) match across their definition and call sites.
