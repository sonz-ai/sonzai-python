"""LIFELONG-SOTOPIA benchmark — multi-episode social intelligence over diverse scenarios.

Implements Goel & Zhu (2025) "LIFELONG SOTOPIA: Evaluating Social Intelligence
of Language Agents Over Lifelong Social Interactions" — https://arxiv.org/abs/2506.12666

Where standard SOTOPIA grades a single interaction and our existing
``benchmarks/sotopia/`` repeats the *same* scenario across N sessions,
LIFELONG-SOTOPIA gives the same character pair a *different* scenario each
episode (sampled by relationship type) across ~40 episodes. Headline finding
in the paper: Goal and Believability decline across the 40-episode arc; an
"advanced" memory technique (per-episode 200-300 word summary) helps but the
best agents still trail humans on scenarios that explicitly require recalling
prior episodes.

Invoke via::

    python -m benchmarks.lifelong_sotopia --pairs 2 --episodes-per-pair 10
"""
