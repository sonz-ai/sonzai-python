# ConvoMem benchmark design

**Status:** design approved, ready for implementation plan
**Date:** 2026-04-24
**Target:** add `benchmarks/convomem/` — a Sonzai-flavored runner for the
[Salesforce ConvoMem benchmark](https://github.com/SalesforceAIResearch/ConvoMem),
comparable line-for-line with
[Supermemory MemoryBench](https://github.com/supermemoryai/memorybench)'s
#1-on-ConvoMem numbers.

## Motivation

`benchmarks/longmemeval/` and `benchmarks/sotopia/` already cover retrieval-heavy
and longitudinal-social dimensions. ConvoMem fills a third axis:
**conversation-level memory across 6 evidence categories** (user facts,
assistant facts, changing facts, abstention, preferences, implicit
connections). Supermemory currently leads ConvoMem's public leaderboard; adding
a first-party Sonzai runner lets us reproduce their slice exactly and publish
comparable numbers.

## Key decisions (locked with the user)

### 1. Dataset slice — match Supermemory exactly

Supermemory's `memorybench` downloads one `batched_000.json` per
`(category, subfolder)` from the HuggingFace dataset root
`core_benchmark/pre_mixed_testcases/`. Category → subfolder:

| Category | Subfolder |
|---|---|
| `user_evidence` | `1_evidence` |
| `assistant_facts_evidence` | `1_evidence` |
| `changing_evidence` | `2_evidence` |
| `abstention_evidence` | `1_evidence` |
| `preference_evidence` | `1_evidence` |
| `implicit_connection_evidence` | `1_evidence` |

We mirror this map. Running the full 75k grid and other `evidence_count`
subfolders is a future expansion; the default loader reproduces the exact
question set Supermemory reports on.

### 2. Ingest cadence — `sessions.end` per conversation + one `advance_time(168h)` flush

ConvoMem has no dates. Options considered:
- **A.** `advance_time(25h)` between every conversation-session. Too slow —
  advance_time takes 1–5 minutes per call.
- **B.** No gap between, one big flush at end. ✅ chosen.
- **C.** No `advance_time` at all. Rejected as default; exposed behind
  `--skip-advance-time`.

Platform code confirms the minimum viable flow:
- `services/contextengine/session.go` — `OnSessionEnd` already extracts facts,
  writes session summaries, updates relationship state, and fires Fibonacci
  breakthroughs per session.
- `services/platform/api/internal/delivery/http/workbench_advance_time.go:451` —
  weekly workers are gated server-side on `sessionCount % 7 == 0`. One
  `advance_time(168h)` call after N sessions catches both the daily
  consolidation path and the weekly gate.

Net cost: O(N) `sessions.end` (fast, wait=True) + one `advance_time` (~3–5
minutes, once) per question. Supermemory's flow is O(N) ingest + index wait —
roughly equivalent wall time.

### 3. Headline metric — QA accuracy judged by Gemini, per category + MemScore

ConvoMem publishes QA accuracy per evidence category; Supermemory reports
MemScore (`accuracy% / avg_latency_ms / avg_context_tokens`). We report both
so the comparison table drops straight into the README.

Retrieval-only metrics (Recall@K / NDCG@K) are **not** reported — ConvoMem's
ground truth is message-level, not session-level, so Recall@K against
conversation IDs would be misleading. Facts retrieved are surfaced in
`extra` as a diagnostic signal only.

### 4. No new `benchmarks/common/` code

Reuses `gemini_judge.GeminiJudge`, `workbench_compat.advance_time_chunked_async`,
`agent_reuse` for `--reuse-agents`, `dataset_cache.ensure_file`, and
`sdk_extras.async_sessions` / `async_memory` / `clear_agent_memory_async`. The
SDK preset `ensure_convomem_agent_async` is added as a sibling to
`ensure_longmemeval_agent_async`.

## Architecture

```
benchmarks/
├── convomem/
│   ├── __init__.py
│   ├── __main__.py            python -m benchmarks.convomem
│   ├── run.py                 orchestrator (async, bounded concurrency)
│   ├── dataset.py             HF loader for pre_mixed_testcases/*/batched_000.json
│   ├── scoring.py             QA accuracy aggregation by evidence category + MemScore
│   ├── backends/
│   │   ├── __init__.py        BackendResult (QA-focused)
│   │   └── sonzai.py          sessions.end-per-conversation + single advance_time flush
│   ├── tests/
│   │   ├── test_dataset.py    fixture-based loader tests
│   │   └── test_scoring.py    abstention judge + MemScore aggregation
│   └── results/               JSONL outputs (iteration runs gitignored)
```

## Components

### `dataset.py`

**Source URLs** (one per category, all `batched_000.json`):

```python
HF_BASE = "https://huggingface.co/datasets/Salesforce/ConvoMem/resolve/main/core_benchmark/pre_mixed_testcases"

CATEGORY_SUBFOLDERS = {
    "user_evidence":               "1_evidence",
    "assistant_facts_evidence":    "1_evidence",
    "changing_evidence":           "2_evidence",
    "abstention_evidence":         "1_evidence",
    "preference_evidence":         "1_evidence",
    "implicit_connection_evidence":"1_evidence",
}
```

**Dataclasses:**

```python
@dataclass
class Message:
    role: str        # "user" | "assistant" — lowercased from dataset's "User"/"Assistant"
    content: str

@dataclass
class Conversation:
    conversation_id: str    # "{question_id}-conv-{i}"
    messages: list[Message]

@dataclass
class EvidenceMessage:
    speaker: str     # "User" | "Assistant"
    text: str

@dataclass
class ConvoMemQuestion:
    question_id: str        # "convomem-{category}-{index}"
    question_type: str      # evidence category — one of the six
    question: str
    answer: str
    evidence_messages: list[EvidenceMessage]
    conversations: list[Conversation]
```

**API:**

```python
def load_questions(
    *,
    limit: int = 0,
    categories: list[str] | None = None,
    cache_dir: Path | None = None,
) -> list[ConvoMemQuestion]: ...
```

- `limit=0` returns everything. Otherwise returns a proportional
  cross-category slice so smoke runs hit all six categories (e.g.
  `limit=60` → 10 from each of 6 categories).
- `categories=None` loads all six; explicit list filters.
- Downloads lazily via `common.dataset_cache.ensure_file`, one JSON file per
  category, stored under `~/.cache/sonzai-bench/convomem/`.

### `backends/__init__.py`

```python
@dataclass
class BackendResult:
    agent_answer: str = ""
    ranked_fact_texts: list[str] = field(default_factory=list)  # diagnostic
    extra: dict[str, object] = field(default_factory=dict)
```

No `ranked_items` / `ranked_session_ids` — ConvoMem doesn't score retrieval.

### `backends/sonzai.py`

**Single public entrypoint** mirroring longmemeval:

```python
async def run_question(
    client: AsyncSonzai,
    question: ConvoMemQuestion,
    *,
    include_qa: bool = True,
    skip_advance_time: bool = False,
    existing_agent_id: str,
    existing_user_id: str | None = None,
    skip_ingest: bool = False,
    clear_memory_before_reuse: bool = False,
    flush_hours: float = 168.0,
    retrieval_limit: int = 50,
) -> BackendResult: ...
```

**Flow per question:**

1. `user_id = existing_user_id or f"convomem-user-{question.question_id[:16]}"`
2. `agent_id = existing_agent_id` (shared agent model, same as longmemeval).
3. If not `skip_ingest` and not `clear_memory_before_reuse=False`:
   `clear_agent_memory_async(agent_id, user_id)` — idempotent reruns.
4. **Ingest loop** (O(N) `sessions.end` with `wait=True`, no gap between):

   ```python
   for i, conv in enumerate(question.conversations):
       sid = f"{question.question_id}-conv-{i}"
       await sessions.start(agent_id=agent_id, user_id=user_id, session_id=sid)
       await sessions.end(
           agent_id=agent_id, user_id=user_id, session_id=sid,
           total_messages=len(conv.messages),
           messages=[{"role": m.role, "content": m.content} for m in conv.messages],
           wait=True,
       )
   ```

5. **Single flush** (unless `skip_advance_time`):
   `await advance_time_chunked_async(client, agent_id, user_id, total_hours=flush_hours)`
   Default 168h = 7 simulated days. Catches daily consolidation plus the
   `sessionCount % 7 == 0` weekly gate.
6. **Retrieval** (diagnostic): `memory.search(agent_id, user_id, question.question, limit=retrieval_limit)`
   → `ranked_fact_texts`. Filter agent-metadata fact_ids (comm_style,
   side_effect, interest:*) using the same filter longmemeval applies.
7. **QA** (headline): `_ask_question(agent_id, user_id, question.question)`
   — the same SSE-stream-consuming helper longmemeval uses so we capture
   `context_ready.loaded_facts` for diagnostics.
8. **Never** delete the shared agent.

**`extra` dict:**

```python
{
  "agent_id": str,
  "user_id": str,
  "reused_agent": bool,
  "conversations_ingested": int,
  "advance_time_calls": int,
  "advance_time_failures": int,
  "consolidation_events": int,
  "skip_advance_time": bool,
  "facts_retrieved": int,
  "facts_stored": int,
  "facts_sample": list[str],  # first 5 stored facts
  # Chat-path SSE diagnostics (when captured):
  "chat_loaded_facts_count": int,
  "chat_loaded_facts_preview": list[str],
  "chat_loaded_facts_texts": list[str],
  "chat_build_duration_ms": int,
}
```

### `scoring.py`

**QA judging:**

- Normal questions: reuse `common.gemini_judge.judge_qa_async` unchanged.
- Abstention questions (`question_type == "abstention_evidence"`): new
  `judge_abstention_async` helper. Correct iff agent_answer expresses
  non-answer (e.g. "I don't know", "not mentioned in our conversation",
  "no information about", "can't recall", or similar). Incorrect if it
  fabricates an answer. Prompt is short and targeted — Gemini 3.1 Flash
  Lite handles this well.

**Summary shape:**

```python
{
  "n": int,
  "qa_accuracy": float,                   # overall
  "by_type": {
    "user_evidence": {"n": int, "qa_accuracy": float, ...},
    "assistant_facts_evidence": {...},
    "changing_evidence": {...},
    "abstention_evidence": {"n": int, "abstention_accuracy": float, ...},
    "preference_evidence": {...},
    "implicit_connection_evidence": {...},
  },
  "memscore": {
    "accuracy_pct": float,                # 0..100
    "avg_latency_ms": float,              # per-question wall time
    "avg_context_tokens": float,          # chat_loaded_facts_count proxy (best-effort)
  },
  "advance_time": {
    "total_calls": int,
    "total_consolidations": int,
    "total_failures": int,
    "avg_calls": float,
  },
}
```

**Category display order** (matches ConvoMem paper tables):

```python
_CATEGORY_ORDER = [
    "user_evidence",
    "assistant_facts_evidence",
    "preference_evidence",
    "changing_evidence",
    "implicit_connection_evidence",
    "abstention_evidence",
]
```

### `run.py` and `__main__.py`

**Flags (mirror longmemeval's vocabulary exactly):**

| Flag | Default | Meaning |
|---|---|---|
| `--backend` | `sonzai` | Only `sonzai` at launch; `supermemory` slot reserved |
| `--limit N` | `20` | Questions to evaluate across all categories (0 = all) |
| `--categories CAT,CAT` | all six | Filter to evidence categories |
| `--concurrency N` | `4` | Questions in flight |
| `--skip-advance-time` | off | Baseline path without CE workers |
| `--flush-hours FLOAT` | `168.0` | Override the single flush duration |
| `--reuse-agents [PATH]` | off | Snapshot-based agent reuse (same format as longmemeval) |
| `--clear-reused-memory` | off | Wipe memory in reuse mode before retrieval |
| `--judge-model NAME` | `gemini-flash-lite-latest` | Gemini model for QA judging |
| `--output PATH` | `results/sonzai_<ts>.jsonl` | JSONL path |
| `--compare FILE FILE...` | — | Compare two or more JSONL result files |
| `-v` | — | Verbosity (repeatable) |

**Output JSONL (one line per question):**

```json
{
  "question_id": "convomem-user_evidence-42",
  "question_type": "user_evidence",
  "backend": "sonzai",
  "question": "...",
  "answer": "...",
  "evidence_messages": [{"speaker": "User", "text": "..."}],
  "agent_answer": "...",
  "qa_correct": true,
  "qa_rationale": "...",
  "elapsed_ms": 84210,
  "extra": {...}
}
```

**Compare output** — matches longmemeval's shape:
1. Per-system summary (n, QA accuracy, MemScore, advance_time diagnostics).
2. Per-category QA accuracy table, text and markdown.
3. Overall row last.

### `tests/`

**`test_dataset.py`:** fixture file checked in under
`tests/fixtures/convomem_sample.json` with 2 items. Assertions:
- `question_id` deterministic across loads.
- Message roles lowercased.
- Evidence-bearing conversation is first in `conversations`.
- Category filter returns only requested types.
- `limit` slices proportionally across categories.

**`test_scoring.py`:**
- Abstention judge prompt returns `True` for decline responses, `False` for
  fabricated answers (mocked Gemini client).
- MemScore aggregation math over a hand-built row list.

**No golden-output tests** — QA judge output isn't deterministic and the
dataset is externally authored. Any smoke test that actually hits
`AsyncSonzai` lives behind `SONZAI_API_KEY` env gating like the other
benchmarks.

## Non-goals

- Full 75k-question grid. Default is Supermemory's `batched_000.json` slice;
  full-grid support is future work behind a new flag.
- Multi-evidence-count runs (e.g. `1_evidence` and `3_evidence` same
  category). Default matches Supermemory's one-count-per-category map.
- Retrieval-metric scoring (Recall@K / NDCG@K). ConvoMem's ground truth is
  message-level; conversation-level retrieval metrics would mislead.
- Direct Supermemory backend (their SDK isn't in our deps). The `backends/`
  folder leaves a slot for it; a later PR can wire it in if helpful for
  reproducing their exact numbers.

## Open questions

None as of 2026-04-24. Ingest cadence, dataset slice, metric shape, and CLI
vocabulary are all locked.
