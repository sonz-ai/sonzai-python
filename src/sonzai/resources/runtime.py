"""Stable platform control-plane contract for custom Sonzai runtimes.

Provider inference is intentionally absent: the runtime calls its selected
LLM provider directly, while this resource fetches context/memory and reports
completed turns plus signed usage back to Sonzai Cloud.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Any, Literal
from urllib.parse import quote

from pydantic import BaseModel, ConfigDict, Field

from .._http import AsyncHTTPClient, HTTPClient

RUNTIME_USAGE_SCHEMA_VERSION = 2
RuntimeBillingMode = Literal["standard", "byok"]


class RuntimeModel(BaseModel):
    """Base wire model that preserves platform snake_case field names."""

    model_config = ConfigDict(extra="allow")


class RuntimeContextBundle(RuntimeModel):
    system_prompt_parts: list[str]
    memory_context: dict[str, Any]
    persona: dict[str, Any] | None = None
    tool_definitions: list[Any]
    ttl: int


class RuntimeBackendAgentArtifact(RuntimeModel):
    slug: str
    name: str
    description: str
    model_hint: str
    system: str
    findings_schema: dict[str, Any] | None = None
    tools: list[str] = Field(default_factory=list)
    disable_tools: bool
    max_tool_rounds: int
    version: str


class RuntimeToolCallFunction(RuntimeModel):
    name: str
    arguments: str


class RuntimeToolCall(RuntimeModel):
    id: str
    type: str = "function"
    function: RuntimeToolCallFunction


class RuntimeTurnMessage(RuntimeModel):
    role: Literal["user", "assistant", "tool", "system"]
    content: str | None = None
    timestamp: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[RuntimeToolCall] = Field(default_factory=list)
    author: str | None = None


class RuntimeCompletedTurn(RuntimeModel):
    user_message: RuntimeTurnMessage
    assistant_message: RuntimeTurnMessage
    tool_results: list[RuntimeTurnMessage] = Field(default_factory=list)


class RuntimeTurnReport(RuntimeModel):
    user_id: str
    session_id: str
    instance_id: str | None = None
    user_display_name: str | None = None
    messages: list[RuntimeTurnMessage] = Field(default_factory=list)
    turns: list[RuntimeCompletedTurn] = Field(default_factory=list)


class RuntimeTurnReportResult(RuntimeModel):
    accepted: bool
    agent_id: str
    user_id: str
    session_id: str
    messages_stored: int


class RuntimeConversation(RuntimeModel):
    agent_id: str
    user_id: str
    session_id: str
    page: int
    page_size: int
    total: int
    has_more: bool
    messages: list[RuntimeTurnMessage]


class RuntimeUsageCounter(RuntimeModel):
    project_id: str
    agent_id: str
    provider: str
    model: str
    use_case: str
    billing_mode: RuntimeBillingMode
    tokens_in: int = 0
    tokens_out: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    turns: int = 0
    unreported_turns: int = 0


class RuntimeUsageReport(RuntimeModel):
    schema_version: int = RUNTIME_USAGE_SCHEMA_VERSION
    report_id: str
    tenant_id: str
    instance_id: str | None = None
    period_start: str
    period_end: str
    heartbeat_at: str
    counters: list[RuntimeUsageCounter] = Field(default_factory=list)
    signature: str = ""


class RuntimeUsageReportResult(RuntimeModel):
    accepted: bool
    report_id: str


class Runtime:
    """Synchronous custom-runtime control-plane operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def backend_agent_artifacts(self) -> list[RuntimeBackendAgentArtifact]:
        """Download versioned execution config; no platform LLM call occurs."""
        data = self._http.get("/api/v1/runtime/backend-agent-artifacts")
        return [RuntimeBackendAgentArtifact.model_validate(item) for item in data["artifacts"]]

    def context_bundle(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        current_message: str | None = None,
    ) -> RuntimeContextBundle:
        body = {
            "user_id": user_id,
            "session_id": session_id,
            "current_message": current_message,
        }
        data = self._http.post(
            f"/api/v1/agents/{quote(agent_id, safe='')}/context-bundle",
            json_data={key: value for key, value in body.items() if value is not None},
        )
        return RuntimeContextBundle.model_validate(data)

    def conversation(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        page: int | None = None,
        page_size: int | None = None,
    ) -> RuntimeConversation:
        data = self._http.get(
            f"/api/v1/agents/{quote(agent_id, safe='')}/conversations",
            params={
                "user_id": user_id,
                "session_id": session_id,
                "page": page,
                "page_size": page_size,
            },
        )
        return RuntimeConversation.model_validate(data)

    def report_turns(
        self,
        agent_id: str,
        report: RuntimeTurnReport,
    ) -> RuntimeTurnReportResult:
        data = self._http.post(
            f"/api/v1/agents/{quote(agent_id, safe='')}/turns",
            json_data=report.model_dump(mode="json", exclude_none=True),
        )
        return RuntimeTurnReportResult.model_validate(data)

    def submit_usage_report(
        self,
        report: RuntimeUsageReport,
    ) -> RuntimeUsageReportResult:
        data = self._http.post(
            "/api/v1/usage/reports",
            json_data=report.model_dump(mode="json", exclude_none=True),
            headers={"X-Sonzai-Metering-Signature": report.signature},
        )
        return RuntimeUsageReportResult.model_validate(data)


