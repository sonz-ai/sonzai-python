# LIFELONG-SOTOPIA benchmark design

**Status:** design draft, awaiting user review
**Date:** 2026-05-04
**Target:** add `benchmarks/lifelong_sotopia/` — a runnable, reproducible
implementation of [LIFELONG-SOTOPIA](https://arxiv.org/abs/2506.12666) (Goel
& Zhu, June 2025), evaluating Sonzai (and comparison memory backends) against
the paper's multi-episode social-intelligence rubric.

## Motivation

The existing `benchmarks/sotopia/` runs the **same scenario** N times to
measure relationship-deepening. LIFELONG-SOTOPIA is the opposite design:
**different scenario per episode**, sampled by relationship type, across
~40 episodes per character pair. The paper's headline finding is that all
tested LLMs (GPT-4o, Gemini-1.5, Llama-3.1) show **declining** Goal and
Believability across the 40-episode arc; the "advanced" memory technique
(per-episode 200-300-word summary) helps but the best agents still trail
humans on scenarios that explicitly require recalling prior episodes.

The two benchmarks measure complementary things:

| Bench | Scenario across sessions | What it measures |
|---|---|---|
| `sotopia/` (existing) | same | relationship deepening, callbacks, identity coherence under repetition |
| `lifelong_sotopia/` (new) | different (sampled by relationship type) | does social skill *degrade* across diverse interactions? does memory help? |

Adding the new bench gives Sonzai a venue to demonstrate the second
property — the paper's cited "decline" phenomenon is something a
production memory layer should resist, and we want a published-rubric
number to point at.

## Key decisions

### 1. Separate top-level benchmark, not a flag on `sotopia/`

`benchmarks/lifelong_sotopia/` parallels the existing benchmark layout
(`run.py`, `__main__.py`, `scenarios.py` or `dataset.py`, `scoring.py`,
`backends/`, `tests/`, `results/`). Reasons:

- **Different headline metrics**: per-episode trajectory of {Goal, Bel,
  BelExt} vs the existing sotopia's snapshot-at-{1,10,30}. Mixing them in
  one CLI obscures both.
- **Different reuse semantics**: this bench iterates *scenarios per
  episode*, not *sessions per scenario*. The pinned-agent / resume-from-
  session machinery needs different keys ("pair_id × episode_index" not
  "scenario_id × session_index").
- **Different output shape**: LIFELONG-SOTOPIA reports per-episode and
  per-relationship-type curves; existing sotopia reports per-dim snapshot.
- **Maps 1:1 to a paper**: gives an obvious citation hook in the
  benchmarks README, which mirrors how LoCoMo/LongMemEval are structured.

Shared code lives in `benchmarks/common/` (gemini_judge primitives,
agent_reuse, sdk_extras). Where the existing sotopia runner has helpers
worth lifting (e.g. partner-prompt summary stitching), they get reused via
import — no duplication.

### 2. Dataset = SOTOPIA characters + relationships + bundled scenarios

The paper uses the SOTOPIA database's 40 characters and 90 relationships,
generates 41 scenarios per relationship type via GPT-4 few-shot, and
samples episodes for each pair from those scenarios (filtered to the
pair's relationship type).

Our implementation:

- **Characters and relationships**: load from `cmu-lti/sotopia` HF dataset
  (already a dependency in `sotopia/scenarios.py`). Same loader pattern.
- **Scenarios**: ship a **bundled, pre-generated scenario corpus** in the
  repo at `benchmarks/lifelong_sotopia/scenarios/<relationship_type>.json`
  — ~10-15 scenarios per type (smaller than paper's 41, sufficient for the
  default 10-episode local default and any meaningful slice). Bundling
  avoids a hard runtime dependency on a frontier-model API call.
- **Bundled corpus size**: 12 scenarios per relationship type, ≥3
  relationship types (mentor-mentee, peer-collaborator, friend-and-friend
  at minimum). Enough to cover `--full` (40 episodes per pair) by random
  sampling with replacement; deduplication-by-scenario-id within a pair
  ensures no episode repeats unless the corpus is exhausted.
- **`--regenerate-scenarios` flag**: re-derives the scenario corpus by
  prompting Gemini with SOTOPIA few-shot examples per relationship type.
  Reproduces the paper's generation step but is opt-in (costs API calls).
  The default is to use the bundled corpus, which keeps the bench
  byte-for-byte reproducible across runs.
- **No reliance on a paper-shipped artifact**: the paper does not publish
  a dataset URL. Bundled scenarios are our own, traceable to the SOTOPIA
  source characters/relationships.

### 3. Two memory conditions, both implemented

The paper compares "simple" (full prior history) vs "advanced" (200-300
word per-episode summary). We need both, because (a) the comparison is
the paper's headline experiment, and (b) Sonzai's value prop is replacing
*both*.

- **`--memory full-history`**: every prior episode's full transcript is
  stitched into the agent prompt. Baseline floor (and what the paper
  shows degrades).
- **`--memory summary`** (default for non-Sonzai backends): per-episode
  200-300 word summary generated by the same Gemini judge using the
  paper's three-aspect template (overview / negotiation techniques / new
  info about partner). Stored in-memory, accumulated across episodes.
