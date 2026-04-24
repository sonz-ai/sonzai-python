"""Tests for LoCoMo scoring: token-F1 + session-level Recall@K + NDCG."""

from __future__ import annotations

import pytest

from benchmarks.locomo.backends import RankedMemoryItem
from benchmarks.locomo.scoring import (
    aggregate_rows,
    evidence_to_session_ids,
    merge_speaker_rankings,
    ndcg_at_k,
    recall_any_at_k,
    token_f1,
)


def test_token_f1_identical():
    assert token_f1("red bike", "red bike") == 1.0


def test_token_f1_disjoint():
    assert token_f1("red bike", "blue car") == 0.0


def test_token_f1_partial_overlap():
    # "red bike" vs "red car" — 1 common token of 2 on each side = P=0.5 R=0.5 F1=0.5
    assert token_f1("red bike", "red car") == 0.5


def test_token_f1_handles_empty():
    assert token_f1("", "anything") == 0.0
    assert token_f1("anything", "") == 0.0
    assert token_f1("", "") == 0.0


def test_token_f1_is_case_insensitive():
    assert token_f1("Red Bike", "red bike") == 1.0


def test_token_f1_strips_punctuation():
    assert token_f1("red, bike!", "red bike") == 1.0


def test_evidence_to_session_ids_maps_dia_ids():
    assert evidence_to_session_ids(["D1:3", "D7:14", "D7:5"]) == {"session_1", "session_7"}


def test_evidence_to_session_ids_drops_malformed():
    assert evidence_to_session_ids(["malformed", "D3:4"]) == {"session_3"}


def test_recall_any_at_k_hit():
    retrieved = ["session_2", "session_5", "session_7"]
    gt = {"session_5"}
    assert recall_any_at_k(retrieved, gt, 1) == 0.0
    assert recall_any_at_k(retrieved, gt, 2) == 1.0
    assert recall_any_at_k(retrieved, gt, 3) == 1.0


def test_recall_any_at_k_no_hit():
    assert recall_any_at_k(["session_2"], {"session_5"}, 10) == 0.0


def test_recall_any_at_k_empty_ground_truth():
    assert recall_any_at_k(["session_2"], set(), 10) == 0.0


def test_ndcg_at_k_matches_manual():
    import math
    retrieved = ["session_1", "session_5", "session_7"]
    gt = {"session_5", "session_7"}
    # Hits at rank 2 and 3 → DCG = 1/log2(3) + 1/log2(4).
    # Ideal DCG (top-3 of [1,1,1,... relevances where 2 are relevant) = 1/log2(2) + 1/log2(3).
    dcg = 1 / math.log2(3) + 1 / math.log2(4)
    idcg = 1 / math.log2(2) + 1 / math.log2(3)
    assert abs(ndcg_at_k(retrieved, gt, 3) - dcg / idcg) < 1e-9


def test_merge_speaker_rankings_dedup_session_order():
    a = [
        RankedMemoryItem(memory_id="a1", text="x", session_id="session_2", score=0.9),
        RankedMemoryItem(memory_id="a2", text="y", session_id="session_5", score=0.5),
    ]
    b = [
        RankedMemoryItem(memory_id="b1", text="z", session_id="session_5", score=0.8),
        RankedMemoryItem(memory_id="b2", text="w", session_id="session_7", score=0.4),
    ]
    merged = merge_speaker_rankings(a, b)
    assert merged == ["session_2", "session_5", "session_7"]


def test_aggregate_rows_per_category():
    rows = [
        {"category": 1, "llm_correct": True, "token_f1": 1.0,
         "retrieval": {"recall_any@1": 1.0, "recall_any@10": 1.0}},
        {"category": 1, "llm_correct": False, "token_f1": 0.5,
         "retrieval": {"recall_any@1": 0.0, "recall_any@10": 1.0}},
        {"category": 2, "llm_correct": True, "token_f1": 0.0,
         "retrieval": {"recall_any@1": 1.0, "recall_any@10": 1.0}},
    ]
    agg = aggregate_rows(rows)
    assert agg["per_category"][1]["llm_accuracy"] == 0.5
    assert agg["per_category"][1]["token_f1"] == 0.75
    assert agg["per_category"][2]["llm_accuracy"] == 1.0
    assert agg["per_category"][1]["n"] == 2
    assert agg["overall"]["llm_accuracy"] == pytest.approx(2 / 3, abs=1e-9)
