# LoCoMo benchmark design

**Status:** design approved, ready for implementation plan
**Date:** 2026-04-24
**Target:** add `benchmarks/locomo/` — a head-to-head **Sonzai vs mem0**
runner for [LoCoMo](https://github.com/snap-research/locomo) (Maharana et al.,
2024), reproducing [mem0's published LoCoMo
methodology](https://github.com/mem0ai/mem0/tree/main/evaluation) byte-for-byte
so our numbers are directly comparable to the mem0 paper's headline results.

## Motivation

`benchmarks/longmemeval/` and `benchmarks/sotopia/` already cover retrieval-heavy
and longitudinal-social dimensions. LoCoMo fills a third axis: **long-term
conversational memory over 19–35-session peer-to-peer dialogues** (300–600
turns, 9k–26k tokens per conversation), with QA split into five reasoning
categories. It is the canonical benchmark mem0 currently claims SOTA on.
Shipping a first-party runner lets us (1) reproduce mem0's slice exactly, (2)
publish directly-comparable numbers, and (3) exercise Sonzai's `/process`
endpoint — the production path for ingesting externally-generated transcripts,
which neither LongMemEval nor SOTOPIA exercises.

## Key decisions (locked with the user)

### 1. Match mem0's LoCoMo methodology step-for-step

The credible SOTA claim requires running mem0's own pipeline byte-for-byte and
swapping in Sonzai on the memory side. Concretely:

| Aspect | mem0 (upstream) | Sonzai backend |
|---|---|---|
| User model | `{speaker_a}_{idx}`, `{speaker_b}_{idx}` — two users per sample | `lc-{sample_id}-a`, `lc-{sample_id}-b` — two users per sample, one shared agent |
| Ingest API | `mem0.add(messages, metadata={timestamp})` | `POST /api/v1/agents/{id}/process` (confirmed as the correct endpoint — not `sessions.end`, `/chat`, `memory/facts/bulk`, `users/.../content`, or `memory/seed`) |
| Perspective | Dual-POV: session fed once as A-user/B-assistant, once reversed | Same — one `/process` call per speaker POV |
| Message shape | `{"role": "user"|"assistant", "content": f"{speaker}: {text}"}` | Same (speaker-name prefix preserved) |
| Batch size | 2 messages per `add` | `--ingest-batch-size N` (default 2, matches mem0; `0` = whole-session ablation) |
| Between-session | None | `workbench.advance_time(gap_hours)` per user, floor 25h (**Sonzai's lift**) |
| Retrieval | `search(query, user_id=a, top_k=30)` × both speakers | `memory.search(user_id=a)` + `memory.search(user_id=b)` |
| Reader | External LLM over mem0's `ANSWER_PROMPT` | Gemini 3.1 Flash Lite over **verbatim port** of `ANSWER_PROMPT` |
| Judge | GPT-4o-mini over `ACCURACY_PROMPT` | Gemini 3.1 Flash Lite over **verbatim port** of `ACCURACY_PROMPT` (matches our LongMemEval/SOTOPIA judges — neutral, not OpenAI/Anthropic) |
| Categories | Filter 5 (adversarial), report 1–4 | Same (flag `--include-adversarial` for ablation) |

### 2. Ingest endpoint: `/process` (not `sessions.end`, `/chat`, or anything else)

Verified against `openapi.json`:

> `POST /api/v1/agents/{agentId}/process` — *"Runs the full Context Engine
> pipeline (behavioral side effects, fact extraction, memory storage, diary,
> knowledge gap detection) on a conversation transcript produced by an external
> LLM. Requires at least 2 messages."*

Alternatives considered and rejected:

| Endpoint | Why rejected |
|---|---|
| `sessions.start` + `sessions.end(messages=...)` | Works (that's what LongMemEval does), but requires `sessions.start` ceremony. `/process` is the cleaner primitive for externally-generated transcripts — designed for exactly this use case. |
| `/agents/{id}/users/{id}/content` | Async + job-ID polling. No role structure. |
| `/agents/{id}/users/{id}/prime` | CRM/LinkedIn primer. Async. Wrong shape. |
| `/agents/{id}/memory/facts/bulk` | Direct fact insertion, **no LLM extraction**. Defeats the point. |
| `/agents/{id}/memory/seed` | Personality-based lore generation, not ingest. |
| `/agents/{id}/chat` | Generates a response — would pollute memory with a Sonzai-invented assistant turn that isn't in the dataset. |

### 3. Single benchmark agent shared across ALL memory benchmarks

A single generic agent is used for LongMemEval, LoCoMo, and any future memory
benchmark — exported from `sonzai.benchmarks` so third-party evaluators hit the
exact same agent profile we did. **No per-benchmark tuning.** This:

- Removes any "we tuned a different agent per benchmark" objection
- Lets the SDK function as the auditable source-of-truth for the bench agent
- Costs us nothing — the existing LongMemEval agent's `speech_patterns`
  ("concise, literal recall") helps LoCoMo equally (LoCoMo's reader prompt
  constrains answers to <5–6 words)

Refactor in this PR:

```python
# src/sonzai/benchmarks/__init__.py
BENCHMARK_AGENT_NAME = "sonzai-benchmark-agent"
async def ensure_benchmark_agent_async(client: AsyncSonzai) -> tuple[str, bool]: ...

# Back-compat aliases — removed in the release after next.
LONGMEMEVAL_AGENT_NAME = BENCHMARK_AGENT_NAME
ensure_longmemeval_agent_async = ensure_benchmark_agent_async
```

`benchmarks/longmemeval/run.py` switches one import line. Existing pinned
`shared_agent.json` files continue to work (same underlying agent_id, just a
renamed bootstrap function).

### 4. LoCoMo-specific `BackendResult` with per-speaker lists

LongMemEval's `BackendResult` flattens into one ranked list. For LoCoMo we
preserve mem0's dual-search shape end-to-end:

```python
@dataclass
class RankedMemoryItem:
    memory_id: str
    text: str
    timestamp: str
    score: float = 0.0

@dataclass
class LocomoBackendResult:
    speaker_a_memories: list[RankedMemoryItem] = field(default_factory=list)
    speaker_b_memories: list[RankedMemoryItem] = field(default_factory=list)
    agent_answer: str = ""
    retrieved_session_ids: list[str] = field(default_factory=list)  # for Recall@K
    extra: dict[str, object] = field(default_factory=dict)
```

### 5. Byte-for-byte port of mem0's prompts

`benchmarks/locomo/prompts.py` copies `ANSWER_PROMPT` and `ACCURACY_PROMPT`
verbatim from mem0's `evaluation/prompts.py` and `evaluation/metrics/llm_judge.py`.
A module-level comment documents upstream source, commit SHA, and date copied. A
snapshot test (`test_prompts_port.py`) guards against accidental edits. If mem0
updates their prompts we can re-port and re-run.

### 6. Headline metric: LLM-judge accuracy per category; token-F1 secondary

mem0 publishes per-category LLM-judge accuracy as the headline. We mirror that
table shape exactly (categories 1–4, overall mean). Token-F1 is reported as
secondary because (a) mem0 also reports it and (b) it's the paper-original
metric. Retrieval Recall@K / NDCG@K at session-level are Sonzai-native
diagnostics that separate "retrieval missed it" from "reader didn't surface it".

### 7. Retrieval scoring at session-level (not dia_id-level)

LoCoMo `evidence` is a list of dia_ids (`"D3:14"`). Neither Sonzai (fact-based)
nor mem0 (narrative-memory-based) stores per-turn provenance for retrieval
scoring. Both systems can report `session_N`-level recall by mapping retrieved
memories back to their source session via timestamp or session_id. We score
`"D3:14" → session_3` on both sides — apples-to-apples.

## Architecture

```
benchmarks/
├── common/                                  (existing — reused)
│   ├── gemini_judge.py                     + judge_locomo_async (mem0 ACCURACY_PROMPT port)
│   ├── workbench_compat.py                 (advance_time_chunked_async — reused)
│   ├── sdk_extras.py                       + async_process() forward-compat shim
│   ├── agent_reuse.py                      + "locomo" branch in SliceKey.matches()
│   └── dataset_cache.py                    (reused)
└── locomo/                                  ⇐ NEW
    ├── __init__.py
    ├── __main__.py                         python -m benchmarks.locomo
    ├── dataset.py                          loader for locomo10.json (auto-download)
    ├── scoring.py                          per-category LLM-judge accuracy + token-F1 + Recall@K
    ├── prompts.py                          verbatim port of mem0 ANSWER_PROMPT / ACCURACY_PROMPT
    ├── run.py                              orchestrator (async, bounded concurrency)
    ├── compare.py                          two-JSONL side-by-side table generator
    ├── backends/
    │   ├── __init__.py                     LocomoBackendResult + RankedMemoryItem
    │   ├── sonzai.py                       /process + advance_time + dual-user search + Gemini reader
    │   └── mem0.py                         mirror of mem0/add.py + search.py (ports verbatim)
    ├── tests/
    │   ├── test_dataset.py                 fixture-based loader tests + date-time parsing
    │   ├── test_scoring.py                 token-F1 + Recall@K sanity
    │   └── test_prompts_port.py            snapshot-assert ANSWER_PROMPT / ACCURACY_PROMPT equal upstream
    └── results/                            JSONL outputs (iteration runs gitignored; headline receipts allow-listed)
```

Plus SDK refactor (small):

```
src/sonzai/benchmarks/
    __init__.py                             add BENCHMARK_AGENT_NAME + ensure_benchmark_agent_async;
                                            alias existing LONGMEMEVAL_* to them for back-compat
```

## Dataset

`benchmarks/locomo/dataset.py`:

```python
DATASET_URL = "https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json"
DATASET_FILE = "locomo10.json"

@dataclass
class LocomoTurn:
    speaker: str             # "Caroline" / "Melanie"
    dia_id: str              # "D1:3"
    text: str
    img_url: str = ""        # v1 ignores multimodal but keeps fields for forward compat
    blip_caption: str = ""

@dataclass
class LocomoSession:
    index: int               # 1..N (from "session_1" key)
    date_time: str           # raw "1:00 pm on 8 May, 2023"
    turns: list[LocomoTurn]

    @property
    def parsed_date_time(self) -> datetime: ...  # robust parser, falls back to index order on failure

@dataclass
class LocomoQA:
    question: str
    answer: str
    category: int            # 1..5
    evidence: list[str]      # dia_ids
    adversarial_answer: str = ""

@dataclass
class LocomoSample:
    sample_id: str
    speaker_a: str
    speaker_b: str
    sessions: list[LocomoSession]   # sorted by parsed_date_time
    qa: list[LocomoQA]

def load_samples(*, limit: int = 0, path: str | None = None) -> list[LocomoSample]: ...
def load_qa(
    samples: list[LocomoSample], *, include_adversarial: bool = False,
) -> list[tuple[LocomoSample, LocomoQA]]:  # filters category 5 by default
    ...
```

Category 5 (adversarial) is filtered out by default to match mem0's report. A
`--include-adversarial` flag on the CLI unlocks it.

## Sonzai backend

Per-sample flow (`backends/sonzai.py`):

### Ingest (skipped if snapshot reuse matches)

```python
user_a = f"lc-{sample.sample_id}-a"
user_b = f"lc-{sample.sample_id}-b"

if clear_before:
    await memory.reset(agent_id, user_id=user_a)
    await memory.reset(agent_id, user_id=user_b)

prev_dt = None
for session in sample.sessions:   # chronological
    if prev_dt is not None:
        gap_h = max((session.parsed_date_time - prev_dt).total_seconds() / 3600, 25.0)
        # Concurrent per-user advance
        await asyncio.gather(
            advance_time_chunked_async(client, agent_id=agent_id, user_id=user_a, total_hours=gap_h),
            advance_time_chunked_async(client, agent_id=agent_id, user_id=user_b, total_hours=gap_h),
        )

    msgs_a = [{"role": "user" if t.speaker == sample.speaker_a else "assistant",
               "content": f"{t.speaker}: {t.text}"} for t in session.turns]
    msgs_b = [{"role": "user" if t.speaker == sample.speaker_b else "assistant",
               "content": f"{t.speaker}: {t.text}"} for t in session.turns]

    # Split into ingest_batch_size chunks (mem0 parity, default 2).
    # batch_size=0 means whole-session in one call.
    for batch in _batches(msgs_a, ingest_batch_size):
        await async_process(client, agent_id=agent_id, user_id=user_a, messages=batch,
                            session_id=f"{sample.sample_id}-s{session.index}-a")
    for batch in _batches(msgs_b, ingest_batch_size):
        await async_process(client, agent_id=agent_id, user_id=user_b, messages=batch,
                            session_id=f"{sample.sample_id}-s{session.index}-b")
    prev_dt = session.parsed_date_time

# Final flush
await asyncio.gather(
    advance_time_chunked_async(client, agent_id=agent_id, user_id=user_a, total_hours=25.0),
    advance_time_chunked_async(client, agent_id=agent_id, user_id=user_b, total_hours=25.0),
)
```

`async_process` is a new forward-compat shim in `benchmarks/common/sdk_extras.py`:

```python
async def async_process(client, *, agent_id, user_id, messages, session_id="", provider="", model=""):
    native = getattr(client, "process", None)
    if native is not None:
        return await native(...)   # use typed binding when the regenerated SDK exposes it
    return await client._http.post(
        f"/api/v1/agents/{agent_id}/process",
        json_data={"userId": user_id, "messages": messages,
                   "sessionId": session_id, "provider": provider, "model": model},
    )
```

`/process` requires ≥2 messages — if a batch has 1 (only possible at whole-session=0 boundary when a session has 1 turn, which is extremely rare), pad via combining with the previous batch tail. Handled inside `_batches()`.

### QA (iterates all non-category-5 QAs against populated memory)

```python
async def answer_one_qa(client, sample, qa, *, agent_id, top_k, reader) -> dict:
    user_a = f"lc-{sample.sample_id}-a"
    user_b = f"lc-{sample.sample_id}-b"

    # Dual search
    a_hits = await memory.search(agent_id=agent_id, user_id=user_a, query=qa.question, limit=top_k)
    b_hits = await memory.search(agent_id=agent_id, user_id=user_b, query=qa.question, limit=top_k)

    # Filter Sonzai metadata facts (comm_style / side_effect / interest:*) —
    # same _is_metadata_fact filter as longmemeval/backends/sonzai.py.
    # Map fact_id → session_id via memory.timeline() → get timestamp from
    # LocomoSession.date_time on the same session.
    a_mems = _to_ranked([h for h in a_hits if not _is_metadata_fact(h.fact_id)], sample)
    b_mems = _to_ranked([h for h in b_hits if not _is_metadata_fact(h.fact_id)], sample)

    # Reader — Gemini 3.1 Flash Lite, ported ANSWER_PROMPT
    answer = await _ask_reader(reader, question=qa.question,
                               speaker_1=sample.speaker_a, speaker_1_memories=a_mems,
                               speaker_2=sample.speaker_b, speaker_2_memories=b_mems)

    return LocomoBackendResult(
        speaker_a_memories=a_mems, speaker_b_memories=b_mems,
        agent_answer=answer,
        retrieved_session_ids=_merge_sid_ranking(a_mems, b_mems),
    )
```

## mem0 backend

`backends/mem0.py` is a direct port of mem0's `evaluation/src/memzero/add.py`
and `search.py`. Differences from upstream:

- Emits `LocomoBackendResult` (our shape, not mem0's dict) so scoring code
  is provider-neutral
- Reader + judge are **ours** (Gemini) — their pipeline from `add` through
  `search` is preserved; we swap the final reader/judge for the bench-neutral
  Gemini path. This is the fair comparison: memory layer differs, reader +
  judge identical.
- Applies mem0's `custom_instructions` (verbatim from their `add.py`) via
  `update_project()` so mem0 runs at its own published capability — not
  sandbagged.
- Rate-limiting (429 backoff, default concurrency 2) mirrors the LongMemEval
  mem0 backend exactly.

Optional `mem0ai` dep is lazy-imported. `MEM0_API_KEY` required only when
`--backend mem0`.

## Reader and judge

**Reader** (`backends/sonzai.py::_ask_reader`, reused by `backends/mem0.py`):
Gemini 3.1 Flash Lite, `ANSWER_PROMPT` ported verbatim from mem0.
Structured-output via Pydantic — returns `{"answer": str}`.
Memories formatted as `"{timestamp}: {text}"` — mem0's exact format.

**Judge** (`common/gemini_judge.py::judge_locomo_async`):
Gemini 3.1 Flash Lite, `ACCURACY_PROMPT` ported verbatim. Returns
`{"label": "CORRECT"|"WRONG"}`. Score = 1 if `CORRECT` else 0.

Using Gemini as the judge (not GPT-4o-mini like mem0) gives us three benefits:
(1) consistency with LongMemEval/SOTOPIA judges, (2) neutral third-party (not
OpenAI, not Anthropic), (3) cheaper. The mem0 ACCURACY_PROMPT is
model-agnostic; it specifies behavior, not model. We ship one flag for a
GPT-4o-mini judge rerun as a sanity ablation (`--judge gpt-4o-mini`) so if
anyone objects "numbers differ because judge differs" we can answer inline.

## Scoring

`benchmarks/locomo/scoring.py`:

```python
@dataclass
class QAScore:
    category: int           # 1..4 (5 filtered upstream)
    llm_correct: bool       # headline
    token_f1: float         # secondary (paper metric)
    recall_any_at_k: dict[int, float]   # {1:..., 3:..., 5:..., 10:..., 30:...}
    ndcg_any_at_k: dict[int, float]

def token_f1(answer: str, gold: str) -> float: ...
def session_recall_at_k(retrieved_session_ids, evidence_dia_ids, k) -> float: ...
def ndcg_at_k_sessions(retrieved_session_ids, evidence_dia_ids, k) -> float: ...

def aggregate(rows: list[dict]) -> dict:
    """Per-category means + overall. Returns the shape used by compare.py."""
```

Session projection: `"D3:14" → "session_3"`. Retrieval scoring merges
`speaker_a_memories` and `speaker_b_memories` (score-descending, dedup by
session_id, order-preserving) before Recall@K. Same projection applied to both
backends.

## Output JSONL schema

One row per (sample_id, qa_index):

```json
{
  "sample_id": "conv-0",
  "qa_index": 3,
  "question": "...",
  "gold_answer": "...",
  "category": 2,
  "evidence": ["D3:14", "D7:8"],
  "generated_answer": "...",
  "llm_correct": true,
  "llm_rationale": "Same topic; matches gold.",
  "token_f1": 0.67,
  "speaker_a_memories": [{"memory_id":"...", "text":"...", "timestamp":"...", "score":0.87}],
  "speaker_b_memories": [...],
  "retrieval": {
    "recall_any@1": 1.0, "recall_any@5": 1.0, "recall_any@10": 1.0,
    "ndcg_any@10": 0.86
  },
  "backend": "sonzai" | "mem0",
  "extra": {"facts_extracted": 142, "advance_time_calls": 8, ...}
}
```

## CLI

```
python -m benchmarks.locomo --backend sonzai --limit 2
python -m benchmarks.locomo --backend mem0   --limit 2
python -m benchmarks.locomo --compare results/sonzai_*.jsonl results/mem0_*.jsonl
```

Flags:

| Flag | Default | Purpose |
|---|---|---|
| `--backend {sonzai,mem0}` | sonzai | which memory system |
| `--limit N` | 2 | samples to run (0 = all 10); 2 for smoke |
| `--concurrency N` | 2 | samples in flight |
| `--top-k N` | 30 | retrieval top-k per speaker (mem0 default) |
| `--ingest-batch-size N` | 2 | mem0 parity; 0 = whole-session |
| `--skip-advance-time` | off | Sonzai baseline (no self-learning) |
| `--include-adversarial` | off | include category 5 |
| `--reuse-agents [PATH]` | off | snapshot-based skip-ingest |
| `--clear-reused-memory` | off | memory.reset before reuse |
| `--mode {retrieval,qa,both}` | both | fast retrieval-only mode skips reader+judge |
| `--judge-model` | `gemini-3.1-flash-lite-preview` | judge LLM |
| `--output PATH` | auto-timestamped | JSONL location |
| `--compare FILE...` | — | head-to-head table generator |

## Reuse + snapshots

Extend `benchmarks/common/agent_reuse.SliceKey.matches()` with a `"locomo"`
branch analogous to the `"longmemeval"` one. Snapshot keyed by `sample_id`
(not QA id — ingest is per-sample, QA iterates fast against populated state).
`shared_agent.json` pinned in `benchmarks/locomo/results/` using the same
multi-pinned pattern.

## Testing

Unit only; no live-API hits (matches the existing benches' policy):
- `tests/test_dataset.py` — round-trip load, date-time parsing edge cases,
  category-5 filter
- `tests/test_scoring.py` — token-F1 against known pairs, Recall@K and
  NDCG@K against tiny synthetic rankings
- `tests/test_prompts_port.py` — snapshot-assert ported `ANSWER_PROMPT` and
  `ACCURACY_PROMPT` equal the upstream strings we copied (guards against
  accidental edits)

## Docs

- Add a LoCoMo section to `benchmarks/README.md` after the SOTOPIA section
  — same structure (headline table, `Running it yourself`, `Methodology`).
- Numbers filled in by `scripts/update_readme_scores.py` (existing helper)
  after first head-to-head run.

## Non-goals

- **Multimodal LoCoMo** — the dataset has `img_url` / `blip_caption` fields
  on some turns. v1 treats them as text (BLIP caption if present, else drop
  the image reference). Mem0 does the same.
- **The paper's event-summarization and multimodal-dialogue-generation
  tasks.** We implement only the QA slice — that's the headline mem0 reports
  against, and the only part with objective ground truth.
- **GPT-4o-mini as default judge.** Available as an ablation flag; Gemini is
  the published headline so our numbers match LongMemEval's and SOTOPIA's.
- **MemPalace backend.** MemPalace wasn't tuned against LoCoMo. Adding them
  in v1 would be unfair to them; can be a follow-up.
- **dia_id-level Recall.** Neither system stores per-turn provenance for
  retrieval; session-level is the honest comparison.

## Open questions (surfaced during implementation)

- Precise format of `session_N_date_time` strings — sample a few from the
  dataset before finalizing the parser. Fallback to session-index ordering
  if parsing fails is already in the design.
- Whether Sonzai's `memory.search` server-side session_id population covers
  facts extracted via `/process` the same way it does for `sessions.end`
  (should, but verify during implementation or fall back to
  `memory.timeline()` as we do in LongMemEval).

## Rollout

- [ ] Dataset loader + unit tests
- [ ] SDK refactor (`ensure_benchmark_agent_async` + aliases)
- [ ] `async_process` shim in `common/sdk_extras.py`
- [ ] Sonzai backend (ingest + QA)
- [ ] mem0 backend
- [ ] Scoring + reader + judge
- [ ] `run.py` + CLI
- [ ] `compare.py`
- [ ] README section + smoke-run numbers
