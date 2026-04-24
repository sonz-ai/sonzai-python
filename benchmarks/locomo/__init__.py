"""LoCoMo benchmark — Sonzai vs mem0 on long-term conversational memory.

Dataset: https://github.com/snap-research/locomo (10 dialogues, 19–35 sessions
each, 300–600 turns). Invoke via::

    python -m benchmarks.locomo --backend sonzai --limit 2
    python -m benchmarks.locomo --backend mem0 --limit 2
    python -m benchmarks.locomo --compare results/sonzai_*.jsonl results/mem0_*.jsonl

See benchmarks/locomo/dataset.py for the data shape and
docs/superpowers/specs/2026-04-24-locomo-benchmark-design.md for the full
evaluation protocol.
"""
