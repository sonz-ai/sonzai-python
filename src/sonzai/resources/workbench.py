"""Workbench resource.

The workbench endpoints drive the time-machine / harness simulations used
by the benchmark suite and the in-app workbench UI. All endpoints live
under ``/workbench/...`` and are tenant-scoped (the server resolves the
tenant from the API key).

Key endpoint: :meth:`Workbench.advance_time` — runs the production
background CE workers (diary, consolidation, constellation, etc.) for a
chosen number of simulated hours. The benchmark calls this with real
``agent_id`` + ``user_id`` overrides and typically ``simulated_hours=25``
(one full day + a sliver so the weekly gate can tick over).

Request/response shapes come from the Go handler
(``services/platform/api/internal/delivery/http/workbench_advance_time.go``).
The OpenAPI declaration is a passthrough (``{}`` body/response), so this
resource hand-writes them in :mod:`sonzai.types` as
``AdvanceTimeResponse`` / ``DiaryEntry`` / ``WakeupExecution``.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import AdvanceTimeResponse


def _build_advance_time_body(
    *,
    agent_id: str | None,
    user_id: str | None,
    simulated_hours: float,
    simulated_base_offset_hours: float,
    instance_id: str | None,
    character_config: dict[str, Any] | None,
    async_: bool = False,
) -> dict[str, Any]:
    """Shape the request body the Go handler expects.

    The Go handler accepts character_config (with a Name field) to derive a
    workbench-hash agent ID when ``agent_id`` is not provided. The SDK
    always requires ``agent_id`` to be meaningful here — benchmarks pass in
    a real UUID returned by ``generate-and-create`` — but we preserve the
    optional ``character_config`` kwarg for parity with non-SDK callers.
    """
    body: dict[str, Any] = {
        "simulated_hours": float(simulated_hours),
        "simulated_base_offset_hours": float(simulated_base_offset_hours),
    }
    # character_config is required by the struct tag but the handler falls
    # back to AgentID override when it can. Send an empty object when not
    # supplied so JSON encoding on the server side doesn't choke on a
    # missing required key.
    body["character_config"] = character_config if character_config is not None else {}
    body["instance_id"] = instance_id if instance_id is not None else ""
    if agent_id is not None:
        body["agent_id"] = agent_id
    if user_id is not None:
        body["user_id"] = user_id
    if async_:
        body["async"] = True
    return body


class Workbench:
    """Sync workbench operations (time-machine, simulate-user, passthrough chat)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    # -- Advance time (PRIMARY) ------------------------------------------------

    def advance_time(
        self,
        agent_id: str,
        user_id: str,
        simulated_hours: float,
        *,
        simulated_base_offset_hours: float = 0.0,
        instance_id: str | None = None,
        character_config: dict[str, Any] | None = None,
        run_async: bool = False,
    ) -> AdvanceTimeResponse | dict[str, Any]:
        """Advance simulated time by ``simulated_hours``.

        Runs the full production CE worker fleet (decays, consolidation,
        diary, constellation extraction, wakeup processing) for each full
        24-hour day contained in ``simulated_hours``, then processes any
        proactive wakeups due inside the simulated window.

        Args:
            agent_id: The real agent UUID — typically the ID returned by
                ``client.generation.generate_and_create``.
            user_id: The user ID used during chat. Must match what was sent
                on ``sessions.start`` / chat so scoped IDs line up.
            simulated_hours: Length of the simulated segment. For a single
                day, pass ``25.0`` so the weekly gate can tick over.
            simulated_base_offset_hours: Hours already processed by prior
                ``advance_time`` calls in the same session gap. Used by the
                server to size the wakeup ``asOf`` window.
            instance_id: Optional instance scope; when ``agent_id`` is
                provided the server does NOT use ``instance_id`` for user
                scoping (see the Go handler comment).
            character_config: Optional character config; only consulted
                when ``agent_id`` is empty. Provided for parity with
                non-SDK callers.

        Returns:
            :class:`sonzai.types.AdvanceTimeResponse` with ``days_processed``,
            consolidation counters, diary entries that were newly created,
            and any wakeups that fired in the window (including the LLM-
            generated proactive message, if the server wired in the
            message generator).

        Example::

            resp = client.workbench.advance_time(
                agent_id="agent-123", user_id="bench-user", simulated_hours=25.0,
            )
            print(resp.days_processed, [d.content for d in resp.diary_entries])
        """
        body = _build_advance_time_body(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
            character_config=character_config,
            async_=run_async,
        )
        data = self._http.post("/api/v1/workbench/advance-time", json_data=body)
        if run_async:
            # 202 body: {"job_id": "...", "status": "running"} — let the
            # caller poll get_advance_time_job until it's terminal.
            return data  # type: ignore[return-value]
        return AdvanceTimeResponse.model_validate(data)

    def get_advance_time_job(self, job_id: str) -> dict[str, Any]:
        """Get the state of an async advance-time job.

        Returns a dict with at least ``job_id``, ``status`` (``running`` |
        ``succeeded`` | ``failed``), and — once terminal — ``result`` (on
        success) or ``error`` (on failure). State lives in Redis with a
        30-minute TTL; poll within that window.
        """
        return self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/workbench/advance-time/jobs/{job_id}"
        )

    # -- Other workbench endpoints --------------------------------------------
    # These are thinner — benchmarks mostly care about advance_time, but we
    # cover the rest for parity so anyone building their own harness has a
    # first-class surface instead of raw _http calls.

    def prepare(self, **body: Any) -> dict[str, Any]:
        """Prepare the workbench for a run. Opaque body — server defines shape."""
        return self._http.post("/api/v1/workbench/prepare", json_data=body)  # type: ignore[no-any-return]

    def get_state(self, **body: Any) -> dict[str, Any]:
        """Get current workbench state. Server uses POST to accept a body."""
        return self._http.post("/api/v1/workbench/state", json_data=body)  # type: ignore[no-any-return]

    def reset_agent(self, **body: Any) -> dict[str, Any]:
        """Reset the workbench agent's data."""
        return self._http.post("/api/v1/workbench/reset-agent", json_data=body)  # type: ignore[no-any-return]

    def session_end(self, **body: Any) -> dict[str, Any]:
        """Trigger session-end processing for the workbench agent."""
        return self._http.post("/api/v1/workbench/session-end", json_data=body)  # type: ignore[no-any-return]

    def simulate_user(self, **body: Any) -> dict[str, Any]:
        """Generate a simulated user turn (workbench-side user simulation)."""
        return self._http.post("/api/v1/workbench/simulate-user", json_data=body)  # type: ignore[no-any-return]

    def generate_bio(self, **body: Any) -> dict[str, Any]:
        """Generate agent bio via workbench flow."""
        return self._http.post("/api/v1/workbench/generate-bio", json_data=body)  # type: ignore[no-any-return]

    def generate_character(self, **body: Any) -> dict[str, Any]:
        """Generate a full character (personality + bio + seeds) via workbench."""
        return self._http.post(
            "/api/v1/workbench/generate-character", json_data=body
        )  # type: ignore[no-any-return]

    def generate_seed_memories(self, **body: Any) -> dict[str, Any]:
        """Generate seed memories for the workbench agent."""
        return self._http.post(
            "/api/v1/workbench/generate-seed-memories", json_data=body
        )  # type: ignore[no-any-return]

    def chat(self, **body: Any) -> Any:
        """Workbench chat (passthrough; non-streaming aggregate).

        The server endpoint is SSE, but this helper consumes the stream and
        returns the raw aggregated dict. Callers who want per-event
        handling should wire ``_http.stream_sse`` directly; the benchmark
        does not use this endpoint today.
        """
        return self._http.post("/api/v1/workbench/chat", json_data=body)


