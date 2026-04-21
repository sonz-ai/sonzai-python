"""SOTOPIA longitudinal benchmark.

Standard SOTOPIA evaluates a single social-interaction scenario and produces a
7-dimension score. We extend it: the SAME Sonzai agent plays the SAME scenario
against the SAME user across N sessions (default 30), with ``advance_time``
between sessions so consolidation, diary, and personality evolution fire.

We report the score trajectory across sessions 1 → 30 and snapshot values at
{1, 10, 30} to show the lift from self-learning. A flat trajectory means
self-learning isn't helping; a rising one is the headline result.

Invoke via::

    python -m benchmarks.sotopia --scenarios 20 --sessions-per-scenario 30
"""
