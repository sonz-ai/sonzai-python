"""Tests for the Sonzai Lead Assignments resource (``client.lead_assignments``).

Pins URL path + HTTP method + request body + response decode for
``offer``/``list``/``get``/``claim``/``release``/``complete`` on both the
sync and async clients. Follows the ``test_ml`` respx pattern.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.types import LeadAssignment, ListLeadAssignmentsResult, OfferLeadAssignmentResult


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


ASSIGNMENT = {
    "assignment_id": "assign-1",
    "lead_ref": "lead-1",
    "rep_user_id": "rep-1",
    "state": "offered",
    "policy": "load_balanced",
    "offered_at": "2026-07-06T10:00:00Z",
    "sla_expires_at": "2026-07-06T10:10:00Z",
}

OFFER_RESULT = {"assignment": ASSIGNMENT, "deduplicated": False}


class TestOffer:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/lead-assignments/offer").mock(
            return_value=httpx.Response(200, json=OFFER_RESULT)
        )

        result = client.lead_assignments.offer(
            lead_ref="lead-1",
            candidates=["rep-1", "rep-2"],
            policy="load_balanced",
            sla_seconds=600,
        )

        assert json.loads(route.calls.last.request.content) == {
            "lead_ref": "lead-1",
            "candidates": ["rep-1", "rep-2"],
            "policy": "load_balanced",
            "sla_seconds": 600,
        }
        assert isinstance(result, OfferLeadAssignmentResult)
        assert result.deduplicated is False
        assert result.assignment.assignment_id == "assign-1"
        assert result.assignment.rep_user_id == "rep-1"

    @respx.mock
    def test_optional_fields_omitted_when_none(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/lead-assignments/offer").mock(
            return_value=httpx.Response(200, json=OFFER_RESULT)
        )

        client.lead_assignments.offer(lead_ref="lead-1", candidates=["rep-1"])

        assert json.loads(route.calls.last.request.content) == {
            "lead_ref": "lead-1",
            "candidates": ["rep-1"],
        }

    @respx.mock
    def test_deduplicated(self, client: Sonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/lead-assignments/offer").mock(
            return_value=httpx.Response(200, json={"assignment": ASSIGNMENT, "deduplicated": True})
        )

        result = client.lead_assignments.offer(lead_ref="lead-1", candidates=["rep-1"])

        assert result.deduplicated is True

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/lead-assignments/offer").mock(
            return_value=httpx.Response(200, json=OFFER_RESULT)
        )
        try:
            result = await async_client.lead_assignments.offer(
                lead_ref="lead-1", candidates=["rep-1"]
            )
            assert isinstance(result, OfferLeadAssignmentResult)
            assert result.assignment.assignment_id == "assign-1"
        finally:
            await async_client.close()


class TestList:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/lead-assignments").mock(
            return_value=httpx.Response(200, json={"assignments": [ASSIGNMENT]})
        )

        result = client.lead_assignments.list(rep_user_id="rep-1", state="offered", limit=10)

        request = route.calls.last.request
        assert request.url.params["rep_user_id"] == "rep-1"
        assert request.url.params["state"] == "offered"
        assert request.url.params["limit"] == "10"
        assert isinstance(result, ListLeadAssignmentsResult)
        assert len(result.assignments) == 1
        assert result.assignments[0].assignment_id == "assign-1"

    @respx.mock
    def test_no_filters(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/lead-assignments").mock(
            return_value=httpx.Response(200, json={"assignments": []})
        )

        client.lead_assignments.list()

        assert dict(route.calls.last.request.url.params) == {}


class TestGet:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/lead-assignments/assign-1").mock(
            return_value=httpx.Response(200, json=ASSIGNMENT)
        )

        result = client.lead_assignments.get("assign-1")

        assert isinstance(result, LeadAssignment)
        assert result.assignment_id == "assign-1"
        assert result.state == "offered"


class TestTransitions:
    @respx.mock
    def test_claim(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/lead-assignments/assign-1/claim").mock(
            return_value=httpx.Response(200, json={**ASSIGNMENT, "state": "claimed"})
        )

        result = client.lead_assignments.claim("assign-1")

        assert route.calls.last.request.method == "POST"
        assert isinstance(result, LeadAssignment)
        assert result.state == "claimed"

    @respx.mock
    def test_release(self, client: Sonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/lead-assignments/assign-1/release").mock(
            return_value=httpx.Response(200, json={**ASSIGNMENT, "state": "released"})
        )

        result = client.lead_assignments.release("assign-1")

        assert result.state == "released"

    @respx.mock
    def test_complete(self, client: Sonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/lead-assignments/assign-1/complete").mock(
            return_value=httpx.Response(200, json={**ASSIGNMENT, "state": "completed"})
        )

        result = client.lead_assignments.complete("assign-1")

        assert result.state == "completed"

    @respx.mock
    async def test_claim_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        respx.post(f"{base_url}/api/v1/lead-assignments/assign-1/claim").mock(
            return_value=httpx.Response(200, json={**ASSIGNMENT, "state": "claimed"})
        )
        try:
            result = await async_client.lead_assignments.claim("assign-1")
            assert result.state == "claimed"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# Client wiring
# ---------------------------------------------------------------------------


class TestWiring:
    def test_wired_on_sync_client(self, client: Sonzai) -> None:
        from sonzai.resources.lead_assignments import LeadAssignments

        assert isinstance(client.lead_assignments, LeadAssignments)

    def test_wired_on_async_client(self, async_client: AsyncSonzai) -> None:
        from sonzai.resources.lead_assignments import AsyncLeadAssignments

        assert isinstance(async_client.lead_assignments, AsyncLeadAssignments)
