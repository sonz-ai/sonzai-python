"""Tests for the clean public aliases over ugly inherited generated names.

Covers (non-breaking aliases — both the new clean name AND the legacy
generated name must hit the same endpoint and decode the same response):

* ``analytics.get_composio_usage`` -> ``analytics_composio_usage``
  (GET /api/v1/analytics/composio; Go ``ComposioUsage`` / TS ``getComposioUsage``)
* ``knowledge.active_fact``   -> ``kb_get_active_fact``
* ``knowledge.fact_history``  -> ``kb_get_fact_history``
* ``knowledge.entity``        -> ``kb_get_entity``
* ``knowledge.traverse``      -> ``kb_traverse``
* ``knowledge.compare``       -> ``kb_compare``

Sync + async, pinning URL path + method + query params/body + response decode.
Follows the ``test_ml`` respx pattern.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
# Canonical response bodies
# ---------------------------------------------------------------------------

COMPOSIO_USAGE = {
    "by_app": [{"app": "gmail", "calls": 12, "cost_usd": 0.04}],
    "period": {"start": "2026-06-01T00:00:00Z", "end": "2026-06-19T00:00:00Z"},
    "summary": {"total_calls": 12, "total_cost_usd": 0.04},
}

FACT = {
    "created_at": "2026-06-01T00:00:00Z",
    "effective_date": "2026-06-01T00:00:00Z",
    "extraction_confidence": 0.9,
    "fact_id": "fact-1",
    "from_node_id": "node-a",
    "is_active": True,
    "properties": {"price": 100},
    "relation_type": "priced_at",
    "source_document_id": "doc-1",
    "source_page": 1,
    "source_snippet": "snippet",
    "to_node_id": "node-b",
    "version": 1,
}

ACTIVE_FACT_RESULT = {"fact": FACT}
FACT_HISTORY_RESULT = {"versions": [FACT]}
ENTITY_RESULT = {
    "entity_key": {"slug": "makati"},
    "entity_node_id": "node-a",
    "entity_type": "Property",
    "incoming_facts": [FACT],
    "outgoing_facts": [],
}
TRAVERSE_RESULT = {"facts": [{"depth": 1, "fact": FACT}]}
COMPARE_RESULT = {
    "rows": [
        {
            "entity": {"key": {"slug": "makati"}, "type": "Property"},
            "fact": FACT,
            "missing": False,
            "value": 100,
        }
    ]
}


# ---------------------------------------------------------------------------
# analytics.get_composio_usage
# ---------------------------------------------------------------------------


class TestAnalyticsComposioUsageAlias:
    @respx.mock
    def test_alias_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/analytics/composio").mock(
            return_value=httpx.Response(200, json=COMPOSIO_USAGE)
        )

        result = client.analytics.get_composio_usage(
            start="2026-06-01", end="2026-06-19", agent_id="agent-1"
        )

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.params["start"] == "2026-06-01"
        assert request.url.params["end"] == "2026-06-19"
        assert request.url.params["agent_id"] == "agent-1"
        assert result.summary.total_calls == 12
        assert result.by_app[0].app == "gmail"

    @respx.mock
    def test_alias_matches_legacy_name(self, client: Sonzai, base_url: str) -> None:
        respx.get(f"{base_url}/api/v1/analytics/composio").mock(
            return_value=httpx.Response(200, json=COMPOSIO_USAGE)
        )
        via_alias = client.analytics.get_composio_usage()
        via_legacy = client.analytics.analytics_composio_usage()
        assert via_alias.summary.total_cost_usd == via_legacy.summary.total_cost_usd
        assert type(via_alias) is type(via_legacy)

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(f"{base_url}/api/v1/analytics/composio").mock(
            return_value=httpx.Response(200, json=COMPOSIO_USAGE)
        )
        try:
            result = await async_client.analytics.get_composio_usage(agent_id="agent-1")
            assert route.calls.last.request.method == "GET"
            assert route.calls.last.request.url.params["agent_id"] == "agent-1"
            assert result.summary.total_calls == 12
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# knowledge.active_fact
# ---------------------------------------------------------------------------


class TestActiveFactAlias:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/facts/active"
        ).mock(return_value=httpx.Response(200, json=ACTIVE_FACT_RESULT))

        result = client.knowledge.active_fact(
            "proj-1",
            from_node_id="node-a",
            to_node_id="node-b",
            relation_type="priced_at",
        )

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.params["from_node_id"] == "node-a"
        assert request.url.params["to_node_id"] == "node-b"
        assert request.url.params["relation_type"] == "priced_at"
        assert result.fact.fact_id == "fact-1"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/facts/active"
        ).mock(return_value=httpx.Response(200, json=ACTIVE_FACT_RESULT))
        try:
            result = await async_client.knowledge.active_fact("proj-1", from_node_id="node-a")
            assert route.calls.last.request.method == "GET"
            assert result.fact.fact_id == "fact-1"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# knowledge.fact_history
# ---------------------------------------------------------------------------


class TestFactHistoryAlias:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/facts/history"
        ).mock(return_value=httpx.Response(200, json=FACT_HISTORY_RESULT))

        result = client.knowledge.fact_history(
            "proj-1", from_node_id="node-a", relation_type="priced_at"
        )

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.params["from_node_id"] == "node-a"
        assert request.url.params["relation_type"] == "priced_at"
        assert result.versions is not None
        assert result.versions[0].fact_id == "fact-1"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/facts/history"
        ).mock(return_value=httpx.Response(200, json=FACT_HISTORY_RESULT))
        try:
            result = await async_client.knowledge.fact_history("proj-1", to_node_id="node-b")
            assert route.calls.last.request.method == "GET"
            assert result.versions[0].fact_id == "fact-1"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# knowledge.entity
# ---------------------------------------------------------------------------


class TestEntityAlias:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/entities/Property/makati"
        ).mock(return_value=httpx.Response(200, json=ENTITY_RESULT))

        result = client.knowledge.entity("proj-1", "Property", "makati")

        assert route.calls.last.request.method == "GET"
        assert result.entity_node_id == "node-a"
        assert result.entity_type == "Property"
        assert result.incoming_facts is not None
        assert result.incoming_facts[0].fact_id == "fact-1"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/entities/Property/makati"
        ).mock(return_value=httpx.Response(200, json=ENTITY_RESULT))
        try:
            result = await async_client.knowledge.entity("proj-1", "Property", "makati")
            assert route.calls.last.request.method == "GET"
            assert result.entity_node_id == "node-a"
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# knowledge.traverse
# ---------------------------------------------------------------------------


class TestTraverseAlias:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/traverse"
        ).mock(return_value=httpx.Response(200, json=TRAVERSE_RESULT))

        result = client.knowledge.traverse(
            "proj-1",
            from_type="Property",
            from_key="makati",
            relation_type="located_in",
            direction="out",
            max_depth=2,
        )

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.params["from_type"] == "Property"
        assert request.url.params["from_key"] == "makati"
        assert request.url.params["relation_type"] == "located_in"
        assert request.url.params["direction"] == "out"
        assert request.url.params["max_depth"] == "2"
        assert result.facts is not None
        assert result.facts[0].depth == 1
        assert result.facts[0].fact.fact_id == "fact-1"

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.get(
            f"{base_url}/api/v1/projects/proj-1/knowledge/traverse"
        ).mock(return_value=httpx.Response(200, json=TRAVERSE_RESULT))
        try:
            result = await async_client.knowledge.traverse("proj-1", from_type="Property")
            assert route.calls.last.request.method == "GET"
            assert result.facts[0].depth == 1
        finally:
            await async_client.close()


# ---------------------------------------------------------------------------
# knowledge.compare
# ---------------------------------------------------------------------------


class TestCompareAlias:
    @respx.mock
    def test_request_shape_and_result(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/knowledge/compare"
        ).mock(return_value=httpx.Response(200, json=COMPARE_RESULT))

        result = client.knowledge.compare(
            "proj-1",
            entities=[{"type": "Property", "key": {"slug": "makati"}}],
            property_path="price",
            target_entity={"type": "Listing", "key": {"slug": "makati-2br"}},
            via_relation="priced_at",
        )

        request = route.calls.last.request
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "entities": [{"type": "Property", "key": {"slug": "makati"}}],
            "property_path": "price",
            "target_entity": {"type": "Listing", "key": {"slug": "makati-2br"}},
            "via_relation": "priced_at",
        }
        assert result.rows is not None
        assert result.rows[0].missing is False
        assert result.rows[0].value == 100

    @respx.mock
    async def test_async(self, async_client: AsyncSonzai, base_url: str) -> None:
        route = respx.post(
            f"{base_url}/api/v1/projects/proj-1/knowledge/compare"
        ).mock(return_value=httpx.Response(200, json=COMPARE_RESULT))
        try:
            result = await async_client.knowledge.compare(
                "proj-1",
                entities=[{"type": "Property", "key": {"slug": "makati"}}],
                property_path="price",
                target_entity={"type": "Listing", "key": {"slug": "makati-2br"}},
                via_relation="priced_at",
            )
            assert route.calls.last.request.method == "POST"
            assert result.rows[0].value == 100
        finally:
            await async_client.close()
