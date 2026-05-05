"""Sonzai open-source benchmark suite.

Four benchmarks ship here:

- ``longmemeval`` — head-to-head recall/QA against MemPalace on the 500-question
  LongMemEval dataset.
- ``sotopia`` — longitudinal social-intelligence benchmark that runs the same
  Sonzai agent across N sessions per scenario to showcase self-learning lift.
- ``lifelong_sotopia`` — Goel & Zhu 2025: multi-episode social intelligence
  over varied scenarios; tests whether the memory layer prevents decline.
- ``locomo`` — head-to-head LLM-judge accuracy against mem0 on the 1540-QA
  LoCoMo conversational-memory dataset.

Each benchmark is invoked as ``python -m benchmarks.<name>``.
"""

from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv_if_present() -> None:
    # Walk up from this file looking for a .env; shell env wins over the file.
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        dotenv = candidate / ".env"
        if dotenv.is_file():
            for raw in dotenv.read_text().splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
            return


_load_dotenv_if_present()
