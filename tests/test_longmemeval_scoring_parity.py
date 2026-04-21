"""Bit-for-bit parity with MemPalace's scoring block.

Embeds MemPalace's exact ``dcg`` / ``ndcg`` / ``evaluate_retrieval`` (copied
verbatim from ``benchmarks/longmemeval_bench.py`` at commit `develop`) so we
can compare their math against ours without pulling chromadb into the test
dependency closure.

If MemPalace changes their scoring, update ``_MP_NDCG`` / ``_MP_EVALUATE``
below from the latest upstream — that's intentional: we WANT this test to
fail on divergence so we can decide whether to track or hold our own line.

Source: https://github.com/MemPalace/mempalace/blob/develop/benchmarks/longmemeval_bench.py
(functions ``dcg``, ``ndcg``, ``evaluate_retrieval`` — currently ~line 53–80)
"""

from __future__ import annotations

import math

import pytest

# ---------------------------------------------------------------------------
# MemPalace reference scoring — copied verbatim, kept pure-Python so this test
# doesn't need chromadb or any other MemPalace runtime dependency.
# ---------------------------------------------------------------------------


def _mp_dcg(relevances, k: int) -> float:
    score = 0.0
    for i, rel in enumerate(relevances[:k]):
        score += rel / math.log2(i + 2)
    return score


def _mp_ndcg(rankings, correct_ids, corpus_ids, k: int) -> float:
    relevances = [1.0 if corpus_ids[idx] in correct_ids else 0.0 for idx in rankings[:k]]
    ideal = sorted(relevances, reverse=True)
    idcg = _mp_dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _mp_dcg(relevances, k) / idcg


def _mp_evaluate_retrieval(rankings, correct_ids, corpus_ids, k: int):
    top_k_ids = set(corpus_ids[idx] for idx in rankings[:k])
    recall_any = float(any(cid in top_k_ids for cid in correct_ids))
    recall_all = float(all(cid in top_k_ids for cid in correct_ids))
    ndcg_score = _mp_ndcg(rankings, correct_ids, corpus_ids, k)
    return recall_any, recall_all, ndcg_score


def _mp_session_from(cid: str) -> str:
    """MemPalace's ``session_id_from_corpus_id`` — copied verbatim."""
    if "_turn_" in cid:
        return cid.rsplit("_turn_", 1)[0]
    return cid


# ---------------------------------------------------------------------------
# Synthetic fixtures — each represents a realistic ranking shape from the bench.
# ---------------------------------------------------------------------------

# (name, corpus_ids_ranked_top_to_bottom, answer_session_ids)
CASES: list[tuple[str, list[str], list[str]]] = [
    # single GT, rank-1 hit
    ("rank1_single_gt", ["s1", "s2", "s3", "s4", "s5"], ["s1"]),
    # single GT, rank-3 hit
    ("rank3_single_gt", ["s1", "s2", "s3", "s4", "s5"], ["s3"]),
    # single GT, not in top-5 but in top-10
    ("rank7_single_gt", ["a", "b", "c", "d", "e", "f", "g", "gt", "h", "i"], ["gt"]),
    # two GTs, both in top-3
    ("both_gt_in_top3", ["gt1", "x", "gt2", "y", "z"], ["gt1", "gt2"]),
    # two GTs, only one in top-5
    ("one_of_two_gt", ["gt1", "x", "y", "z", "w", "gt2"], ["gt1", "gt2"]),
    # three GTs, scattered
    (
        "three_gt_scattered",
        ["gt1", "a", "gt2", "b", "c", "d", "gt3", "e"],
        ["gt1", "gt2", "gt3"],
    ),
    # turn-granular: same session appearing multiple times
    (
        "same_session_multiple_turns",
        ["s1_turn_0", "s1_turn_2", "s2_turn_1", "s3_turn_0", "s1_turn_5"],
        ["s1"],
    ),
    # mixed: some turns from GT session, one turn from non-GT
    (
        "mixed_turn_granular",
        ["s1_turn_0", "s2_turn_1", "s1_turn_3", "s3_turn_0", "s4_turn_1"],
        ["s1", "s4"],
    ),
    # no hits in top-k
    ("no_hits", ["x", "y", "z", "a", "b"], ["gt"]),
    # empty GT — both implementations must return 0.0
    ("empty_gt", ["x", "y", "z"], []),
]

