"""Forward-compatible shim for ``client.workbench.advance_time``.

Two things this file does that the raw SDK doesn't:

1. Falls back to a direct transport call when the regenerated SDK binding
   isn't present. When the native typed binding lands, we transparently
   delegate to it, so benchmarks switch over with no code change.

2. Bypasses Cloudflare's 100s origin-read timeout by default via the
   backend's async-job endpoint (``POST /workbench/advance-time`` with
   ``async=true`` → ``GET /workbench/advance-time/jobs/{jobId}``). A single
   simulated day can genuinely exceed 100s on a small platform pod — see the
   worker list in ``platform/api/.../workbench_advance_time.go``. Polling the
   Redis-backed job state is the documented production escape hatch.

   Toggle via ``SONZAI_WORKBENCH_ADVANCE_TIME_SYNC=1`` if you need the sync
   contract (e.g. to reproduce a specific edge-timeout failure mode).
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import Any

from pydantic import BaseModel, Field, field_validator
from sonzai import AsyncSonzai, Sonzai

logger = logging.getLogger(__name__)


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
    """Matches ``workbenchAdvanceTimeResponse`` from the platform API handler.

    Go's JSON encoder serializes empty slices as ``null`` rather than ``[]``
    (omitempty + nil slice). That means ``diary_entries`` and
    ``wakeups_executed`` come back as ``None`` on quiet advance-time calls,
    and pydantic's default ``list`` type rejects ``None``. The pre-validator
    below coerces ``None`` into an empty list so the contract stays
    ``list[...]`` for callers while still accepting Go's wire shape.
    """

    days_processed: int = 0
    consolidation_ran: bool = False
    weekly_consolidations: int = 0
    diary_entries_created: int = 0
    diary_entries: list[DiaryEntry] = Field(default_factory=list)
    wakeups_executed: list[WakeupExecution] = Field(default_factory=list)
    consolidation_processed: int = 0

    model_config = {"extra": "allow"}

    @field_validator("diary_entries", "wakeups_executed", mode="before")
    @classmethod
    def _none_to_empty_list(cls, v):
        return [] if v is None else v


def _body(
    *,
    agent_id: str,
    user_id: str,
    simulated_hours: float,
    simulated_base_offset_hours: float,
    instance_id: str | None,
    async_mode: bool = False,
) -> dict[str, Any]:
    body: dict[str, Any] = {
        "agent_id": agent_id,
        "user_id": user_id,
        "simulated_hours": simulated_hours,
        "simulated_base_offset_hours": simulated_base_offset_hours,
        "instance_id": instance_id or "",
        "character_config": {},
    }
    if async_mode:
        body["async"] = True
    return body


def _native_sync(client: Sonzai):
    wb = getattr(client, "workbench", None)
    return getattr(wb, "advance_time", None) if wb is not None else None


def _native_async(client: AsyncSonzai):
    wb = getattr(client, "workbench", None)
    return getattr(wb, "advance_time", None) if wb is not None else None


# ---------------------------------------------------------------------------
# Async-job polling
# ---------------------------------------------------------------------------


# Backend keeps job state in Redis with a 30-min TTL
# (see platform/api/.../workbench_advance_time_async.go: advanceTimeJobTTL).
# We deliberately allow more headroom than the server-side 25-min cap so pollers
# observe the terminal state even when the server hit its own timeout.
DEFAULT_ASYNC_POLL_DEADLINE_S = 30 * 60
DEFAULT_ASYNC_POLL_INITIAL_S = 2.0
DEFAULT_ASYNC_POLL_MAX_S = 15.0


def _async_mode_enabled() -> bool:
    """Default ON. Opt out with SONZAI_WORKBENCH_ADVANCE_TIME_SYNC=1."""
    return os.environ.get("SONZAI_WORKBENCH_ADVANCE_TIME_SYNC", "").strip() not in {
        "1",
        "true",
        "yes",
    }


async def _poll_async_job(
    client: AsyncSonzai,
    job_id: str,
    *,
    deadline_s: float = DEFAULT_ASYNC_POLL_DEADLINE_S,
    initial_interval_s: float = DEFAULT_ASYNC_POLL_INITIAL_S,
    max_interval_s: float = DEFAULT_ASYNC_POLL_MAX_S,
) -> AdvanceTimeResponse:
    """Poll the async-job status endpoint until terminal state or deadline.

    Exponential backoff (1.5×) capped at ``max_interval_s`` — early polls are
    cheap and help short jobs return quickly; later polls avoid hammering
    Redis for genuinely long (~20 min) runs.
    """
    started = time.monotonic()
    interval = initial_interval_s
    while True:
        if time.monotonic() - started > deadline_s:
            raise TimeoutError(
                f"advance-time async job {job_id} did not finish within {deadline_s:.0f}s"
            )
        try:
            state = await client._http.get(  # type: ignore[attr-defined]
                f"/api/v1/workbench/advance-time/jobs/{job_id}",
            )
        except Exception as e:
            # Transient network / 5xx on the status endpoint — keep polling
            # up to the deadline rather than aborting. We log at debug; the
            # caller decides whether the eventual timeout is fatal.
            logger.debug("advance-time status poll failed (will retry): %s", e)
            await asyncio.sleep(interval)
            interval = min(interval * 1.5, max_interval_s)
            continue

        status = ""
        if isinstance(state, dict):
            status = str(state.get("status") or "")
            result = state.get("result")
            error = state.get("error")
        else:
            status = str(getattr(state, "status", "") or "")
            result = getattr(state, "result", None)
            error = getattr(state, "error", "")

        if status == "succeeded":
            if result is None:
                return AdvanceTimeResponse()
            if isinstance(result, dict):
                return AdvanceTimeResponse.model_validate(result)
            return AdvanceTimeResponse.model_validate(
                result.model_dump() if hasattr(result, "model_dump") else result
            )
        if status == "failed":
            raise RuntimeError(
                f"advance-time async job {job_id} failed: {error or 'unknown'}"
            )
        # Still running — backoff and retry.
        await asyncio.sleep(interval)
        interval = min(interval * 1.5, max_interval_s)


# ---------------------------------------------------------------------------
# Sync + async flavours of advance_time
# ---------------------------------------------------------------------------


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

    Sync variant. No async-job polling — callers on the sync client are not
    expected to have an event loop handy. If you're running the benchmark,
    use ``advance_time_async`` instead.
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
    async_mode: bool | None = None,
) -> AdvanceTimeResponse:
    """Async variant.

    ``async_mode`` selects the server-side path:

    - ``True`` (default): submit as an async job (``"async": true``), grab the
      returned ``job_id``, and poll ``/workbench/advance-time/jobs/{jobId}``
      until terminal. Immune to Cloudflare's 100s origin-read timeout.
    - ``False``: classic sync path. Kept for reproducing specific timeout
      failure modes or when the backend doesn't have Redis wired.

    Default is taken from ``SONZAI_WORKBENCH_ADVANCE_TIME_SYNC`` — set to ``1``
    to force sync.
    """
    if async_mode is None:
        async_mode = _async_mode_enabled()

    # Native binding doesn't know about async_mode yet — only use it on the
    # sync path. Async-job path has to go through the raw transport.
    if not async_mode:
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

    # Async-job path — POST with async=true, then poll.
    submit = await client._http.post(  # type: ignore[attr-defined]
        "/api/v1/workbench/advance-time",
        json_data=_body(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
            async_mode=True,
        ),
    )
    job_id = ""
    if isinstance(submit, dict):
        job_id = str(submit.get("job_id") or "")
    else:
        job_id = str(getattr(submit, "job_id", "") or "")
    if not job_id:
        # Backend didn't accept async mode (probably older build). Fall back
        # to sync — safer than raising, the caller's outer try/except already
        # downgrades failures to warnings.
        logger.debug("advance-time async submit returned no job_id; falling back to sync")
        return await advance_time_async(
            client,
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
            async_mode=False,
        )
    return await _poll_async_job(client, job_id)


# ---------------------------------------------------------------------------
# Chunked runner — resilient per-chunk
# ---------------------------------------------------------------------------


# Cloudflare's origin timeout is 100s. Even with async-job mode, we still chunk
# so individual runs stay bounded — a 168h (one-week) simulation split into 24h
# chunks lets the server release workers between chunks and keeps each async
# job's 25-min server-side cap comfortably safe.
CHUNK_HOURS_DEFAULT = 24.0
CHUNK_MAX_ATTEMPTS = 3
CHUNK_RETRY_BASE_S = 4.0


async def advance_time_chunked_async(
    client: AsyncSonzai,
    *,
    agent_id: str,
    user_id: str,
    total_hours: float,
    chunk_hours: float = CHUNK_HOURS_DEFAULT,
    instance_id: str | None = None,
    async_mode: bool | None = None,
) -> list[AdvanceTimeResponse]:
    """Break a long gap into ``chunk_hours`` pieces and run them sequentially.

    Per-chunk resilience:
      - Each chunk is retried up to ``CHUNK_MAX_ATTEMPTS`` times with
        exponential backoff on transient failures.
      - After max attempts the chunk is **skipped** and the loop continues
        with the next chunk — one bad chunk never aborts the whole gap.
      - ``simulated_base_offset_hours`` still accumulates across every chunk
        (succeeded or not) so the wakeup asOf windows stay aligned with the
        caller's intended elapsed time.

    The returned list contains only successful chunks. Callers that need to
    distinguish "ran nothing" from "ran partially" can compare
    ``len(responses) * chunk_hours`` against ``total_hours``.
    """
    if total_hours <= 0:
        return []
    responses: list[AdvanceTimeResponse] = []
    elapsed = 0.0
    remaining = total_hours
    while remaining > 0.0:
        size = min(chunk_hours, remaining)
        got = False
        for attempt in range(1, CHUNK_MAX_ATTEMPTS + 1):
            try:
                r = await advance_time_async(
                    client,
                    agent_id=agent_id,
                    user_id=user_id,
                    simulated_hours=size,
                    simulated_base_offset_hours=elapsed,
                    instance_id=instance_id,
                    async_mode=async_mode,
                )
                responses.append(r)
                got = True
                break
            except Exception as e:
                if attempt >= CHUNK_MAX_ATTEMPTS:
                    logger.warning(
                        "advance_time chunk failed (giving up after %d attempts, gap will be partial): "
                        "agent=%s hours=%.1f offset=%.1f err=%s",
                        attempt,
                        agent_id,
                        size,
                        elapsed,
                        e,
                    )
                    break
                backoff = CHUNK_RETRY_BASE_S * (2 ** (attempt - 1))
                logger.debug(
                    "advance_time chunk attempt %d/%d failed (will retry in %.1fs): %s",
                    attempt,
                    CHUNK_MAX_ATTEMPTS,
                    backoff,
                    e,
                )
                await asyncio.sleep(backoff)
        elapsed += size
        remaining -= size
        if not got:
            # Move on to the next chunk instead of aborting the whole gap.
            continue
    return responses
