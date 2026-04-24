"""Persistent agent snapshots for iterative benchmark runs.

Both LongMemEval and SOTOPIA benchmarks spend most of their wall time
ingesting sessions + running ``advance_time`` — work that's redundant when
the iteration loop only changes the chat/retrieval path. This module saves
the post-ingest agent state to disk so subsequent runs can skip straight
to the measurement call.

Typical flow
------------

1. First run: bench ingests all N questions/scenarios, calls
   :func:`save_snapshot` after each item (or at end), writes a JSON file.
2. Subsequent runs: bench calls :func:`load_snapshot` at startup. If the
   snapshot's **slice** matches the current CLI flags (``--limit``,
   ``--max-sessions-per-question``, etc.), the bench uses the persisted
   ``agent_id``/``user_id`` directly and skips ingestion. Mismatched slice
   → ignore snapshot, ingest fresh.
3. Across all runs: the snapshot file is the ground truth for which server-
   side agents belong to this benchmark harness. Benchmark cleanup scripts
   can iterate the file and call ``agents.delete`` when finished.

Design choices
--------------

- **Keyed by question_id / scenario_id**, not by agent_id. Lets us re-match
  snapshots after ``--limit`` changes: if you bump from 10 to 25 questions,
  the 10 already-ingested ones keep their agents, the 15 new ones get
  ingested fresh.
- **Slice fingerprint** (``SliceKey``) is the minimal set of bench flags
  that change *ingestion semantics*. Flags that only affect *scoring* (e.g.
  ``--judge-model``) are deliberately excluded — they don't require re-
  ingest. Add a new flag here only if it changes what gets stored in memory.
- **Atomic writes**: we write to ``<path>.tmp`` then rename, so a crash
  mid-write leaves the old snapshot intact.
- **Per-entry TTL** is not enforced here — server-side agent cleanup is the
  tenant's responsibility. The snapshot file can be deleted any time to
  force re-ingest.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class SliceKey:
    """Fingerprint of the flags that affect ingestion.

    Two snapshots with the same SliceKey can be interchanged; different
    SliceKey means re-ingest. Keep this minimal — anything that only
    affects scoring (judge model, mode, concurrency) stays out.
    """

    benchmark: str  # "longmemeval" | "sotopia" | "locomo"
    limit: int
    max_sessions_per_question: int = 0
    # SOTOPIA-specific: count of sessions per scenario run so far.
    # For LongMemEval this stays 0 since ingestion is complete per item.
    sessions_per_scenario: int = 0
    # Dataset identity — if someone overrides the dataset file, the hash
    # derived from ``--dataset-path`` is part of the key so stale snapshots
    # don't silently bleed in.
    dataset_tag: str = ""

    def matches(self, other: "SliceKey") -> bool:
        """Check whether two slice keys describe compatible ingested state.

        Identity-affecting fields are benchmark-specific:
          * ``limit`` and ``dataset_tag`` always matter (different scenario /
            question pool → different ingestion).
          * LongMemEval: ``max_sessions_per_question`` picks the haystack
            slice, so it's part of identity.
          * SOTOPIA: ``sessions_per_scenario`` is a **target**, not an
            identity — a snapshot taken at N sessions resumes cleanly for
            any target ≥ N. Including it in equality would throw away the
            last_session_index every time the user bumps ``--sessions-per-
            scenario`` from 30 → 60 → 90.
          * LoCoMo: ingests the full conversation every run — there is no
            per-question session cap, so ``max_sessions_per_question`` is
            not part of identity.
        """
        if self.benchmark != other.benchmark:
            return False
        if self.limit != other.limit:
            return False
        if self.dataset_tag != other.dataset_tag:
            return False
        if self.benchmark == "sotopia":
            return True
        if self.benchmark == "locomo":
            # LoCoMo ingests the full conversation every time — no per-question
            # session cap, so max_sessions_per_question is not part of identity.
            return True
        return self.max_sessions_per_question == other.max_sessions_per_question


@dataclass
class AgentSnapshot:
    """Post-ingest state for one question/scenario."""

    key: str  # question_id or scenario_id
    agent_id: str
    user_id: str
    # Ingestion metadata for observability / cleanup.
    session_ids: list[str] = field(default_factory=list)
    ingested_at: str = ""
    # Optional per-benchmark metadata (e.g. SOTOPIA's current session index).
    meta: dict = field(default_factory=dict)


@dataclass
class SnapshotFile:
    """On-disk shape of the snapshot file."""

    slice: SliceKey
    saved_at: str
    agents: dict[str, AgentSnapshot] = field(default_factory=dict)

    def to_json(self) -> dict:
        return {
            "slice": asdict(self.slice),
            "saved_at": self.saved_at,
            "agents": {k: asdict(v) for k, v in self.agents.items()},
        }

    @classmethod
    def from_json(cls, data: dict) -> "SnapshotFile":
        slice_data = data.get("slice") or {}
        agents_data = data.get("agents") or {}
        return cls(
            slice=SliceKey(**slice_data) if slice_data else SliceKey(benchmark="", limit=0),
            saved_at=str(data.get("saved_at") or ""),
            agents={
                k: AgentSnapshot(**v) for k, v in agents_data.items() if isinstance(v, dict)
            },
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_snapshot(path: str | Path) -> SnapshotFile | None:
    """Load a snapshot file, or return None if missing / unreadable.

    Callers pass the result to :func:`should_reuse` to decide per-item
    whether to skip ingest. A return of None means "fresh start" — no
    snapshots available at all.
    """
    p = Path(path)
    if not p.exists():
        return None
    try:
        with open(p) as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return SnapshotFile.from_json(raw)


def save_snapshot(path: str | Path, snapshot: SnapshotFile) -> None:
    """Atomic write: temp file + rename. Never leaves the old file clobbered
    if the process crashes mid-save."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    snapshot.saved_at = datetime.now(timezone.utc).isoformat()
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(snapshot.to_json(), f, indent=2)
    os.replace(tmp, p)