- **`--memory none`**: pure no-memory baseline; agent gets only the
  current scenario. Useful as a floor to interpret deltas.

For the **Sonzai backend** the memory condition is not user-selected —
Sonzai *is* the memory layer. The agent talks to its own production
memory across episodes (via `agents.chat` keyed on a stable
`{pair_id}` user_id). The summary/full-history paths exist for the
generic Gemini-only baseline runners (and the mempalace/mem0 backends
as appropriate).

### 4. Scoring: Bel, Goal, BelExt — the paper's three signals

Implemented in `lifelong_sotopia/scoring.py`:

- **Believability (0..10)** — reuses the existing `judge_sotopia_async`
  in `common/gemini_judge.py`. We extract just the `believability` field.
- **Goal (0..10)** — same path, extract the `goal` field.
- **BelievabilityExtended (0..10)** — **new** judge in
  `common/gemini_judge.py`. An 8-item checkpoint checklist:
  1. **No verbatim repetition** of prior turns
  2. **Character consistency** (no drift in stated facts/preferences)
  3. **No stalling** (every turn moves the conversation)
  4. **No mode collapse** to a single response shape
  5. **Appropriate emotional register** for the scenario
  6. **No unprompted confessions** of secrets / private info
  7. **Acknowledges scenario change** (doesn't reuse last episode's setup)
  8. **Stays in the agent's voice** (not the partner's)

  Formula: `BelExt = max(Bel - 5 * checkpoints_failed, 0)`. The judge
  returns `believability` *and* the 8 booleans; the formula is computed
  on the SDK side so it's verifiable / unit-testable.

  The 8-item list is the spec's single editorial choice — the paper
  describes the construct but does not enumerate every checkpoint
  publicly. The set above is faithful to the paper's stated failure
  modes (repetition, drift, stalling) and extended to the canonical
  SOTOPIA failure surface (secret, character voice, scenario-change
  acknowledgement).

### 5. The 5 "memory-required" scenarios

Hand-authored, inserted at deterministic indices computed as
`floor(N * f)` for `f ∈ {0.125, 0.25, 0.5, 0.75, 0.97}` where `N` is the
total episodes. For `--full` (N=40) → `[5, 10, 20, 30, 38]`; for the
default (N=10) → `[1, 2, 5, 7, 9]`; for `--quick` (N=5) → `[0, 1, 2, 3, 4]`
(all 5). The first index is clamped to `>= 1` so the bench never opens
with a memory-required scenario (which would have nothing to recall).
Each scenario's setting starts with an explicit reference to a prior
episode:

> "Two episodes ago, Mika promised to share a Go puzzle with Alex. The
> current scenario takes place after that — Alex now wants to discuss it."

These scenarios provide the **memory-required slope**: the gap between
how an agent does on these vs the random-sampled scenarios at adjacent
indices is a direct measure of explicit-memory utility. They live in
`benchmarks/lifelong_sotopia/scenarios/memory_required.json`.

### 6. Default local slice + full-paper slice

| Mode | pairs | episodes/pair | est. runtime | use |
|---|---:|---:|---:|---|
| `--quick` | 1 | 5 | ~5 min | smoke / dev loop |
| (default) | 2 | 10 | ~30 min | local meaningful demo |
| `--full` | 5 | 40 | ~6h | published-rubric run |

The paper's full setup is 40 characters × scenarios per relationship
type. Running anywhere near that size requires CI infrastructure, so
the local default is calibrated to the same ~30-min budget as the
existing benchmarks' demo modes.

### 7. Backends

Mirror the existing `sotopia/backends/` layout:

- `backends/sonzai.py` — main path. Per-pair stable agent + user_id;
  agent observed across N episodes. Uses `agents.chat` directly (no
  `--memory` flag — Sonzai is the memory).
- `backends/baseline.py` — Gemini-only generator with selectable
  `--memory {none,summary,full-history}`. Implements the paper's two
  memory conditions for the apples-to-apples comparison the paper
  reports.
**v1 scope: sonzai + baseline only.** Mempalace and mem0 backends are
**deferred** to a follow-up. Rationale: the paper's headline experiment
is the *memory-condition* sweep (none / summary / full-history) on a
fixed generator, which `baseline.py` covers fully; cross-backend
comparison (Sonzai vs MemPalace vs mem0) is already extensively covered
by the existing `sotopia/` and `longmemeval/` benchmarks. Adding it here
would duplicate plumbing without testing a new claim.

