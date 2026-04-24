# LongMemEval Error-Analysis Harness

The harness turns bench JSONL output into CI-tight per-subtype metrics plus a
markdown failure report. Three commands form the workflow:

## Usage

```bash
# 1. Run the bench N times with fresh agents per question.
#    Default N=5 gets multi-session CI to roughly ±9pp. Use 10 for ±6pp.
./run_loop.sh 5

# 2. Aggregate — per-subtype accuracy with Wilson 95% CI, flip rate, and
#    a failure classification into four buckets.
python -m benchmarks.longmemeval.aggregate \
    results/sonzai_YYYYMMDD-HHMMSS_run*.jsonl \
    --output failures.json

# 3. Inspect — expand the failures into a readable markdown report.
python -m benchmarks.longmemeval.inspect \
    --failures failures.json \
    --output report.md
```

## Failure buckets

Each failing `(question, run)` pair is classified into one of four buckets,
each pointing at a distinct intervention class:

| Bucket | Meaning | Intervention class |
|---|---|---|
| `retrieval-miss` | No expected session ID in top-10 | Retrieval-side (decomposition, graph walks) |
| `retrieval-hit / qa-miss` | Right session retrieved, wrong answer | Composition-side (ensemble, prompting) |
| `marginal` | Expected session at rank 8–9 | Render-cap / ordering |
| `ambiguous` | Judge rationale suggests defensible answer | None — judge noise |

The `ambiguous` bucket uses a string-match heuristic on the judge rationale
(phrases like "partially", "defensible", "close to"). It's imperfect by
design; review those cases manually.

## Why fresh agents

`run_loop.sh` refuses to forward `--reuse-agents`: reusing agents pollutes
memory across runs, invalidating the independence assumption of multi-run
CI. See the 0.233 → 0.667 multi-session swing observed before/after the
agent-isolation fix landed.

## Confidence intervals

Wilson score 95% CI is used over Normal approximation because at n=30
subtype level (LongMemEval-S's multi-session slice), Normal extends outside
[0,1] at extreme p. Wilson stays in [0,1] by construction.

## Caveats

- **Markdown injection from LLM text.** Bench fields `question`, `agent_answer`,
  and `qa_rationale` flow into the report verbatim. A backtick or leading
  `#` in LLM output can cosmetically disturb adjacent rendering. This is a
  dev-internal tool — do not share `report.md` externally without reviewing
  for injected markup.
- **Fresh-agent requirement.** The multi-run CI assumes inter-run independence.
  Anything that threads state (reused agents, shared caches, persistent
  memory across runs) invalidates the Wilson interval.

## What's next

Run the harness. Read `report.md`. The bucket that dominates the failure
distribution determines which next-layer design to execute. See
`docs/superpowers/specs/2026-04-24-multi-session-qa-retrieval-planner-design.md`
for the intervention that follows if `retrieval-miss` dominates.
