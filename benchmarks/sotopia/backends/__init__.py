"""Pluggable backends for the SOTOPIA longitudinal benchmark.

Each backend pairs a memory system (Sonzai, MemPalace, …) with a matching
chat loop so the scenario runner can swap the system under test without
changing the harness. The judge, scoring, and output writers live one level
up in :mod:`benchmarks.sotopia` and are backend-agnostic.
"""
