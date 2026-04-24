"""Pre-configured Sonzai agent presets for benchmark runs.

Third parties evaluating Sonzai on memory benchmarks (LongMemEval, LoCoMo,
SOTOPIA, etc.) should not have to guess at the right agent configuration —
specifically the `speech_patterns` that make the agent answer concisely vs
conversationally, which dominates QA-grading scores on answer-string match
benchmarks.

This module exposes both the raw constants (so you can inline them into your
own agent-creation code) and convenience helpers (so the full setup is one
call for the common case).

Usage — async (the typical benchmark driver):

    from sonzai import AsyncSonzai
    from sonzai.benchmarks import ensure_longmemeval_agent_async

    client = AsyncSonzai(api_key=os.environ["SONZAI_API_KEY"])
    agent_id, existed = await ensure_longmemeval_agent_async(client)
    # ... now run your benchmark against agent_id

Usage — sync:

    from sonzai import Sonzai
    from sonzai.benchmarks import ensure_longmemeval_agent

    client = Sonzai(api_key=os.environ["SONZAI_API_KEY"])
    agent_id, existed = ensure_longmemeval_agent(client)

Idempotent: the agent is keyed by `name` server-side, so repeated calls
return the same agent_id. The `speech_patterns` are re-applied on every
call (cheap PATCH), so if you ever want to tweak them you can pass
`speech_patterns=[...]` to override.

Why this lives in the SDK, not the benchmark scripts: the LongMemEval and
SOTOPIA benches in `sonzai-python/benchmarks/` both import from here, and
so can any third-party harness. Keeping the canonical preset in one place
means our published scores and yours are measuring the same agent.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import AsyncSonzai, Sonzai

__all__ = [
    "LONGMEMEVAL_AGENT_NAME",
    "LONGMEMEVAL_AGENT_DESCRIPTION",
    "LONGMEMEVAL_SPEECH_PATTERNS",
    "ensure_longmemeval_agent",
    "ensure_longmemeval_agent_async",
    "CONVOMEM_AGENT_NAME",
    "CONVOMEM_AGENT_DESCRIPTION",
    "CONVOMEM_SPEECH_PATTERNS",
    "ensure_convomem_agent",
    "ensure_convomem_agent_async",
]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LongMemEval preset
# ---------------------------------------------------------------------------
#
# Description is the seed the server's `generate-and-create` endpoint expands
# into a full Big5 / personality_prompt / baseline speech_patterns profile.
# We keep the character's memory-assistant framing but then override
# speech_patterns explicitly (next constant) so the agent answers in the
# shape the grader expects.

LONGMEMEVAL_AGENT_NAME = "sonzai-bench-longmemeval"

LONGMEMEVAL_AGENT_DESCRIPTION = (
    "A helpful AI assistant that maintains a rich long-term memory of the "
    "user. Remembers specific personal details (routines, preferences, "
    "places, people, milestones, plans) and recalls them accurately when "
    "asked. Warm and attentive in day-to-day chat but switches to crisp, "
    "factual answers when the user is clearly asking for a lookup."
)

# Speech patterns that steer the agent's voice toward literal-value recall.
# These land in the chat prompt under `=== CHARACTER (STAY IN VOICE) ===`
# as `Voice cues: ...`, read on every turn. Not benchmark-specific tricks —
# any end user who wants a Sonzai agent that answers lookup questions
# directly would set similar patterns via `client.agents.update(
# speech_patterns=[...])`.
#
# NOTE: deliberately ONE pattern. Earlier iterations bundled "say I don't
# know if not in memory" and "enumerate then count" cues — both made the
# agent over-conservative. Even when 37 relevant facts were loaded into
# context, an explicit "say I don't know" cue caused the agent to bail
# instead of answering, dropping single-session QA from 0.94 → 0.76.
# The model already knows when to admit uncertainty; nudging that
# behavior in a Voice cue overweights it. Lead-with-value is the only
# cue that consistently correlates with grading without backfiring.
LONGMEMEVAL_SPEECH_PATTERNS: list[str] = [
    "Answers recall questions with the literal value first — a number, "
    "name, date, or short phrase — before any optional context.",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ensure_longmemeval_agent(
    client: "Sonzai",
    *,
    name: str = LONGMEMEVAL_AGENT_NAME,
    description: str = LONGMEMEVAL_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Create or return the canonical LongMemEval benchmark agent (sync).

    Returns ``(agent_id, existed_before)``. The agent is generated via
    ``/agents/generate-and-create`` on first call (LLM expands the
    description into a Big5 + personality_prompt profile) and cached by
    name server-side. Speech patterns are then applied via PATCH so the
    agent answers in the shape LongMemEval grades on.

    Override any field by passing it explicitly.
    """
    sp = speech_patterns if speech_patterns is not None else LONGMEMEVAL_SPEECH_PATTERNS
    agent_id, existed = _generate_and_create_sync(client, name=name, description=description)
    try:
        client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:  # fail-open: preset is desirable but not blocking
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed


async def ensure_longmemeval_agent_async(
    client: "AsyncSonzai",
    *,
    name: str = LONGMEMEVAL_AGENT_NAME,
    description: str = LONGMEMEVAL_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Async variant of :func:`ensure_longmemeval_agent`."""
    sp = speech_patterns if speech_patterns is not None else LONGMEMEVAL_SPEECH_PATTERNS
    agent_id, existed = await _generate_and_create_async(
        client, name=name, description=description
    )
    try:
        await client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed


# ---------------------------------------------------------------------------
# Internal transport helpers
# ---------------------------------------------------------------------------


def _generate_and_create_sync(
    client: "Sonzai", *, name: str, description: str
) -> tuple[str, bool]:
    """Call /agents/generate-and-create and unpack (agent_id, existed)."""
    resp = client._http.post(  # type: ignore[attr-defined]
        "/api/v1/agents/generate-and-create",
        json_data={"name": name, "description": description},
    )
    return _unpack_generate_create_response(resp)


async def _generate_and_create_async(
    client: "AsyncSonzai", *, name: str, description: str
) -> tuple[str, bool]:
    """Async variant of :func:`_generate_and_create_sync`."""
    resp = await client._http.post(  # type: ignore[attr-defined]
        "/api/v1/agents/generate-and-create",
        json_data={"name": name, "description": description},
    )
    return _unpack_generate_create_response(resp)


def _unpack_generate_create_response(resp: object) -> tuple[str, bool]:
    """Return (agent_id, existed) from a /generate-and-create payload."""
    if not isinstance(resp, dict):
        try:
            resp = resp.model_dump()  # type: ignore[attr-defined]
        except Exception as exc:
            raise RuntimeError(
                f"generate-and-create returned unexpected type {type(resp)}"
            ) from exc
    agent_id = str(resp.get("agent_id") or "")
    if not agent_id:
        raise RuntimeError(
            f"generate-and-create response missing agent_id: keys={list(resp.keys())}"
        )
    return agent_id, bool(resp.get("existing"))


# ---------------------------------------------------------------------------
# ConvoMem preset
# ---------------------------------------------------------------------------
#
# Same idea as the LongMemEval preset: one canonical agent so third-party
# evaluators measure against the same configuration we publish against.
# ConvoMem's six evidence categories mostly want literal-value recall (user
# facts, assistant facts, changing facts) with correct abstention behavior
# on the unanswerable category. The longmemeval speech pattern — "answer
# with the literal value first" — also serves ConvoMem well; abstention is
# a capability of the underlying model, nudged (not forced) by the voice.

CONVOMEM_AGENT_NAME = "sonzai-bench-convomem"

CONVOMEM_AGENT_DESCRIPTION = (
    "A helpful AI assistant that maintains a rich long-term memory of the "
    "user across many conversations. Remembers user-stated facts, its own "
    "prior statements, evolving preferences, and multi-hop connections. "
    "Answers factual recall questions with the specific value first, and "
    "declines clearly when the topic was never discussed."
)

CONVOMEM_SPEECH_PATTERNS: list[str] = [
    "Answers recall questions with the literal value first — a number, "
    "name, date, or short phrase — before any optional context.",
]


def ensure_convomem_agent(
    client: "Sonzai",
    *,
    name: str = CONVOMEM_AGENT_NAME,
    description: str = CONVOMEM_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Create or return the canonical ConvoMem benchmark agent (sync).

    Behavior mirrors :func:`ensure_longmemeval_agent` exactly — idempotent,
    keyed by ``name`` server-side, speech_patterns re-applied on every call.
    """
    sp = speech_patterns if speech_patterns is not None else CONVOMEM_SPEECH_PATTERNS
    agent_id, existed = _generate_and_create_sync(client, name=name, description=description)
    try:
        client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed


async def ensure_convomem_agent_async(
    client: "AsyncSonzai",
    *,
    name: str = CONVOMEM_AGENT_NAME,
    description: str = CONVOMEM_AGENT_DESCRIPTION,
    speech_patterns: list[str] | None = None,
) -> tuple[str, bool]:
    """Async variant of :func:`ensure_convomem_agent`."""
    sp = speech_patterns if speech_patterns is not None else CONVOMEM_SPEECH_PATTERNS
    agent_id, existed = await _generate_and_create_async(
        client, name=name, description=description
    )
    try:
        await client.agents.update(agent_id, speech_patterns=sp)
    except Exception as exc:
        logger.warning(
            "sonzai.benchmarks: failed to apply speech_patterns to %s (continuing): %s",
            agent_id, exc,
        )
    return agent_id, existed
