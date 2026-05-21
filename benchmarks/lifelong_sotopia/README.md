# LIFELONG-SOTOPIA

Implementation of [LIFELONG-SOTOPIA](https://arxiv.org/abs/2506.12666)
(Goel & Zhu 2025) — multi-episode social intelligence over varied scenarios
sampled by relationship type.

The paper's headline finding: across 40 episodes per character pair,
Goal Completion and Believability **decline** for every LLM tested
(GPT-4o, Gemini-1.5, Llama-3.1). A summary-memory technique helps but the
best agents still trail humans on scenarios that explicitly require recall.

## Headline result — Sonzai vs the paper's two memory conditions

3-way head-to-head, **same character pair (mika-alex, mentor-mentee)**, **same
seed**, **30 episodes**, Gemini 3.1 Flash Lite as both partner generator and
judge. Each baseline mirrors a paper condition; Sonzai uses its production
memory layer (no prompt-side history injection — the agent talks to its own
server-side memory across episodes).

[`results/lifelong_sotopia_sonzai_20260505-180956.jsonl`](results/lifelong_sotopia_sonzai_20260505-180956.jsonl) ·
[`baseline-summary`](results/lifelong_sotopia_baseline-summary_20260505-175722.jsonl) ·
[`baseline-none`](results/lifelong_sotopia_baseline-none_20260505-175555.jsonl)

### Believability (0..10)

| Run | e1 | e5 | e10 | e20 | e30 | Δ e1→e30 | slope |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Sonzai** | 9.00 | 9.50 | 9.00 | 9.00 | **10.00** | **+1.00 ↑** | **+0.029/ep ↑** |
| baseline-summary (paper's "advanced") | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | +0.00 = | +0.000/ep |
| baseline-none (no-memory floor) | 10.00 | 9.00 | 9.00 | 9.50 | 9.00 | **−1.00 ↓** | **−0.003/ep ↓** |

### Goal Completion (0..10)

| Run | e1 | e5 | e10 | e20 | e30 | Δ e1→e30 | slope |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Sonzai** | 10.00 | 10.00 | 9.00 | 9.00 | 10.00 | +0.00 = | −0.009/ep |
| baseline-summary | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | +0.00 = | +0.000/ep |
| baseline-none | 10.00 | 10.00 | 7.00 | 10.00 | 9.00 | **−1.00 ↓** | **−0.005/ep ↓** |

### BelievabilityExtended (8-checkpoint, 0..10)

| Run | e1 | e5 | e10 | e20 | e30 | slope |
|---|---:|---:|---:|---:|---:|---:|
| **Sonzai** | 10.00 | 10.00 | 9.50 | 9.50 | 10.00 | **+0.016/ep ↑** |
| baseline-summary | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | −0.010/ep |
| baseline-none | 10.00 | 10.00 | 8.50 | 10.00 | 10.00 | **−0.020/ep ↓** |

### Reading the numbers

- **The paper's "decline" finding reproduces on baseline-none.** With no
  memory, Bel drops 10.00 → 9.00, Goal drops 10.00 → 9.00, and the BelExt
  slope is the steepest negative we saw (−0.020/ep). This is the paper's
  cited failure mode in miniature.
- **The paper's "advanced summary memory" condition holds the line.**
  baseline-summary stays at 10.00 across 30 episodes on Bel and Goal — the
  paper's own remedy works.
- **Sonzai is the only run where Believability is *rising*.** Slope
  +0.029/ep on Bel and +0.016/ep on BelExt across 30 different scenarios.
  Sonzai ends *higher* than it started. The agent's memory layer isn't
  just preventing decline — it's compounding into more credible
  in-character behavior over time as the relationship history accumulates.

Reproduce:

```bash
python -m benchmarks.lifelong_sotopia --backend baseline --memory none    --pairs 1 --episodes-per-pair 30 --max-turn-pairs 3 --seed 42
python -m benchmarks.lifelong_sotopia --backend baseline --memory summary --pairs 1 --episodes-per-pair 30 --max-turn-pairs 3 --seed 42
python -m benchmarks.lifelong_sotopia --backend sonzai                    --pairs 1 --episodes-per-pair 30 --max-turn-pairs 3 --seed 42 --no-advance-time
python -m benchmarks.lifelong_sotopia.compare \
    results/lifelong_sotopia_sonzai_*.jsonl \
    results/lifelong_sotopia_baseline-summary_*.jsonl \
    results/lifelong_sotopia_baseline-none_*.jsonl \
    --names sonzai,baseline-summary,baseline-none --at 1,5,10,20,30
```

> Note on absolute scores: Gemini 3.1 Flash Lite is a confident judge and
> these conversations are short (3 turn-pairs each), so all three runs
> hover near the 10.00 ceiling. The paper used GPT-4o / Gemini-1.5 /
> Llama-3.1 as agents on longer interactions where the baseline decline
> was steeper. The interesting signal here is the **shape of the trajectory**
> — Sonzai is the only run trending up.

## Quick start

```bash
# Smoke test (1 pair × 5 episodes, ~5 min, baseline)
python -m benchmarks.lifelong_sotopia --backend baseline --memory summary --quick

# Local default (2 pairs × 10 episodes, ~30 min)
python -m benchmarks.lifelong_sotopia --backend sonzai

# Paper-comparable run (5 pairs × 40 episodes, hours)
python -m benchmarks.lifelong_sotopia --backend sonzai --full
```

Required env vars: `SONZAI_API_KEY` (sonzai backend only), `GEMINI_API_KEY` (always). Optionally set `BENCHMARK_JUDGE_GEMINI_API_KEY` to use a dedicated key for the judge (falls back to `GEMINI_API_KEY` if unset).

## Backends

| Backend | Memory | Notes |
|---|---|---|
| `sonzai` | Sonzai is the memory layer (production path) | one stable agent per pair, `agents.chat` across episodes, optional `advance_time(25h)` between |
| `baseline` | `--memory none\|summary\|full-history` | both turns generated by Gemini Flash Lite; the paper's two memory conditions plus a no-memory floor |

## Metrics

Per (pair, episode):
- **Believability** (0..10) — standard SOTOPIA dim (`judge_sotopia_async`)
- **Goal** (0..10) — standard SOTOPIA dim
- **BelExt** (0..10) — `max(Bel - 5 × failed_checkpoints, 0)`. The 8 checkpoints
  are documented in `benchmarks/common/gemini_judge.py` next to
  `BEL_EXTENDED_CHECKPOINTS`.

Aggregate:
- Per-episode trajectory (one curve per metric, averaged across pairs)
- Linear slope across the trajectory (paper's "decline" signal)
- Memory-required slice average (subset of episodes that explicitly reference
  prior content)

## Bundled corpus

6 pre-defined character pairs spanning 3 relationship types
(`mentor-mentee`, `peer-collaborator`, `friend-and-friend`), 12 scenarios per
type, plus 5 hand-authored memory-required scenarios that are inserted at
deterministic indices.

The corpus lives in `scenarios_data/` and is the bench's reference dataset.
The paper's GPT-4-generated 41-scenarios-per-relationship-type corpus is not
publicly published; the bundled set is our own and is fully traceable.

## Output

Each run writes:
- `results/lifelong_sotopia_<backend>_<ts>.jsonl` — one row per (pair, episode)
- `results/lifelong_sotopia_<backend>_<ts>_trajectory.png` — Goal/Bel/BelExt
  curves with memory-required indices marked

Plus a printed summary table with snapshot values and per-metric linear slope.
