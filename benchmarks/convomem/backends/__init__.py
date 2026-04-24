"""Memory-system backends for ConvoMem.

Each backend exposes one async function::

    async def run_question(
        client, question, *, include_qa: bool = True, ...
    ) -> BackendResult

ConvoMem doesn't grade retrieval — ground truth is message-level, not
session-level. So the BackendResult is deliberately thinner than
longmemeval's: an ``agent_answer`` for QA judging, plus diagnostic fields
for stored-fact counts and CE-worker activity.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BackendResult:
    # The agent's free-text answer to the question (for QA scoring).
    # Empty string means the backend doesn't support end-to-end QA.
    agent_answer: str = ""

    # Ranked memory.search hits — diagnostic only. Useful for debugging
    # "retrieval found it, chat didn't surface it" vs "retrieval missed it"
    # without being a scored metric.
    ranked_fact_texts: list[str] = field(default_factory=list)

    # Per-backend diagnostics — serialized into the JSONL output unchanged.
    extra: dict[str, object] = field(default_factory=dict)
