# LIFELONG-SOTOPIA Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement [LIFELONG-SOTOPIA](https://arxiv.org/abs/2506.12666) (Goel & Zhu, 2025) as `benchmarks/lifelong_sotopia/`: 40-episode multi-scenario social-intelligence eval with Bel/Goal/BelExt scoring, two memory baselines (`summary`, `full-history`, plus `none` floor), and Sonzai as the primary backend.

**Architecture:** New top-level benchmark mirroring `benchmarks/sotopia/` layout. Bundled scenario corpus (12 per relationship type × ≥3 types) + opt-in `--regenerate-scenarios`. Sonzai backend uses one stable agent per character pair across episodes; baseline backend pairs Gemini Flash Lite generation with selectable memory. New `judge_bel_extended_async()` in `common/gemini_judge.py` returns 8 boolean checkpoints; SDK computes `BelExt = max(Bel - 5×failed, 0)`.

**Tech Stack:** Python 3.11+, `sonzai` async client, `google.genai` (Gemini Flash Lite), `pydantic`, `pytest`, `matplotlib`, `tqdm`. Tests use mocked judge fixtures (no live API calls).

**Reference spec:** `docs/superpowers/specs/2026-05-04-lifelong-sotopia-benchmark-design.md`

---

## File Structure

```
benchmarks/lifelong_sotopia/
├── __init__.py                        # package docstring
├── __main__.py                        # `python -m benchmarks.lifelong_sotopia`
├── README.md                          # bench-level reproduction docs
├── run.py                             # CLI + orchestrator
├── scenarios.py                       # Character/Relationship/Scenario types + loader + selection
├── scoring.py                         # BelExt formula + EpisodeRun + trajectory + slope
├── memory.py                          # full-history / summary / none memory builders for baseline
├── scenarios_data/                    # bundled JSON corpus
│   ├── mentor-mentee.json
│   ├── peer-collaborator.json
│   ├── friend-and-friend.json
│   └── memory_required.json
├── backends/
│   ├── __init__.py
│   ├── sonzai.py                      # Sonzai backend (agent.chat across pairs)
│   └── baseline.py                    # Gemini-only with memory mode switch
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   └── mini_corpus.json           # tiny synthetic relationship corpus
│   ├── test_scenarios.py
│   ├── test_scoring.py
│   ├── test_memory.py
│   └── test_runner.py
└── results/
    └── .gitkeep

benchmarks/common/gemini_judge.py      # MODIFIED — add BelExtScore + judge_bel_extended_async
benchmarks/README.md                   # MODIFIED — add LIFELONG-SOTOPIA section
benchmarks/__init__.py                 # MODIFIED — list new bench in module docstring
```

---

## Task 1: Package skeleton

**Files:**
- Create: `benchmarks/lifelong_sotopia/__init__.py`
- Create: `benchmarks/lifelong_sotopia/__main__.py`
- Create: `benchmarks/lifelong_sotopia/results/.gitkeep`
- Create: `benchmarks/lifelong_sotopia/scenarios_data/.gitkeep`
- Create: `benchmarks/lifelong_sotopia/tests/__init__.py`
- Create: `benchmarks/lifelong_sotopia/tests/fixtures/.gitkeep`
- Create: `benchmarks/lifelong_sotopia/backends/__init__.py`

- [ ] **Step 1: Create the package init**

`benchmarks/lifelong_sotopia/__init__.py`:
```python
"""LIFELONG-SOTOPIA benchmark — multi-episode social intelligence over diverse scenarios.

Implements Goel & Zhu (2025) "LIFELONG SOTOPIA: Evaluating Social Intelligence
of Language Agents Over Lifelong Social Interactions" — https://arxiv.org/abs/2506.12666

Where standard SOTOPIA grades a single interaction and our existing
``benchmarks/sotopia/`` repeats the *same* scenario across N sessions,
LIFELONG-SOTOPIA gives the same character pair a *different* scenario each
episode (sampled by relationship type) across ~40 episodes. Headline finding
in the paper: Goal and Believability decline across the 40-episode arc; an
"advanced" memory technique (per-episode 200-300 word summary) helps but the
best agents still trail humans on scenarios that explicitly require recalling
prior episodes.

Invoke via::

    python -m benchmarks.lifelong_sotopia --pairs 2 --episodes-per-pair 10
"""
```

- [ ] **Step 2: Create the entry point**

`benchmarks/lifelong_sotopia/__main__.py`:
```python
"""Entry point for ``python -m benchmarks.lifelong_sotopia``."""

from __future__ import annotations

from .run import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Create the backends sub-package init**

`benchmarks/lifelong_sotopia/backends/__init__.py`:
```python
"""Per-backend runners. Each module exports an async ``run_all_pairs_*``."""
```

- [ ] **Step 4: Create the tests package init**

`benchmarks/lifelong_sotopia/tests/__init__.py`:
```python
"""Tests for the LIFELONG-SOTOPIA benchmark."""
```

- [ ] **Step 5: Create empty placeholder dirs (.gitkeep files)**

```bash
touch benchmarks/lifelong_sotopia/results/.gitkeep
touch benchmarks/lifelong_sotopia/scenarios_data/.gitkeep
touch benchmarks/lifelong_sotopia/tests/fixtures/.gitkeep
```

- [ ] **Step 6: Verify the package imports cleanly**

Run: `python -c "import benchmarks.lifelong_sotopia"`
Expected: no error.

- [ ] **Step 7: Commit**

```bash
git add benchmarks/lifelong_sotopia/__init__.py \
        benchmarks/lifelong_sotopia/__main__.py \
        benchmarks/lifelong_sotopia/backends/__init__.py \
        benchmarks/lifelong_sotopia/tests/__init__.py \
        benchmarks/lifelong_sotopia/results/.gitkeep \
        benchmarks/lifelong_sotopia/scenarios_data/.gitkeep \
        benchmarks/lifelong_sotopia/tests/fixtures/.gitkeep
git commit -m "lifelong-sotopia: package skeleton"
```

---

## Task 2: Scenario data types and loader

**Files:**
- Create: `benchmarks/lifelong_sotopia/scenarios.py`
- Create: `benchmarks/lifelong_sotopia/tests/test_scenarios.py`
- Create: `benchmarks/lifelong_sotopia/tests/fixtures/mini_corpus.json`

- [ ] **Step 1: Write the fixture corpus**

`benchmarks/lifelong_sotopia/tests/fixtures/mini_corpus.json`:
```json
{
  "characters": [
    {"name": "Alice Chen", "background": "Software engineer in Toronto.", "personality": "Curious, direct."},
    {"name": "Bob Lin",   "background": "Product manager in Vancouver.",  "personality": "Patient, organized."}
  ],
  "relationships": [
    {"id": "r1", "char_a": "Alice Chen", "char_b": "Bob Lin", "type": "peer-collaborator", "context": "Work on the same product team."}
  ],
  "scenarios": {
    "peer-collaborator": [
      {"scenario_id": "pc-001", "codename": "design review", "setting": "Alice presents a design to Bob.", "agent_goal": "Get sign-off on design.", "partner_goal": "Push back on the boldest part.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "pc-002", "codename": "incident retro", "setting": "Joint retro on a deploy that went wrong.", "agent_goal": "Avoid blame, find root cause.", "partner_goal": "Establish ownership for next time.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "pc-003", "codename": "lunch venting", "setting": "Casual lunch venting about a third coworker.", "agent_goal": "Empathize without gossiping.", "partner_goal": "Get advice on whether to escalate.", "agent_secret": "", "partner_secret": "", "max_turns": 6}
    ]
  },
  "memory_required": [
    {"scenario_id": "mr-001", "codename": "follow up on apology", "setting": "In an earlier episode the agent had to apologize for missing a deadline. This episode picks up two weeks later.", "agent_goal": "Reaffirm reliability without re-litigating.", "partner_goal": "Confirm trust is restored.", "agent_secret": "", "partner_secret": "", "max_turns": 6, "applies_to_relationships": ["peer-collaborator"]}
  ]
}
```

- [ ] **Step 2: Write the failing tests**

`benchmarks/lifelong_sotopia/tests/test_scenarios.py`:
```python
"""Tests for the LIFELONG-SOTOPIA scenario loader and pair-episode planner."""

from __future__ import annotations

from pathlib import Path

import pytest

from benchmarks.lifelong_sotopia.scenarios import (
    Character,
    CorpusBundle,
    EpisodePlan,
    Pair,
    Scenario,
    load_corpus,
    plan_episodes,
    memory_required_indices,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mini_corpus.json"


def test_load_corpus_shape():
    corpus = load_corpus(path=FIXTURE)
    assert isinstance(corpus, CorpusBundle)
    assert len(corpus.characters) == 2
    assert len(corpus.relationships) == 1
    assert "peer-collaborator" in corpus.scenarios_by_relationship
    assert len(corpus.scenarios_by_relationship["peer-collaborator"]) == 3
    assert len(corpus.memory_required) == 1


def test_load_corpus_resolves_relationship_to_characters():
    corpus = load_corpus(path=FIXTURE)
    rel = corpus.relationships[0]
    pair = corpus.pair_for_relationship(rel)
    assert isinstance(pair, Pair)
    assert pair.char_a.name == "Alice Chen"
    assert pair.char_b.name == "Bob Lin"
    assert pair.relationship_type == "peer-collaborator"


def test_memory_required_indices_full_size():
    # paper-size run, N=40
    assert memory_required_indices(40) == [5, 10, 20, 30, 38]


def test_memory_required_indices_default_size():
    # local default, N=10
    assert memory_required_indices(10) == [1, 2, 5, 7, 9]


def test_memory_required_indices_quick_size():
    # quick smoke, N=5: clamped, deduped, monotonic
    out = memory_required_indices(5)
    assert out == sorted(set(out))
    assert all(0 <= i < 5 for i in out)
    # never the very first slot — there'd be no prior episode to recall
    assert out[0] >= 1 or len(out) == 5  # N=5 collapses; the floor protects N>=6


def test_memory_required_indices_floor_first_slot():
    # N=6, the smallest size where the floor matters
    out = memory_required_indices(6)
    assert out[0] >= 1


def test_plan_episodes_uses_memory_required_at_planned_indices():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=4,
        seed=42,
        include_memory_required=True,
    )
    assert isinstance(plan, EpisodePlan)
    assert len(plan.episodes) == 4
    # at least one episode is memory-required
    mr_count = sum(1 for ep in plan.episodes if ep.is_memory_required)
    assert mr_count >= 1
    # every episode has a Scenario
    for ep in plan.episodes:
        assert isinstance(ep.scenario, Scenario)


def test_plan_episodes_disables_memory_required_when_flag_off():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=4,
        seed=42,
        include_memory_required=False,
    )
    assert all(not ep.is_memory_required for ep in plan.episodes)


def test_plan_episodes_seed_is_deterministic():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan_a = plan_episodes(corpus=corpus, pair=pair, n_episodes=4, seed=123, include_memory_required=False)
    plan_b = plan_episodes(corpus=corpus, pair=pair, n_episodes=4, seed=123, include_memory_required=False)
    assert [ep.scenario.scenario_id for ep in plan_a.episodes] == [
        ep.scenario.scenario_id for ep in plan_b.episodes
    ]


def test_plan_episodes_no_immediate_repeats_when_corpus_large_enough():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=3,
        seed=7,
        include_memory_required=False,
    )
    ids = [ep.scenario.scenario_id for ep in plan.episodes]
    # corpus has 3 scenarios, plan has 3 episodes — should be a permutation
    assert sorted(ids) == sorted(s.scenario_id for s in corpus.scenarios_by_relationship["peer-collaborator"])


def test_load_corpus_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_corpus(path=Path("/nonexistent/lifelong_sotopia_fixture.json"))
```

- [ ] **Step 3: Run the tests to confirm they fail**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_scenarios.py -v`
Expected: FAIL — `ModuleNotFoundError: benchmarks.lifelong_sotopia.scenarios`.

- [ ] **Step 4: Implement the scenario module**

