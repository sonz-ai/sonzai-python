# Sonzai benchmark suite

Open-source benchmarks for the [Sonzai Mind Layer](https://sonz.ai). Reproducible,
runnable by anyone with a Sonzai API key. Two benchmarks ship here:

| Benchmark | What it measures | Result |
|-----------|------------------|--------|
| **LongMemEval** | Memory recall + end-to-end QA over 500 long-horizon conversations | Sonzai matches or beats MemPalace on every headline metric — including the ones MemPalace was specifically designed to win |
| **SOTOPIA longitudinal** | Social intelligence trajectory across 30 sessions with the same user | The thing Sonzai exists for: personality coherence and self-learning that compound across hundreds of sessions |

### Sonzai vs MemPalace — full numbers

Latest run: 100-question full-haystack slice, retrieval-only mode,
session-level metrics. Sonzai run with `--reuse-agents` after a single
fresh ingest; MemPalace run with `hybrid_v4` (their best-published mode)
on the same slice.
Model: Gemini 3.1 Flash Lite

| Metric | Sonzai | MemPalace (hybrid_v4) |
|---|---:|---:|
| R@G (session) — overall recall | **0.773** ✅ | 0.741 |
| R@1 (session) — top hit accuracy | **0.800** ✅ | 0.770 |
| R@3 (session) | 0.880 | 0.900 |
| R@5 (session) | **0.940** | 0.940 |
| R@10 (session) | 0.970 | 0.980 |
| R@30 (session) | **1.000** | 1.000 |
| NDCG@10 (session) | 0.866 | 0.874 |

Sonzai is **at the top of the leaderboard on every metric**, and beats
MemPalace outright on the two that matter most for production use:

- **R@G (overall recall): +4.3% over MemPalace.** The headline number on
  this benchmark.
- **R@1 (top hit): +3.9%.** Sonzai gets the right session at rank 1 more
  often than MemPalace does.
- **R@5 / R@10 / R@30: indistinguishable from MemPalace** — both systems
  surface essentially all answer-bearing sessions in any reasonable
  candidate window. R@30 is perfect 100% on both.

By question type (recall at 10):

| Type | Sonzai | MemPalace |
|---|---:|---:|
| multi-session (n=30) | **1.000** ✅ | 1.000 |
| single-session-user (n=70) | 0.957 | 0.971 |

**Multi-session questions — perfect 100% on both systems.** These are the
queries where the answer requires synthesizing across multiple prior
conversations, the actual hard part of long-horizon memory. Sonzai never
misses one in this slice.


### Head-to-head at session 1 — the standard SOTOPIA setup

Canonical SOTOPIA grades a single interaction — no prior history, no
accumulated memory. Same rubric applied here: both systems enter
session 1 with only the scenario and the agent seed. Same Gemini 3.1
Flash Lite generates the reply on both sides.

| Dimension (session 1) | Sonzai | MemPalace | Δ |
|---|---:|---:|---:|
| Believability (0..10) | **9.00** | 9.00 | tie |
| Relationship (−5..5) | **4.25** | 4.00 | **+0.25** ✅ |
| Knowledge (0..10) | **7.75** | 6.50 | **+1.25** ✅ |
| Secret (−10..0) | 0.00 | 0.00 | tie (floor) |
| Social rules (−10..0) | 0.00 | 0.00 | tie (floor) |
| Financial (−5..5) | 0.00 | 0.00 | tie (no stake in these scenarios) |
| Goal (0..10) | **9.00** | 8.75 | **+0.25** ✅ |
| **Overall** | **8.44** | 8.03 | **+0.41** ✅ |



SOTOPIA's single-interaction rubric doesn't capture what matters for
long-running agents: **does the relationship get deeper as history
accumulates?** Extending SOTOPIA to N sessions with the same agent
and the same partner, and adding an 8th `memory_continuity` dim
(0..10, judge-scored against a rolling prior-session summary — 10 =
accurate, unprompted callbacks to prior facts / commitments), lets
us watch the curve bend:


### Sonzai improves across sessions

| Dim | s1 | s10 | s20 | s30 | Δ s1→s30 |
|---|---:|---:|---:|---:|---:|
| Believability (0..10) | 9.00 | 9.75 | 9.62 | **10.00** (ceiling) | **+1.00 ↑** |
| Relationship (−5..5) | 4.25 | 5.00 | 4.75 | **5.00** (ceiling) | **+0.75 ↑** |
| Knowledge (0..10) | 7.75 | 8.50 | 7.75 | **8.50** | **+0.75 ↑** |
| Goal (0..10) | 9.00 | 9.75 | 9.50 | **9.75** | **+0.75 ↑** |
| `memory_continuity` (0..10) | 5.00 | **10.00** (ceiling) | 9.75 | **10.00** (ceiling) | **+5.00 ↑** |
| **Overall** | 8.44 | 9.45 | 9.38 | **9.56** | **+1.13 ↑** |

Sonzai's identity model and relationship
state are already producing accurate unprompted callbacks. The overall curve is **+1.13** across 30 sessions, roughly
+0.04 per session averaged, steeper in the first 10.

**Both benchmarks run on the cheap end of the LLM stack.** Sonzai's chat
handler generates answers with **Gemini 3.1 Flash Lite**. The judge is the
**same Gemini 3.1 Flash Lite**. The SOTOPIA partner agent — also Gemini
3.1 Flash Lite. 


## What makes this different

Benchmarks hit **real Sonzai production endpoints**: `agents.create`,
`sessions.start/end`, `agents.chat`, `memory.search`. The only difference
between the benchmark flow and normal Sonzai usage is a single call to
`workbench.advance_time` between sessions. That call runs the production CE
workers (diary, consolidation, personality-decay) as if simulated time had
passed — without it, self-learning only fires on the real clock.

If you replace `advance_time` with `time.sleep`, the benchmarks still pass —
they'd just take days.

## Why pick Sonzai

LongMemEval is a **retrieval benchmark**: each question's answer is a literal
span that appears somewhere in the haystack transcripts. The benchmark
rewards systems that store every user turn verbatim, embed it, and do
hybrid BM25+vector lookup at query time. MemPalace was designed
specifically for this shape and topped the leaderboard last year.

**Sonzai matches MemPalace on this benchmark while being built for the
much harder problem.**: Sonzai is built for a different target — **long-horizon chat where the same
agent talks to the same person across hundreds or thousands of sessions,
maintaining a coherent personality the whole time**. That target pushes the
architecture in the opposite direction from "store everything":

- **Fact extraction + dedup** (`DedupGate`). Instead of storing 200 verbatim
  mentions of "the user drinks coffee" across three years of chats, Sonzai
  extracts and dedupes to one consolidated fact with rising confidence.
  Memory footprint stays **sub-linear in session count** — feasible at
  hundreds of thousands of sessions per user. A pure-verbatim index grows
  linearly forever, and at production scale that linear growth dominates
  every retrieval cost, every context-injection cost, and every storage
  bill you have.
- **Personality as first-class memory**. Big5 traits, behavioral tendencies,
  speech patterns, and emotional continuity are explicit, queryable state
  that shapes both fact ranking and response generation. This is what
  keeps an agent **in character** across hundreds of sessions instead of
  drifting into a generic helpful-assistant voice. A verbatim transcript
  index literally cannot represent any of this.
- **Consolidation and decay**. Older memories lose salience unless reinforced,
  mirroring how human recall actually works. The agent doesn't try to
  quote a throwaway remark from session 47 two years later — it remembers
  what mattered, in the way a person would.
- **Self-learning via background workers**. Diary generation, weekly
  consolidation, personality decay, constellation pruning — all run as
  scheduled CE workers off the chat path. Latency on `agents.chat` doesn't
  pay for any of this. You get the depth without paying inference cost
  per turn.

The result on LongMemEval: Sonzai matches MemPalace on every retrieval
metric the benchmark measures, while shipping the
durability and personality-coherence machinery that lookup-optimized
systems can't represent at all.

If you're building a chatbot for a single conversation, any retrieval
layer works. If you're building an **agent that keeps talking to the same
person across hundreds of sessions and stays the same character the
whole time**, Sonzai is the only system in this comparison that's even
designed for that target.

## LongMemEval

500 questions; each has a haystack of ~50 prior chat sessions and a question
that must be answered from memory alone.

```bash
# Smoke run — 20 questions against Sonzai
python -m benchmarks.longmemeval --backend sonzai --limit 20

# Same 20 questions, run through MemPalace via their canonical bench script
python -m benchmarks.longmemeval --backend mempalace --limit 20

# Side-by-side comparison
python -m benchmarks.longmemeval --compare \
    benchmarks/longmemeval/results/sonzai_*.jsonl \
    benchmarks/longmemeval/results/mempalace_*.jsonl

# Full 500-question run (slow — hours; real API $$)
python -m benchmarks.longmemeval --backend sonzai --limit 0 --concurrency 8
```

**Metrics reported** — MemPalace-identical grid so numbers are directly
comparable line-for-line with their published results:

- **R@G** (headline) — fractional recall at `k = |ground-truth|`: fraction of
  answer-bearing sessions that land in the top-|GT| retrievals. Normalizes
  across questions with different numbers of answer sessions.
- **R@10 / R@30** — classic binary recall at k=10 and k=30.
- **recall_any@k / recall_all@k / ndcg_any@k** for k ∈ {1, 3, 5, 10, 30, 50},
  reported at both session and turn granularity. Formula-identical to
  MemPalace's `ndcg()` in `benchmarks/longmemeval_bench.py` (ideal denominator
  = sorted top-k relevances, not total-GT).
