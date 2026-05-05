"""Tests for baseline-backend memory builders."""

from __future__ import annotations

import pytest

from benchmarks.lifelong_sotopia.memory import (
    EpisodeMemoryEntry,
    MemoryStore,
    build_memory_block,
)


def _entry(idx: int, summary: str, transcript: str = "") -> EpisodeMemoryEntry:
    return EpisodeMemoryEntry(
        episode_index=idx,
        scenario_codename=f"sc-{idx}",
        summary=summary,
        transcript_text=transcript,
    )


def test_memory_store_starts_empty():
    s = MemoryStore()
    assert s.entries() == []


def test_memory_store_appends_in_order():
    s = MemoryStore()
    s.append(_entry(0, "a"))
    s.append(_entry(1, "b"))
    assert [e.episode_index for e in s.entries()] == [0, 1]


def test_build_memory_block_none_yields_neutral_text():
    s = MemoryStore()
    s.append(_entry(0, "alpha"))
    out = build_memory_block(s, mode="none")
    assert "no prior" in out.lower() or "first episode" in out.lower()


def test_build_memory_block_summary_is_compact():
    s = MemoryStore()
    s.append(_entry(0, "alpha summary"))
    s.append(_entry(1, "beta summary"))
    out = build_memory_block(s, mode="summary")
    assert "alpha summary" in out
    assert "beta summary" in out
    # the per-episode markers are present
    assert "Episode 1" in out  # 1-based label
    assert "Episode 2" in out


def test_build_memory_block_full_history_includes_transcripts():
    s = MemoryStore()
    s.append(_entry(0, "alpha s", transcript="A: hi\nB: hi back"))
    out = build_memory_block(s, mode="full-history")
    assert "A: hi" in out
    assert "B: hi back" in out


def test_build_memory_block_for_first_episode_is_neutral():
    s = MemoryStore()
    out = build_memory_block(s, mode="summary")
    assert "first episode" in out.lower() or "no prior" in out.lower()


def test_build_memory_block_unknown_mode_raises():
    with pytest.raises(ValueError):
        build_memory_block(MemoryStore(), mode="bogus")  # type: ignore[arg-type]
