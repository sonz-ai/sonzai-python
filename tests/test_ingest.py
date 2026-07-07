"""Tests for the Sonzai adapter-ingestion resource (``client.ingest``).

Pins URL path + HTTP method + request body + response decode for
``send_event``/``upsert_contact``/``list_events`` on both the sync and async
clients. Follows the ``test_ml`` respx pattern.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.resources.ingest import INGEST_EVENT_LEAD_CREATED, INGEST_EVENT_OUTCOME_RECORDED
from sonzai.types import IngestContact, IngestEventResult, ListIngestEventsResult


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


class TestSendEvent:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(
                200,
                json={
                    "event_id": "11111111-1111-1111-1111-111111111111",
                    "type": INGEST_EVENT_LEAD_CREATED,
                    "duplicate": False,
                },
            )
        )

        occurred_at = datetime(2026, 7, 6, 10, 0, 0, tzinfo=UTC)
        result = client.ingest.send_event(
            event_id="11111111-1111-1111-1111-111111111111",
            type=INGEST_EVENT_LEAD_CREATED,
            occurred_at=occurred_at,
            lead_ref="lead-1",
            payload={"source": "salesforce"},
        )

        body = json.loads(route.calls.last.request.content)
        assert body["event_id"] == "11111111-1111-1111-1111-111111111111"
        assert body["type"] == INGEST_EVENT_LEAD_CREATED
        assert body["lead_ref"] == "lead-1"
        assert body["payload"] == {"source": "salesforce"}
        assert isinstance(result, IngestEventResult)
        assert result.duplicate is False

    @respx.mock
    def test_optional_fields_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(
                200,
                json={"event_id": "e1", "type": INGEST_EVENT_OUTCOME_RECORDED, "duplicate": False},
            )
        )

        client.ingest.send_event(
            event_id="e1",
            type=INGEST_EVENT_OUTCOME_RECORDED,
            occurred_at=datetime(2026, 7, 6, tzinfo=UTC),
        )

        body = json.loads(route.calls.last.request.content)
        assert "lead_ref" not in body
        assert "contact_ref" not in body
        assert "payload" not in body

    @respx.mock
    def test_duplicate_replay(self, client: Sonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(
                200, json={"event_id": "e1", "type": "lead.created", "duplicate": True}
            )
        )

        result = client.ingest.send_event(
            event_id="e1", type="lead.created", occurred_at=datetime.now(UTC)
        )

        assert result.duplicate is True

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(
                200, json={"event_id": "e1", "type": "lead.created", "duplicate": False}
            )
        )
        try:
            result = await async_client.ingest.send_event(
                event_id="e1", type="lead.created", occurred_at=datetime.now(UTC)
            )
            assert isinstance(result, IngestEventResult)
        finally:
            await async_client.close()


class TestUpsertContact:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/ingest/contacts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "contact-1",
                    "contact_ref": "rep-1",
                    "kind": "rep",
                    "crm_owner_id": "sf-owner-1",
                },
            )
        )

        result = client.ingest.upsert_contact(
            contact_ref="rep-1", kind="rep", crm_owner_id="sf-owner-1"
        )

        assert json.loads(route.calls.last.request.content) == {
            "contact_ref": "rep-1",
            "kind": "rep",
            "crm_owner_id": "sf-owner-1",
        }
        assert isinstance(result, IngestContact)
        assert result.id == "contact-1"
        assert result.crm_owner_id == "sf-owner-1"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/ingest/contacts").mock(
            return_value=httpx.Response(
                200, json={"id": "c1", "contact_ref": "rep-1", "kind": "rep"}
            )
        )
        try:
            result = await async_client.ingest.upsert_contact(contact_ref="rep-1", kind="rep")
            assert isinstance(result, IngestContact)
        finally:
            await async_client.close()


class TestListEvents:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        since = datetime(2026, 7, 6, tzinfo=UTC)
        route = respx.get(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(
                200,
                json={
                    "events": [
                        {"event_id": "evt-1", "type": "outcome.recorded", "lead_ref": "lead-1"}
                    ],
                    "next_cursor": "cursor-2",
                },
            )
        )

        result = client.ingest.list_events(since=since, limit=50)

        request = route.calls.last.request
        assert request.url.params["since"] == since.isoformat()
        assert request.url.params["limit"] == "50"
        assert isinstance(result, ListIngestEventsResult)
        assert len(result.events) == 1
        assert result.events[0].event_id == "evt-1"
        assert result.next_cursor == "cursor-2"

    @respx.mock
    def test_cursor_param(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/ingest/events").mock(
            return_value=httpx.Response(200, json={"events": []})
        )

        client.ingest.list_events(since=datetime.now(UTC), cursor="cur-1")

        assert route.calls.last.request.url.params["cursor"] == "cur-1"


# ---------------------------------------------------------------------------
# Client wiring
# ---------------------------------------------------------------------------


class TestWiring:
    def test_wired_on_sync_client(self, client: Sonzai) -> None:
        from sonzai.resources.ingest import Ingest

        assert isinstance(client.ingest, Ingest)

    def test_wired_on_async_client(self, async_client: AsyncSonzai) -> None:
        from sonzai.resources.ingest import AsyncIngest

        assert isinstance(async_client.ingest, AsyncIngest)
