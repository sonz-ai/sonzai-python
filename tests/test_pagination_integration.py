"""Integration tests for Page[T] against real resource methods."""
from __future__ import annotations

import httpx
import pytest
import respx

from sonzai import AsyncPage, AsyncSonzai, Page, Sonzai

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_USER_FIXTURE = {"user_id": "u0", "role": "user"}

_AGENT_INDEX_FIXTURE = {
    "agent_id": "ag1",
    "name": "Agent One",
    "tenant_id": "t1",
    "owner_user_id": "u1",
    "is_active": True,
    "instance_count": 0,
    "created_at": "2026-01-01T00:00:00Z",
}

_EVAL_RUN_FIXTURE = {
    "run_id": "r1",
    "agent_id": "ag1",
    "agent_name": "Agent One",
    "status": "completed",
    "character_config": {},
    "template_id": "tpl-1",
    "template_snapshot": {},
    "simulation_config": {},
    "simulation_model": "gpt-4",
    "user_persona": {},
    "transcript": [],
    "evaluation_result": {},
    "adaptation_result": {},
    "simulation_state": {},
    "total_sessions": 1,
    "total_turns": 10,
    "simulated_minutes": 15,
    "total_cost_usd": 0.1,
    "simulation_cost_usd": 0.06,
    "evaluation_cost_usd": 0.04,
    "adaptation_template_id": "adapt-1",
    "adaptation_template_snapshot": None,
    "started_at": "2026-01-01T00:00:00Z",
    "created_at": "2026-01-01T00:00:00Z",
    "completed_at": None,
}

_TICKET_FIXTURE = {
    "ticket_id": "t1",
    "title": "Login issue",
    "type": "support",
    "status": "open",
    "priority": "medium",
    "created_by_email": "user@example.com",
    "comment_count": 0,
    "created_at": "2026-04-21T10:00:00Z",
    "updated_at": "2026-04-21T10:00:00Z",
}

_WEBHOOK_ATTEMPT_FIXTURE = {
    "attempt_id": "a1",
    "attempt_number": 1,
    "created_at": "2026-01-01T00:00:00Z",
    "duration_ms": 150,
    "event_type": "agent.message",
    "project_id": "p1",
    "response_code": 200,
    "status": "success",
    "webhook_url": "https://example.com/hook",
}

_KB_NODE_FIXTURE = {
    "node_id": "n1",
    "label": "Node One",
    "node_type": "entity",
    "project_id": "p1",
    "confidence": 0.9,
    "is_active": True,
    "norm_label": "node one",
    "properties": {},
    "source_docs": [],
    "source_type": "manual",
    "version": 1,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z",
}

_INVENTORY_GROUP_FIXTURE = {
    "group": "weapons",
    "values": {"count": 3},
}


# ---------------------------------------------------------------------------
# Sync tests
# ---------------------------------------------------------------------------


class TestAgentsListUsersPagination:
    def test_list_users_iterates_across_pages(self) -> None:
        page1_users = [
            {"user_id": f"u{i}", "role": "user"} for i in range(100)
        ]
        page2_users = [
            {"user_id": "u100", "role": "user"},
            {"user_id": "u101", "role": "user"},
        ]
        with respx.mock() as router:
            route = router.get("https://api.sonz.ai/api/v1/agents/a1/users")
            route.side_effect = [
                httpx.Response(200, json={"users": page1_users, "total": 102}),
                httpx.Response(200, json={"users": page2_users, "total": 102}),
            ]
            client = Sonzai(api_key="test-key")
            try:
                page = client.agents.get_users(agent_id="a1", limit=100)
                assert isinstance(page, Page)
                users = page.to_list()
                assert len(users) == 102
                assert page.total == 102
                assert users[0].user_id == "u0"
                assert users[100].user_id == "u100"
            finally:
                client.close()

    def test_list_users_single_page(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/agents/a1/users").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "users": [
                            {"user_id": "u1", "role": "user"},
                            {"user_id": "u2", "role": "user"},
                        ],
                        "total": 2,
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.agents.get_users(agent_id="a1", limit=100)
                assert isinstance(page, Page)
                users = page.to_list()
                assert len(users) == 2
                assert page.total == 2
            finally:
                client.close()