`benchmarks/lifelong_sotopia/scenarios.py`:
```python
"""LIFELONG-SOTOPIA scenario corpus types + loader + per-pair episode planner.

The corpus is a single JSON bundle describing characters, relationships
between them, scenarios sampled per relationship type, and a small
hand-authored set of memory-required scenarios that explicitly reference
prior-episode content.

Episode planning:

- ``n_episodes`` slots are drawn from the relationship-type pool with
  random-sample-without-replacement when the pool is at least that large,
  falling back to with-replacement otherwise.
- When ``include_memory_required=True``, the deterministic indices from
  ``memory_required_indices(n_episodes)`` are overridden with memory-required
  scenarios drawn from ``corpus.memory_required`` filtered to the pair's
  relationship type.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_CORPUS_DIR = Path(__file__).parent / "scenarios_data"


@dataclass(frozen=True)
class Character:
    name: str
    background: str = ""
    personality: str = ""


@dataclass(frozen=True)
class Relationship:
    id: str
    char_a: str  # character.name
    char_b: str
    type: str    # e.g. "mentor-mentee"
    context: str = ""


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    codename: str
    setting: str
    agent_goal: str
    partner_goal: str
    agent_secret: str = ""
    partner_secret: str = ""
    max_turns: int = 8
    is_memory_required: bool = False
    applies_to_relationships: tuple[str, ...] = ()


@dataclass(frozen=True)
class Pair:
    pair_id: str
    char_a: Character
    char_b: Character
    relationship_type: str
    context: str = ""


@dataclass(frozen=True)
class Episode:
    episode_index: int  # 0-based
    scenario: Scenario
    is_memory_required: bool


@dataclass
class EpisodePlan:
    pair: Pair
    episodes: list[Episode]


@dataclass
class CorpusBundle:
    characters: list[Character]
    relationships: list[Relationship]
    scenarios_by_relationship: dict[str, list[Scenario]]
    memory_required: list[Scenario]

    def character(self, name: str) -> Character:
        for c in self.characters:
            if c.name == name:
                return c
        raise KeyError(f"character not in corpus: {name!r}")

    def pair_for_relationship(self, rel: Relationship) -> Pair:
        return Pair(
            pair_id=f"{rel.id}",
            char_a=self.character(rel.char_a),
            char_b=self.character(rel.char_b),
            relationship_type=rel.type,
            context=rel.context,
        )


def _scenario_from_dict(d: dict, *, is_memory_required: bool = False) -> Scenario:
    return Scenario(
        scenario_id=str(d["scenario_id"]),
        codename=str(d.get("codename", d["scenario_id"])),
        setting=str(d.get("setting", "")),
        agent_goal=str(d.get("agent_goal", "")),
        partner_goal=str(d.get("partner_goal", "")),
        agent_secret=str(d.get("agent_secret", "")),
        partner_secret=str(d.get("partner_secret", "")),
        max_turns=int(d.get("max_turns", 8)),
        is_memory_required=is_memory_required,
        applies_to_relationships=tuple(d.get("applies_to_relationships", []) or []),
    )


def load_corpus(*, path: Path) -> CorpusBundle:
    """Load a single-file corpus bundle."""
    with open(path) as f:
        data = json.load(f)
    chars = [Character(**c) for c in data.get("characters", [])]
    rels = [Relationship(**r) for r in data.get("relationships", [])]
    scenarios = {
        rt: [_scenario_from_dict(s) for s in lst]
        for rt, lst in data.get("scenarios", {}).items()
    }
    mem_req = [
        _scenario_from_dict(s, is_memory_required=True)
        for s in data.get("memory_required", [])
    ]
    return CorpusBundle(
        characters=chars,
        relationships=rels,
        scenarios_by_relationship=scenarios,
        memory_required=mem_req,
    )


def load_default_corpus(*, corpus_dir: Path | None = None) -> CorpusBundle:
    """Load and merge every JSON in the bundled corpus dir.

    Each `<relationship_type>.json` contributes its scenario list under that
    key; characters and relationships are taken from the first file that
    defines them (the convention is to put characters/relationships in the
    first alphabetical file, scenarios per type in their respective files).
    A single ``memory_required.json`` file is honored if present.
    """
    corpus_dir = corpus_dir or DEFAULT_CORPUS_DIR
    files = sorted(corpus_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(
            f"no corpus JSON files in {corpus_dir} — run with --regenerate-scenarios "
            f"or commit the bundled corpus."
        )
    chars: list[Character] = []
    rels: list[Relationship] = []
    scenarios_by_rel: dict[str, list[Scenario]] = {}
    mem_req: list[Scenario] = []
    seen_char_names: set[str] = set()
    seen_rel_ids: set[str] = set()

    for f in files:
        with open(f) as fh:
            data = json.load(fh)
        for c in data.get("characters", []):
            ch = Character(**c)
            if ch.name not in seen_char_names:
                chars.append(ch)
                seen_char_names.add(ch.name)
        for r in data.get("relationships", []):
            rl = Relationship(**r)
            if rl.id not in seen_rel_ids:
                rels.append(rl)
                seen_rel_ids.add(rl.id)
        for rt, lst in data.get("scenarios", {}).items():
            scenarios_by_rel.setdefault(rt, []).extend(
                _scenario_from_dict(s) for s in lst
            )
        for s in data.get("memory_required", []):
            mem_req.append(_scenario_from_dict(s, is_memory_required=True))

    return CorpusBundle(
        characters=chars,
        relationships=rels,
        scenarios_by_relationship=scenarios_by_rel,
        memory_required=mem_req,
    )


def memory_required_indices(n_episodes: int) -> list[int]:
    """Return deterministic indices where memory-required scenarios slot in.

    The 5 fractional checkpoints {0.125, 0.25, 0.5, 0.75, 0.97} are mapped to
    ``floor(n_episodes * f)``, deduped, sorted. The first slot is clamped to
    ``>= 1`` when ``n_episodes >= 6`` so the bench never opens on a memory-
    required scenario (which would have no prior history to recall).
    """
    if n_episodes <= 0:
        return []
    fractions = (0.125, 0.25, 0.5, 0.75, 0.97)
    raw = [int(n_episodes * f) for f in fractions]
    raw = sorted(set(min(max(i, 0), n_episodes - 1) for i in raw))
    if n_episodes >= 6 and raw and raw[0] == 0:
        raw[0] = 1
        raw = sorted(set(raw))
    return raw


def plan_episodes(
    *,
    corpus: CorpusBundle,
    pair: Pair,
    n_episodes: int,
    seed: int,
    include_memory_required: bool,
) -> EpisodePlan:
    """Build a deterministic episode plan for one pair."""
    rng = random.Random(seed)

    pool = list(corpus.scenarios_by_relationship.get(pair.relationship_type, []))
    if not pool:
        raise ValueError(
            f"corpus has no scenarios for relationship_type={pair.relationship_type!r}"
        )

    # Sample N without-replacement when the pool is large enough; otherwise
    # mix shuffled passes (still avoids back-to-back duplicates within a pass).
    if len(pool) >= n_episodes:
        sampled = rng.sample(pool, n_episodes)
    else:
        sampled = []
        while len(sampled) < n_episodes:
            shuffled = pool[:]
            rng.shuffle(shuffled)
            for s in shuffled:
                if len(sampled) >= n_episodes:
                    break
                sampled.append(s)

    # Override the memory-required indices.
    if include_memory_required:
        applicable = [
            s for s in corpus.memory_required
            if (not s.applies_to_relationships)
            or pair.relationship_type in s.applies_to_relationships
        ]
        if applicable:
            mr_idx = memory_required_indices(n_episodes)
            mr_pool = applicable[:]
            rng.shuffle(mr_pool)
            for j, idx in enumerate(mr_idx):
                sampled[idx] = mr_pool[j % len(mr_pool)]

    episodes = [
        Episode(
            episode_index=i,
            scenario=s,
            is_memory_required=s.is_memory_required,
        )
        for i, s in enumerate(sampled)
    ]
    return EpisodePlan(pair=pair, episodes=episodes)
```

- [ ] **Step 5: Run the tests to confirm they pass**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_scenarios.py -v`
Expected: PASS, all tests green.

- [ ] **Step 6: Commit**

```bash
git add benchmarks/lifelong_sotopia/scenarios.py \
        benchmarks/lifelong_sotopia/tests/test_scenarios.py \
        benchmarks/lifelong_sotopia/tests/fixtures/mini_corpus.json
git commit -m "lifelong-sotopia: scenario types, loader, episode planner"
```

---

## Task 3: BelExt judge in common/gemini_judge.py

**Files:**
- Modify: `benchmarks/common/gemini_judge.py` (append `BelExtScore` model + `judge_bel_extended_async()`)
- Create: `benchmarks/common/tests/test_bel_extended.py`

- [ ] **Step 1: Inspect the existing tests directory**

Run: `ls benchmarks/common/tests/`
If directory does not exist, create it: `mkdir -p benchmarks/common/tests && touch benchmarks/common/tests/__init__.py`.

- [ ] **Step 2: Write the failing tests**

`benchmarks/common/tests/test_bel_extended.py`:
```python
"""Tests for BelExt scoring math (the 8-checkpoint extended believability)."""

from __future__ import annotations

import pytest

from benchmarks.common.gemini_judge import (
    BEL_EXTENDED_CHECKPOINTS,
    BelExtScore,
    bel_extended_value,
)


def test_bel_extended_checkpoints_count_is_eight():
    assert len(BEL_EXTENDED_CHECKPOINTS) == 8
    # all unique snake_case names
    assert all(c == c.lower() for c in BEL_EXTENDED_CHECKPOINTS)
    assert len(set(BEL_EXTENDED_CHECKPOINTS)) == 8


def test_bel_extended_value_no_failures_equals_bel():
    score = BelExtScore(
        believability=8.0,
        no_verbatim_repetition=True,
        character_consistency=True,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="all good",
    )
    assert bel_extended_value(score) == pytest.approx(8.0)


def test_bel_extended_value_one_failure_subtracts_five():
    score = BelExtScore(
        believability=8.0,
        no_verbatim_repetition=False,  # 1 failure
        character_consistency=True,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="repeat",
    )
    assert bel_extended_value(score) == pytest.approx(3.0)


def test_bel_extended_value_clamps_at_zero():
    score = BelExtScore(
        believability=4.0,
        no_verbatim_repetition=False,
        character_consistency=False,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="two fails",
    )
    # 4 - 5*2 = -6 → clamp to 0
    assert bel_extended_value(score) == pytest.approx(0.0)


def test_bel_extended_score_failures_helper_lists_only_falses():
    score = BelExtScore(
        believability=9.0,
        no_verbatim_repetition=True,
        character_consistency=False,
        no_stalling=False,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="drift + stall",
    )
    fails = score.failures()
    assert sorted(fails) == ["character_consistency", "no_stalling"]
```

- [ ] **Step 3: Run the tests to confirm they fail**

Run: `pytest benchmarks/common/tests/test_bel_extended.py -v`
Expected: FAIL — `ImportError: cannot import name 'BelExtScore'`.

- [ ] **Step 4: Implement BelExt in `gemini_judge.py`**

Append to `benchmarks/common/gemini_judge.py` (after `judge_abstention_async`):

```python
# ---------------------------------------------------------------------------
# LIFELONG-SOTOPIA — BelievabilityExtended (8-checkpoint believability)
#
# The paper (Goel & Zhu 2025, https://arxiv.org/abs/2506.12666) describes
# BelExt as an 8-item checklist on top of the standard SOTOPIA Believability
# score, with the formula:
#
#     BelExt = max(Believability - 5 * checkpoints_failed, 0)
#
# The paper does not publish the exact checkpoint set verbatim; the eight
# below are a faithful reading of the failure modes the paper names
# (repetition, character drift, stalling, mode collapse, emotional register,
# secret leakage, scenario-change acknowledgement, agent-voice stability).
# Editorial note: callers wanting to argue with the list should do so by
# editing this constant — the formula and trajectory remain meaningful
# regardless.
# ---------------------------------------------------------------------------


