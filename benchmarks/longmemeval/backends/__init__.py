"""Memory-system backends for LongMemEval.

Each backend exposes one async function::

    async def run_question(
        *, question: LongMemEvalQuestion, ...
    ) -> BackendResult

The runner calls this, scores the result, and writes JSONL. Adding a new memory
system to the comparison is a single file in this folder.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BackendResult:
    """What a backend must return for scoring.

    Two retrieval modes are supported because MemPalace and Sonzai have
    fundamentally different data models:

    - **Session-level** (MemPalace): systems that store raw conversation
      sessions rank whole sessions. Scored against ``answer_session_ids``.
    - **Fact-level** (Sonzai): systems that extract atomic facts rank facts.
      Scored by whether any retrieved fact contains the ground-truth answer.

    Backends populate whichever of the two they can; the head-to-head
    apples-to-apples metric is end-to-end QA accuracy (``agent_answer``
    graded by Gemini), which works for both.
    """

    # Ranked list of session IDs retrieved for the question.
    # Populated by session-storing systems (e.g. MemPalace).
    ranked_session_ids: list[str] = field(default_factory=list)

    # Ranked list of retrieved fact/memory texts.
    # Populated by fact-extracting systems (e.g. Sonzai).
    ranked_fact_texts: list[str] = field(default_factory=list)

    # The agent's free-text answer to the question (for QA scoring).
    # Empty string means the backend doesn't support end-to-end QA.
    agent_answer: str = ""

    # Optional per-backend diagnostics — serialized into the JSONL output.
    extra: dict[str, object] = field(default_factory=dict)