def should_reuse(
    snapshot: SnapshotFile | None,
    current_slice: SliceKey,
    item_key: str,
) -> AgentSnapshot | None:
    """Return the persisted snapshot for ``item_key`` iff the slice matches.

    Slice mismatch → return None for every item (caller should ingest fresh
    and write a new snapshot). Per-item miss within a matching slice → also
    None; caller ingests that item and appends to the snapshot.
    """
    if snapshot is None:
        return None
    if not snapshot.slice.matches(current_slice):
        return None
    return snapshot.agents.get(item_key)


def upsert_agent(
    snapshot: SnapshotFile,
    *,
    key: str,
    agent_id: str,
    user_id: str,
    session_ids: list[str] | None = None,
    meta: dict | None = None,
) -> AgentSnapshot:
    """Add or replace one agent entry. Caller persists via ``save_snapshot``."""
    entry = AgentSnapshot(
        key=key,
        agent_id=agent_id,
        user_id=user_id,
        session_ids=list(session_ids or []),
        ingested_at=datetime.now(timezone.utc).isoformat(),
        meta=dict(meta or {}),
    )
    snapshot.agents[key] = entry
    return entry


def new_snapshot(slice_key: SliceKey) -> SnapshotFile:
    """Start an empty snapshot for a fresh ingest run."""
    return SnapshotFile(
        slice=slice_key,
        saved_at=datetime.now(timezone.utc).isoformat(),
        agents={},
    )


# ---------------------------------------------------------------------------
# Dataset-tag helper — turn a path into a stable short hash so the SliceKey
# can detect dataset override changes without storing the full path.
# ---------------------------------------------------------------------------