KS = [1, 3, 5, 10, 30, 50]


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_session_level_parity(case: tuple[str, list[str], list[str]]) -> None:
    """Our session-level metrics == MemPalace's evaluate_retrieval on the same input."""
    from benchmarks.longmemeval.scoring import (
        ndcg_at_k,
        recall_all_at_k,
        recall_any_at_k,
    )

    _, corpus_ids, answer_sids = case
    rankings = list(range(len(corpus_ids)))
    session_level_ids = [_mp_session_from(cid) for cid in corpus_ids]
    session_correct = set(answer_sids)

    for k in KS:
        mp_ra, mp_rl, mp_nd = _mp_evaluate_retrieval(
            rankings, session_correct, session_level_ids, k
        )
        our_ra = recall_any_at_k(session_level_ids, answer_sids, k)
        our_rl = recall_all_at_k(session_level_ids, answer_sids, k)
        our_nd = ndcg_at_k(session_level_ids, answer_sids, k)

        assert our_ra == pytest.approx(mp_ra, abs=1e-9), (
            f"recall_any@{k} mismatch: ours={our_ra} mp={mp_ra}"
        )
        assert our_rl == pytest.approx(mp_rl, abs=1e-9), (
            f"recall_all@{k} mismatch: ours={our_rl} mp={mp_rl}"
        )
        assert our_nd == pytest.approx(mp_nd, abs=1e-9), (
            f"ndcg_any@{k} mismatch: ours={our_nd} mp={mp_nd}"
        )


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_turn_level_parity(case: tuple[str, list[str], list[str]]) -> None:
    """Turn-granular scoring matches MemPalace's turn_correct comprehension."""
    from benchmarks.longmemeval.scoring import (
        ndcg_at_k,
        recall_all_at_k,
        recall_any_at_k,
    )

    _, corpus_ids, answer_sids = case
    rankings = list(range(len(corpus_ids)))
    answer_set = set(answer_sids)
    turn_correct = {cid for cid in corpus_ids if _mp_session_from(cid) in answer_set}

    for k in KS:
        mp_ra, mp_rl, mp_nd = _mp_evaluate_retrieval(
            rankings, turn_correct, corpus_ids, k
        )
        our_ra = recall_any_at_k(corpus_ids, list(turn_correct), k)
        our_rl = recall_all_at_k(corpus_ids, list(turn_correct), k)
        our_nd = ndcg_at_k(corpus_ids, list(turn_correct), k)

        assert our_ra == pytest.approx(mp_ra, abs=1e-9)
        assert our_rl == pytest.approx(mp_rl, abs=1e-9)
        assert our_nd == pytest.approx(mp_nd, abs=1e-9)


def test_retrieval_metrics_aggregator_shape() -> None:
    """``_retrieval_metrics`` emits the full MemPalace k-grid at both granularities,
    plus R@G. No key should be missing on a non-empty input."""
    from benchmarks.longmemeval.backends import RankedItem
    from benchmarks.longmemeval.run import _retrieval_metrics

    items = [
        RankedItem(corpus_id="s1_turn_0", text="x"),
        RankedItem(corpus_id="s2_turn_1", text="y"),
        RankedItem(corpus_id="s1_turn_3", text="z"),
    ]
    m = _retrieval_metrics(items, ["s1"])

    assert set(m.keys()) == {"session", "turn"}
    for gran in ("session", "turn"):
        for k in KS:
            assert f"recall_any@{k}" in m[gran]
            assert f"recall_all@{k}" in m[gran]
            assert f"ndcg_any@{k}" in m[gran]
        assert "recall_at_g" in m[gran]


def test_retrieval_metrics_uses_positional_session_ids() -> None:
    """_retrieval_metrics must NOT dedup before session-level scoring — MemPalace
    uses ``session_level_ids = [session_id_from_corpus_id(cid) for cid in corpus_ids]``
    (one entry per ranked item). Dedup would drop duplicate positions and
    under-score NDCG when the same session appears at multiple ranks.
    """
    from benchmarks.longmemeval.backends import RankedItem
    from benchmarks.longmemeval.run import _retrieval_metrics

    # Two turns from the GT session, one from a non-GT session, in that order.
    items = [
        RankedItem(corpus_id="gt_turn_0", text="a"),
        RankedItem(corpus_id="other_turn_0", text="b"),
        RankedItem(corpus_id="gt_turn_1", text="c"),
    ]
    m = _retrieval_metrics(items, ["gt"])

    # Reference using the embedded MemPalace scoring — session_level_ids
    # must include BOTH "gt" positions, not dedup to one.
    session_level_ids = ["gt", "other", "gt"]
    rankings = [0, 1, 2]
    mp_ra, _, mp_nd = _mp_evaluate_retrieval(rankings, {"gt"}, session_level_ids, 3)

    assert m["session"]["recall_any@3"] == pytest.approx(mp_ra)
    assert m["session"]["ndcg_any@3"] == pytest.approx(mp_nd)


def test_recall_at_g_fractional() -> None:
    """R@G: ``|top-|GT| ∩ GT| / |GT|``. Matches Mem0/A-Mem definition."""
    from benchmarks.longmemeval.scoring import recall_at_g

    assert recall_at_g(["gt", "x", "y"], ["gt", "z"]) == pytest.approx(0.5)
    assert recall_at_g(["gt", "z", "x"], ["gt", "z"]) == pytest.approx(1.0)
    assert recall_at_g(["a", "b", "c"], ["gt"]) == pytest.approx(0.0)
    assert recall_at_g(["a", "b"], []) == pytest.approx(0.0)