class TestAgentsListPagination:
    def test_list_agents_returns_page(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/agents").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "items": [_AGENT_INDEX_FIXTURE],
                        "has_more": False,
                        "total_count": 1,
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.agents.list(limit=100)
                assert isinstance(page, Page)
                agents = page.to_list()
                assert len(agents) == 1
                assert agents[0].agent_id == "ag1"
            finally:
                client.close()


class TestEvalRunsListPagination:
    def test_list_eval_runs_returns_page(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/eval-runs").mock(
                return_value=httpx.Response(
                    200,
                    json={"runs": [_EVAL_RUN_FIXTURE], "total_count": 1},
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.eval_runs.list(limit=100)
                assert isinstance(page, Page)
                runs = page.to_list()
                assert len(runs) == 1
                assert runs[0].run_id == "r1"
                assert runs[0].status == "completed"
            finally:
                client.close()


class TestSupportListTicketsPagination:
    def test_list_tickets_returns_page(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/support/tickets").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "tickets": [_TICKET_FIXTURE],
                        "total": 1,
                        "has_more": False,
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.support.list_tickets(limit=100)
                assert isinstance(page, Page)
                tickets = page.to_list()
                assert len(tickets) == 1
                assert page.total == 1
                assert tickets[0].ticket_id == "t1"
            finally:
                client.close()


class TestWebhooksListDeliveryAttemptsPagination:
    def test_list_delivery_attempts_returns_page(self) -> None:
        with respx.mock() as router:
            router.get(
                "https://api.sonz.ai/api/v1/webhooks/agent.message/attempts"
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={"attempts": [_WEBHOOK_ATTEMPT_FIXTURE]},
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.webhooks.list_delivery_attempts(
                    "agent.message", limit=100
                )
                assert isinstance(page, Page)
                attempts = page.to_list()
                assert len(attempts) == 1
                assert attempts[0].attempt_id == "a1"
            finally:
                client.close()

    def test_list_delivery_attempts_for_project_returns_page(self) -> None:
        with respx.mock() as router:
            router.get(
                "https://api.sonz.ai/api/v1/projects/p1/webhooks/agent.message/attempts"
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={"attempts": [_WEBHOOK_ATTEMPT_FIXTURE]},
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.webhooks.list_delivery_attempts_for_project(
                    "p1", "agent.message", limit=100
                )
                assert isinstance(page, Page)
                attempts = page.to_list()
                assert len(attempts) == 1
                assert attempts[0].status == "success"
            finally:
                client.close()


class TestKnowledgeListNodesPagination:
    def test_list_nodes_returns_page(self) -> None:
        with respx.mock() as router:
            router.get(
                "https://api.sonz.ai/api/v1/projects/p1/knowledge/nodes"
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "nodes": [_KB_NODE_FIXTURE],
                        "total": 1,
                        "next_cursor": "",
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.knowledge.list_nodes("p1", limit=100)
                assert isinstance(page, Page)
                nodes = page.to_list()
                assert len(nodes) == 1
                assert page.total == 1
                assert nodes[0].node_id == "n1"
            finally:
                client.close()


class TestInventoryQueryPagination:
    def test_query_returns_page(self) -> None:
        with respx.mock() as router:
            router.get(
                "https://api.sonz.ai/api/v1/agents/ag1/users/u1/inventory"
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "groups": [_INVENTORY_GROUP_FIXTURE],
                        "items": [],
                        "total_items": 3,
                        "next_cursor": "",
                        "totals": {},
                    },
                )
            )
            client = Sonzai(api_key="test-key")
            try:
                page = client.agents.inventory.query(
                    "ag1", "u1", limit=100
                )
                assert isinstance(page, Page)
                groups = page.to_list()
                assert len(groups) == 1
                assert groups[0].group == "weapons"
            finally:
                client.close()


# ---------------------------------------------------------------------------
# Async tests
# ---------------------------------------------------------------------------


class TestAsyncPagination:
    @pytest.mark.asyncio
    async def test_async_list_users_iterates_across_pages(self) -> None:
        page1_users = [
            {"user_id": f"u{i}", "role": "user"} for i in range(100)
        ]
        page2_users = [
            {"user_id": "u100", "role": "user"},
            {"user_id": "u101", "role": "user"},
        ]
        with respx.mock() as router:
            route = router.get("https://api.sonz.ai/api/v1/agents/a1/users")
            route.side_effect = [
                httpx.Response(200, json={"users": page1_users, "total": 102}),
                httpx.Response(200, json={"users": page2_users, "total": 102}),
            ]
            client = AsyncSonzai(api_key="test-key")
            try:
                page = await client.agents.get_users(agent_id="a1", limit=100)
                assert isinstance(page, AsyncPage)
                users = await page.to_list()
                assert len(users) == 102
                assert page.total == 102
            finally:
                await client.close()

    @pytest.mark.asyncio
    async def test_async_eval_runs_list_returns_page(self) -> None:
        with respx.mock() as router:
            router.get("https://api.sonz.ai/api/v1/eval-runs").mock(
                return_value=httpx.Response(
                    200,
                    json={"runs": [_EVAL_RUN_FIXTURE], "total_count": 1},
                )
            )
            client = AsyncSonzai(api_key="test-key")
            try:
                page = await client.eval_runs.list(limit=100)
                assert isinstance(page, AsyncPage)
                runs = await page.to_list()
                assert len(runs) == 1
                assert runs[0].status == "completed"
            finally:
                await client.close()
