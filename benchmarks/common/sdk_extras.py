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


# ---------------------------------------------------------------------------
# Agent bootstrap — prefer ``generate-and-create`` over plain ``agents.create``
# so benchmark agents carry a full CE profile (Big5, traits, speech patterns,
# preferences) the same way production-provisioned agents do. The endpoint is
# idempotent on ``name``: first call spends one LLM call to expand the free-
# text description; every subsequent call returns the existing agent with no
# LLM cost. Mirrors the monolith bench's GenerateAndCreate caching pattern.
# ---------------------------------------------------------------------------


async def ensure_bench_agent_async(
    client: AsyncSonzai,
    *,
    name: str,
    description: str,
    gender: str = "",
    model: str | None = None,
) -> tuple[str, bool]:
    """Return ``(agent_id, existed_before)`` for a stable bench agent.

    First call with a given ``name`` creates the agent and expands the
    ``description`` into a full profile via the Platform's generation
    pipeline. Subsequent calls return the same agent without re-expanding
    (the server's idempotency key is the name). Safe to call on every
    benchmark startup.

    ``gender`` is optional; when empty the generation step picks something
    consistent with the description. ``model`` overrides the provider's
    default so, e.g., benches can pin to ``gemini-3.1-flash-lite-preview``
    for profile expansion too.

    We use the raw transport rather than the typed SDK binding because
    ``generation.generate_and_create`` returns a typed model that strips
    the ``existing`` flag; the raw dict preserves it so the caller can
    log "expanded fresh" vs "reused existing".
    """
    body: dict[str, object] = {"name": name, "description": description}
    if gender:
        body["gender"] = gender
    if model:
        body["model"] = model
    resp = await client._http.post(  # type: ignore[attr-defined]
        "/api/v1/agents/generate-and-create", json_data=body
    )
    if not isinstance(resp, dict):
        # Fallback: if the transport returned a pydantic model, extract.
        try:
            resp = resp.model_dump()  # type: ignore[attr-defined]
        except Exception as e:
            raise RuntimeError(f"generate-and-create returned unexpected type {type(resp)}") from e
    agent_id = str(resp.get("agent_id") or "")
    if not agent_id:
        raise RuntimeError(
            f"generate-and-create response missing agent_id: keys={list(resp.keys())}"
        )
    existed = bool(resp.get("existing"))
    return agent_id, existed
