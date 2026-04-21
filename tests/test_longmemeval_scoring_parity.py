"""Bit-for-bit parity with MemPalace's scoring block.

This test imports MemPalace's actual ``dcg`` / ``ndcg`` / ``evaluate_retrieval``
from the sibling clone at ``sonzai-sdk/mempalace/benchmarks/longmemeval_bench.py``
and asserts that our scoring helpers produce identical numbers on hand-crafted
inputs. **Scientifically rigorous — no frozen copy, no transcription risk.**

Additionally, a frozen reference of MemPalace's formulas is kept inline and
compared against the live import. If MemPalace ever changes their scoring
math upstream, ``test_upstream_mempalace_unchanged`` fails and we decide
whether to track the change or hold our own line deliberately.

Fails (rather than skipping) if the clone or chromadb is missing — the
benchmark's reproducibility contract is that these conditions are met:

    git clone https://github.com/MemPalace/mempalace.git   # at sonzai-sdk root
    uv pip install "chromadb>=0.5"                          # auto from dev extras

Source for the frozen reference:
    https://github.com/MemPalace/mempalace/blob/develop/benchmarks/longmemeval_bench.py
    (functions ``dcg``, ``ndcg``, ``evaluate_retrieval`` — currently ~line 53–80)
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMPALACE_BENCH = REPO_ROOT / "mempalace" / "benchmarks" / "longmemeval_bench.py"


# ---------------------------------------------------------------------------
# Load MemPalace's bench module directly. No skip: the reproducibility
# contract says the clone must be present and chromadb must be installed.
# If either fails, the test fails loudly so the env gets fixed.
# ---------------------------------------------------------------------------


def _load_mempalace_bench():
    if not MEMPALACE_BENCH.exists():
        raise AssertionError(
            f"MemPalace clone missing at {REPO_ROOT / 'mempalace'}. "
            "Reproducibility requires it — run:\n\n"
            "  cd {repo_root} && git clone https://github.com/MemPalace/mempalace.git\n".format(
                repo_root=REPO_ROOT
            )
        )
    spec = importlib.util.spec_from_file_location(
        "_mempalace_bench", MEMPALACE_BENCH
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_mempalace_bench"] = mod
    spec.loader.exec_module(mod)
    return mod


_MP = _load_mempalace_bench()


# ---------------------------------------------------------------------------
# Frozen reference — MemPalace's functions copied verbatim for upstream-drift
# detection. test_upstream_mempalace_unchanged asserts the LIVE import still
# matches this copy; any upstream change fails that test and forces a review.
# ---------------------------------------------------------------------------


def _frozen_mp_dcg(relevances, k: int) -> float:
    score = 0.0
    for i, rel in enumerate(relevances[:k]):
        score += rel / math.log2(i + 2)
    return score


def _frozen_mp_ndcg(rankings, correct_ids, corpus_ids, k: int) -> float:
    relevances = [1.0 if corpus_ids[idx] in correct_ids else 0.0 for idx in rankings[:k]]
    ideal = sorted(relevances, reverse=True)
    idcg = _frozen_mp_dcg(ideal, k)
    if idcg == 0:
        return 0.0
    return _frozen_mp_dcg(relevances, k) / idcg


def _frozen_mp_evaluate_retrieval(rankings, correct_ids, corpus_ids, k: int):
    top_k_ids = set(corpus_ids[idx] for idx in rankings[:k])
    recall_any = float(any(cid in top_k_ids for cid in correct_ids))
    recall_all = float(all(cid in top_k_ids for cid in correct_ids))
    ndcg_score = _frozen_mp_ndcg(rankings, correct_ids, corpus_ids, k)
    return recall_any, recall_all, ndcg_score


def _mp_session_from(cid: str) -> str:
    """Matches MemPalace's ``session_id_from_corpus_id`` exactly."""
    return _MP.session_id_from_corpus_id(cid)


# ---------------------------------------------------------------------------
# Synthetic fixtures — each represents a realistic ranking shape from the bench.
# ---------------------------------------------------------------------------

# (name, corpus_ids_ranked_top_to_bottom, answer_session_ids)
CASES: list[tuple[str, list[str], list[str]]] = [
    ("rank1_single_gt", ["s1", "s2", "s3", "s4", "s5"], ["s1"]),
    ("rank3_single_gt", ["s1", "s2", "s3", "s4", "s5"], ["s3"]),
    ("rank7_single_gt", ["a", "b", "c", "d", "e", "f", "g", "gt", "h", "i"], ["gt"]),
    ("both_gt_in_top3", ["gt1", "x", "gt2", "y", "z"], ["gt1", "gt2"]),
    ("one_of_two_gt", ["gt1", "x", "y", "z", "w", "gt2"], ["gt1", "gt2"]),
    (
        "three_gt_scattered",
        ["gt1", "a", "gt2", "b", "c", "d", "gt3", "e"],
        ["gt1", "gt2", "gt3"],
    ),
    (
        "same_session_multiple_turns",
        ["s1_turn_0", "s1_turn_2", "s2_turn_1", "s3_turn_0", "s1_turn_5"],
        ["s1"],
    ),
    (
        "mixed_turn_granular",
        ["s1_turn_0", "s2_turn_1", "s1_turn_3", "s3_turn_0", "s4_turn_1"],
        ["s1", "s4"],
    ),
    ("no_hits", ["x", "y", "z", "a", "b"], ["gt"]),
    ("empty_gt", ["x", "y", "z"], []),
]