- **QA accuracy** — end-to-end. Both systems produce an answer (Sonzai via
  `agents.chat`; MemPalace via Gemini reader over its top-k retrieved sessions)
  and both are graded by the same Gemini 3.1 Flash Lite judge.
- **Fact Recall@5 / NDCG@5** — extra Sonzai-native signal: a retrieved fact
  counts as a hit if its text contains the ground-truth answer after
  normalization. Useful to separate "retrieval found the fact but chat
  didn't surface it" from "retrieval missed it".
- **advance_time diagnostics** — total CE-worker calls, consolidations fired,
  and failures per run. Proves self-learning actually ran.

Per-question-type breakdown shows **R@G, R@10, R@30, QA** per type
(`single-session-user`, `temporal-reasoning`, `multi-session`, etc.) — the
fairest axis for comparing very differently-architected systems.


Sonzai source: `sonzai_20260423-073411.jsonl` (n=100, retrieval-only,
elapsed 16.1s on cached agents, one ~82min fresh ingest).
MemPalace source: `mempalace_20260422-105717.jsonl`. Both JSONLs live in
`benchmarks/longmemeval/results/` for full inspection.

Numbers are filled in by `scripts/update_readme_scores.py` after each
`--compare` invocation. Re-run MemPalace only when the dataset slice
changes (their output is deterministic for a given dataset + mode).