def dataset_tag(path: str | Path | None) -> str:
    """Short stable tag for a dataset path override.

    Empty string when the caller uses the default auto-downloaded dataset —
    that's the common case and the tag stays out of the snapshot slice.
    """
    if not path:
        return ""
    import hashlib

    return hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Persistent shared-agent pinning — separate file from the sliced snapshot
# so the agent_id survives changes to --limit / --max-sessions-per-question
# that invalidate the per-user ingest snapshot. Avoids leaking fresh agents
# on the platform every time we tweak the bench slice.
# ---------------------------------------------------------------------------


@dataclass
class PinnedAgent:
    """A long-lived (agent_id, name) pinned to disk for cross-slice reuse."""

    benchmark: str  # "longmemeval" | "sotopia"
    agent_id: str
    name: str
    created_at: str = ""


def _pinned_path(bench_dir: str | Path) -> Path:
    """Where the pinned-agent manifest lives for a given bench results dir."""
    return Path(bench_dir) / "shared_agent.json"


def load_pinned_agent(bench_dir: str | Path, benchmark: str) -> PinnedAgent | None:
    """Return the pinned agent for this benchmark, or None if unset."""
    p = _pinned_path(bench_dir)
    if not p.exists():
        return None
    try:
        with open(p) as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    if str(raw.get("benchmark") or "") != benchmark:
        # The file exists but names a different benchmark — caller should
        # treat as unset and write its own. Shouldn't normally happen since
        # each bench keeps its manifest in its own results dir.
        return None
    return PinnedAgent(
        benchmark=str(raw.get("benchmark") or ""),
        agent_id=str(raw.get("agent_id") or ""),
        name=str(raw.get("name") or ""),
        created_at=str(raw.get("created_at") or ""),
    )


def save_pinned_agent(
    bench_dir: str | Path, *, benchmark: str, agent_id: str, name: str
) -> PinnedAgent:
    """Persist the shared agent's identity atomically."""
    p = _pinned_path(bench_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    pa = PinnedAgent(
        benchmark=benchmark,
        agent_id=agent_id,
        name=name,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(asdict(pa), f, indent=2)
    os.replace(tmp, p)
    return pa


# ---------------------------------------------------------------------------
# Multi-entry pinned store — for benches with many long-lived agents (SOTOPIA
# pins one agent per scenario). Separate file from the sliced snapshot so
# agent identity survives changes to ``--sessions-per-scenario`` that only
# affect resume-from-session semantics, not the agent themselves.
# ---------------------------------------------------------------------------


def _multi_pinned_path(bench_dir: str | Path) -> Path:
    return Path(bench_dir) / "pinned_agents.json"


def load_pinned_agents(
    bench_dir: str | Path, benchmark: str
) -> dict[str, PinnedAgent]:
    """Return ``{scenario_id/key: PinnedAgent}`` for this benchmark (possibly empty)."""
    p = _multi_pinned_path(bench_dir)
    if not p.exists():
        return {}
    try:
        with open(p) as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    out: dict[str, PinnedAgent] = {}
    for key, entry in (raw.get("agents") or {}).items():
        if not isinstance(entry, dict):
            continue
        if str(entry.get("benchmark") or "") != benchmark:
            continue
        out[str(key)] = PinnedAgent(
            benchmark=str(entry.get("benchmark") or ""),
            agent_id=str(entry.get("agent_id") or ""),
            name=str(entry.get("name") or ""),
            created_at=str(entry.get("created_at") or ""),
        )
    return out


def save_pinned_agents(
    bench_dir: str | Path, *, benchmark: str, pins: dict[str, PinnedAgent]
) -> None:
    """Persist the full multi-entry pinned map atomically."""
    p = _multi_pinned_path(bench_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "agents": {
            k: {
                "benchmark": v.benchmark or benchmark,
                "agent_id": v.agent_id,
                "name": v.name,
                "created_at": v.created_at or datetime.now(timezone.utc).isoformat(),
            }
            for k, v in pins.items()
        },
    }
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, p)
