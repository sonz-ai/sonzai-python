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
