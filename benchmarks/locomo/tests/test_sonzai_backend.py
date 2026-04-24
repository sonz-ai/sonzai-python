"""Tests for benchmarks/locomo/backends/sonzai.py pure-function helpers.

Live-API behaviours aren't tested here — they're exercised in the end-to-end
smoke-run workflow. Pure helpers (message construction, batching, session-id
derivation, metadata-filter) are the only units with deterministic inputs.
"""

from __future__ import annotations

from benchmarks.locomo.backends.sonzai import (
    _batch_messages,
    _build_messages,
    _is_metadata_fact,
    _sonzai_session_id,
)
from benchmarks.locomo.dataset import LocomoSession, LocomoTurn


def _session(turns: list[tuple[str, str, str]]) -> LocomoSession:
    return LocomoSession(
        index=1,
        date_time="1:00 pm on 8 May, 2023",
        turns=[LocomoTurn(speaker=s, dia_id=d, text=t) for s, d, t in turns],
    )


def test_build_messages_speaker_a_pov():
    sess = _session([
        ("Alice", "D1:1", "hi"),
        ("Bob", "D1:2", "hey"),
        ("Alice", "D1:3", "how are you"),
    ])
    msgs = _build_messages(sess, "Alice", "Bob", pov="a")
    assert msgs == [
        {"role": "user", "content": "Alice: hi"},
        {"role": "assistant", "content": "Bob: hey"},
        {"role": "user", "content": "Alice: how are you"},
    ]


def test_build_messages_speaker_b_pov_reverses_roles():
    sess = _session([
        ("Alice", "D1:1", "hi"),
        ("Bob", "D1:2", "hey"),
    ])
    msgs = _build_messages(sess, "Alice", "Bob", pov="b")
    assert msgs == [
        {"role": "assistant", "content": "Alice: hi"},
        {"role": "user", "content": "Bob: hey"},
    ]


def test_batch_messages_default_size_2():
    msgs = [{"role": "user", "content": str(i)} for i in range(5)]
    batches = list(_batch_messages(msgs, 2))
    assert len(batches) == 3
    assert batches[0] == msgs[:2]
    assert batches[1] == msgs[2:4]
    # Last batch would be size-1, which /process rejects — helper pads by
    # re-attaching to the previous batch.
    assert batches[2] == [msgs[3], msgs[4]]


def test_batch_messages_whole_session_when_size_zero():
    msgs = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}, {"role": "user", "content": "c"}]  # noqa: E501
    batches = list(_batch_messages(msgs, 0))
    assert len(batches) == 1
    assert batches[0] == msgs


def test_batch_messages_raises_on_size_one_input():
    # Even with batch_size=2, a session with only 1 turn can't be batched.
    # /process requires >=2 messages — caller should skip such sessions.
    assert list(_batch_messages([{"role": "user", "content": "only"}], 2)) == []


def test_sonzai_session_id_format():
    assert _sonzai_session_id("sample-0", 3, "a") == "sample-0-s3-a"


def test_is_metadata_fact_flags_comm_style():
    assert _is_metadata_fact("agentX:userY:comm_style") is True


def test_is_metadata_fact_flags_side_effect():
    assert _is_metadata_fact("agentX:userY:side_effect:abc") is True


def test_is_metadata_fact_flags_interest():
    assert _is_metadata_fact("agentX:userY:interest:music") is True


def test_is_metadata_fact_allows_regular_fact_id():
    assert _is_metadata_fact("fact-12345") is False


# ---------------------------------------------------------------------------
# Reader prompt formatting — mem0-parity ANSWER_PROMPT rendering
# ---------------------------------------------------------------------------


def test_render_answer_prompt_has_all_placeholders_substituted():
    from benchmarks.locomo.backends import RankedMemoryItem
    from benchmarks.locomo.backends.sonzai import _render_answer_prompt

    a = [RankedMemoryItem(memory_id="m1", text="Alice wants to be a data scientist", timestamp="8 May 2023")]  # noqa: E501
    b = [RankedMemoryItem(memory_id="m2", text="Bob bought a bike", timestamp="12 May 2023")]
    prompt = _render_answer_prompt(
        question="Who bought a bike?",
        speaker_1="Alice", speaker_1_memories=a,
        speaker_2="Bob",   speaker_2_memories=b,
    )
    assert "{{" not in prompt  # jinja placeholders substituted
    assert "Alice" in prompt
    assert "Bob" in prompt
    assert "data scientist" in prompt
    assert "bought a bike" in prompt
    assert "Who bought a bike?" in prompt
