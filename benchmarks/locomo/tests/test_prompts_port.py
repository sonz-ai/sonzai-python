"""Snapshot tests guarding the mem0 prompt ports against accidental edits.

The LoCoMo benchmark's credibility depends on running mem0's ANSWER_PROMPT
and ACCURACY_PROMPT byte-for-byte. If mem0 updates their prompts upstream,
we re-port deliberately; if someone edits ours locally, this test catches it.
"""

from __future__ import annotations

from benchmarks.locomo.prompts import (
    ACCURACY_PROMPT,
    ANSWER_PROMPT,
    ANSWER_PROMPT_GRAPH,
    PROMPT_SOURCE,
)


def test_prompt_source_documents_provenance():
    assert "mem0ai/mem0" in PROMPT_SOURCE
    assert "evaluation/prompts.py" in PROMPT_SOURCE
    assert "evaluation/metrics/llm_judge.py" in PROMPT_SOURCE


def test_answer_prompt_contains_required_instructions():
    # Structural invariants — if any of these disappear we have broken parity.
    assert "{{speaker_1_user_id}}" in ANSWER_PROMPT
    assert "{{speaker_2_user_id}}" in ANSWER_PROMPT
    assert "{{speaker_1_memories}}" in ANSWER_PROMPT
    assert "{{speaker_2_memories}}" in ANSWER_PROMPT
    assert "{{question}}" in ANSWER_PROMPT
    assert "less than 5-6 words" in ANSWER_PROMPT
    assert "timestamps" in ANSWER_PROMPT.lower()


def test_answer_prompt_graph_contains_graph_relations():
    assert "{{speaker_1_graph_memories}}" in ANSWER_PROMPT_GRAPH
    assert "{{speaker_2_graph_memories}}" in ANSWER_PROMPT_GRAPH
    assert "knowledge graph" in ANSWER_PROMPT_GRAPH.lower()


def test_accuracy_prompt_invariants():
    assert "{question}" in ACCURACY_PROMPT
    assert "{gold_answer}" in ACCURACY_PROMPT
    assert "{generated_answer}" in ACCURACY_PROMPT
    assert "CORRECT" in ACCURACY_PROMPT
    assert "WRONG" in ACCURACY_PROMPT
    assert '"label"' in ACCURACY_PROMPT