### 8. Output schema

`results/lifelong_sotopia_<backend>_<ts>.jsonl` — one row per (pair,
episode):

```json
{
  "pair_id": "mika-alex",
  "relationship_type": "mentor-mentee",
  "episode_index": 7,
  "scenario_id": "ll-sotopia-mentor-007",
  "is_memory_required": false,
  "transcript": [...],
  "scores": {
    "believability": 8.5,
    "goal": 7.0,
    "bel_extended": 6.5,
    "checkpoints_failed": ["no_stalling"]
  },
  "judge_rationale": "..."
}
```

Plus a trajectory PNG with three lines (Goal, Bel, BelExt) averaged
across pairs, with the memory-required indices marked. And a printed
summary table:

```
=== LIFELONG-SOTOPIA trajectory (sonzai) ===
                e1     e5    e10
goal          8.50   8.25   8.00     slope -0.005/episode
bel           9.00   8.75   8.50     slope -0.005/episode
bel_ext       8.50   7.50   7.25     slope -0.014/episode
memory-req    7.00   7.50            (avg over indices 5,10)
```

### 9. CLI

```
python -m benchmarks.lifelong_sotopia [--backend sonzai|baseline|mempalace|mem0]
                                       [--memory none|summary|full-history]   # baseline only
                                       [--pairs N]                            # default 2
                                       [--episodes-per-pair N]                # default 10
                                       [--quick]                              # 1 × 5
                                       [--full]                               # 5 × 40
                                       [--regenerate-scenarios]
                                       [--include-memory-required]            # default true
                                       [--judge-model ...]
                                       [--output PATH]
                                       [--reuse-agents [PATH]]
                                       [-v]
```

### 10. Tests

`benchmarks/lifelong_sotopia/tests/`:

- `test_scenario_loader.py` — bundled scenarios load, character/
  relationship filtering works, memory-required interleaving honors the
  fixed indices.
- `test_scoring.py` — BelExt formula arithmetic (esp. floor at 0,
  failed-list parsing), trajectory aggregation, slope calculation.
- `test_runner.py` — integration test with a mocked judge fixture: 1
  pair × 3 episodes runs end-to-end, output jsonl shape verified.

Tests follow the same patterns as `benchmarks/locomo/tests/` and
`benchmarks/longmemeval/tests/` — fixtures dir, no live API calls.

## File layout

```
benchmarks/lifelong_sotopia/
├── __init__.py
├── __main__.py
├── README.md                          # bench-level reproduction notes
├── run.py                             # orchestrator + CLI
├── scenarios.py                       # loader + dataclasses
├── scoring.py                         # BelExt + trajectory + slope
├── scenarios/                         # bundled scenario corpus
│   ├── mentor-mentee.json
│   ├── ... (one per relationship type)
│   └── memory_required.json
├── backends/
│   ├── __init__.py
│   ├── sonzai.py                      # primary — Sonzai is the memory layer
│   └── baseline.py                    # Gemini-only with --memory {none,summary,full-history}
├── tests/
│   ├── fixtures/
│   │   └── mini_run.jsonl
│   ├── test_scenario_loader.py
│   ├── test_scoring.py
│   └── test_runner.py
└── results/                           # gitignored except .gitkeep
    └── .gitkeep
```

Plus:

- `benchmarks/common/gemini_judge.py` — add `BelExtScore` model and
  `judge_bel_extended_async()` function (the new 8-checkpoint judge).
- `benchmarks/README.md` — add a section.

## Out of scope

- Reproducing the paper's human-baseline study (no human in the loop
  here; the rubric is the same)
- Llama-3.1 / GPT-4o agent runs (we measure Sonzai vs the paper-style
  baselines; cross-LLM comparisons are not the point)
- Persisting scenario corpora across forks (regeneration is opt-in)

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Bundled scenarios drift from "what the paper would generate" | `--regenerate-scenarios` flag reproduces the generation step from SOTOPIA seeds; bundled set is documented as our reference corpus, not an authoritative dataset |
| Paper does not enumerate the 8 BelExt checkpoints | The 8-item list is documented inline in the spec and in the `judge_bel_extended_async` docstring; reviewers can argue with our list, the formula and the trajectory are still meaningful |
| 40-episode runs are expensive | Defaults are tuned for ~30-min local runs; `--full` is the published-paper-comparable mode |
| Sonzai backend mixes "Sonzai memory" with the paper's "baseline memory modes" categorically | The Sonzai backend is *one* condition, the baseline backend is *the other family of conditions*. Reported separately, never collapsed into one number. |