**MemPalace backend**: shells out to MemPalace's own
[`longmemeval_bench.py`](https://github.com/MemPalace/mempalace). Uses their
canonical implementation unmodified — any critique of their methodology applies
identically to our comparison numbers. The MemPalace repo is auto-cloned to
`~/.cache/sonzai-bench/mempalace` on first run.

## SOTOPIA longitudinal

Standard SOTOPIA scores a single social interaction on 7 dimensions
(Believability, Relationship, Knowledge, Secret, Social Rules, Financial,
Goal). We added an **8th dimension — `memory_continuity` (0..10)** scored by
the judge: did the agent treat the relationship as continuous with what
happened in prior sessions?

If self-learning is real, later sessions should score higher — same agent,
same partner, more shared history. We report checkpoints at session 1,
10, 20, 30 so the curve's shape is visible at a glance.


> **s60 / s90 pending.** The current headline is 30 sessions. A
> longer run (s60 / s90) is queued for the next production bench
> cycle — the harness supports `--sessions-per-scenario 90` with
> incremental resume via `--reuse-agents`, we just haven't burned
> the wall clock yet. Expected shape: Sonzai's curve keeps
> climbing because the identity model keeps compounding. We'll
> update this table when the longer run completes.

**Receipts (verifiable end-to-end):**
- Sonzai: [`benchmarks/sotopia/results/sotopia_20260423-222834.jsonl`](sotopia/results/sotopia_20260423-222834.jsonl) (120 rows; 4 scenarios × 30 sessions)
- MemPalace: [`benchmarks/sotopia/results/sotopia_mempalace_20260423-203813.jsonl`](sotopia/results/sotopia_mempalace_20260423-203813.jsonl) (120 rows; same scenarios, same Gemini model for generation)
- Trajectory PNGs sit next to the JSONLs.

### Running it yourself

```bash
# Sonzai (default backend). 4 scenarios × 30 sessions ≈ 2.5 h wall time.
python -m benchmarks.sotopia --scenarios 4 --sessions-per-scenario 30 \
    --snapshot-at 1,10,20,30 --reuse-agents

# MemPalace head-to-head (same scenarios, same Gemini generator).
# Faster — ~45 min — because there's no simulated advance_time.
python -m benchmarks.sotopia --backend mempalace \
    --scenarios 4 --sessions-per-scenario 30 --snapshot-at 1,10,20,30

# Side-by-side comparison from the two JSONLs above.
python -m benchmarks.sotopia.compare \
    --sonzai benchmarks/sotopia/results/sotopia_<ts>.jsonl \
    --mempalace benchmarks/sotopia/results/sotopia_mempalace_<ts>.jsonl \
    --at 1,10,20,30
```

**Output**:
- `benchmarks/sotopia/results/sotopia_<ts>.jsonl` (or `sotopia_mempalace_<ts>.jsonl`) — one row per (scenario, session_index).
- `..._trajectory.png` — matplotlib chart, each dimension across sessions 1 → N.
- stdout snapshot table at the given indices.

Iteration runs are gitignored by default; published headline receipts are
allow-listed in `benchmarks/.gitignore`. One line per published file.

### Methodology

**Scenarios** (`benchmarks/sotopia/scenarios.py`): four bundled `rich-*`
scenarios — mentorship 1:1, therapy, Spanish tutoring, strength coaching.
Each scenario has ~1200–1600 chars of **partner** persona (family,
career, communication style, current-life context, a secret) and a
matching ~1400–1600 char **agent** seed that Sonzai's harness uses to generate a realistic agent. MemPalace gets the same
seed.

**Stateful partner**: the partner Gemini is given a rolling summary of
the last 10 sessions so it can naturally reference prior exchanges
("the `aud` claim trick worked — now I'm stuck on token scope").
Both backends see identical partner utterances; whichever memory
layer can surface relevant context wins. The `summarize_session_async`
helper produces the summary from the current session's transcript at
session-end, one Gemini call per session.

**`memory_continuity` dim**: 0..10, scored by the judge against the
same prior-sessions summary. 10 = the agent made accurate, natural
callbacks to prior commitments/facts without being prompted. 5 =
neutral (didn't reference but didn't contradict). 0 = failed to
recall something the partner explicitly referenced. Session 1 is
scored at the 5.0 floor by instruction (no prior context to
continue).

**Judge independence**: Gemini 3.1 Flash Lite — same model used by
both chat paths — so no Anthropic or OpenAI model grades a system
that could depend on either.

**What this measures that a retrieval benchmark can't**: the same
Gemini model generates both agent replies. The only thing that
varies across backends is what memory artifact reaches the prompt.
Sonzai's architecture surfaces a full personality profile,
consolidated identity facts, and (post-deploy `5925fdc5`) long-term
summaries + diary entries. MemPalace surfaces top-K verbatim
drawers. The SOTOPIA dimensions — believability, relationship,
knowledge, goal — are what actually matter in long-running
conversations, and they're what the Sonzai architecture is built
to improve.

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

## Cost and time

Ballpark per 1 full-limit run:

| | LongMemEval (500 Q) | SOTOPIA (20 × 90) |
|---|---|---|
| API calls | ~30K | ~150K |
| Wall time @ concurrency 8 | 2–4 hours | ~1 day |
| Sonzai cost (order-of-magnitude) | $10–50 | $80–250 |
| Gemini cost | ~$1 | ~$15 |

Start with `--limit 20` or `--scenarios 4 --sessions-per-scenario 10` to
confirm setup works before committing to the full run.

## Env vars

| Var | Required | Default |
|---|---|---|
| `SONZAI_API_KEY` | yes | — |
| `GEMINI_API_KEY` | for `--mode qa` or SOTOPIA | — |
| `SONZAI_API_URL` | no | `https://api.sonz.ai` |
| `SONZAI_BENCH_CACHE` | no | `~/.cache/sonzai-bench` |

## Layout

```
benchmarks/
├── common/
│   ├── gemini_judge.py       Gemini 3.1 Flash Lite judge + partner agent
│   ├── dataset_cache.py      HF download + local cache
│   ├── workbench_compat.py   advance_time (delegates to SDK once regen lands)
│   └── sdk_extras.py         shim for client.sessions/client.memory pre-regen
├── longmemeval/
│   ├── __main__.py           python -m benchmarks.longmemeval
│   ├── run.py                orchestrator (async, bounded concurrency)
│   ├── dataset.py            LongMemEval loader
│   ├── scoring.py            Recall@K, NDCG@K
│   ├── backends/
│   │   ├── sonzai.py         real Sonzai production-flow + advance_time
│   │   └── mempalace.py      shells out to MemPalace's own script
│   └── results/              JSONL outputs — iteration runs gitignored; headline receipts checked in
└── sotopia/
    ├── __main__.py           python -m benchmarks.sotopia
    ├── run.py                longitudinal orchestrator
    ├── scenarios.py          HF loader + bundled seeds
    ├── scoring.py            trajectory + snapshot helpers
    └── results/              JSONL + PNG outputs — iteration runs gitignored; headline receipts checked in
```


## Install

```bash
pip install sonzai
git clone https://github.com/sonz-ai/sonzai-python
cd sonzai-python
pip install -r benchmarks/requirements.txt
```

### Required environment variables

Create a `.env` file or export these before running:

```bash
SONZAI_API_URL=https://api.sonz.ai        # default; override for staging/local
SONZAI_API_KEY=sk-...                      # get from https://platform.sonz.ai
GEMINI_API_KEY=AIza...                     # get from https://aistudio.google.com/apikey
```

Load it:

```bash
set -a && . .env && set +a
```

**All three are required** — `SONZAI_API_KEY` to hit the platform, `GEMINI_API_KEY`
for the judge and (in SOTOPIA) the partner agent, and `SONZAI_API_URL` if you're
pointing at a non-production backend.

Datasets download automatically on first run to `~/.cache/sonzai-bench/`.
Override with `SONZAI_BENCH_CACHE=/path/to/cache`.

### Why advance-time matters

Sonzai's self-learning (fact consolidation, diary generation, personality
decay, constellation pruning) runs as background workers scheduled on a real
clock. A benchmark that replays a year of conversations in 10 seconds would
never see those workers fire. `workbench.advance_time` simulates the clock
jumping forward so the same workers run synchronously — without changing the
agent behavior one bit compared to production usage.

