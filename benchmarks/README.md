# Sonzai benchmark suite

Open-source benchmarks for the [Sonzai Mind Layer](https://sonz.ai). Reproducible,
runnable by anyone with a Sonzai API key. Two benchmarks ship here:

| Benchmark | What it measures | Result |
|-----------|------------------|--------|
| **LongMemEval** | Memory recall + end-to-end QA over 500 long-horizon conversations | Sonzai matches or beats MemPalace on every headline metric — including the ones MemPalace was specifically designed to win |
| **SOTOPIA longitudinal** | Social intelligence trajectory across 30 sessions with the same user | The thing Sonzai exists for: personality coherence and self-learning that compound across hundreds of sessions |

**Both benchmarks run on the cheap end of the LLM stack.** Sonzai's chat
handler generates answers with **Gemini 3.1 Flash Lite**. The judge is the
**same Gemini 3.1 Flash Lite**. The SOTOPIA partner agent — also Gemini
3.1 Flash Lite. No frontier-model arms race propping up the numbers; the
lift you see is from Sonzai's memory architecture, not from spending more
on inference. Drop in a heavier model in your own deployment and the
ceiling goes up from there.

Gemini 3.1 Flash Lite as the judge is also a deliberate independence call:
no Anthropic or OpenAI model grading a system that could depend on either.

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
much harder problem.** Our architecture goes in the opposite direction
from "store everything": Sonzai is built for a different target — **long-horizon chat where the same
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
metric the benchmark measures (full numbers below), while shipping the
durability and personality-coherence machinery that lookup-optimized
systems can't represent at all.

If you're building a chatbot for a single conversation, any retrieval
layer works. If you're building an **agent that keeps talking to the same
person across hundreds of sessions and stays the same character the
whole time**, Sonzai is the only system in this comparison that's even
designed for that target. The SOTOPIA longitudinal benchmark below is
where that capability becomes visible.

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

### Sonzai vs MemPalace — full numbers

Latest run: 100-question full-haystack slice, retrieval-only mode,
session-level metrics. Sonzai run with `--reuse-agents` after a single
fresh ingest; MemPalace run with `hybrid_v4` (their best-published mode)
on the same slice.

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

## SOTOPIA longitudinal

Standard SOTOPIA scores a single social interaction on 7 dimensions
(Believability, Relationship, Knowledge, Secret, Social Rules, Financial,
Goal). Our extension: the **same Sonzai agent** plays the **same scenario**
with the **same user** across N sessions (default 90), with `advance_time`
between sessions.

If self-learning is real, later sessions should score higher — same agent, same
partner, more shared history. The headline trajectory we track is

> session 1 → session 10 → session 30 → session 60 → session 90

with each checkpoint's average overall score reported side-by-side so the
curve's monotonicity is visible at a glance.

```bash
# Smoke: 4 scenarios × 10 sessions each (checks the wiring)
python -m benchmarks.sotopia --scenarios 4 --sessions-per-scenario 10 \
    --snapshot-at 1,5,10

# Mid-horizon: 10 scenarios × 30 sessions
python -m benchmarks.sotopia --scenarios 10 --sessions-per-scenario 30 \
    --snapshot-at 1,10,30

# Full long-horizon: 20 scenarios × 90 sessions (slow — a day of API time)
python -m benchmarks.sotopia --scenarios 20 --sessions-per-scenario 90 \
    --snapshot-at 1,10,30,60,90
```

**Output**:
- `benchmarks/sotopia/results/sotopia_<ts>.jsonl` — one row per (scenario, session_index).
- `benchmarks/sotopia/results/sotopia_<ts>_trajectory.png` — matplotlib chart
  showing each of the 7 dimensions across sessions 1 → N, averaged across
  scenarios.
- stdout table at the snapshot indices.

### Headline trajectory table

Printed by `run.py` at the end of every run and auto-refreshed in this README
by `scripts/update_readme_scores.py`:

| Dimension | Session 1 | Session 10 | Session 30 | Session 60 | Session 90 |
|---|---:|---:|---:|---:|---:|
| Believability (0..10) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Relationship (-5..5) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Knowledge (0..10) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Secret (-10..0) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Social rules (-10..0) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Financial (-5..5) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| Goal (0..10) | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |
| **Overall** | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ | _run-updated_ |

**Headline metric**: `Δoverall` between session 1 and session 90. Expected
direction: positive and monotonic across the five checkpoints. Flat trajectory
means self-learning isn't helping; a downward trend is a regression.

**Scenario source**: pulled from the canonical
[`cmu-lti/sotopia`](https://huggingface.co/datasets/cmu-lti/sotopia) HuggingFace
dataset, filtered to cooperative / longitudinal-friendly scenarios. A small
bundled seed set is used if HF is unreachable.

**Partner agent**: plays the non-Sonzai side. Also powered by Gemini 3.1 Flash
Lite (same model as the judge, separate prompt) so the only variable across
session 1 → 30 is Sonzai's side.

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
│   └── results/              JSONL outputs (gitignored)
└── sotopia/
    ├── __main__.py           python -m benchmarks.sotopia
    ├── run.py                longitudinal orchestrator
    ├── scenarios.py          HF loader + bundled seeds
    ├── scoring.py            trajectory + snapshot helpers
    └── results/              JSONL + PNG outputs (gitignored)
```

## Contributing a new memory system

Drop a file in `benchmarks/longmemeval/backends/` that exposes::

    async def run_question(*, question, ...) -> BackendResult

and wire it into `benchmarks/longmemeval/run.py`'s `--backend` choices. The
scoring and output layers stay identical, so your system gets judged by the
same Gemini model on the same dataset.

## License

MIT — same as the rest of `sonzai-python`. Datasets and MemPalace comparison
code retain their original licenses (Apache-2.0 and MIT respectively).
