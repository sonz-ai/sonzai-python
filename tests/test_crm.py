"""Tests for runtime CRM resource."""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, CRMImportItem, Sonzai
from sonzai.resources.crm import AsyncCrm, Crm


@pytest.fixture
def platform_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def runtime_url() -> str:
    return "https://runtime.test.sonz.ai"


@pytest.fixture
def client(platform_url: str, runtime_url: str) -> Sonzai:
    c = Sonzai(
        api_key="platform-key",
        base_url=platform_url,
        runtime_base_url=runtime_url,
        runtime_api_key="adapter-token",
    )
    yield c
    c.close()


@pytest.fixture
def async_client(platform_url: str, runtime_url: str) -> AsyncSonzai:
    return AsyncSonzai(
        api_key="platform-key",
        base_url=platform_url,
        runtime_base_url=runtime_url,
        runtime_api_key="adapter-token",
    )


CONTACT = {
    "id": "contact-1",
    "tenant_id": "tenant-1",
    "project_id": "proj-1",
    "first_name": "Grace",
    "last_name": "Hopper",
    "emails": ["grace@example.com"],
    "phones": [],
    "lead_ref": "lead-1",
    "owner_user_id": "owner-1",
    "source": "salesforce",
    "external_ref": "sf-1",
    "custom": {"segment": "enterprise"},
    "archived": False,
    "created_at": "2026-07-10T00:00:00Z",
    "updated_at": "2026-07-10T00:00:00Z",
}


def test_client_exposes_runtime_crm(client: Sonzai, async_client: AsyncSonzai) -> None:
    assert isinstance(client.crm, Crm)
    assert isinstance(async_client.crm, AsyncCrm)
    assert hasattr(client.crm, "import_contacts")
    assert hasattr(client.crm, "events")


@respx.mock
def test_import_contacts_uses_runtime_base_url_token_and_tenant(
    client: Sonzai, runtime_url: str
) -> None:
    route = respx.post(f"{runtime_url}/api/rt/crm/import").mock(
        return_value=httpx.Response(200, json={"imported": 1, "contacts": [CONTACT]})
    )

    result = client.crm.import_contacts(
        [
            CRMImportItem(
                external_ref="sf-1",
                project_id="proj-1",
                first_name="Grace",
                last_name="Hopper",
                emails=["grace@example.com"],
                phones=[],
                lead_ref="lead-1",
                owner_user_id="owner-1",
                source="salesforce",
                custom={"segment": "enterprise"},
            )
        ],
        tenant_id="tenant-1",
        idempotency_key="idem-1",
    )

    request = route.calls.last.request
    assert request.url.host == "runtime.test.sonz.ai"
    assert request.headers["Authorization"] == "Bearer adapter-token"
    assert request.headers["X-Sonzai-Tenant-ID"] == "tenant-1"
    assert request.headers["Idempotency-Key"] == "idem-1"
    assert json.loads(request.content) == {
        "contacts": [
            {
                "external_ref": "sf-1",
                "project_id": "proj-1",
                "first_name": "Grace",
                "last_name": "Hopper",
                "emails": ["grace@example.com"],
                "phones": [],
                "lead_ref": "lead-1",
                "owner_user_id": "owner-1",
                "source": "salesforce",
                "custom": {"segment": "enterprise"},
            }
        ]
    }
    assert result.imported == 1
    assert result.contacts[0].external_ref == "sf-1"


@respx.mock
def test_events_uses_cursor_pagination(client: Sonzai, runtime_url: str) -> None:
    first = respx.get(f"{runtime_url}/api/rt/crm/events").mock(
        return_value=httpx.Response(
            200,
            json={
                "events": [
                    {
                        "cursor": "1",
                        "tenant_id": "tenant-1",
                        "event": "contact.imported",
                        "entity_id": "contact-1",
                        "entity_type": "contact",
                        "payload": {"contact_id": "contact-1"},
                        "at": "2026-07-10T00:00:00Z",
                    }
                ],
                "next_cursor": "1",
            },
        )
    )
    second = respx.get(f"{runtime_url}/api/rt/crm/events").mock(
        return_value=httpx.Response(200, json={"events": [], "next_cursor": ""})
    )

    page = client.crm.events(cursor="0", limit=1, tenant_id="tenant-1")
    events = list(page)

    assert first.calls[0].request.url.params["cursor"] == "0"
    assert first.calls[0].request.url.params["limit"] == "1"
    assert first.calls[0].request.headers["X-Sonzai-Tenant-ID"] == "tenant-1"
    assert second.calls[0].request.url.params["cursor"] == "1"
    assert events[0].event == "contact.imported"
    assert events[0].payload == {"contact_id": "contact-1"}


def test_crm_requires_runtime_base_url() -> None:
    client = Sonzai(api_key="platform-key", base_url="https://api.test.sonz.ai")
    try:
        with pytest.raises(ValueError, match="runtime_base_url"):
            client.crm.import_contacts([{"external_ref": "sf-1"}])
    finally:
        client.close()


@respx.mock
async def test_async_import_contacts(async_client: AsyncSonzai, runtime_url: str) -> None:
    route = respx.post(f"{runtime_url}/api/rt/crm/import").mock(
        return_value=httpx.Response(200, json={"imported": 1, "contacts": [CONTACT]})
    )

    try:
        result = await async_client.crm.import_contacts(
            [{"external_ref": "sf-1", "first_name": "Grace"}], tenant_id="tenant-1"
        )
    finally:
        await async_client.close()

    assert route.calls.last.request.headers["Authorization"] == "Bearer adapter-token"
    assert route.calls.last.request.headers["X-Sonzai-Tenant-ID"] == "tenant-1"
    assert result.contacts[0].first_name == "Grace"


@respx.mock
async def test_async_events(async_client: AsyncSonzai, runtime_url: str) -> None:
    route = respx.get(f"{runtime_url}/api/rt/crm/events").mock(
        return_value=httpx.Response(
            200,
            json={
                "events": [
                    {
                        "cursor": "7",
                        "event": "deal.stage_changed",
                        "entity_id": "deal-1",
                        "entity_type": "deal",
                        "payload": {"deal_id": "deal-1"},
                        "at": "2026-07-10T00:00:00Z",
                    }
                ],
                "next_cursor": "",
            },
        )
    )

    try:
        page = await async_client.crm.events(limit=25)
        events = await page.first_page()
    finally:
        await async_client.close()

    assert route.calls.last.request.url.params["limit"] == "25"
    assert events[0].cursor == "7"