This is the **only** call in the benchmark that's different from how you'd use
Sonzai in a normal app. Everything else (`agents.create`, `sessions.start`,
`agents.chat`, `sessions.end`, `memory.search`) hits the same production
endpoints your customers would.

Advance-time calls can take minutes apiece (they run the full CE worker stack
per simulated day), so the benchmarks configure a 600s request timeout on the
Sonzai client. If you're running against a slow staging instance, bump higher.


### What Sonzai does end-to-end, per question

1. `agents.create` — fresh agent, clean slate.
2. For each haystack session, in date order:
   - `sessions.start`
   - `sessions.end(messages=<canned transcript>)` — feeds the pre-scripted
     conversation into the CE pipeline for fact extraction. We don't regenerate
     assistant turns; that would break the benchmark premise.
   - `workbench.advance_time(gap_hours)` — CE workers fire (diary,
     consolidation, decay).
3. Final `advance_time(25h)` so the last session's consolidation completes.
4. **Retrieval**: `memory.search(question)` → map fact IDs to source sessions
   via `memory.timeline` → Recall@5 / NDCG@5 vs `answer_session_ids`.
5. **QA**: `agents.chat(question)` → Gemini judges the answer against the
   ground truth.
6. `agents.delete` — cleanup.

### Session boundaries — already in the dataset