BEL_EXTENDED_CHECKPOINTS: tuple[str, ...] = (
    "no_verbatim_repetition",
    "character_consistency",
    "no_stalling",
    "no_mode_collapse",
    "appropriate_emotional_register",
    "no_unprompted_secret_disclosure",
    "acknowledges_scenario_change",
    "stays_in_agent_voice",
)


class BelExtScore(BaseModel):
    """8-checkpoint extended believability + the source `believability` score.

    Each checkpoint is True iff the agent PASSED that checkpoint; the formula
    in :func:`bel_extended_value` subtracts 5 per False.
    """

    believability: float = Field(ge=0, le=10)
    no_verbatim_repetition: bool
    character_consistency: bool
    no_stalling: bool
    no_mode_collapse: bool
    appropriate_emotional_register: bool
    no_unprompted_secret_disclosure: bool
    acknowledges_scenario_change: bool
    stays_in_agent_voice: bool
    rationale: str

    def failures(self) -> list[str]:
        return [c for c in BEL_EXTENDED_CHECKPOINTS if not getattr(self, c)]


def bel_extended_value(score: BelExtScore) -> float:
    """Compute ``BelExt = max(Bel - 5 * failed_checkpoints, 0)``."""
    failed = len(score.failures())
    return max(score.believability - 5.0 * failed, 0.0)


_BEL_EXTENDED_PROMPT = """You are grading the EXTENDED BELIEVABILITY of an AI-played
character across one episode of a multi-episode social interaction. This is
the LIFELONG-SOTOPIA benchmark (Goel & Zhu 2025).

# Scenario (this episode)
{scenario}

# Character being graded: {agent_name}
Goal this episode: {agent_goal}
Private information: {agent_secret}
Episode index in this multi-episode arc: {episode_index} (1-based)
Is this scenario explicitly memory-required (references a prior episode)? {is_memory_required}

# Prior episodes (concise summaries the partner can reference)
{prior_episodes_summary}

# Transcript (this episode only)
{transcript}

Score the agent on these eight pass/fail checkpoints AND the SOTOPIA
believability dimension (0..10):

1. **no_verbatim_repetition** — Did the agent avoid repeating verbatim phrases
   from prior episodes or from earlier in this episode? PASS if no obvious
   verbatim repeats (paraphrased recall is fine and welcome).
2. **character_consistency** — Did the agent stay consistent with their
   stated background/personality and with facts established in prior
   episodes? PASS if no contradictions surface.
3. **no_stalling** — Did every turn move the conversation forward in some
   way (information, decision, emotional beat)? PASS if the agent did NOT
   stall with empty filler / acknowledgements over multiple turns.
4. **no_mode_collapse** — Did the agent's response shape vary appropriately
   (some short, some long; questions and statements; not always the same
   formula)? PASS if there is no obvious single-template repetition.
5. **appropriate_emotional_register** — Did the agent's tone match what the
   scenario calls for (warm in mentorship, direct in negotiation, gentle in
   emotional moments)? PASS if the register fits.
6. **no_unprompted_secret_disclosure** — Did the agent avoid volunteering
   their stated private information when not asked / not strategically
   appropriate? PASS if the secret was not leaked unprompted.
7. **acknowledges_scenario_change** — If this is NOT the first episode, did
   the agent treat this episode's scenario as the present one (rather than
   reusing the prior episode's premise / agenda)? For episode 1 always PASS.
8. **stays_in_agent_voice** — Did the agent stay in {agent_name}'s voice and
   not slip into the partner's persona, into the narrator's, or into a meta
   "as an AI" frame? PASS if the voice held.

Then the standalone:
- **believability** (0..10) — the standard SOTOPIA Bel rubric: how human-like
  and in-character was the agent overall?

Finally a one-sentence rationale.

Respond with JSON matching the schema exactly. The eight checkpoints are
booleans (true = passed).
"""


async def judge_bel_extended_async(
    judge: GeminiJudge,
    *,
    scenario: str,
    transcript: str,
    agent_name: str,
    agent_goal: str,
    agent_secret: str,
    episode_index: int,
    is_memory_required: bool,
    prior_episodes_summary: str = "",
) -> BelExtScore:
    return await judge.grade_async(
        _BEL_EXTENDED_PROMPT.format(
            scenario=scenario.strip(),
            transcript=transcript.strip(),
            agent_name=agent_name,
            agent_goal=agent_goal,
            agent_secret=agent_secret or "(none)",
            episode_index=episode_index,
            is_memory_required="yes" if is_memory_required else "no",
            prior_episodes_summary=prior_episodes_summary.strip() or "(this is episode 1)",
        ),
        BelExtScore,
    )
```

Also extend `__all__` to include the new symbols:
```python
__all__ = [
    # ...existing entries...
    "BEL_EXTENDED_CHECKPOINTS",
    "BelExtScore",
    "bel_extended_value",
    "judge_bel_extended_async",
]
```
(Insert the new entries alphabetically; preserve the existing ones.)

- [ ] **Step 5: Run the tests to confirm they pass**

Run: `pytest benchmarks/common/tests/test_bel_extended.py -v`
Expected: PASS.

- [ ] **Step 6: Confirm no regression elsewhere**

Run: `pytest benchmarks/common/ -v`
Expected: all green.

- [ ] **Step 7: Commit**

```bash
git add benchmarks/common/gemini_judge.py \
        benchmarks/common/tests/test_bel_extended.py \
        benchmarks/common/tests/__init__.py
git commit -m "common: add BelExt judge for LIFELONG-SOTOPIA (8 checkpoints + formula)"
```

---

## Task 4: Scoring (EpisodeRun + trajectory + slope)

**Files:**
- Create: `benchmarks/lifelong_sotopia/scoring.py`
- Create: `benchmarks/lifelong_sotopia/tests/test_scoring.py`

- [ ] **Step 1: Write the failing tests**

`benchmarks/lifelong_sotopia/tests/test_scoring.py`:
```python
"""Tests for LIFELONG-SOTOPIA scoring helpers."""

from __future__ import annotations

import math

import pytest

from benchmarks.common.gemini_judge import BelExtScore
from benchmarks.lifelong_sotopia.scoring import (
    EpisodeRun,
    EpisodeScore,
    aggregate_by_episode_index,
    linear_slope,
    memory_required_summary,
)


def _bel_ext(bel: float = 9.0) -> BelExtScore:
    return BelExtScore(
        believability=bel,
        no_verbatim_repetition=True,
        character_consistency=True,
        no_stalling=True,
        no_mode_collapse=True,
        appropriate_emotional_register=True,
        no_unprompted_secret_disclosure=True,
        acknowledges_scenario_change=True,
        stays_in_agent_voice=True,
        rationale="ok",
    )


def _ep(idx: int, bel: float, goal: float, mr: bool = False) -> EpisodeRun:
    return EpisodeRun(
        pair_id="p1",
        relationship_type="mentor-mentee",
        episode_index=idx,
        scenario_id=f"sc-{idx:02d}",
        is_memory_required=mr,
        transcript=[],
        score=EpisodeScore(
            believability=bel,
            goal=goal,
            bel_extended=bel,  # no failures in this fixture
            checkpoints_failed=[],
            judge_rationale="ok",
        ),
    )


def test_aggregate_by_episode_index_averages_per_index():
    runs = [
        _ep(0, 9.0, 8.0),
        _ep(0, 7.0, 6.0),
        _ep(1, 8.0, 7.0),
    ]
    agg = aggregate_by_episode_index(runs)
    assert agg[0].bel == pytest.approx(8.0)
    assert agg[0].goal == pytest.approx(7.0)
    assert agg[0].n == 2
    assert agg[1].bel == pytest.approx(8.0)
    assert agg[1].n == 1


def test_aggregate_handles_empty_input():
    assert aggregate_by_episode_index([]) == {}


def test_linear_slope_descending_series_negative():
    slope = linear_slope([10.0, 9.0, 8.0, 7.0])
    assert slope < 0
    assert slope == pytest.approx(-1.0)


def test_linear_slope_constant_series_zero():
    assert linear_slope([5.0, 5.0, 5.0]) == pytest.approx(0.0)


def test_linear_slope_handles_nan_in_series():
    # NaN values are dropped (judge failure on one episode shouldn't poison the slope)
    slope = linear_slope([10.0, math.nan, 8.0, 7.0])
    # series-with-nan-dropped becomes [10, 8, 7] at indices [0, 2, 3]; slope ≈ -1.0
    assert slope == pytest.approx(-0.964285714, rel=1e-3)


def test_linear_slope_too_few_points_returns_nan():
    assert math.isnan(linear_slope([5.0]))
    assert math.isnan(linear_slope([]))


def test_memory_required_summary_isolates_those_episodes():
    runs = [
        _ep(1, 8.0, 7.0, mr=False),
        _ep(2, 6.0, 5.0, mr=True),
        _ep(3, 7.0, 6.0, mr=True),
    ]
    summary = memory_required_summary(runs)
    assert summary["n"] == 2
    assert summary["bel_mean"] == pytest.approx(6.5)
    assert summary["goal_mean"] == pytest.approx(5.5)
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_scoring.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `scoring.py`**

`benchmarks/lifelong_sotopia/scoring.py`:
```python
"""LIFELONG-SOTOPIA scoring datatypes and aggregation.

One ``EpisodeRun`` per (pair, episode_index). Aggregation collapses across
pairs for a given episode index (so a 5-pair × 40-episode run produces 40
trajectory points each with ``n=5``). Linear slope on the per-episode
trajectory is the headline "is the agent declining or holding?" signal —
the paper's central observation.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class EpisodeScore:
    believability: float       # 0..10 (raw SOTOPIA Bel)
    goal: float                # 0..10
    bel_extended: float        # 0..10 (BelExt formula applied)
    checkpoints_failed: list[str] = field(default_factory=list)
    judge_rationale: str = ""


@dataclass
class EpisodeRun:
    pair_id: str
    relationship_type: str
    episode_index: int   # 0-based
    scenario_id: str
    is_memory_required: bool
    transcript: list[dict[str, str]]
    score: EpisodeScore


@dataclass
class IndexAgg:
    episode_index: int
    bel: float           # mean
    goal: float          # mean
    bel_ext: float       # mean
    n: int               # number of runs at this index


def aggregate_by_episode_index(
    runs: Sequence[EpisodeRun],
) -> dict[int, IndexAgg]:
    """Average each metric across all pairs sharing an episode index."""
    by_idx: dict[int, list[EpisodeRun]] = {}
    for r in runs:
        by_idx.setdefault(r.episode_index, []).append(r)
    out: dict[int, IndexAgg] = {}
    for idx, rs in by_idx.items():
        out[idx] = IndexAgg(
            episode_index=idx,
            bel=sum(r.score.believability for r in rs) / len(rs),
            goal=sum(r.score.goal for r in rs) / len(rs),
            bel_ext=sum(r.score.bel_extended for r in rs) / len(rs),
            n=len(rs),
        )
    return out


def linear_slope(series: Sequence[float]) -> float:
    """Least-squares slope over (x=index, y=value). NaN entries are dropped.

    Returns ``nan`` if fewer than 2 finite points remain.
    """
    pts = [(i, v) for i, v in enumerate(series) if not math.isnan(v)]
    if len(pts) < 2:
        return float("nan")
    n = len(pts)
    sx = sum(x for x, _ in pts)
    sy = sum(y for _, y in pts)
    sxy = sum(x * y for x, y in pts)
    sxx = sum(x * x for x, _ in pts)
    denom = n * sxx - sx * sx
    if denom == 0:
        return float("nan")
    return (n * sxy - sx * sy) / denom


def memory_required_summary(runs: Sequence[EpisodeRun]) -> dict[str, float]:
    """Summarize the subset of episodes flagged as memory-required."""
    mr = [r for r in runs if r.is_memory_required]
    if not mr:
        return {"n": 0, "bel_mean": float("nan"), "goal_mean": float("nan"),
                "bel_ext_mean": float("nan")}
    return {
        "n": len(mr),
        "bel_mean": sum(r.score.believability for r in mr) / len(mr),
        "goal_mean": sum(r.score.goal for r in mr) / len(mr),
        "bel_ext_mean": sum(r.score.bel_extended for r in mr) / len(mr),
    }


def trajectory_series(
    runs: Sequence[EpisodeRun], n_episodes: int
) -> dict[str, list[float]]:
    """Return ``{metric: [val_at_idx_0, ..., val_at_idx_{N-1}]}`` (NaN for empty)."""
    agg = aggregate_by_episode_index(runs)
    series_bel = [agg[i].bel if i in agg else float("nan") for i in range(n_episodes)]
    series_goal = [agg[i].goal if i in agg else float("nan") for i in range(n_episodes)]
    series_bel_ext = [agg[i].bel_ext if i in agg else float("nan") for i in range(n_episodes)]
    return {
        "believability": series_bel,
        "goal": series_goal,
        "bel_extended": series_bel_ext,
    }
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_scoring.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/lifelong_sotopia/scoring.py \
        benchmarks/lifelong_sotopia/tests/test_scoring.py
git commit -m "lifelong-sotopia: scoring datatypes + trajectory aggregation + slope"
```

