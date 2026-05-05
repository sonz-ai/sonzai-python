"""LIFELONG-SOTOPIA scenario corpus types + loader + per-pair episode planner.

The corpus is a single JSON bundle (or a directory of bundles) describing
characters, relationships between them, scenarios sampled per relationship
type, and a small hand-authored set of memory-required scenarios that
explicitly reference prior-episode content.

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
            pair_id=rel.id,
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

    Each ``<relationship_type>.json`` contributes its scenario list under that
    key; characters and relationships are taken from the first file that
    defines them. A single ``memory_required.json`` file is honored if present.
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
    raw = sorted({min(max(i, 0), n_episodes - 1) for i in raw})
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