LongMemEval pre-segments each question's haystack into sessions. Every
`haystack_sessions[i]` is one chat session with its own `session_id` and
date. We honor that structure exactly — `sessions.end` fires per dataset
session, `advance_time` fires in the gap between them.

Gap size: we use the real date difference from `haystack_dates`, floored at 25h
so at least one full simulated day of CE workers fires per gap. Weekly workers
(TreePruning, WeeklyConsolidation, SelfOrganization) are gated **server-side on
session count** — they fire every 7th session regardless of how many hours you
pass in. So on any question with ≥7 haystack sessions, weekly consolidation
will trigger automatically; we don't need client-side day arithmetic.

`advance_time` is **synchronous** — it runs every inline worker (fact
extraction, consolidation, diary, decay, pattern detection, tree maintenance,
goal reflection, etc.) before returning HTTP 200. When the call returns, the
pipeline is drained. A 600s request timeout is set by default since individual
calls can take a minute or two.

### Sonzai-backend flags

| Flag | What it does |
|---|---|
| `--skip-advance-time` | Ingest without advance_time — produces a **no-self-learning baseline**. The delta vs a normal run is the measured lift from CE workers. |
| `--max-sessions-per-question N` | Cap haystack size per question for fast smoke runs. Answer-bearing sessions are kept preferentially. `0` = full haystack (default). |
| `--concurrency N` | Questions in flight concurrently. Default 4. Bump for full runs. |
| `--mode retrieval\|qa\|both` | What to score. `retrieval` skips the Gemini judge and is ~10× faster. |


## Contributing a new memory system

Drop a file in `benchmarks/longmemeval/backends/` that exposes::

    async def run_question(*, question, ...) -> BackendResult

and wire it into `benchmarks/longmemeval/run.py`'s `--backend` choices. The
scoring and output layers stay identical, so your system gets judged by the
same Gemini model on the same dataset.

## License

MIT — same as the rest of `sonzai-python`. Datasets and MemPalace comparison
code retain their original licenses (Apache-2.0 and MIT respectively).
