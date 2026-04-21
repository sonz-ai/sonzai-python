"""Forward-compatible shim for ``client.workbench.advance_time``.

The SDK regeneration from the OpenAPI spec will add a typed
``client.workbench.advance_time(...)`` binding. Until that lands we call the
endpoint directly via the SDK's internal transport so auth/retries/base-URL are
preserved.

When the regenerated SDK is installed, ``advance_time`` below transparently
delegates to the native typed binding, so benchmarks switch over with no code
change.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field
from sonzai import AsyncSonzai, Sonzai


class DiaryEntry(BaseModel):
    date: str = ""
    content: str = ""
    mood: str = ""
    topics: list[str] = Field(default_factory=list)


class WakeupExecution(BaseModel):
    wakeup_id: str = ""
    check_type: str = ""
    intent: str = ""
    user_id: str = ""
    agent_id: str = ""
    generated_message: str = ""


class AdvanceTimeResponse(BaseModel):
    """Matches ``workbenchAdvanceTimeResponse`` from the platform API handler."""

    days_processed: int = 0
    consolidation_ran: bool = False
    weekly_consolidations: int = 0
    diary_entries_created: int = 0
    diary_entries: list[DiaryEntry] = Field(default_factory=list)
    wakeups_executed: list[WakeupExecution] = Field(default_factory=list)
    consolidation_processed: int = 0

    model_config = {"extra": "allow"}


def _body(
    *,
    agent_id: str,
    user_id: str,
    simulated_hours: float,
    simulated_base_offset_hours: float,
    instance_id: str | None,
) -> dict[str, Any]:
    return {
        "agent_id": agent_id,
        "user_id": user_id,
        "simulated_hours": simulated_hours,
        "simulated_base_offset_hours": simulated_base_offset_hours,
        "instance_id": instance_id or "",
        "character_config": {},
    }


def _native_sync(client: Sonzai):
    wb = getattr(client, "workbench", None)
    return getattr(wb, "advance_time", None) if wb is not None else None


def _native_async(client: AsyncSonzai):
    wb = getattr(client, "workbench", None)
    return getattr(wb, "advance_time", None) if wb is not None else None


def advance_time(
    client: Sonzai,
    *,
    agent_id: str,
    user_id: str,
    simulated_hours: float,
    simulated_base_offset_hours: float = 0.0,
    instance_id: str | None = None,
) -> AdvanceTimeResponse:
    """Run production CE workers (diary, consolidation, decay) for a simulated gap.

    The only difference between the benchmark flow and normal Sonzai usage:
    benchmarks call this between sessions so background self-learning fires
    without waiting wall-clock time.
    """
    native = _native_sync(client)
    if native is not None:
        resp = native(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
        )
        if isinstance(resp, AdvanceTimeResponse):
            return resp
        return AdvanceTimeResponse.model_validate(
            resp.model_dump() if hasattr(resp, "model_dump") else resp
        )

    data = client._http.post(  # type: ignore[attr-defined]
        "/api/v1/workbench/advance-time",
        json_data=_body(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
        ),
    )
    return AdvanceTimeResponse.model_validate(data)


async def advance_time_async(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    simulated_hours: float,
    simulated_base_offset_hours: float = 0.0,
    instance_id: str | None = None,
) -> AdvanceTimeResponse:
    native = _native_async(client)
    if native is not None:
        resp = await native(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
        )
        if isinstance(resp, AdvanceTimeResponse):
            return resp
        return AdvanceTimeResponse.model_validate(
            resp.model_dump() if hasattr(resp, "model_dump") else resp
        )

    data = await client._http.post(  # type: ignore[attr-defined]
        "/api/v1/workbench/advance-time",
        json_data=_body(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
        ),
    )
    return AdvanceTimeResponse.model_validate(data)


# Cloudflare's origin timeout is 100s. A single advance_time call running ~5
# simulated days can genuinely exceed that (CE workers run per-day inline).
# Chunk long gaps into sub-calls with ``simulated_base_offset_hours`` so each
# request stays well under the edge timeout, matching what the workbench UI
# does for long-horizon runs.
CHUNK_HOURS_DEFAULT = 24.0


async def advance_time_chunked_async(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    total_hours: float,
    chunk_hours: float = CHUNK_HOURS_DEFAULT,
    instance_id: str | None = None,
) -> list[AdvanceTimeResponse]:
    """Break a long gap into ≤``chunk_hours`` chunks to avoid edge-timeouts.

    Returns the per-chunk responses in order. ``simulated_base_offset_hours``
    accumulates so wakeup asOf windows don't overlap across chunks (per the
    handler comment in workbench_advance_time.go).
    """
    if total_hours <= 0:
        return []
    responses: list[AdvanceTimeResponse] = []
    elapsed = 0.0
    remaining = total_hours
    while remaining > 0.0:
        size = min(chunk_hours, remaining)
        r = await advance_time_async(
            client,
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=size,
            simulated_base_offset_hours=elapsed,
            instance_id=instance_id,
        )
        responses.append(r)
        elapsed += size
        remaining -= size
    return responses