class AsyncRuntime:
    """Asynchronous custom-runtime control-plane operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def backend_agent_artifacts(self) -> list[RuntimeBackendAgentArtifact]:
        """Download versioned execution config; no platform LLM call occurs."""
        data = await self._http.get("/api/v1/runtime/backend-agent-artifacts")
        return [RuntimeBackendAgentArtifact.model_validate(item) for item in data["artifacts"]]

    async def context_bundle(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        current_message: str | None = None,
    ) -> RuntimeContextBundle:
        body = {
            "user_id": user_id,
            "session_id": session_id,
            "current_message": current_message,
        }
        data = await self._http.post(
            f"/api/v1/agents/{quote(agent_id, safe='')}/context-bundle",
            json_data={key: value for key, value in body.items() if value is not None},
        )
        return RuntimeContextBundle.model_validate(data)

    async def conversation(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str,
        page: int | None = None,
        page_size: int | None = None,
    ) -> RuntimeConversation:
        data = await self._http.get(
            f"/api/v1/agents/{quote(agent_id, safe='')}/conversations",
            params={
                "user_id": user_id,
                "session_id": session_id,
                "page": page,
                "page_size": page_size,
            },
        )
        return RuntimeConversation.model_validate(data)

    async def report_turns(
        self,
        agent_id: str,
        report: RuntimeTurnReport,
    ) -> RuntimeTurnReportResult:
        data = await self._http.post(
            f"/api/v1/agents/{quote(agent_id, safe='')}/turns",
            json_data=report.model_dump(mode="json", exclude_none=True),
        )
        return RuntimeTurnReportResult.model_validate(data)

    async def submit_usage_report(
        self,
        report: RuntimeUsageReport,
    ) -> RuntimeUsageReportResult:
        data = await self._http.post(
            "/api/v1/usage/reports",
            json_data=report.model_dump(mode="json", exclude_none=True),
            headers={"X-Sonzai-Metering-Signature": report.signature},
        )
        return RuntimeUsageReportResult.model_validate(data)


def canonical_runtime_usage_report(report: RuntimeUsageReport) -> str:
    """Return the stable, counter-order-independent v2 signing payload."""
    counters = sorted(report.counters, key=_counter_sort_key)
    lines = [
        str(report.schema_version or RUNTIME_USAGE_SCHEMA_VERSION),
        report.report_id,
        report.tenant_id,
        report.instance_id or "",
        _canonical_timestamp(report.period_start),
        _canonical_timestamp(report.period_end),
        _canonical_timestamp(report.heartbeat_at),
    ]
    for counter in counters:
        lines.append(
            "\t".join(
                [
                    counter.project_id,
                    counter.agent_id,
                    counter.provider,
                    counter.model,
                    counter.use_case,
                    counter.billing_mode,
                    str(counter.tokens_in),
                    str(counter.tokens_out),
                    str(counter.cache_read_tokens),
                    str(counter.cache_creation_tokens),
                    str(counter.turns),
                    str(counter.unreported_turns),
                ]
            )
        )
    return "\n".join(lines)


def sign_runtime_usage_report(report: RuntimeUsageReport, key: str) -> str:
    """Return the lowercase hex HMAC-SHA256 signature for ``report``."""
    return hmac.new(
        key.encode(), canonical_runtime_usage_report(report).encode(), hashlib.sha256
    ).hexdigest()


def _counter_sort_key(counter: RuntimeUsageCounter) -> tuple[str, ...]:
    return (
        counter.project_id,
        counter.agent_id,
        counter.provider,
        counter.model,
        counter.use_case,
        counter.billing_mode,
    )


def _canonical_timestamp(value: str) -> str:
    value = value.replace("+00:00", "Z")
    if value.endswith("Z") and "." in value:
        prefix, fraction = value[:-1].split(".", 1)
        fraction = fraction.rstrip("0")
        return f"{prefix}.{fraction}Z" if fraction else f"{prefix}Z"
    return value
