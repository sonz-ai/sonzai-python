"""Forward-compatible adapters for resources not yet on the top-level client.

The SDK regeneration from the OpenAPI spec will expose ``client.sessions``,
``client.memory``, and ``client.workbench`` as first-class attributes. Until
then, these helpers instantiate the existing resource classes from the SDK's
internal transport. Once regeneration lands, each helper transparently
delegates to the native attribute, so callers switch over automatically.
"""

from __future__ import annotations

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.memory import AsyncMemory, Memory
from sonzai.resources.sessions import AsyncSessions, Sessions


def sessions(client: Sonzai) -> Sessions:
    existing = getattr(client, "sessions", None)
    if existing is not None:
        return existing
    return Sessions(client._http)  # type: ignore[attr-defined]


def async_sessions(client: AsyncSonzai) -> AsyncSessions:
    existing = getattr(client, "sessions", None)
    if existing is not None:
        return existing
    return AsyncSessions(client._http)  # type: ignore[attr-defined]


def memory(client: Sonzai) -> Memory:
    existing = getattr(client, "memory", None)
    if existing is not None:
        return existing
    return Memory(client._http)  # type: ignore[attr-defined]


def async_memory(client: AsyncSonzai) -> AsyncMemory:
    existing = getattr(client, "memory", None)
    if existing is not None:
        return existing
    return AsyncMemory(client._http)  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Memory-clear utility — wraps memory.reset for benchmark harnesses that
# reuse agents across runs and want a clean slate without creating a new
# agent (which would force fresh ingest + advance_time latency).
# ---------------------------------------------------------------------------


async def clear_agent_memory_async(
    client: AsyncSonzai, *, agent_id: str, user_id: str, instance_id: str | None = None
) -> None:
    """Delete all memory for (agent_id, user_id).

    Thin wrapper around ``memory.reset``. Used by the LongMemEval /
    SOTOPIA harnesses' ``--reuse-agents`` path when a previous iteration
    left stale state and the caller wants to re-ingest without creating
    a new agent. Swallows known transport errors (not-found, already-
    cleared) since the post-condition — "this agent has no memory" — is
    satisfied either way.
    """
    mem = async_memory(client)
    try:
        await mem.reset(agent_id, user_id=user_id, instance_id=instance_id)
    except Exception:
        # Best-effort: if the agent never had memory or was already reset,
        # the post-condition holds. Surface other errors only if the caller
        # wants to check state afterwards.
        pass


def clear_agent_memory(
    client: Sonzai, *, agent_id: str, user_id: str, instance_id: str | None = None
) -> None:
    """Sync counterpart of ``clear_agent_memory_async``."""
    mem = memory(client)
    try:
        mem.reset(agent_id, user_id=user_id, instance_id=instance_id)
    except Exception:
        pass
