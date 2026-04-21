# Sonzai benchmark suite

Open-source benchmarks for the [Sonzai Mind Layer](https://sonz.ai). Reproducible,
runnable by anyone with a Sonzai API key. Two benchmarks ship here:

| Benchmark | What it measures | Comparison |
|-----------|------------------|------------|
| **LongMemEval** | Memory recall + end-to-end QA over 500 long-horizon conversations | Head-to-head vs MemPalace |
| **SOTOPIA longitudinal** | Social intelligence trajectory across 30 sessions with the same user | Self-vs-self (session 1 vs 10 vs 30) |

Both benchmarks are graded by **Gemini 3.1 Flash Lite** — third-party neutral,
no Anthropic or OpenAI model judges a system that might depend on them.

## What makes this different

Benchmarks hit **real Sonzai production endpoints**: `agents.create`,
`sessions.start/end`, `agents.chat`, `memory.search`. The only difference
between the benchmark flow and normal Sonzai usage is a single call to
`workbench.advance_time` between sessions. That call runs the production CE
workers (diary, consolidation, personality-decay) as if simulated time had
passed — without it, self-learning only fires on the real clock.

If you replace `advance_time` with `time.sleep`, the benchmarks still pass —
they'd just take days.

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

**Metrics reported**:

- **QA accuracy** — primary, apples-to-apples head-to-head metric. Both systems
  produce an answer (Sonzai via `agents.chat`; MemPalace via Gemini reader over
  its top-k retrieved sessions) and both are graded by the same Gemini judge.
- **Session Recall@5 / NDCG@5** — meaningful for MemPalace (it stores sessions
  verbatim). Sonzai extracts atomic facts, so session IDs aren't always
  populated on retrieved items; reported only when the backend produces them.
- **Fact Recall@5 / NDCG@5** — meaningful for Sonzai (fact-based retrieval).
  A retrieved fact counts as a hit if its text contains the ground-truth
  answer after normalization.

The per-question-type breakdown (`single-session-user`, `temporal-reasoning`,
`multi-session`, etc.) is reported for QA accuracy — that's the fair axis for
comparing very differently-architected systems.

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
with the **same user** across N sessions (default 30), with `advance_time`
between sessions.

If self-learning is real, later sessions should score higher — same agent, same
partner, more shared history.

```bash
# Smoke: 4 scenarios × 10 sessions each
python -m benchmarks.sotopia --scenarios 4 --sessions-per-scenario 10 \
    --snapshot-at 1,5,10

# Full: 20 scenarios × 30 sessions (slow — many hours of API time)
python -m benchmarks.sotopia --scenarios 20 --sessions-per-scenario 30 \
    --snapshot-at 1,10,30
```

**Output**:
- `benchmarks/sotopia/results/sotopia_<ts>.jsonl` — one row per (scenario, session_index).
- `benchmarks/sotopia/results/sotopia_<ts>_trajectory.png` — matplotlib chart
  showing each of the 7 dimensions across sessions 1 → N, averaged across
  scenarios.
- stdout table at the snapshot indices.

**Headline metric**: `Δoverall` between session 1 and session 30. Expected
direction: positive. Flat trajectory means self-learning isn't helping; a
downward trend is a regression.

**Scenario source**: pulled from the canonical
[`cmu-lti/sotopia`](https://huggingface.co/datasets/cmu-lti/sotopia) HuggingFace
dataset, filtered to cooperative / longitudinal-friendly scenarios. A small
bundled seed set is used if HF is unreachable.

**Partner agent**: plays the non-Sonzai side. Also powered by Gemini 3.1 Flash
Lite (same model as the judge, separate prompt) so the only variable across
session 1 → 30 is Sonzai's side.

## Cost and time

Ballpark per 1 full-limit run (all 500 LongMemEval questions OR 20 scenarios ×
30 sessions):

| | LongMemEval | SOTOPIA longitudinal |
|---|---|---|
| API calls | ~30K | ~50K |
| Wall time @ concurrency 8 | 2–4 hours | 4–8 hours |
| Sonzai cost (order-of-magnitude) | $10–50 | $30–100 |
| Gemini cost | ~$1 | ~$5 |

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