class AsyncWorkbench:
    """Async workbench operations (mirror of :class:`Workbench`)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def advance_time(
        self,
        agent_id: str,
        user_id: str,
        simulated_hours: float,
        *,
        simulated_base_offset_hours: float = 0.0,
        instance_id: str | None = None,
        character_config: dict[str, Any] | None = None,
        run_async: bool = False,
    ) -> AdvanceTimeResponse | dict[str, Any]:
        body = _build_advance_time_body(
            agent_id=agent_id,
            user_id=user_id,
            simulated_hours=simulated_hours,
            simulated_base_offset_hours=simulated_base_offset_hours,
            instance_id=instance_id,
            character_config=character_config,
            async_=run_async,
        )
        data = await self._http.post(
            "/api/v1/workbench/advance-time", json_data=body
        )
        if run_async:
            return data  # type: ignore[return-value]
        return AdvanceTimeResponse.model_validate(data)

    async def get_advance_time_job(self, job_id: str) -> dict[str, Any]:
        """Get the state of an async advance-time job."""
        return await self._http.get(  # type: ignore[no-any-return]
            f"/api/v1/workbench/advance-time/jobs/{job_id}"
        )

    async def prepare(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/workbench/prepare", json_data=body)  # type: ignore[no-any-return]

    async def get_state(self, **body: Any) -> dict[str, Any]:
        return await self._http.post("/api/v1/workbench/state", json_data=body)  # type: ignore[no-any-return]

    async def reset_agent(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/reset-agent", json_data=body
        )  # type: ignore[no-any-return]

    async def session_end(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/session-end", json_data=body
        )  # type: ignore[no-any-return]

    async def simulate_user(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/simulate-user", json_data=body
        )  # type: ignore[no-any-return]

    async def generate_bio(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/generate-bio", json_data=body
        )  # type: ignore[no-any-return]

    async def generate_character(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/generate-character", json_data=body
        )  # type: ignore[no-any-return]

    async def generate_seed_memories(self, **body: Any) -> dict[str, Any]:
        return await self._http.post(
            "/api/v1/workbench/generate-seed-memories", json_data=body
        )  # type: ignore[no-any-return]

    async def chat(self, **body: Any) -> Any:
        return await self._http.post("/api/v1/workbench/chat", json_data=body)
