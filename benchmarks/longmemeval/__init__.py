"""LongMemEval benchmark runner.

Runs the same 500-question recall + QA benchmark MemPalace reports on, but
using real Sonzai production endpoints end-to-end. A ``--backend mempalace``
flag runs MemPalace's own memory system through the identical scoring pipeline
for head-to-head comparison.

Invoke via::

    python -m benchmarks.longmemeval --backend sonzai --limit 20
    python -m benchmarks.longmemeval --backend mempalace --limit 20
    python -m benchmarks.longmemeval --compare   # diff two JSONL result files
"""
