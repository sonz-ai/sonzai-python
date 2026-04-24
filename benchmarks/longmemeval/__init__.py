"""LongMemEval benchmark runner + error-analysis harness.

Runs the same 500-question recall + QA benchmark MemPalace reports on, but
using real Sonzai production endpoints end-to-end. A ``--backend mempalace``
flag runs MemPalace's own memory system through the identical scoring pipeline
for head-to-head comparison.

Invoke the runner via::

    python -m benchmarks.longmemeval --backend sonzai --limit 20
    python -m benchmarks.longmemeval --backend mempalace --limit 20
    python -m benchmarks.longmemeval --compare   # diff two JSONL result files

The error-analysis harness layered on top turns bench JSONL into CI-tight
per-subtype metrics and markdown failure reports (see HARNESS.md)::

    ./run_loop.sh 5                                              # batch runs
    python -m benchmarks.longmemeval.aggregate results/*.jsonl   # metrics
    python -m benchmarks.longmemeval.inspect --failures f.json   # report
"""
