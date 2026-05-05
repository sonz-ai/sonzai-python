"""Memory builders for the LIFELONG-SOTOPIA baseline backend.

The paper compares "simple" (full prior interaction history) and "advanced"
(per-episode 200-300 word summary). We support both, plus a ``none`` floor.
The Sonzai backend does not use this module — Sonzai *is* the memory layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

MemoryMode = Literal["none", "summary", "full-history"]


@dataclass
class EpisodeMemoryEntry:
    episode_index: int           # 0-based
    scenario_codename: str
    summary: str = ""
    transcript_text: str = ""    # rendered "Speaker: line\n..." form


@dataclass
class MemoryStore:
    """Append-only list of per-episode entries for one (pair, run)."""

    _entries: list[EpisodeMemoryEntry] = field(default_factory=list)

    def append(self, entry: EpisodeMemoryEntry) -> None:
        self._entries.append(entry)

    def entries(self) -> list[EpisodeMemoryEntry]:
        return list(self._entries)


def build_memory_block(store: MemoryStore, *, mode: MemoryMode) -> str:
    """Render the memory store into the prompt block expected by ``agent_turn_async``.

    - ``none`` → constant neutral string. The agent gets no prior context.
    - ``summary`` → numbered list of per-episode summaries.
    - ``full-history`` → numbered list of per-episode FULL transcripts plus
      summaries.
    """
    if mode not in ("none", "summary", "full-history"):
        raise ValueError(f"unknown memory mode: {mode!r}")

    entries = store.entries()
    if mode == "none" or not entries:
        return "(no prior episodes — this is the first episode of the arc)"

    parts: list[str] = []
    for i, e in enumerate(entries, start=1):
        header = f"Episode {i} ({e.scenario_codename})"
        if mode == "summary":
            parts.append(f"{header}:\n{e.summary or '(no summary available)'}")
        else:  # full-history
            body = e.transcript_text or "(transcript unavailable)"
            sumr = e.summary or "(no summary available)"
            parts.append(f"{header}:\nSummary: {sumr}\nTranscript:\n{body}")
    return "\n\n".join(parts)