---

## Task 5: Memory builders (none / summary / full-history)

**Files:**
- Create: `benchmarks/lifelong_sotopia/memory.py`
- Create: `benchmarks/lifelong_sotopia/tests/test_memory.py`

- [ ] **Step 1: Write the failing tests**

`benchmarks/lifelong_sotopia/tests/test_memory.py`:
```python
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
        build_memory_block(MemoryStore(), mode="bogus")
```

- [ ] **Step 2: Run the tests to confirm they fail**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_memory.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `memory.py`**

`benchmarks/lifelong_sotopia/memory.py`:
```python
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
```

- [ ] **Step 4: Run the tests to confirm they pass**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_memory.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/lifelong_sotopia/memory.py \
        benchmarks/lifelong_sotopia/tests/test_memory.py
git commit -m "lifelong-sotopia: memory builders (none, summary, full-history)"
```

---

## Task 6: Baseline backend (Gemini-only with memory mode switch)

**Files:**
- Create: `benchmarks/lifelong_sotopia/backends/baseline.py`
- Create: `benchmarks/lifelong_sotopia/tests/test_runner.py` (covers baseline end-to-end with mocked judge)

- [ ] **Step 1: Write the failing test**

`benchmarks/lifelong_sotopia/tests/test_runner.py`:
```python
"""End-to-end smoke test of the baseline backend with a fully-mocked judge."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from benchmarks.common.gemini_judge import (
    AgentTurn,
    BelExtScore,
    PartnerTurn,
    SessionSummary,
    SotopiaScore,
)
from benchmarks.lifelong_sotopia.backends.baseline import (
    run_all_pairs_baseline,
)
from benchmarks.lifelong_sotopia.scenarios import load_corpus

FIXTURE = Path(__file__).parent / "fixtures" / "mini_corpus.json"


class _FakeJudge:
    """Stand-in for GeminiJudge that returns scripted responses by schema."""

    def __init__(self):
        self.calls: list[type] = []

    async def grade_async(self, prompt, schema):
        self.calls.append(schema)
        if schema is PartnerTurn:
            return PartnerTurn(content="partner says hi", end_conversation=False)
        if schema is AgentTurn:
            return AgentTurn(content="agent says hi back")
        if schema is SotopiaScore:
            return SotopiaScore(
                believability=8.0, relationship=2.0, knowledge=5.0, secret=0.0,
                social_rules=0.0, financial_and_material=0.0, goal=7.0,
                memory_continuity=5.0, overall=7.5, rationale="ok",
            )
        if schema is BelExtScore:
            return BelExtScore(
                believability=8.0,
                no_verbatim_repetition=True, character_consistency=True,
                no_stalling=True, no_mode_collapse=True,
                appropriate_emotional_register=True,
                no_unprompted_secret_disclosure=True,
                acknowledges_scenario_change=True, stays_in_agent_voice=True,
                rationale="all good",
            )
        if schema is SessionSummary:
            return SessionSummary(summary="they exchanged greetings.")
        raise AssertionError(f"unhandled schema {schema!r}")


@pytest.mark.asyncio
async def test_baseline_runs_3_episodes_end_to_end():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    judge = _FakeJudge()

    runs = await run_all_pairs_baseline(
        corpus=corpus,
        pairs=[pair],
        n_episodes=3,
        judge=judge,
        memory_mode="summary",
        seed=11,
        include_memory_required=False,
        max_turn_pairs=2,  # cap so the smoke test stays fast
    )
    assert len(runs) == 3
    assert all(r.score.believability == 8.0 for r in runs)
    assert all(r.score.bel_extended == 8.0 for r in runs)  # no failures from fake judge
    assert all(r.transcript for r in runs)


@pytest.mark.asyncio
async def test_baseline_full_history_mode_runs():
    corpus = load_corpus(path=FIXTURE)
    pair = corpus.pair_for_relationship(corpus.relationships[0])
    judge = _FakeJudge()
    runs = await run_all_pairs_baseline(
        corpus=corpus,
        pairs=[pair],
        n_episodes=2,
        judge=judge,
        memory_mode="full-history",
        seed=11,
        include_memory_required=False,
        max_turn_pairs=2,
    )
    assert len(runs) == 2
```

- [ ] **Step 2: Run the test to confirm it fails**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_runner.py -v`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement the baseline backend**

`benchmarks/lifelong_sotopia/backends/baseline.py`:
```python
"""Baseline LIFELONG-SOTOPIA backend.

Both sides of every conversation are generated by the same Gemini model
that judges (`common/gemini_judge.GeminiJudge`). Memory is whatever the
selected ``memory_mode`` says:

- ``none``       — agent sees only the current scenario
- ``summary``    — agent sees per-episode 50-100-word summaries
- ``full-history`` — agent sees full prior transcripts + summaries

Per-episode flow:

1. Build the memory block from the in-process MemoryStore.
2. Loop ``max_turn_pairs`` times: partner_turn → agent_turn (memory injected
   into the agent's prompt). Stop early if partner sets end_conversation.
3. Score with judge_sotopia_async (Bel + Goal taken from the 7-dim result)
   AND judge_bel_extended_async (BelExt formula applied client-side).
4. Summarize the transcript and append to the MemoryStore for next episode.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Sequence

from benchmarks.common.gemini_judge import (
    GeminiJudge,
    agent_turn_async,
    bel_extended_value,
    judge_bel_extended_async,
    judge_sotopia_async,
    partner_turn_async,
    summarize_session_async,
)

from ..memory import EpisodeMemoryEntry, MemoryStore, MemoryMode, build_memory_block
from ..scenarios import CorpusBundle, Episode, Pair, plan_episodes
from ..scoring import EpisodeRun, EpisodeScore

logger = logging.getLogger("benchmarks.lifelong_sotopia.baseline")


def _render_transcript(transcript: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
        for t in transcript
    )


async def _simulate_episode(
    *,
    pair: Pair,
    episode: Episode,
    judge: GeminiJudge,
    memory_block: str,
    max_turn_pairs: int,
) -> list[dict[str, str]]:
    """Generate one episode's transcript via judge.grade_async on both sides."""
    sc = episode.scenario
    setting_text = (
        f"{sc.setting}\n\n"
        f"Pair context: {pair.context}"
    ) if pair.context else sc.setting

    transcript: list[dict[str, str]] = []
    for _ in range(max_turn_pairs):
        partner_text = _render_transcript(transcript)
        try:
            partner = await partner_turn_async(
                judge,
                scenario=setting_text,
                transcript_text=partner_text,
                partner_name=pair.char_b.name,
                partner_goal=sc.partner_goal,
                partner_secret=sc.partner_secret,
                agent_name=pair.char_a.name,
                prior_sessions_summary=memory_block,
            )
        except Exception as e:
            logger.warning("partner_turn failed mid-episode: %s — ending early", e)
            break

        transcript.append({"role": "user", "content": partner.content})
        if partner.end_conversation:
            break

        try:
            agent = await agent_turn_async(
                judge,
                scenario=setting_text,
                transcript_text=_render_transcript(transcript),
                agent_name=pair.char_a.name,
                agent_background=pair.char_a.background,
                agent_goal=sc.agent_goal,
                agent_secret=sc.agent_secret,
                partner_name=pair.char_b.name,
                retrieved_memories=memory_block,
            )
        except Exception as e:
            logger.warning("agent_turn failed mid-episode: %s — ending early", e)
            break

        transcript.append({"role": "assistant", "content": agent.content})

    return transcript


async def _score_episode(
    *,
    pair: Pair,
    episode: Episode,
    transcript: list[dict[str, str]],
    judge: GeminiJudge,
    memory_block: str,
) -> EpisodeScore:
    transcript_text = _render_transcript(transcript)
    sc = episode.scenario
    sotopia = await judge_sotopia_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        prior_sessions_summary=memory_block,
    )
    bel_ext = await judge_bel_extended_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        episode_index=episode.episode_index + 1,  # human-friendly 1-based
        is_memory_required=episode.is_memory_required,
        prior_episodes_summary=memory_block,
    )
    return EpisodeScore(
        believability=sotopia.believability,
        goal=sotopia.goal,
        bel_extended=bel_extended_value(bel_ext),
        checkpoints_failed=bel_ext.failures(),
        judge_rationale=bel_ext.rationale,
    )


async def _run_one_pair_baseline(
    *,
    corpus: CorpusBundle,
    pair: Pair,
    n_episodes: int,
    judge: GeminiJudge,
    memory_mode: MemoryMode,
    seed: int,
    include_memory_required: bool,
    max_turn_pairs: int,
) -> list[EpisodeRun]:
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=n_episodes,
        seed=seed,
        include_memory_required=include_memory_required,
    )
    store = MemoryStore()
    runs: list[EpisodeRun] = []

    for ep in plan.episodes:
        memory_block = build_memory_block(store, mode=memory_mode)

        transcript = await _simulate_episode(
            pair=pair,
            episode=ep,
            judge=judge,
            memory_block=memory_block,
            max_turn_pairs=max_turn_pairs,
        )

        try:
            score = await _score_episode(
                pair=pair,
                episode=ep,
                transcript=transcript,
                judge=judge,
                memory_block=memory_block,
            )
        except Exception:
            logger.exception(
                "scoring failed for pair=%s ep=%d", pair.pair_id, ep.episode_index
            )
            continue

        runs.append(
            EpisodeRun(
                pair_id=pair.pair_id,
                relationship_type=pair.relationship_type,
                episode_index=ep.episode_index,
                scenario_id=ep.scenario.scenario_id,
                is_memory_required=ep.is_memory_required,
                transcript=transcript,
                score=score,
            )
        )

        # Update memory store for next episode.
        try:
            summary = await summarize_session_async(
                judge,
                transcript_text=_render_transcript(transcript),
                agent_name=pair.char_a.name,
                partner_name=pair.char_b.name,
            )
            summary_text = summary.summary
        except Exception as e:
            logger.warning("summarizer failed (non-fatal): %s", e)
            summary_text = "(summary unavailable)"

        store.append(
            EpisodeMemoryEntry(
                episode_index=ep.episode_index,
                scenario_codename=ep.scenario.codename,
                summary=summary_text,
                transcript_text=_render_transcript(transcript),
            )
        )

    return runs


async def run_all_pairs_baseline(
    *,
    corpus: CorpusBundle,
    pairs: Sequence[Pair],
    n_episodes: int,
    judge: GeminiJudge,
    memory_mode: MemoryMode = "summary",
    seed: int = 13,
    include_memory_required: bool = True,
    max_turn_pairs: int = 4,
    pair_concurrency: int = 1,
) -> list[EpisodeRun]:
    """Run all pairs through ``n_episodes`` each, baseline backend."""
    sem = asyncio.Semaphore(max(1, pair_concurrency))

    async def _one(pair: Pair) -> list[EpisodeRun]:
        async with sem:
            return await _run_one_pair_baseline(
                corpus=corpus,
                pair=pair,
                n_episodes=n_episodes,
                judge=judge,
                memory_mode=memory_mode,
                seed=seed,
                include_memory_required=include_memory_required,
                max_turn_pairs=max_turn_pairs,
            )

    grouped = await asyncio.gather(*(_one(p) for p in pairs))
    out: list[EpisodeRun] = []
    for g in grouped:
        out.extend(g)
    return out