KS = [1, 3, 5, 10, 30, 50]


# ---------------------------------------------------------------------------
# Upstream-drift detector: if MemPalace changes their scoring formula, this
# test fails FIRST so we know to decide what to do before downstream tests
# misleadingly pass/fail for the wrong reason.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_upstream_mempalace_unchanged(case: tuple[str, list[str], list[str]]) -> None:
    """MemPalace's live code still computes identical numbers to our frozen copy.

    If this fails, MemPalace has changed their scoring. Read their diff,
    decide whether to update our frozen copy (and possibly our own scoring)
    or deliberately diverge.
    """
    _, corpus_ids, answer_sids = case
    rankings = list(range(len(corpus_ids)))
    session_level_ids = [_mp_session_from(cid) for cid in corpus_ids]
    session_correct = set(answer_sids)

    for k in KS:
        live_ra, live_rl, live_nd = _MP.evaluate_retrieval(
            rankings, session_correct, session_level_ids, k
        )
        frz_ra, frz_rl, frz_nd = _frozen_mp_evaluate_retrieval(
            rankings, session_correct, session_level_ids, k
        )
        assert live_ra == pytest.approx(frz_ra, abs=1e-9), (
            f"upstream recall_any@{k} drifted: live={live_ra} frozen={frz_ra}"
        )
        assert live_rl == pytest.approx(frz_rl, abs=1e-9), (
            f"upstream recall_all@{k} drifted: live={live_rl} frozen={frz_rl}"
        )
        assert live_nd == pytest.approx(frz_nd, abs=1e-9), (
            f"upstream ndcg@{k} drifted: live={live_nd} frozen={frz_nd}"
        )


# ---------------------------------------------------------------------------
# Our scoring == MemPalace's live scoring.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case", CASES, ids=[c[0] for c in CASES])
def test_session_level_parity(case: tuple[str, list[str], list[str]]) -> None:
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
        mp_ra, mp_rl, mp_nd = _MP.evaluate_retrieval(
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
        mp_ra, mp_rl, mp_nd = _MP.evaluate_retrieval(
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

    items = [
        RankedItem(corpus_id="gt_turn_0", text="a"),
        RankedItem(corpus_id="other_turn_0", text="b"),
        RankedItem(corpus_id="gt_turn_1", text="c"),
    ]
    m = _retrieval_metrics(items, ["gt"])

    session_level_ids = ["gt", "other", "gt"]
    rankings = [0, 1, 2]
    mp_ra, _, mp_nd = _MP.evaluate_retrieval(rankings, {"gt"}, session_level_ids, 3)

    assert m["session"]["recall_any@3"] == pytest.approx(mp_ra)
    assert m["session"]["ndcg_any@3"] == pytest.approx(mp_nd)


def test_recall_at_g_fractional() -> None:
    """R@G: ``|top-|GT| ∩ GT| / |GT|``. Matches Mem0/A-Mem definition."""
    from benchmarks.longmemeval.scoring import recall_at_g

    assert recall_at_g(["gt", "x", "y"], ["gt", "z"]) == pytest.approx(0.5)
    assert recall_at_g(["gt", "z", "x"], ["gt", "z"]) == pytest.approx(1.0)
    assert recall_at_g(["a", "b", "c"], ["gt"]) == pytest.approx(0.0)
    assert recall_at_g(["a", "b"], []) == pytest.approx(0.0)


def test_metrics_from_row_backfills_legacy_schema() -> None:
    """Old result JSONLs (pre-parity rewrite) stored flat ``session_recall_at_5``
    and ``ranked_session_ids`` without ``retrieval_results.metrics``. The
    summarizer must back-fill the full MemPalace grid from the ranked list so
    ``--compare`` across mixed-schema files gives consistent numbers."""
    from benchmarks.longmemeval.run import _metrics_from_row

    # Legacy shape: answer session at rank 1 in ranked_session_ids, no
    # retrieval_results.metrics block.
    legacy_row = {
        "question_id": "legacy-1",
        "answer_session_ids": ["answer_abc"],
        "ranked_session_ids": ["answer_abc", "x", "y", "z"],
        "session_recall_at_5": 1.0,
        "session_ndcg_at_5": 1.0,
    }
    m = _metrics_from_row(legacy_row)
    assert m["session"]["recall_at_g"] == pytest.approx(1.0)
    assert m["session"]["recall_any@10"] == pytest.approx(1.0)
    assert m["session"]["ndcg_any@1"] == pytest.approx(1.0)

    # New-schema row with populated metrics must pass through unchanged.
    new_row = {
        "retrieval_results": {
            "metrics": {
                "session": {"recall_any@10": 0.5, "recall_at_g": 0.25},
                "turn": {"recall_any@5": 1.0},
            }
        }
    }
    m = _metrics_from_row(new_row)
    assert m["session"]["recall_any@10"] == pytest.approx(0.5)
    assert m["session"]["recall_at_g"] == pytest.approx(0.25)
    assert m["turn"]["recall_any@5"] == pytest.approx(1.0)
