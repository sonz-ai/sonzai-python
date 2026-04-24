"""Memory-system backends for LoCoMo.

Each backend exposes one async function::

    async def run_sample(
        client, sample, *, shared_agent_id, ..., reader=GeminiJudge,
    ) -> dict[int, LocomoBackendResult]

keyed by qa_index. The runner scores the result, writes JSONL. Adding a new
memory system = one file in this folder.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RankedMemoryItem:
    """One retrieved memory entry.

    ``memory_id`` is the provider-native ID (Sonzai ``fact_id`` or mem0 memory id).
    ``timestamp`` is the LoCoMo session_N_date_time string passed through
    verbatim so the reader can do temporal reasoning (matches mem0's "%timestamp%: %memory%"
    formatting).
    """

    memory_id: str
    text: str
    timestamp: str = ""
    score: float = 0.0
    session_id: str = ""  # LoCoMo "session_N" — used for Recall@K scoring


@dataclass
class LocomoBackendResult:
    """Per-question output from a LoCoMo backend.

    Preserves the dual-speaker retrieval shape from mem0's evaluation — separate
    ranked lists per speaker, merged at scoring time for session-level recall.
    """

    speaker_a_memories: list[RankedMemoryItem] = field(default_factory=list)
    speaker_b_memories: list[RankedMemoryItem] = field(default_factory=list)
    agent_answer: str = ""
    retrieved_session_ids: list[str] = field(default_factory=list)
    extra: dict[str, object] = field(default_factory=dict)
