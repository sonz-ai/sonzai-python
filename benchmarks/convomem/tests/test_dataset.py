"""Unit tests for the ConvoMem dataset loader.

No network calls — tests point the loader at a local fixture file via the
``cache_dir`` override.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from benchmarks.convomem.dataset import (
    CATEGORY_SUBFOLDERS,
    ConvoMemQuestion,
    Conversation,
    EvidenceMessage,
    Message,
    load_questions,
)

FIXTURE = Path(__file__).parent / "fixtures" / "convomem_sample.json"


def _populate_cache(cache_dir: Path) -> None:
    """Mirror the cache-dir layout load_questions expects, from a single fixture."""
    for category, subfolder in CATEGORY_SUBFOLDERS.items():
        target_dir = cache_dir / category / subfolder
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(FIXTURE, target_dir / "batched_000.json")


def test_category_map_has_all_six_categories():
    assert set(CATEGORY_SUBFOLDERS) == {
        "user_evidence",
        "assistant_facts_evidence",
        "changing_evidence",
        "abstention_evidence",
        "preference_evidence",
        "implicit_connection_evidence",
    }
    # Supermemory's map: everything is 1_evidence except changing_evidence.
    assert CATEGORY_SUBFOLDERS["changing_evidence"] == "2_evidence"
    for k, v in CATEGORY_SUBFOLDERS.items():
        if k != "changing_evidence":
            assert v == "1_evidence"


def test_load_all_categories(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path)
    # 6 categories × 2 items per fixture = 12 questions
    assert len(qs) == 12
    cats = {q.question_type for q in qs}
    assert cats == set(CATEGORY_SUBFOLDERS)


def test_question_shape(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, categories=["user_evidence"])
    assert len(qs) == 2
    q = qs[0]
    assert isinstance(q, ConvoMemQuestion)
    assert q.question_type == "user_evidence"
    assert q.question_id == "convomem-user_evidence-0"
    assert q.question == "How many kids do I have?"
    assert q.answer == "3"
    assert q.evidence_messages == [
        EvidenceMessage(speaker="User", text="I have 3 kids named Emma, Josh, and Lily.")
    ]
    assert len(q.conversations) == 2
    assert q.conversations[0].conversation_id == "convomem-user_evidence-0-conv-0"
    first_conv = q.conversations[0]
    assert isinstance(first_conv, Conversation)
    assert first_conv.messages[0] == Message(role="user", content="Morning. Quick thing.")
    # Dataset uses "Assistant"/"User"; loader lowercases to SDK's "assistant"/"user".
    assert first_conv.messages[1].role == "assistant"


def test_question_ids_stable_across_loads(tmp_path: Path):
    _populate_cache(tmp_path)
    a = [q.question_id for q in load_questions(cache_dir=tmp_path)]
    b = [q.question_id for q in load_questions(cache_dir=tmp_path)]
    assert a == b


def test_category_filter(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, categories=["abstention_evidence"])
    assert len(qs) == 2
    assert {q.question_type for q in qs} == {"abstention_evidence"}


def test_limit_slices_across_categories(tmp_path: Path):
    """``limit=6`` must spread across all six categories, one each."""
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, limit=6)
    assert len(qs) == 6
    assert len({q.question_type for q in qs}) == 6


def test_limit_zero_returns_everything(tmp_path: Path):
    _populate_cache(tmp_path)
    qs = load_questions(cache_dir=tmp_path, limit=0)
    assert len(qs) == 12


def test_unknown_category_raises(tmp_path: Path):
    _populate_cache(tmp_path)
    with pytest.raises(ValueError, match="unknown category"):
        load_questions(cache_dir=tmp_path, categories=["not_a_real_category"])
