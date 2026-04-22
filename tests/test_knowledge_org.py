"""Tests for org-global KB SDK methods (Phase 5c)."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import (
    AsyncSonzai,
    CreateOrgNodeOptions,
    KBScope,
    Sonzai,
)


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


# ---------------------------------------------------------------------------
# KBScope wire-value lock
# ---------------------------------------------------------------------------


def test_kb_scope_wire_values():
    # These round-trip through the platform API alongside sonzai-go /
    # sonzai-typescript — a drift breaks cross-SDK compatibility.
    assert KBScope.PROJECT_ONLY.value == "project_only"
    assert KBScope.ORG_ONLY.value == "org_only"
    assert KBScope.CASCADE.value == "cascade"
    assert KBScope.UNION.value == "union"


# ---------------------------------------------------------------------------
# create_org_node
# ---------------------------------------------------------------------------


@respx.mock
def test_create_org_node_sync(base_url):
    route = respx.post(f"{base_url}/api/v1/tenants/tenant-abc/knowledge/org-nodes").mock(
        return_value=httpx.Response(
            200,
            json={
                "project_id": "",
                "node_id": "n1",
                "node_type": "policy",
                "label": "Refund",
                "norm_label": "refund",
                "properties": {},
                "source_docs": None,
                "source_type": "api",
                "version": 1,
                "is_active": True,
                "confidence": 1.0,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            },
        )
    )

    client = Sonzai(api_key="test-key", base_url=base_url)
    try:
        node = client.knowledge.create_org_node(
            "tenant-abc",
            CreateOrgNodeOptions(
                node_type="policy",
                label="Refund",
                properties={"description": "default refund"},
            ),
        )
    finally:
        client.close()

    assert node.node_id == "n1"
    assert route.called
    # Verify the body shape.
    body = json.loads(route.calls[0].request.content)
    assert body["node_type"] == "policy"
    assert body["label"] == "Refund"
    assert body["properties"] == {"description": "default refund"}


@respx.mock
def test_create_org_node_accepts_dict(base_url):
    route = respx.post(f"{base_url}/api/v1/tenants/t1/knowledge/org-nodes").mock(
        return_value=httpx.Response(
            200,
            json={
                "project_id": "",
                "node_id": "n1",
                "node_type": "t",
                "label": "l",
                "norm_label": "l",
                "properties": {},
                "source_docs": None,
                "source_type": "api",
                "version": 1,
                "is_active": True,
                "confidence": 1.0,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            },
        )
    )
    client = Sonzai(api_key="test-key", base_url=base_url)
    try:
        client.knowledge.create_org_node("t1", {"node_type": "t", "label": "l"})
    finally:
        client.close()
    assert route.called


# ---------------------------------------------------------------------------
# promote_node_to_org
# ---------------------------------------------------------------------------


@respx.mock
def test_promote_node_to_org_sync(base_url):
    route = respx.post(
        f"{base_url}/api/v1/projects/proj-a/knowledge/nodes/p1/promote-to-org"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "project_id": "",
                "node_id": "org-n1",
                "node_type": "policy",
                "label": "Privacy",
                "norm_label": "privacy",
                "properties": {},
                "source_docs": None,
                "source_type": "promotion",
                "version": 1,
                "is_active": True,
                "confidence": 1.0,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
                "scope_type": "organization",
                "relevance": 1.0,
            },
        )
    )
    client = Sonzai(api_key="test-key", base_url=base_url)
    try:
        got = client.knowledge.promote_node_to_org("proj-a", "p1", "tenant-abc")
    finally:
        client.close()

    assert got.scope_type == "organization"
    assert got.node_id == "org-n1"
    body = json.loads(route.calls[0].request.content)
    assert body == {"tenant_id": "tenant-abc"}


# ---------------------------------------------------------------------------
# Async parity
# ---------------------------------------------------------------------------


@pytest.mark.anyio
@respx.mock
async def test_create_org_node_async(base_url):
    respx.post(f"{base_url}/api/v1/tenants/t1/knowledge/org-nodes").mock(
        return_value=httpx.Response(
            200,
            json={
                "project_id": "",
                "node_id": "async-n1",
                "node_type": "t",
                "label": "l",
                "norm_label": "l",
                "properties": {},
                "source_docs": None,
                "source_type": "api",
                "version": 1,
                "is_active": True,
                "confidence": 1.0,
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
            },
        )
    )
    client = AsyncSonzai(api_key="test-key", base_url=base_url)
    try:
        node = await client.knowledge.create_org_node(
            "t1", CreateOrgNodeOptions(node_type="t", label="l")
        )
    finally:
        await client.close()
    assert node.node_id == "async-n1"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
