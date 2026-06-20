"""Tests for the MCP Catalog resource (``client.mcp_catalog``).

Pins URL path + HTTP method + request body (where applicable) + response
decode for every clean method — ``list`` / ``get`` / ``create`` / ``update`` /
``delete`` / ``probe_config`` / ``probe`` / ``list_tools`` / ``list_usages`` —
on both the sync and async clients. Also asserts the resource is wired onto
both ``Sonzai`` and ``AsyncSonzai`` as ``client.mcp_catalog`` and that the raw
generated-named methods remain reachable via inheritance.

Follows the ``test_ml`` / ``test_builtin_agents`` respx pattern. Shapes mirror
the Go SDK's ``mcp.go`` (``MCPCatalogResource``) and the TS SDK's
``mcp-catalog.ts`` (``MCPCatalog``).
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.mcp_catalog import AsyncMCPCatalog, MCPCatalog
from sonzai.types import (
    ListMCPCatalogOutputBody,
    MCPCatalogEntry,
    MCPCatalogToolsResponse,
    MCPCatalogUsagesResponse,
    MCPProbeResponseBody,
)


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def client(base_url: str) -> Sonzai:
    c = Sonzai(api_key="test-key", base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def async_client(base_url: str) -> AsyncSonzai:
    return AsyncSonzai(api_key="test-key", base_url=base_url)


# ---------------------------------------------------------------------------
# Canonical response bodies (snake_case, mirrors mcp.go / openapi shapes)
# ---------------------------------------------------------------------------

ENTRY = {
    "id": "mcp-1",
    "name": "Weather",
    "description": "Weather MCP server",
    "url": "https://mcp.example.com/weather",
    "transport": "streamable-http",
    "auth": {"kind": "bearer", "bearer_secret_ref": "sm://proj/mcp-1/bearer"},
    "health": {
        "status": "ok",
        "last_ok_at": "2026-06-01T00:00:00Z",
        "failures_1h": 0,
    },
    "created_at": "2026-06-01T00:00:00Z",
    "updated_at": "2026-06-01T00:00:00Z",
}

LIST_RESULT = {"entries": [ENTRY]}

PROBE_RESULT = {"ok": True, "latency_ms": 42, "tool_count": 3, "error": ""}

TOOLS_RESULT = {
    "tools": [
        {
            "name": "get_forecast",
            "description": "Get the weather forecast",
            "input_schema": {"type": "object"},
        }
    ]
}

USAGES_RESULT = {"agent_ids": ["agent-a", "agent-b"]}


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------


class TestWiring:
    def test_sync_client_exposes_mcp_catalog(self, client: Sonzai) -> None:
        assert isinstance(client.mcp_catalog, MCPCatalog)
        # raw generated-named methods remain reachable via inheritance
        assert hasattr(client.mcp_catalog, "list_mcp_catalog")
        assert hasattr(client.mcp_catalog, "create_mcp_catalog_entry")

    def test_async_client_exposes_mcp_catalog(self, async_client: AsyncSonzai) -> None:
        assert isinstance(async_client.mcp_catalog, AsyncMCPCatalog)
        assert hasattr(async_client.mcp_catalog, "list_mcp_catalog")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


class TestList:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog"
        ).mock(return_value=httpx.Response(200, json=LIST_RESULT))

        result = client.mcp_catalog.list("proj-1")

        assert route.calls.last.request.method == "GET"
        assert isinstance(result, ListMCPCatalogOutputBody)
        assert result.entries is not None
        assert result.entries[0].id == "mcp-1"
        assert result.entries[0].health.status == "ok"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog"
        ).mock(return_value=httpx.Response(200, json=LIST_RESULT))
        try:
            result = await async_client.mcp_catalog.list("proj-1")
            assert route.calls.last.request.method == "GET"
            assert result.entries[0].id == "mcp-1"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json=ENTRY))

        result = client.mcp_catalog.get("proj-1", "mcp-1")

        assert route.calls.last.request.method == "GET"
        assert isinstance(result, MCPCatalogEntry)
        assert result.name == "Weather"
        assert result.transport == "streamable-http"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json=ENTRY))
        try:
            result = await async_client.mcp_catalog.get("proj-1", "mcp-1")
            assert route.calls.last.request.method == "GET"
            assert result.name == "Weather"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


class TestCreate:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog"
        ).mock(return_value=httpx.Response(200, json=ENTRY))

        result = client.mcp_catalog.create(
            "proj-1",
            name="Weather",
            url="https://mcp.example.com/weather",
            transport="streamable-http",
            auth={"kind": "bearer", "bearer_token": "sk-xyz"},
            description="Weather MCP server",
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "auth": {"kind": "bearer", "bearer_token": "sk-xyz"},
            "name": "Weather",
            "transport": "streamable-http",
            "url": "https://mcp.example.com/weather",
            "description": "Weather MCP server",
        }
        assert isinstance(result, MCPCatalogEntry)
        assert result.id == "mcp-1"

    @respx.mock
    def test_description_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog"
        ).mock(return_value=httpx.Response(200, json=ENTRY))

        client.mcp_catalog.create(
            "proj-1",
            name="Weather",
            url="https://mcp.example.com/weather",
            transport="streamable-http",
            auth={"kind": "none"},
        )

        sent = json.loads(route.calls.last.request.content)
        assert "description" not in sent
        assert "$schema" not in sent
        assert sent["url"] == "https://mcp.example.com/weather"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog"
        ).mock(return_value=httpx.Response(200, json=ENTRY))
        try:
            result = await async_client.mcp_catalog.create(
                "proj-1",
                name="Weather",
                url="https://mcp.example.com/weather",
                transport="streamable-http",
                auth={"kind": "none"},
            )
            assert route.calls.last.request.method == "POST"
            assert result.id == "mcp-1"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


class TestUpdate:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.patch(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json=ENTRY))

        result = client.mcp_catalog.update(
            "proj-1",
            "mcp-1",
            name="Weather v2",
            auth={"kind": "bearer", "bearer_token": "sk-new"},
        )

        request = route.calls.last.request
        assert request.method == "PATCH"
        assert json.loads(request.content) == {
            "auth": {"kind": "bearer", "bearer_token": "sk-new"},
            "name": "Weather v2",
        }
        assert isinstance(result, MCPCatalogEntry)

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.patch(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json=ENTRY))
        try:
            await async_client.mcp_catalog.update("proj-1", "mcp-1", name="Renamed")
            request = route.calls.last.request
            assert request.method == "PATCH"
            assert json.loads(request.content) == {"name": "Renamed"}
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


class TestDelete:
    @respx.mock
    def test_request_shape(self, client: Sonzai, base_url: str) -> None:
        route = respx.delete(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json={"ok": True}))

        client.mcp_catalog.delete("proj-1", "mcp-1")

        assert route.calls.last.request.method == "DELETE"
        assert "force" not in route.calls.last.request.url.params

    @respx.mock
    def test_force_param(self, client: Sonzai, base_url: str) -> None:
        route = respx.delete(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json={"ok": True}))

        client.mcp_catalog.delete("proj-1", "mcp-1", force=True)

        assert route.calls.last.request.url.params["force"] == "true"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.delete(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1"
        ).mock(return_value=httpx.Response(200, json={"ok": True}))
        try:
            await async_client.mcp_catalog.delete("proj-1", "mcp-1")
            assert route.calls.last.request.method == "DELETE"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# probe_config (pre-create)
# ---------------------------------------------------------------------------


class TestProbeConfig:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/probe"
        ).mock(return_value=httpx.Response(200, json=PROBE_RESULT))

        result = client.mcp_catalog.probe_config(
            "proj-1",
            name="Weather",
            url="https://mcp.example.com/weather",
            transport="sse",
            auth={"kind": "none"},
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "auth": {"kind": "none"},
            "name": "Weather",
            "transport": "sse",
            "url": "https://mcp.example.com/weather",
        }
        assert isinstance(result, MCPProbeResponseBody)
        assert result.ok is True
        assert result.tool_count == 3
        assert result.latency_ms == 42

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/probe"
        ).mock(return_value=httpx.Response(200, json=PROBE_RESULT))
        try:
            result = await async_client.mcp_catalog.probe_config(
                "proj-1",
                name="Weather",
                url="https://mcp.example.com/weather",
                transport="sse",
                auth={"kind": "none"},
            )
            assert route.calls.last.request.method == "POST"
            assert result.tool_count == 3
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# probe (existing entry)
# ---------------------------------------------------------------------------


class TestProbe:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/probe"
        ).mock(return_value=httpx.Response(200, json=PROBE_RESULT))

        result = client.mcp_catalog.probe("proj-1", "mcp-1")

        assert route.calls.last.request.method == "POST"
        assert isinstance(result, MCPProbeResponseBody)
        assert result.ok is True

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/probe"
        ).mock(return_value=httpx.Response(200, json=PROBE_RESULT))
        try:
            result = await async_client.mcp_catalog.probe("proj-1", "mcp-1")
            assert route.calls.last.request.method == "POST"
            assert result.ok is True
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# list_tools
# ---------------------------------------------------------------------------


class TestListTools:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/tools"
        ).mock(return_value=httpx.Response(200, json=TOOLS_RESULT))

        result = client.mcp_catalog.list_tools("proj-1", "mcp-1")

        assert route.calls.last.request.method == "GET"
        assert isinstance(result, MCPCatalogToolsResponse)
        assert result.tools is not None
        assert result.tools[0].name == "get_forecast"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/tools"
        ).mock(return_value=httpx.Response(200, json=TOOLS_RESULT))
        try:
            result = await async_client.mcp_catalog.list_tools("proj-1", "mcp-1")
            assert route.calls.last.request.method == "GET"
            assert result.tools[0].name == "get_forecast"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# list_usages
# ---------------------------------------------------------------------------


class TestListUsages:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/usages"
        ).mock(return_value=httpx.Response(200, json=USAGES_RESULT))

        result = client.mcp_catalog.list_usages("proj-1", "mcp-1")

        assert route.calls.last.request.method == "GET"
        assert isinstance(result, MCPCatalogUsagesResponse)
        assert result.agent_ids == ["agent-a", "agent-b"]

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/mcp/catalog/mcp-1/usages"
        ).mock(return_value=httpx.Response(200, json=USAGES_RESULT))
        try:
            result = await async_client.mcp_catalog.list_usages("proj-1", "mcp-1")
            assert route.calls.last.request.method == "GET"
            assert result.agent_ids == ["agent-a", "agent-b"]
        finally:
            await async_client.close()