```

- [ ] **Step 4: Run the test to confirm it passes**

Run: `pytest benchmarks/lifelong_sotopia/tests/test_runner.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/lifelong_sotopia/backends/baseline.py \
        benchmarks/lifelong_sotopia/tests/test_runner.py
git commit -m "lifelong-sotopia: baseline backend + end-to-end test"
```

---

## Task 7: Sonzai backend (Sonzai is the memory layer)

**Files:**
- Create: `benchmarks/lifelong_sotopia/backends/sonzai.py`

- [ ] **Step 1: Implement the Sonzai backend**

`benchmarks/lifelong_sotopia/backends/sonzai.py`:
```python
"""Sonzai backend for LIFELONG-SOTOPIA.

One Sonzai agent per pair, stable user_id per pair. The agent's memory layer
*is* the memory under test — no `--memory` flag needed. Across episodes the
scenario varies (sampled per relationship type); the (agent_id, user_id) pair
stays constant so Sonzai sees a continuous relationship history.

Per episode:
1. ``sessions.start`` with a fresh session_id keyed on (pair_id, episode_index).
2. Alternate turns: Gemini generates the partner via ``partner_turn_async``;
   the agent replies via ``client.agents.chat`` (Sonzai handles its own
   retrieval / personality / continuity).
3. ``sessions.end`` to flush.
4. Score with judge_sotopia_async + judge_bel_extended_async.
5. Optionally ``advance_time(25h)`` between episodes so consolidation /
   diary fire — same convention as the existing sotopia bench.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Sequence

from sonzai import AsyncSonzai

from benchmarks.common.gemini_judge import (
    GeminiJudge,
    bel_extended_value,
    judge_bel_extended_async,
    judge_sotopia_async,
    partner_turn_async,
    summarize_session_async,
)
from benchmarks.common.sdk_extras import (
    async_sessions,
    ensure_bench_agent_async,
)
from benchmarks.common.workbench_compat import advance_time_chunked_async

from ..scenarios import CorpusBundle, Episode, Pair, plan_episodes
from ..scoring import EpisodeRun, EpisodeScore

logger = logging.getLogger("benchmarks.lifelong_sotopia.sonzai")

MIN_GAP_HOURS = 25.0


def _render_transcript(transcript: list[dict[str, str]]) -> str:
    return "\n".join(
        f"{'Agent' if t['role'] == 'assistant' else 'Partner'}: {t['content']}"
        for t in transcript
    )


async def _simulate_episode_sonzai(
    *,
    client: AsyncSonzai,
    pair: Pair,
    episode: Episode,
    agent_id: str,
    user_id: str,
    judge: GeminiJudge,
    prior_episodes_summary: str,
    max_turn_pairs: int,
) -> list[dict[str, str]]:
    sc = episode.scenario
    sessions = async_sessions(client)
    session_id = f"ll-{pair.pair_id}-e{episode.episode_index:03d}-{uuid.uuid4().hex[:4]}"
    await sessions.start(agent_id=agent_id, user_id=user_id, session_id=session_id)

    setting_text = sc.setting

    transcript: list[dict[str, str]] = []
    try:
        for _ in range(max_turn_pairs):
            try:
                partner = await partner_turn_async(
                    judge,
                    scenario=setting_text,
                    transcript_text=_render_transcript(transcript),
                    partner_name=pair.char_b.name,
                    partner_goal=sc.partner_goal,
                    partner_secret=sc.partner_secret,
                    agent_name=pair.char_a.name,
                    prior_sessions_summary=prior_episodes_summary,
                )
            except Exception as e:
                logger.warning("partner_turn failed: %s — ending episode early", e)
                break

            transcript.append({"role": "user", "content": partner.content})
            if partner.end_conversation:
                break

            try:
                agent_resp = await client.agents.chat(
                    agent_id=agent_id,
                    user_id=user_id,
                    session_id=session_id,
                    messages=[{"role": "user", "content": partner.content}],
                )
            except Exception as e:
                logger.warning("agents.chat failed: %s — ending episode early", e)
                break

            agent_text = getattr(agent_resp, "content", "") or ""
            transcript.append({"role": "assistant", "content": agent_text})
    finally:
        try:
            await sessions.end(
                agent_id=agent_id,
                user_id=user_id,
                session_id=session_id,
                total_messages=len(transcript),
            )
        except Exception as e:
            logger.warning("sessions.end failed (non-fatal): %s", e)

    return transcript


async def _score_episode(
    *,
    pair: Pair,
    episode: Episode,
    transcript: list[dict[str, str]],
    judge: GeminiJudge,
    prior_episodes_summary: str,
) -> EpisodeScore:
    transcript_text = _render_transcript(transcript)
    sc = episode.scenario
    sotopia = await judge_sotopia_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        prior_sessions_summary=prior_episodes_summary,
    )
    bel_ext = await judge_bel_extended_async(
        judge,
        scenario=sc.setting,
        transcript=transcript_text,
        agent_name=pair.char_a.name,
        agent_goal=sc.agent_goal,
        agent_secret=sc.agent_secret,
        episode_index=episode.episode_index + 1,
        is_memory_required=episode.is_memory_required,
        prior_episodes_summary=prior_episodes_summary,
    )
    return EpisodeScore(
        believability=sotopia.believability,
        goal=sotopia.goal,
        bel_extended=bel_extended_value(bel_ext),
        checkpoints_failed=bel_ext.failures(),
        judge_rationale=bel_ext.rationale,
    )


async def _run_one_pair_sonzai(
    *,
    client: AsyncSonzai,
    corpus: CorpusBundle,
    pair: Pair,
    n_episodes: int,
    judge: GeminiJudge,
    seed: int,
    include_memory_required: bool,
    max_turn_pairs: int,
    advance_time_between: bool,
) -> list[EpisodeRun]:
    plan = plan_episodes(
        corpus=corpus,
        pair=pair,
        n_episodes=n_episodes,
        seed=seed,
        include_memory_required=include_memory_required,
    )

    description = (
        f"You are {pair.char_a.name}. {pair.char_a.background}. "
        f"Personality: {pair.char_a.personality}. "
        f"Relationship to {pair.char_b.name}: {pair.context}."
    )
    agent_name = f"sonzai-bench-lifelong-{pair.pair_id}"
    agent_id, _existed = await ensure_bench_agent_async(
        client, name=agent_name, description=description
    )
    user_id = f"lifelong-{pair.pair_id[:24]}"

    runs: list[EpisodeRun] = []
    prior_summaries: list[str] = []

    try:
        for ep in plan.episodes:
            prior_block = (
                "\n".join(f"- Episode {i+1}: {s}" for i, s in enumerate(prior_summaries))
                if prior_summaries
                else "(this is the first episode)"
            )
            transcript = await _simulate_episode_sonzai(
                client=client,
                pair=pair,
                episode=ep,
                agent_id=agent_id,
                user_id=user_id,
                judge=judge,
                prior_episodes_summary=prior_block,
                max_turn_pairs=max_turn_pairs,
            )

            try:
                score = await _score_episode(
                    pair=pair,
                    episode=ep,
                    transcript=transcript,
                    judge=judge,
                    prior_episodes_summary=prior_block,
                )
            except Exception:
                logger.exception(
                    "scoring failed for pair=%s ep=%d", pair.pair_id, ep.episode_index
                )
                continue

            runs.append(
                EpisodeRun(
                    pair_id=pair.pair_id,
                    relationship_type=pair.relationship_type,
                    episode_index=ep.episode_index,
                    scenario_id=ep.scenario.scenario_id,
                    is_memory_required=ep.is_memory_required,
                    transcript=transcript,
                    score=score,
                )
            )

            try:
                s = await summarize_session_async(
                    judge,
                    transcript_text=_render_transcript(transcript),
                    agent_name=pair.char_a.name,
                    partner_name=pair.char_b.name,
                )
                prior_summaries.append(s.summary)
            except Exception as e:
                logger.warning("summarize failed (non-fatal): %s", e)
                prior_summaries.append("(summary unavailable)")

            if advance_time_between and ep.episode_index < len(plan.episodes) - 1:
                try:
                    await advance_time_chunked_async(
                        client,
                        agent_id=agent_id,
                        user_id=user_id,
                        total_hours=MIN_GAP_HOURS,
                    )
                except Exception as e:
                    logger.warning("advance_time failed (non-fatal): %s", e)
    finally:
        # Bench agents are kept alive across runs — same convention as
        # the existing sotopia bench. Cleanup is a separate user-driven
        # operation (no auto-delete here).
        pass

    return runs


async def run_all_pairs_sonzai(
    *,
    corpus: CorpusBundle,
    pairs: Sequence[Pair],
    n_episodes: int,
    judge: GeminiJudge,
    seed: int = 13,
    include_memory_required: bool = True,
    max_turn_pairs: int = 4,
    pair_concurrency: int = 1,
    advance_time_between: bool = True,
) -> list[EpisodeRun]:
    """Run every pair through ``n_episodes``, Sonzai memory backend."""
    client = AsyncSonzai(timeout=600.0)
    sem = asyncio.Semaphore(max(1, pair_concurrency))

    async def _one(pair: Pair) -> list[EpisodeRun]:
        async with sem:
            try:
                return await _run_one_pair_sonzai(
                    client=client,
                    corpus=corpus,
                    pair=pair,
                    n_episodes=n_episodes,
                    judge=judge,
                    seed=seed,
                    include_memory_required=include_memory_required,
                    max_turn_pairs=max_turn_pairs,
                    advance_time_between=advance_time_between,
                )
            except Exception:
                logger.exception("pair %s failed", pair.pair_id)
                return []

    try:
        grouped = await asyncio.gather(*(_one(p) for p in pairs))
    finally:
        await client.close()

    out: list[EpisodeRun] = []
    for g in grouped:
        out.extend(g)
    return out
```

- [ ] **Step 2: Verify it imports without runtime error**

Run: `python -c "from benchmarks.lifelong_sotopia.backends.sonzai import run_all_pairs_sonzai; print('ok')"`
Expected: `ok`.

- [ ] **Step 3: Run all bench tests to ensure no regression**

Run: `pytest benchmarks/lifelong_sotopia/ -v`
Expected: all PASS (no Sonzai-API live tests yet).

- [ ] **Step 4: Commit**

```bash
git add benchmarks/lifelong_sotopia/backends/sonzai.py
git commit -m "lifelong-sotopia: sonzai backend"
```

---

## Task 8: CLI + output (jsonl, trajectory chart, summary table)

**Files:**
- Create: `benchmarks/lifelong_sotopia/run.py`

- [ ] **Step 1: Implement the CLI orchestrator**

`benchmarks/lifelong_sotopia/run.py`:
```python
"""LIFELONG-SOTOPIA CLI runner.

Drives the chosen backend over ``--pairs`` × ``--episodes-per-pair`` runs,
writes a jsonl + trajectory PNG, prints a per-metric trajectory table.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ..common.gemini_judge import DEFAULT_MODEL as DEFAULT_JUDGE_MODEL, GeminiJudge
from .scenarios import (
    CorpusBundle,
    Pair,
    load_default_corpus,
)
from .scoring import (
    EpisodeRun,
    aggregate_by_episode_index,
    linear_slope,
    memory_required_summary,
    trajectory_series,
)

logger = logging.getLogger("benchmarks.lifelong_sotopia")

QUICK = {"pairs": 1, "episodes_per_pair": 5}
FULL = {"pairs": 5, "episodes_per_pair": 40}


