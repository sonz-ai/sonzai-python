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
class RankedItem:
    """One retrieved item, in MemPalace's ``retrieval_results.ranked_items`` shape.

    ``corpus_id`` is a session id at session granularity, or ``"{session_id}_turn_{n}"``
    at turn granularity — ``scoring.session_id_from_corpus_id`` maps between them.
    """

    corpus_id: str
    text: str
    timestamp: str = ""


@dataclass
class BackendResult:
    """What a backend must return for scoring.

    The canonical field for retrieval scoring is ``ranked_items`` — it carries
    enough information to derive session-level and turn-level metrics the same
    way MemPalace does. The pre-computed ``ranked_session_ids`` and
    ``ranked_fact_texts`` are convenience projections for backends that only
    produce one granularity natively:

    - **Session-level** (MemPalace): systems that store raw conversation
      sessions rank whole sessions. Scored against ``answer_session_ids``.
    - **Fact-level** (Sonzai): systems that extract atomic facts rank facts.
      Session ids are best-effort via a fact→session map; fact-level recall
      is an additional signal for how well retrieval found the answer span.

    End-to-end QA (``agent_answer`` graded by Gemini) is provider-neutral and
    applies to both.
    """

    # MemPalace-shaped retrieval log: the authoritative retrieval output.
    ranked_items: list[RankedItem] = field(default_factory=list)

    # Ranked list of session IDs retrieved for the question. Derived from
    # ``ranked_items`` for MemPalace; populated directly by fact-based backends
    # that maintain a fact→session mapping.
    ranked_session_ids: list[str] = field(default_factory=list)

    # Ranked list of retrieved fact/memory texts.
    # Populated by fact-extracting systems (e.g. Sonzai).
    ranked_fact_texts: list[str] = field(default_factory=list)

    # The agent's free-text answer to the question (for QA scoring).
    # Empty string means the backend doesn't support end-to-end QA.
    agent_answer: str = ""

    # Optional per-backend diagnostics — serialized into the JSONL output.
    extra: dict[str, object] = field(default_factory=dict)
