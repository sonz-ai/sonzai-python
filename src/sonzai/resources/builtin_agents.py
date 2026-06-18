"""Sonzai Built-in Agents resource.

Platform-hosted vertical task agents that run managed deep-work loops on
Sonzai infrastructure. The catalog currently includes ``lead_research``,
``market_intel``, ``lead_extract``, ``lead_score``, and ``lead_qualifier``.

Two ways to drive an agent:

* **One-shot invoke** — ``client.builtin_agents.invoke(slug, input=...)``
  runs the agent to completion and returns a
  :class:`~sonzai.types.BuiltinAgentInvokeResult`. These runs can take many
  minutes, so the SDK applies a 15-minute HTTP timeout by default
  (override via ``timeout=``).
* **Sessions** — ``client.builtin_agents.sessions`` creates a persistent
  conversation with one agent and sends follow-up turns to it.

Both ``invoke`` and session ``send`` have streaming variants that surface
the agent's live progress as Server-Sent Events: ``event: update`` frames
(tool calls, status text, elapsed heartbeats) followed by a terminal
``event: result`` frame. The streaming methods are generators that yield
:class:`~sonzai.types.BuiltinAgentUpdate` items and finish by yielding the
typed terminal result as the **last item** — same idiom as
``client.agents.chat(stream=True)``, where the aggregate frame arrives
in-stream. A terminal ``event: error`` frame raises
:class:`sonzai.StreamError`.

These endpoints are not in the committed OpenAPI snapshot yet, so this
resource is fully hand-written (no ``_generated`` base class) — same posture
as the workbench resource before its spec landed.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._exceptions import StreamError
from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    AgentGuidance,
    BuiltinAgentChatTurnResult,
    BuiltinAgentInvokeResult,
    BuiltinAgentListResponse,
    BuiltinAgentSession,
    BuiltinAgentSessionListResponse,
    BuiltinAgentUpdate,
    Calibration,
    EnrichJob,
    LearnResult,
)

# Built-in agent runs are long deep-work loops (web research, scoring whole
# lead books). 15 minutes matches the platform-side hard cap on a single run.
DEFAULT_INVOKE_TIMEOUT_SECONDS = 900.0


def _build_invoke_body(input: dict[str, Any], title: str | None) -> dict[str, Any]:
    body: dict[str, Any] = {"input": input}
    if title is not None:
        body["title"] = title
    return body


def _build_enrich_body(
    name: str,
    phone: str | None,
    email: str | None,
    company: str | None,
    brand: str | None,
    vertical: str | None,
    raw: str | None,
    webhook_url: str | None,
) -> dict[str, Any]:
    lead: dict[str, Any] = {"name": name}
    if phone is not None:
        lead["phone"] = phone
    if email is not None:
        lead["email"] = email
    if company is not None:
        lead["company"] = company
    if brand is not None:
        lead["brand"] = brand
    if vertical is not None:
        lead["vertical"] = vertical
    if raw is not None:
        lead["raw"] = raw
    body: dict[str, Any] = {"lead": lead}
    if webhook_url is not None:
        body["webhook_url"] = webhook_url
    return body


def _raise_stream_error(frame: dict[str, Any]) -> None:
    """Raise :class:`StreamError` from a terminal ``event: error`` frame."""
    raise StreamError(str(frame.get("error") or "built-in agent stream failed"))


class BuiltinAgentSessions:
    """Sync session operations for built-in agents."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def create(self, *, agent: str, title: str | None = None) -> BuiltinAgentSession:
        """Create a persistent session with a built-in agent.

        Args:
            agent: Catalog slug, e.g. ``"lead_research"``.
            title: Optional human-readable session title.
        """
        body: dict[str, Any] = {"agent": agent}
        if title is not None:
            body["title"] = title
        data = self._http.post("/api/v1/builtin-agents/sessions", json_data=body)
        return BuiltinAgentSession.model_validate(data)

    def list(self, *, limit: int | None = None) -> BuiltinAgentSessionListResponse:
        """List built-in agent sessions, newest first."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get("/api/v1/builtin-agents/sessions", params=params)
        return BuiltinAgentSessionListResponse.model_validate(data)

    def get(self, session_id: str) -> BuiltinAgentSession:
        """Get one session, including the ``billed_*`` token counters."""
        data = self._http.get(f"/api/v1/builtin-agents/sessions/{session_id}")
        return BuiltinAgentSession.model_validate(data)

    def send(
        self,
        session_id: str,
        text: str,
        *,
        stream: bool = False,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> BuiltinAgentChatTurnResult | Iterator[BuiltinAgentUpdate | BuiltinAgentChatTurnResult]:
        """Send a message turn to a session.

        With ``stream=False`` (default) blocks until the turn completes and
        returns a :class:`~sonzai.types.BuiltinAgentChatTurnResult`. With
        ``stream=True`` returns a generator yielding
        :class:`~sonzai.types.BuiltinAgentUpdate` progress frames; the final
        item is the :class:`~sonzai.types.BuiltinAgentChatTurnResult`.
        Raises :class:`sonzai.StreamError` on a terminal error frame.

        Args:
            session_id: Session ID from :meth:`create` / :meth:`list`.
            text: The user message for this turn.
            stream: Stream progress updates instead of blocking.
            timeout: HTTP timeout in seconds (turns can run for minutes).
        """
        path = f"/api/v1/builtin-agents/sessions/{session_id}/messages"
        if stream:
            return self._send_stream(path, text, timeout)
        data = self._http.post(
            path,
            json_data={"text": text},
            params={"stream": False},
            timeout=timeout,
        )
        return BuiltinAgentChatTurnResult.model_validate(data)

    def _send_stream(
        self, path: str, text: str, timeout: float
    ) -> Iterator[BuiltinAgentUpdate | BuiltinAgentChatTurnResult]:
        for event_name, frame in self._http.stream_sse_named(
            "POST",
            path,
            json_data={"text": text},
            params={"stream": True},
            timeout=timeout,
        ):
            if event_name == "error":
                _raise_stream_error(frame)
            if event_name == "result":
                yield BuiltinAgentChatTurnResult.model_validate(frame)
                return
            yield BuiltinAgentUpdate.model_validate(frame)


class BuiltinAgents:
    """Sync operations on the Sonzai Built-in Agents catalog.

    Example::

        result = client.builtin_agents.invoke(
            "lead_research",
            input={"company": "Ayala Land", "focus": "office leasing"},
        )
        print(result.summary, result.cost_usd)

        # Stream progress; the last item is the typed result.
        for item in client.builtin_agents.invoke_stream(
            "market_intel", input={"market": "Makati CBD"}
        ):
            if isinstance(item, BuiltinAgentInvokeResult):
                print("done:", item.summary)
            else:
                print(item.type, item.text or item.tool)
    """

    sessions: BuiltinAgentSessions

    def __init__(self, http: HTTPClient) -> None:
        self._http = http
        self.sessions = BuiltinAgentSessions(http)

    def list(self) -> BuiltinAgentListResponse:
        """List the built-in agent catalog with per-agent provisioning state."""
        data = self._http.get("/api/v1/builtin-agents")
        return BuiltinAgentListResponse.model_validate(data)

    def invoke(
        self,
        slug: str,
        *,
        input: dict[str, Any],
        title: str | None = None,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> BuiltinAgentInvokeResult:
        """Run a built-in agent to completion and return its findings.

        Blocks for the full run — these are deep-work loops that routinely
        take minutes, hence the 15-minute default ``timeout``.

        Args:
            slug: Catalog slug, e.g. ``"lead_research"``.
            input: Agent-specific input payload.
            title: Optional title for the session the run creates.
            timeout: HTTP timeout in seconds for this call.
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/{slug}/invoke",
            json_data=_build_invoke_body(input, title),
            params={"stream": False},
            timeout=timeout,
        )
        return BuiltinAgentInvokeResult.model_validate(data)

    def invoke_stream(
        self,
        slug: str,
        *,
        input: dict[str, Any],
        title: str | None = None,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> Iterator[BuiltinAgentUpdate | BuiltinAgentInvokeResult]:
        """Run a built-in agent, streaming live progress.

        Yields :class:`~sonzai.types.BuiltinAgentUpdate` frames as the agent
        works; the **final item** is the
        :class:`~sonzai.types.BuiltinAgentInvokeResult`. Raises
        :class:`sonzai.StreamError` if the server emits a terminal
        ``event: error`` frame.
        """
        for event_name, frame in self._http.stream_sse_named(
            "POST",
            f"/api/v1/builtin-agents/{slug}/invoke",
            json_data=_build_invoke_body(input, title),
            params={"stream": True},
            timeout=timeout,
        ):
            if event_name == "error":
                _raise_stream_error(frame)
            if event_name == "result":
                yield BuiltinAgentInvokeResult.model_validate(frame)
                return
            yield BuiltinAgentUpdate.model_validate(frame)

    # -- Lead-scoring feedback loop (bandit) --

    def record_lead_outcome(
        self,
        *,
        lead_ref: str,
        outcome: str,
        predicted_score: int | None = None,
        predicted_band: str | None = None,
        features: dict[str, Any] | None = None,
        score_signal: str | None = None,
        note: str | None = None,
    ) -> Calibration:
        """Record a realized lead-scoring outcome (won/lost/…).

        Recomputes and returns the project's scoring calibration the
        ``lead_score`` agent applies to future leads.

        Args:
            lead_ref: Identifier for the lead this outcome belongs to.
            outcome: The realized result (e.g. ``"won"``, ``"lost"``).
            predicted_score: The score the agent assigned, if known.
            predicted_band: The score band the agent assigned, if known.
            features: The lead's scored features, for segment calibration.
            score_signal: Optional override for how the outcome maps to a conversion.
            note: Optional free-text annotation.
        """
        body: dict[str, Any] = {"lead_ref": lead_ref, "outcome": outcome}
        if predicted_score is not None:
            body["predicted_score"] = predicted_score
        if predicted_band is not None:
            body["predicted_band"] = predicted_band
        if features is not None:
            body["features"] = features
        if score_signal is not None:
            body["score_signal"] = score_signal
        if note is not None:
            body["note"] = note
        data = self._http.post("/api/v1/builtin-agents/lead_score/outcome", json_data=body)
        return Calibration.model_validate(data)

    def get_lead_calibration(self) -> Calibration:
        """Return the current lead-scoring calibration.

        Predicted-vs-actual accuracy by band plus per-segment adjustments.
        """
        data = self._http.get("/api/v1/builtin-agents/lead_score/calibration")
        return Calibration.model_validate(data)

    # -- Async lead enrichment --

    def enrich_lead(
        self,
        *,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        company: str | None = None,
        brand: str | None = None,
        vertical: str | None = None,
        raw: str | None = None,
        webhook_url: str | None = None,
    ) -> EnrichJob:
        """Enqueue an async lead-enrichment job.

        Returns an :class:`~sonzai.types.EnrichJob` handle with
        ``status="queued"``; poll :meth:`get_enrichment` with its ``job_id``
        until ``status`` is ``"done"`` (or ``"error"``).

        Args:
            name: Lead name.
            phone: Lead phone number.
            email: Lead email.
            company: Lead's company.
            brand: Brand the lead is associated with.
            vertical: Vertical the lead belongs to.
            raw: Raw unstructured lead text.
            webhook_url: Optional callback URL invoked when the job completes.
        """
        body = _build_enrich_body(
            name, phone, email, company, brand, vertical, raw, webhook_url
        )
        data = self._http.post("/api/v1/builtin-agents/lead/enrich", json_data=body)
        return EnrichJob.model_validate(data)

    def get_enrichment(self, job_id: str) -> EnrichJob:
        """Return the current state of an async lead-enrichment job.

        When ``status`` is ``"done"``, ``result`` carries the enriched lead
        profile; when ``"error"``, ``error`` carries the failure reason.
        """
        data = self._http.get(f"/api/v1/builtin-agents/lead/enrich/{job_id}")
        return EnrichJob.model_validate(data)

    # -- Closed-loop agent self-improvement (learned guidance) --

    def learn_agent(self, slug: str, evidence: Any = None) -> LearnResult:
        """Run one distillation cycle for an agent.

        Turns accumulated critiques/outcomes into a new, bounded, auto-applied
        guidance version (respects the project kill switch — see
        :meth:`set_agent_learning`).
        """
        data = self._http.post(
            f"/api/v1/builtin-agents/{slug}/learn", json_data={"evidence": evidence}
        )
        return LearnResult.model_validate(data)

    def get_agent_guidance(self, slug: str) -> AgentGuidance:
        """Return an agent's active learned guidance plus recent version history."""
        data = self._http.get(f"/api/v1/builtin-agents/{slug}/guidance")
        return AgentGuidance.model_validate(data)

    def rollback_agent_guidance(self, slug: str) -> AgentGuidance:
        """Roll an agent's active guidance back to the prior version."""
        data = self._http.post(f"/api/v1/builtin-agents/{slug}/guidance/rollback", json_data={})
        return AgentGuidance.model_validate(data)

    def set_agent_learning(self, enabled: bool) -> bool:
        """Toggle closed-loop auto-apply for the project (the kill switch).

        Returns the effective enabled state.
        """
        data = self._http.put("/api/v1/builtin-agents/learning", json_data={"enabled": enabled})
        return bool(data.get("enabled", enabled))


class AsyncBuiltinAgentSessions:
    """Async session operations for built-in agents."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def create(self, *, agent: str, title: str | None = None) -> BuiltinAgentSession:
        """Create a persistent session with a built-in agent."""
        body: dict[str, Any] = {"agent": agent}
        if title is not None:
            body["title"] = title
        data = await self._http.post("/api/v1/builtin-agents/sessions", json_data=body)
        return BuiltinAgentSession.model_validate(data)

    async def list(self, *, limit: int | None = None) -> BuiltinAgentSessionListResponse:
        """List built-in agent sessions, newest first."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get("/api/v1/builtin-agents/sessions", params=params)
        return BuiltinAgentSessionListResponse.model_validate(data)

    async def get(self, session_id: str) -> BuiltinAgentSession:
        """Get one session, including the ``billed_*`` token counters."""
        data = await self._http.get(f"/api/v1/builtin-agents/sessions/{session_id}")
        return BuiltinAgentSession.model_validate(data)

    async def send(
        self,
        session_id: str,
        text: str,
        *,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> BuiltinAgentChatTurnResult:
        """Send a message turn and block until the turn completes.

        For streaming progress use :meth:`send_stream` — async generators
        can't share a signature with a coroutine the way the sync ``stream=``
        flag does, so the async surface splits the two (same split as
        ``invoke`` / ``invoke_stream``).
        """
        data = await self._http.post(
            f"/api/v1/builtin-agents/sessions/{session_id}/messages",
            json_data={"text": text},
            params={"stream": False},
            timeout=timeout,
        )
        return BuiltinAgentChatTurnResult.model_validate(data)

    async def send_stream(
        self,
        session_id: str,
        text: str,
        *,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> AsyncIterator[BuiltinAgentUpdate | BuiltinAgentChatTurnResult]:
        """Send a message turn, streaming progress updates.

        Yields :class:`~sonzai.types.BuiltinAgentUpdate` frames; the final
        item is the :class:`~sonzai.types.BuiltinAgentChatTurnResult`.
        Raises :class:`sonzai.StreamError` on a terminal error frame.
        """
        async for event_name, frame in self._http.stream_sse_named(
            "POST",
            f"/api/v1/builtin-agents/sessions/{session_id}/messages",
            json_data={"text": text},
            params={"stream": True},
            timeout=timeout,
        ):
            if event_name == "error":
                _raise_stream_error(frame)
            if event_name == "result":
                yield BuiltinAgentChatTurnResult.model_validate(frame)
                return
            yield BuiltinAgentUpdate.model_validate(frame)


class AsyncBuiltinAgents:
    """Async operations on the Sonzai Built-in Agents catalog.

    Mirror of :class:`BuiltinAgents`; see that class for usage examples.
    """

    sessions: AsyncBuiltinAgentSessions

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http
        self.sessions = AsyncBuiltinAgentSessions(http)

    async def list(self) -> BuiltinAgentListResponse:
        """List the built-in agent catalog with per-agent provisioning state."""
        data = await self._http.get("/api/v1/builtin-agents")
        return BuiltinAgentListResponse.model_validate(data)

    async def invoke(
        self,
        slug: str,
        *,
        input: dict[str, Any],
        title: str | None = None,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> BuiltinAgentInvokeResult:
        """Run a built-in agent to completion and return its findings."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/{slug}/invoke",
            json_data=_build_invoke_body(input, title),
            params={"stream": False},
            timeout=timeout,
        )
        return BuiltinAgentInvokeResult.model_validate(data)

    async def invoke_stream(
        self,
        slug: str,
        *,
        input: dict[str, Any],
        title: str | None = None,
        timeout: float = DEFAULT_INVOKE_TIMEOUT_SECONDS,
    ) -> AsyncIterator[BuiltinAgentUpdate | BuiltinAgentInvokeResult]:
        """Run a built-in agent, streaming live progress.

        Yields :class:`~sonzai.types.BuiltinAgentUpdate` frames; the final
        item is the :class:`~sonzai.types.BuiltinAgentInvokeResult`. Raises
        :class:`sonzai.StreamError` on a terminal ``event: error`` frame.
        """
        async for event_name, frame in self._http.stream_sse_named(
            "POST",
            f"/api/v1/builtin-agents/{slug}/invoke",
            json_data=_build_invoke_body(input, title),
            params={"stream": True},
            timeout=timeout,
        ):
            if event_name == "error":
                _raise_stream_error(frame)
            if event_name == "result":
                yield BuiltinAgentInvokeResult.model_validate(frame)
                return
            yield BuiltinAgentUpdate.model_validate(frame)

    # -- Lead-scoring feedback loop (bandit) --

    async def record_lead_outcome(
        self,
        *,
        lead_ref: str,
        outcome: str,
        predicted_score: int | None = None,
        predicted_band: str | None = None,
        features: dict[str, Any] | None = None,
        score_signal: str | None = None,
        note: str | None = None,
    ) -> Calibration:
        """Record a realized lead-scoring outcome and return the recomputed calibration."""
        body: dict[str, Any] = {"lead_ref": lead_ref, "outcome": outcome}
        if predicted_score is not None:
            body["predicted_score"] = predicted_score
        if predicted_band is not None:
            body["predicted_band"] = predicted_band
        if features is not None:
            body["features"] = features
        if score_signal is not None:
            body["score_signal"] = score_signal
        if note is not None:
            body["note"] = note
        data = await self._http.post("/api/v1/builtin-agents/lead_score/outcome", json_data=body)
        return Calibration.model_validate(data)

    async def get_lead_calibration(self) -> Calibration:
        """Return the current lead-scoring calibration."""
        data = await self._http.get("/api/v1/builtin-agents/lead_score/calibration")
        return Calibration.model_validate(data)

    # -- Async lead enrichment --

    async def enrich_lead(
        self,
        *,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        company: str | None = None,
        brand: str | None = None,
        vertical: str | None = None,
        raw: str | None = None,
        webhook_url: str | None = None,
    ) -> EnrichJob:
        """Enqueue an async lead-enrichment job.

        Returns an :class:`~sonzai.types.EnrichJob` handle with
        ``status="queued"``; poll :meth:`get_enrichment` with its ``job_id``
        until ``status`` is ``"done"`` (or ``"error"``).
        """
        body = _build_enrich_body(
            name, phone, email, company, brand, vertical, raw, webhook_url
        )
        data = await self._http.post("/api/v1/builtin-agents/lead/enrich", json_data=body)
        return EnrichJob.model_validate(data)

    async def get_enrichment(self, job_id: str) -> EnrichJob:
        """Return the current state of an async lead-enrichment job."""
        data = await self._http.get(f"/api/v1/builtin-agents/lead/enrich/{job_id}")
        return EnrichJob.model_validate(data)

    # -- Closed-loop agent self-improvement (learned guidance) --

    async def learn_agent(self, slug: str, evidence: Any = None) -> LearnResult:
        """Run one distillation cycle for an agent (respects the kill switch)."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/{slug}/learn", json_data={"evidence": evidence}
        )
        return LearnResult.model_validate(data)

    async def get_agent_guidance(self, slug: str) -> AgentGuidance:
        """Return an agent's active learned guidance plus recent version history."""
        data = await self._http.get(f"/api/v1/builtin-agents/{slug}/guidance")
        return AgentGuidance.model_validate(data)

    async def rollback_agent_guidance(self, slug: str) -> AgentGuidance:
        """Roll an agent's active guidance back to the prior version."""
        data = await self._http.post(
            f"/api/v1/builtin-agents/{slug}/guidance/rollback", json_data={}
        )
        return AgentGuidance.model_validate(data)

    async def set_agent_learning(self, enabled: bool) -> bool:
        """Toggle closed-loop auto-apply for the project (the kill switch)."""
        data = await self._http.put(
            "/api/v1/builtin-agents/learning", json_data={"enabled": enabled}
        )
        return bool(data.get("enabled", enabled))


__all__ = [
    "DEFAULT_INVOKE_TIMEOUT_SECONDS",
    "BuiltinAgents",
    "AsyncBuiltinAgents",
    "BuiltinAgentSessions",
    "AsyncBuiltinAgentSessions",
]