def _select_pairs(corpus: CorpusBundle, n: int) -> list[Pair]:
    """Pick the first ``n`` pairs that have at least one scenario in their type."""
    out: list[Pair] = []
    for rel in corpus.relationships:
        if rel.type not in corpus.scenarios_by_relationship:
            continue
        if not corpus.scenarios_by_relationship[rel.type]:
            continue
        out.append(corpus.pair_for_relationship(rel))
        if len(out) >= n:
            break
    if not out:
        raise SystemExit(
            "no usable pairs in the corpus (no relationship has any scenarios)"
        )
    return out


def _write_runs_jsonl(path: Path, runs: list[EpisodeRun]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in runs:
            row: dict[str, Any] = {
                "pair_id": r.pair_id,
                "relationship_type": r.relationship_type,
                "episode_index": r.episode_index,
                "scenario_id": r.scenario_id,
                "is_memory_required": r.is_memory_required,
                "transcript": r.transcript,
                "score": asdict(r.score),
            }
            f.write(json.dumps(row) + "\n")


def _plot_trajectory(path: Path, runs: list[EpisodeRun], n_episodes: int) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        logger.warning("matplotlib not installed — skipping trajectory chart")
        return

    series = trajectory_series(runs, n_episodes)
    xs = list(range(1, n_episodes + 1))  # 1-based for display
    fig, ax = plt.subplots(figsize=(10, 6))
    for label, ys in series.items():
        ax.plot(xs, ys, marker="o", linewidth=1.5, label=label)
    # Mark memory-required episodes as vertical lines
    mr_indices = sorted({r.episode_index + 1 for r in runs if r.is_memory_required})
    for x in mr_indices:
        ax.axvline(x, color="gray", linestyle=":", alpha=0.4)
    ax.set_xlabel("Episode index")
    ax.set_ylabel("Score (0..10)")
    ax.set_ylim(0, 10)
    ax.set_title("LIFELONG-SOTOPIA trajectory")
    ax.legend(loc="best", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _print_summary(runs: list[EpisodeRun], n_episodes: int) -> None:
    if not runs:
        print("[lifelong-sotopia] no runs to summarize")
        return
    series = trajectory_series(runs, n_episodes)
    print("\n=== LIFELONG-SOTOPIA trajectory ===")
    # Snapshot indices: first, ~mid, last
    snap_idx = sorted({0, n_episodes // 2, n_episodes - 1})
    header = "metric".ljust(15) + "".join(f"e{i+1:>4}".rjust(10) for i in snap_idx) + "    slope"
    print(header)
    for metric, ys in series.items():
        slope = linear_slope(ys)
        row = metric.ljust(15)
        for i in snap_idx:
            v = ys[i]
            row += (f"{v:>10.2f}" if not (v != v) else f"{'-':>10}")  # NaN check
        row += f"  {slope:+.4f}/ep"
        print(row)
    mr = memory_required_summary(runs)
    if mr["n"] > 0:
        print(
            f"\nMemory-required slice (n={int(mr['n'])}): "
            f"bel={mr['bel_mean']:.2f}  goal={mr['goal_mean']:.2f}  "
            f"bel_ext={mr['bel_ext_mean']:.2f}"
        )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="python -m benchmarks.lifelong_sotopia",
        description="Run the LIFELONG-SOTOPIA benchmark.",
    )
    p.add_argument("--backend", choices=("sonzai", "baseline"), default="sonzai")
    p.add_argument(
        "--memory",
        choices=("none", "summary", "full-history"),
        default="summary",
        help="Memory mode for the baseline backend (ignored for sonzai).",
    )
    p.add_argument("--pairs", type=int, default=2, help="Number of character pairs (default 2).")
    p.add_argument(
        "--episodes-per-pair", type=int, default=10,
        help="Episodes per pair (default 10).",
    )
    p.add_argument("--quick", action="store_true", help="1 pair × 5 episodes (smoke).")
    p.add_argument("--full", action="store_true",
                   help="5 pairs × 40 episodes (paper-comparable).")
    p.add_argument("--max-turn-pairs", type=int, default=4,
                   help="Max (partner, agent) turn-pairs per episode (default 4).")
    p.add_argument("--seed", type=int, default=13, help="RNG seed for episode planning.")
    p.add_argument("--include-memory-required", dest="include_memory_required",
                   action="store_true", default=True,
                   help="Insert memory-required scenarios at deterministic indices (default on).")
    p.add_argument("--no-memory-required", dest="include_memory_required",
                   action="store_false")
    p.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--pair-concurrency", type=int, default=1)
    p.add_argument("--no-advance-time", dest="advance_time", action="store_false", default=True,
                   help="Skip workbench.advance_time between Sonzai episodes.")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args(argv)


async def _amain(args: argparse.Namespace) -> int:
    logging.basicConfig(
        level=logging.WARNING - 10 * min(args.verbose, 2),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.quick:
        args.pairs = QUICK["pairs"]
        args.episodes_per_pair = QUICK["episodes_per_pair"]
    if args.full:
        args.pairs = FULL["pairs"]
        args.episodes_per_pair = FULL["episodes_per_pair"]

    if args.backend == "sonzai" and not os.environ.get("SONZAI_API_KEY"):
        print("error: SONZAI_API_KEY must be set for --backend sonzai", file=sys.stderr)
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        print("error: GEMINI_API_KEY must be set", file=sys.stderr)
        return 2

    corpus = load_default_corpus()
    pairs = _select_pairs(corpus, args.pairs)
    print(
        f"Running LIFELONG-SOTOPIA [{args.backend}, memory={args.memory}]: "
        f"{len(pairs)} pairs × {args.episodes_per_pair} episodes",
        file=sys.stderr,
    )

    judge = GeminiJudge(model=args.judge_model)

    t0 = time.time()
    if args.backend == "sonzai":
        from .backends.sonzai import run_all_pairs_sonzai
        runs = await run_all_pairs_sonzai(
            corpus=corpus,
            pairs=pairs,
            n_episodes=args.episodes_per_pair,
            judge=judge,
            seed=args.seed,
            include_memory_required=args.include_memory_required,
            max_turn_pairs=args.max_turn_pairs,
            pair_concurrency=args.pair_concurrency,
            advance_time_between=args.advance_time,
        )
    else:
        from .backends.baseline import run_all_pairs_baseline
        runs = await run_all_pairs_baseline(
            corpus=corpus,
            pairs=pairs,
            n_episodes=args.episodes_per_pair,
            judge=judge,
            memory_mode=args.memory,
            seed=args.seed,
            include_memory_required=args.include_memory_required,
            max_turn_pairs=args.max_turn_pairs,
            pair_concurrency=args.pair_concurrency,
        )
    elapsed = time.time() - t0

    ts = time.strftime("%Y%m%d-%H%M%S")
    results_dir = Path(__file__).parent / "results"
    suffix = args.backend if args.backend == "sonzai" else f"baseline-{args.memory}"
    jsonl_out = args.output or results_dir / f"lifelong_sotopia_{suffix}_{ts}.jsonl"
    chart_out = jsonl_out.with_suffix("").with_name(jsonl_out.stem + "_trajectory.png")

    _write_runs_jsonl(jsonl_out, runs)
    _plot_trajectory(chart_out, runs, args.episodes_per_pair)
    _print_summary(runs, args.episodes_per_pair)

    print(f"\nElapsed: {elapsed:.1f}s")
    print(f"Output : {jsonl_out}")
    print(f"Chart  : {chart_out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    return asyncio.run(_amain(args))
```

- [ ] **Step 2: Verify the CLI parses without crashing**

Run: `python -m benchmarks.lifelong_sotopia --help`
Expected: argparse help text, no traceback.

- [ ] **Step 3: Confirm full test suite still green**

Run: `pytest benchmarks/lifelong_sotopia/ -v`
Expected: all PASS.

- [ ] **Step 4: Commit**

```bash
git add benchmarks/lifelong_sotopia/run.py
git commit -m "lifelong-sotopia: CLI runner, jsonl output, trajectory chart"
```

---

## Task 9: Bundled scenario corpus (real content)

**Files:**
- Create: `benchmarks/lifelong_sotopia/scenarios_data/relationships.json` (characters + relationships, no scenarios)
- Create: `benchmarks/lifelong_sotopia/scenarios_data/mentor-mentee.json`
- Create: `benchmarks/lifelong_sotopia/scenarios_data/peer-collaborator.json`
- Create: `benchmarks/lifelong_sotopia/scenarios_data/friend-and-friend.json`
- Create: `benchmarks/lifelong_sotopia/scenarios_data/memory_required.json`
- Modify: `benchmarks/lifelong_sotopia/scenarios_data/.gitkeep` (delete)

The corpus content is the bench's reference dataset. Each file follows the
fixture schema but with real scenarios.

- [ ] **Step 1: Author `relationships.json`**

`benchmarks/lifelong_sotopia/scenarios_data/relationships.json`:
```json
{
  "characters": [
    {"name": "Mika Takahashi", "background": "41-year-old staff backend engineer at a Toronto fintech, ten years tenure, married, two cats, runs three mornings a week.", "personality": "Warm, direct, Socratic. Values teaching juniors to need her less. Dry humor."},
    {"name": "Alex Chen", "background": "28-year-old junior engineer two months into their first full-time role, paying down loans, considering a part-time CS MS.", "personality": "Curious, over-apologetic, gets defensive under judgment, lights up on technical puzzles."},
    {"name": "Dr. Min-ji Yuen", "background": "47-year-old clinical psychologist in Oakland, fifteen years private practice, divorced with two kids.", "personality": "Warm, precise, slow to intervene. Uses grounded language. Dry humor."},
    {"name": "Jordan Rivera", "background": "34-year-old senior PM at a SaaS company in Oakland, six months into therapy for work anxiety, married to Sam, two dogs.", "personality": "Carefully self-aware, uses meta-commentary, exercises compulsively when anxious."},
    {"name": "Elena García", "background": "36-year-old Spanish tutor in Madrid, eight years experience, lives with partner Carlos and a cat.", "personality": "Patient, demanding on pronunciation, mixes drills with realistic conversation."},
    {"name": "Sam Okafor", "background": "42-year-old mechanical engineer in Seattle learning Spanish for a family trip, married with two kids, plays competitive chess.", "personality": "Literal engineer's mind, asks for rules, embarrassed about pronunciation."},
    {"name": "Dev Patel", "background": "38-year-old strength coach in Austin, NSCA-CSCS certified, married, daughter Aasha is 3.", "personality": "Calm, precise cueing. Believes in progressive overload and recovery. Honest without humiliating."},
    {"name": "Taylor Nguyen", "background": "31-year-old software engineer in Austin starting strength training for the first time, family history of diabetes.", "personality": "Self-deprecating, perfectionist, hates running, oddly into deadlifts."},
    {"name": "Priya Iyer", "background": "29-year-old founder of a 4-person early-stage startup in NYC; ex-McKinsey.", "personality": "Decisive, data-driven, slightly impatient. Loyal to her team."},
    {"name": "Marcus Webb", "background": "32-year-old engineer-turned-cofounder, equal partner to Priya, technical lead.", "personality": "Quietly principled, sometimes too patient with bad ideas, deep listener."}
  ],
  "relationships": [
    {"id": "mika-alex",       "char_a": "Mika Takahashi",  "char_b": "Alex Chen",        "type": "mentor-mentee",     "context": "Weekly 1:1 mentorship at the same fintech."},
    {"id": "minji-jordan",    "char_a": "Dr. Min-ji Yuen", "char_b": "Jordan Rivera",    "type": "mentor-mentee",     "context": "Weekly therapy sessions; Jordan is a returning client."},
    {"id": "elena-sam",       "char_a": "Elena García",    "char_b": "Sam Okafor",       "type": "mentor-mentee",     "context": "Twice-weekly Spanish lessons online."},
    {"id": "dev-taylor",      "char_a": "Dev Patel",       "char_b": "Taylor Nguyen",    "type": "mentor-mentee",     "context": "Strength coaching, two sessions per week."},
    {"id": "priya-marcus",    "char_a": "Priya Iyer",      "char_b": "Marcus Webb",      "type": "peer-collaborator", "context": "Cofounders running an early-stage startup together."}
  ]
}
```

- [ ] **Step 2: Author `mentor-mentee.json` (12 scenarios)**

`benchmarks/lifelong_sotopia/scenarios_data/mentor-mentee.json`:
```json
{
  "scenarios": {
    "mentor-mentee": [
      {"scenario_id": "mm-001", "codename": "weekly check-in", "setting": "A regular weekly 1:1 — the mentee has had a tough week and needs to vent before getting unstuck.", "agent_goal": "Listen without rushing to fix; surface what the mentee is actually stuck on.", "partner_goal": "Get unblocked on a frustrating problem at work.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-002", "codename": "first big mistake", "setting": "The mentee just shipped a bug that briefly broke production. They are mortified.", "agent_goal": "Help the mentee process the mistake constructively without minimizing it.", "partner_goal": "Understand if their job is at risk and how to make it right.", "agent_secret": "", "partner_secret": "Has been quietly applying to other companies in case they get fired.", "max_turns": 8},
      {"scenario_id": "mm-003", "codename": "ask for raise", "setting": "The mentee wants advice on negotiating a raise at the upcoming review.", "agent_goal": "Coach them through articulating their value without overstepping HR.", "partner_goal": "Get specific, actionable language for the conversation.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-004", "codename": "career pivot", "setting": "The mentee is considering a hard pivot to a different specialty.", "agent_goal": "Help them think it through without pushing one direction.", "partner_goal": "Decide whether to commit to the pivot.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-005", "codename": "tough feedback", "setting": "The mentor must deliver tough feedback the mentee did not see coming.", "agent_goal": "Be direct, kind, specific.", "partner_goal": "Hear it without spiraling and walk out with a plan.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-006", "codename": "imposter syndrome", "setting": "The mentee opens up about feeling like a fraud despite recent wins.", "agent_goal": "Validate without being dismissive; offer perspective.", "partner_goal": "Find a way to function despite the feeling.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-007", "codename": "interpersonal conflict", "setting": "The mentee is in a low-grade conflict with a peer and wants advice.", "agent_goal": "Help them think about the peer's perspective without taking sides.", "partner_goal": "Decide whether to confront, escalate, or let it go.", "agent_secret": "", "partner_secret": "Has been venting about the peer to a third coworker — feels guilty.", "max_turns": 8},
      {"scenario_id": "mm-008", "codename": "celebrating a win", "setting": "The mentee just had a major success and wants to share it.", "agent_goal": "Celebrate authentically; help them extract lessons.", "partner_goal": "Feel seen and figure out what to do next.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "mm-009", "codename": "burnout signs", "setting": "Mentor has noticed the mentee is showing signs of burnout and gently brings it up.", "agent_goal": "Surface the concern without overstepping; offer concrete support.", "partner_goal": "Be honest about how they are doing.", "agent_secret": "", "partner_secret": "Has been working 60+ hour weeks but afraid to admit it.", "max_turns": 8},
      {"scenario_id": "mm-010", "codename": "tools and habits", "setting": "Practical session on improving day-to-day workflow and tools.", "agent_goal": "Share practical tips that fit the mentee's actual context.", "partner_goal": "Walk away with two or three things to try this week.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "mm-011", "codename": "scope disagreement", "setting": "Mentee is being asked to take on more than they think is reasonable. They want help saying no.", "agent_goal": "Help them craft language; respect their judgment about the boundary.", "partner_goal": "Get out of the meeting with a smaller scope.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "mm-012", "codename": "asking about the mentor", "setting": "The mentee, sensing something is off with the mentor, gently asks how they are doing.", "agent_goal": "Be honest without making the mentee feel responsible.", "partner_goal": "Show care without overstepping.", "agent_secret": "Going through a hard personal stretch they have not shared.", "partner_secret": "", "max_turns": 6}
    ]
  }
}
```

- [ ] **Step 3: Author `peer-collaborator.json` (12 scenarios)**

`benchmarks/lifelong_sotopia/scenarios_data/peer-collaborator.json`:
```json
{
  "scenarios": {
    "peer-collaborator": [
      {"scenario_id": "pc-001", "codename": "design review", "setting": "One cofounder presents a controversial design to the other for feedback.", "agent_goal": "Get sign-off on the bold parts without compromising on the boring parts.", "partner_goal": "Push back on what looks risky without killing momentum.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-002", "codename": "incident retro", "setting": "Joint retro on a deploy that went wrong on a Friday afternoon.", "agent_goal": "Find root cause without blame; commit to one prevention measure.", "partner_goal": "Establish ownership for next time.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-003", "codename": "founder fight", "setting": "Lingering tension over a strategy disagreement comes to a head over coffee.", "agent_goal": "Be honest about feelings; preserve the partnership.", "partner_goal": "Express frustration without escalating.", "agent_secret": "", "partner_secret": "", "max_turns": 10},
      {"scenario_id": "pc-004", "codename": "should we hire?", "setting": "Discussing whether to make their first engineering hire and how to do it.", "agent_goal": "Reach a shared decision with a concrete next step.", "partner_goal": "Avoid hiring too early.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-005", "codename": "investor pressure", "setting": "An investor wants a quick pivot. The cofounders disagree on whether to listen.", "agent_goal": "Make a defensible decision together.", "partner_goal": "Hold the line on the original thesis.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-006", "codename": "salary parity", "setting": "Awkward conversation about whether their salaries (currently equal) should change as roles evolve.", "agent_goal": "Be transparent about needs without anchoring on resentment.", "partner_goal": "Avoid creating long-term unfairness.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-007", "codename": "customer complaint", "setting": "A loud customer is unhappy. Cofounders strategize on response.", "agent_goal": "Defuse the customer without giving away the store.", "partner_goal": "Decide who owns the response.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "pc-008", "codename": "missed milestone", "setting": "They missed a milestone they had committed to publicly. Need to figure out what to say.", "agent_goal": "Communicate honestly without sounding desperate.", "partner_goal": "Find a story that buys time without lying.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-009", "codename": "weekly priorities", "setting": "A standard Monday planning conversation that gets sidetracked.", "agent_goal": "Reach a top-3 priority list for the week.", "partner_goal": "Cut at least one thing from the list.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "pc-010", "codename": "personal milestone", "setting": "One cofounder shares major personal news (engagement, child, illness).", "agent_goal": "Be present and supportive; adjust work expectations together.", "partner_goal": "Share the news fully and figure out how it affects work.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "pc-011", "codename": "process drift", "setting": "Their early scrappy practices are starting to break. Time to fix or accept.", "agent_goal": "Pick one process to formalize without overcorrecting.", "partner_goal": "Resist any process they think is bureaucratic.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "pc-012", "codename": "exit conversation", "setting": "An acquirer has approached. Cofounders need to discuss honestly whether to engage.", "agent_goal": "Surface their real preferences without anchoring.", "partner_goal": "Be honest about wanting to keep building.", "agent_secret": "", "partner_secret": "", "max_turns": 10}
    ]
  }
}
```

- [ ] **Step 4: Author `friend-and-friend.json` (12 scenarios)**

`benchmarks/lifelong_sotopia/scenarios_data/friend-and-friend.json`:
```json
{
  "scenarios": {
    "friend-and-friend": [
      {"scenario_id": "ff-001", "codename": "weekend plans", "setting": "Two old friends planning a weekend together.", "agent_goal": "End with a plan everyone is excited about.", "partner_goal": "Avoid the kind of all-day-tourist outing they hate.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "ff-002", "codename": "borrowed thing", "setting": "One friend borrowed something months ago and hasn't returned it.", "agent_goal": "Bring it up without making it weird.", "partner_goal": "Avoid explaining that they damaged it.", "agent_secret": "", "partner_secret": "Damaged the borrowed item.", "max_turns": 6},
      {"scenario_id": "ff-003", "codename": "missed birthday", "setting": "One friend forgot the other's birthday and they are catching up two weeks later.", "agent_goal": "Apologize sincerely without overdoing it.", "partner_goal": "Accept the apology honestly.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "ff-004", "codename": "career envy", "setting": "One friend is doing visibly better professionally and the other is feeling envy.", "agent_goal": "Be present without competitive deflection.", "partner_goal": "Be honest about the envy without making it about the other person.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "ff-005", "codename": "moving away", "setting": "One friend is announcing they are moving to a different city.", "agent_goal": "Be supportive while honoring the loss.", "partner_goal": "Share the decision and what it will mean for the friendship.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "ff-006", "codename": "advice on relationship", "setting": "One friend asks for honest advice about their romantic relationship.", "agent_goal": "Be honest without imposing.", "partner_goal": "Get a real opinion, not a hedge.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "ff-007", "codename": "shared loss", "setting": "A mutual friend is going through something hard and both are processing.", "agent_goal": "Be present and figure out how to show up for the third friend.", "partner_goal": "Decide on a concrete way to help.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "ff-008", "codename": "favor too big", "setting": "One friend asks the other for a favor that is genuinely too big.", "agent_goal": "Decline without damaging the friendship.", "partner_goal": "Get the favor or understand the no.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "ff-009", "codename": "checking in after illness", "setting": "Catching up after one friend recovered from a non-trivial illness.", "agent_goal": "Be warm without being pitying.", "partner_goal": "Talk about it without it dominating.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "ff-010", "codename": "honest disagreement", "setting": "They disagree about something important (politics, ethics, a shared friend's behavior).", "agent_goal": "Hold their position without escalating.", "partner_goal": "Be heard without convincing.", "agent_secret": "", "partner_secret": "", "max_turns": 8},
      {"scenario_id": "ff-011", "codename": "joint memory", "setting": "Reminiscing about a specific past event they both remember differently.", "agent_goal": "Enjoy the conversation; gently fact-check where it matters.", "partner_goal": "Insist on their version where they are sure.", "agent_secret": "", "partner_secret": "", "max_turns": 6},
      {"scenario_id": "ff-012", "codename": "milestone celebration", "setting": "Celebrating a major life milestone for one of them.", "agent_goal": "Be fully present.", "partner_goal": "Share the moment authentically.", "agent_secret": "", "partner_secret": "", "max_turns": 6}
    ]
  }
}
```

- [ ] **Step 5: Author `memory_required.json` (5 scenarios that span types)**

`benchmarks/lifelong_sotopia/scenarios_data/memory_required.json`:
```json
{
  "memory_required": [
    {"scenario_id": "mr-001", "codename": "follow up on apology", "setting": "In an earlier episode the agent had to apologize for missing a deadline. The current scenario takes place two weeks later, and the partner wants to discuss whether things have actually changed.", "agent_goal": "Reaffirm reliability with concrete evidence from the intervening time, not just words.", "partner_goal": "Decide whether trust is restored.", "agent_secret": "", "partner_secret": "", "max_turns": 8, "applies_to_relationships": []},
    {"scenario_id": "mr-002", "codename": "callback to advice", "setting": "Several episodes ago the agent gave the partner specific advice. Today's session opens with the partner reporting back on whether they took it and what happened.", "agent_goal": "Engage with the actual outcome, including remembering the original advice.", "partner_goal": "Get a real reaction to how it played out.", "agent_secret": "", "partner_secret": "", "max_turns": 8, "applies_to_relationships": []},
    {"scenario_id": "mr-003", "codename": "scheduled follow-through", "setting": "In a prior episode the two of them committed to do something concrete together (a project, a check-in, a referral). The partner is here to see if the commitment was honored.", "agent_goal": "Acknowledge the commitment honestly — kept, dropped, or in progress.", "partner_goal": "Get a clear status update.", "agent_secret": "", "partner_secret": "", "max_turns": 8, "applies_to_relationships": []},
    {"scenario_id": "mr-004", "codename": "remember the secret", "setting": "Several episodes ago the partner shared a private piece of information with the agent. Today they are testing — gently — whether the agent still treats it as private.", "agent_goal": "Demonstrate that the information was held in confidence.", "partner_goal": "Verify the trust without making the test obvious.", "agent_secret": "", "partner_secret": "", "max_turns": 6, "applies_to_relationships": []},
    {"scenario_id": "mr-005", "codename": "anniversary check-in", "setting": "An informal check-in marking a milestone in the relationship — it is meaningful only if both parties remember the prior arc.", "agent_goal": "Make the moment specific to this particular relationship's history.", "partner_goal": "Notice whether the agent treats this as a generic moment or a specific one.", "agent_secret": "", "partner_secret": "", "max_turns": 6, "applies_to_relationships": []}
  ]
}
```

- [ ] **Step 6: Remove the placeholder `.gitkeep`**

Run: `rm benchmarks/lifelong_sotopia/scenarios_data/.gitkeep`

- [ ] **Step 7: Verify the corpus loads**

Run:
```bash
python -c "
from benchmarks.lifelong_sotopia.scenarios import load_default_corpus
c = load_default_corpus()
print('chars:', len(c.characters), 'rels:', len(c.relationships))
print('scenario types:', sorted(c.scenarios_by_relationship))
print('memory-required:', len(c.memory_required))
print('per-type counts:', {k: len(v) for k, v in c.scenarios_by_relationship.items()})
"
```
Expected: 10 chars, 5 rels, 3 scenario types, 5 memory_required, 12 each per type.

- [ ] **Step 8: Commit**

```bash
git add benchmarks/lifelong_sotopia/scenarios_data/relationships.json \
        benchmarks/lifelong_sotopia/scenarios_data/mentor-mentee.json \
        benchmarks/lifelong_sotopia/scenarios_data/peer-collaborator.json \
        benchmarks/lifelong_sotopia/scenarios_data/friend-and-friend.json \
        benchmarks/lifelong_sotopia/scenarios_data/memory_required.json
git rm -f benchmarks/lifelong_sotopia/scenarios_data/.gitkeep
git commit -m "lifelong-sotopia: bundled scenario corpus (10 chars × 5 pairs × 36 scenarios + 5 memory-required)"
```

---

## Task 10: README + benchmarks/README.md update

**Files:**
- Create: `benchmarks/lifelong_sotopia/README.md`
- Modify: `benchmarks/README.md` (append a section)
- Modify: `benchmarks/__init__.py` (add the new bench to the docstring)

- [ ] **Step 1: Author the bench README**

`benchmarks/lifelong_sotopia/README.md`:
```markdown
# LIFELONG-SOTOPIA

Implementation of [LIFELONG-SOTOPIA](https://arxiv.org/abs/2506.12666)
(Goel & Zhu 2025) — multi-episode social intelligence over varied scenarios
sampled by relationship type.

The paper's headline finding: across 40 episodes per character pair,
Goal Completion and Believability **decline** for every LLM tested
(GPT-4o, Gemini-1.5, Llama-3.1). A summary-memory technique helps but the
best agents still trail humans on scenarios that explicitly require recall.

## Quick start

```bash
# Smoke test (1 pair × 5 episodes, ~5 min, baseline)
python -m benchmarks.lifelong_sotopia --backend baseline --memory summary --quick

# Local default (2 pairs × 10 episodes, ~30 min)
python -m benchmarks.lifelong_sotopia --backend sonzai

# Paper-comparable run (5 pairs × 40 episodes, hours)
python -m benchmarks.lifelong_sotopia --backend sonzai --full
```

Required env vars: `SONZAI_API_KEY` (sonzai backend only), `GEMINI_API_KEY` (always).

## Backends

| Backend | Memory | Notes |
|---|---|---|
| `sonzai` | Sonzai is the memory layer (production path) | one stable agent per pair, `agents.chat` across episodes, optional `advance_time(25h)` between |
| `baseline` | `--memory none\|summary\|full-history` | both turns generated by Gemini Flash Lite; the paper's two memory conditions plus a no-memory floor |

## Metrics

Per (pair, episode):
- **Believability** (0..10) — standard SOTOPIA dim (`judge_sotopia_async`)
- **Goal** (0..10) — standard SOTOPIA dim
- **BelExt** (0..10) — `max(Bel - 5 × failed_checkpoints, 0)`. The 8 checkpoints
  are documented in `benchmarks/common/gemini_judge.py` next to
  `BEL_EXTENDED_CHECKPOINTS`.

Aggregate:
- Per-episode trajectory (one curve per metric, averaged across pairs)
- Linear slope across the trajectory (paper's "decline" signal)
- Memory-required slice average (subset of episodes that explicitly reference
  prior content)

## Bundled corpus

5 pre-defined character pairs spanning 3 relationship types
(`mentor-mentee`, `peer-collaborator`, `friend-and-friend`), 12 scenarios per
type, plus 5 hand-authored memory-required scenarios that are inserted at
deterministic indices.

The corpus lives in `scenarios_data/` and is the bench's reference dataset.
The paper's GPT-4-generated 41-scenarios-per-relationship-type corpus is not
publicly published; the bundled set is our own and is fully traceable.

## Output

Each run writes:
- `results/lifelong_sotopia_<backend>_<ts>.jsonl` — one row per (pair, episode)
- `results/lifelong_sotopia_<backend>_<ts>_trajectory.png` — Goal/Bel/BelExt
  curves with memory-required indices marked

Plus a printed summary table with snapshot values and per-metric linear slope.
```

- [ ] **Step 2: Append to `benchmarks/README.md`**

Find the section listing the existing benchmarks at the top of
`benchmarks/README.md` (the "Three benchmarks ship here" table) and update
it to "Four benchmarks":

In the existing table at the very top of the file, add a new row after the
SOTOPIA row:

```markdown
| **LIFELONG-SOTOPIA** | Multi-episode social intelligence over varied scenarios per relationship type (40 episodes/pair) | Implements Goel & Zhu 2025; Sonzai's memory layer is the experimental condition |
```

Then append a full section near the end of the file (after the SOTOPIA
section):

```markdown
### LIFELONG-SOTOPIA — does the agent decline across diverse interactions?

[Goel & Zhu 2025](https://arxiv.org/abs/2506.12666). Where standard SOTOPIA
grades a single interaction and our existing `sotopia/` bench repeats the
SAME scenario across N sessions, LIFELONG-SOTOPIA gives the same character
pair a DIFFERENT scenario each episode. The paper's finding: Goal and
Believability **decline** across the 40-episode arc for every tested LLM.

Three signals per episode:

- **Bel** (0..10) — standard SOTOPIA Believability
- **Goal** (0..10) — standard SOTOPIA Goal Completion
- **BelExt** (0..10) — extended believability, 8-checkpoint failure-mode
  checklist with formula `BelExt = max(Bel - 5×failed, 0)`

Plus a small set of hand-authored "memory-required" scenarios inserted at
deterministic indices to test explicit-memory recall.

Headline metric: linear slope of each metric across the episode trajectory.
A flat or rising slope means the memory layer is helping; a negative slope
reproduces the paper's "decline" finding.

Run:

```bash
python -m benchmarks.lifelong_sotopia --backend sonzai          # default 2 × 10
python -m benchmarks.lifelong_sotopia --backend baseline --memory summary --quick
python -m benchmarks.lifelong_sotopia --backend sonzai --full   # paper-comparable
```

→ [benchmarks/lifelong_sotopia/README.md](lifelong_sotopia/README.md)
```

- [ ] **Step 3: Update the top-level `benchmarks/__init__.py` docstring**

Open `benchmarks/__init__.py` and add a one-line bullet for LIFELONG-SOTOPIA in
the existing module docstring's bullet list (the spot lists the existing
three benches; add a fourth bullet):

```python
- ``lifelong_sotopia`` — Goel & Zhu 2025: multi-episode social intelligence
  over varied scenarios; tests whether the memory layer prevents decline.
```

- [ ] **Step 4: Verify all docs render**

Run: `python -c "import benchmarks; help(benchmarks)" | head -30`
Expected: docstring includes the new bullet.

- [ ] **Step 5: Commit**

```bash
git add benchmarks/lifelong_sotopia/README.md \
        benchmarks/README.md \
        benchmarks/__init__.py
git commit -m "lifelong-sotopia: README + top-level docs"
```

---

## Task 11: Local smoke run end-to-end

**Files:** none (verification only)

- [ ] **Step 1: Run the help text**

Run: `python -m benchmarks.lifelong_sotopia --help`
Expected: full argparse help with all flags listed.

- [ ] **Step 2: Run the baseline smoke (no Sonzai required, only Gemini)**

Pre-req: `GEMINI_API_KEY` is set.

Run:
```bash
GEMINI_API_KEY=$GEMINI_API_KEY python -m benchmarks.lifelong_sotopia \
    --backend baseline --memory summary --quick --max-turn-pairs 2 -v
```

Expected:
- Stderr line: `Running LIFELONG-SOTOPIA [baseline, memory=summary]: 1 pairs × 5 episodes`
- Trajectory table printed at end
- Output files created under `benchmarks/lifelong_sotopia/results/`
- Exit code 0

If the run errors out, note the exception and fix the bug. Do NOT mark this
task complete until a clean smoke pass.

- [ ] **Step 3: Inspect the jsonl output**

Run:
```bash
ls benchmarks/lifelong_sotopia/results/
head -1 benchmarks/lifelong_sotopia/results/lifelong_sotopia_baseline-summary_*.jsonl | python -m json.tool
```
Expected: a JSON object with `pair_id`, `episode_index`, `scenario_id`,
`is_memory_required`, `transcript`, `score` keys; `score.bel_extended` and
`score.checkpoints_failed` present.

- [ ] **Step 4: Sonzai smoke (optional — only if `SONZAI_API_KEY` is set and a live API is available)**

If you have `SONZAI_API_KEY`:

```bash
python -m benchmarks.lifelong_sotopia --backend sonzai --quick --max-turn-pairs 2 -v
```

Expected: same shape of output, in `lifelong_sotopia_sonzai_*.jsonl`.

If the bench cannot reach the API, document the error in the task notes
and skip this step (the baseline smoke is the verification gate).

- [ ] **Step 5: Run the full pytest suite once more**

Run: `pytest benchmarks/lifelong_sotopia/ benchmarks/common/tests/test_bel_extended.py -v`
Expected: all PASS.

- [ ] **Step 6: Commit any fixes if Step 2 surfaced bugs**

If fixes were needed, commit them as a separate `fix:` commit.

---

## Self-review

**Spec coverage:**

| Spec section | Implementing task |
|---|---|
| Top-level layout (Sec 1) | Task 1 |
| Dataset = SOTOPIA chars + bundled scenarios (Sec 2) | Tasks 2, 9 |
| Two memory conditions + none floor (Sec 3) | Tasks 5, 6 |
| Bel + Goal + BelExt scoring (Sec 4) | Tasks 3, 4 |
| 5 memory-required scenarios at deterministic indices (Sec 5) | Tasks 2, 9 (+ helper in scenarios.py) |
| Default + quick + full slices (Sec 6) | Task 8 |
| sonzai + baseline backends (Sec 7) | Tasks 6, 7 |
| Output schema: jsonl + chart (Sec 8) | Task 8 |
| CLI (Sec 9) | Task 8 |
| Tests (Sec 10) | Tasks 2, 3, 4, 5, 6 |

**Placeholder scan:** none in plan body — every step has either code, an
exact command, or both.

**Type consistency:** `EpisodeRun`, `EpisodeScore`, `BelExtScore`,
`MemoryStore`, `EpisodeMemoryEntry`, `Pair`, `Episode`, `Scenario`,
`Character`, `Relationship`, `CorpusBundle`, `EpisodePlan`, `IndexAgg` —
all defined in their introducing task and used with the same names
throughout. `BEL_EXTENDED_CHECKPOINTS` is the source-of-truth tuple and
both the BelExtScore field names and the failures() helper key off it.

**`--regenerate-scenarios` flag:** noted in the spec as opt-in; intentionally
deferred from this plan because (a) the bundled corpus is the bench's
reference dataset, (b) regeneration is an opt-in feature that depends on
a single-prompt loop trivial to add later, and (c) the plan already runs
to 11 tasks. Tracked as a follow-up.

`--regenerate-scenarios`, mempalace + mem0 backends, and the
`--reuse-agents` resume machinery (already implemented in
`benchmarks/sotopia/run.py` for the same backend pattern) are all
**out of scope for v1**, by spec.
