"""Tests for benchmarks/locomo/backends/mem0.py pure helpers."""

from __future__ import annotations

from benchmarks.locomo.backends import RankedMemoryItem
from benchmarks.locomo.backends.mem0 import (
    MEM0_CUSTOM_INSTRUCTIONS,
    _hits_to_items,
    _mem0_user_id,
    _session_messages_mem0,
)
from benchmarks.locomo.dataset import LocomoSession, LocomoTurn


def test_mem0_user_id_uses_sample_and_speaker_names():
    assert _mem0_user_id("fixture-sample-0", "Alice") == "Alice_fixture-sample-0"


def test_session_messages_mem0_a_pov():
    sess = LocomoSession(
        index=1, date_time="1:00 pm on 8 May, 2023",
        turns=[
            LocomoTurn(speaker="Alice", dia_id="D1:1", text="hi"),
            LocomoTurn(speaker="Bob", dia_id="D1:2", text="hey"),
        ],
    )
    msgs = _session_messages_mem0(sess, "Alice", "Bob", pov="a")
    assert msgs == [
        {"role": "user", "content": "Alice: hi"},
        {"role": "assistant", "content": "Bob: hey"},
    ]


def test_hits_to_items_extracts_score_and_timestamp():
    raw = [
        {
            "id": "mem-1",
            "memory": "Alice is applying for data science roles.",
            "score": 0.87,
            "metadata": {"timestamp": "1:00 pm on 8 May, 2023", "session_id": "session_1"},
        }
    ]
    items = _hits_to_items(raw)
    assert items == [
        RankedMemoryItem(
            memory_id="mem-1",
            text="Alice is applying for data science roles.",
            timestamp="1:00 pm on 8 May, 2023",
            score=0.87,
            session_id="session_1",
        )
    ]


def test_mem0_custom_instructions_contains_identity_cue():
    # mem0's upstream instructions emphasise naming people not "user" —
    # we must preserve that or mem0 retrieves worse.
    assert "not use \"user\"" in MEM0_CUSTOM_INSTRUCTIONS
    assert "self-contained" in MEM0_CUSTOM_INSTRUCTIONS
