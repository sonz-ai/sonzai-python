"""Sonzai open-source benchmark suite.

Three benchmarks ship here:

- ``longmemeval`` — head-to-head recall/QA against MemPalace on the 500-question
  LongMemEval dataset.
- ``sotopia`` — longitudinal social-intelligence benchmark that runs the same
  Sonzai agent across N sessions per scenario to showcase self-learning lift.

Each benchmark is invoked as ``python -m benchmarks.<name>``.
"""
