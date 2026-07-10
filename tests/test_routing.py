from __future__ import annotations

import httpx

from sonzai import AsyncSonzai, Sonzai

CONFIG = {
    "tiers": [],
    "guide_agent": {
        "agent_id": "guide-1",
        "agent_name": "Guide",
        "criteria": [],
        "questions": [],
    },
    "handoffs": [],
    "channel_bindings": [],
}


def test_routing_put_config() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/projects/project-1/routing-config"
        assert request.method == "PUT"
        return httpx.Response(200, json=CONFIG, request=request)

    with httpx.Client(
        transport=httpx.MockTransport(handler), base_url="https://api.test"
    ) as http_client:
        client = Sonzai(api_key="test", base_url="https://api.test", http_client=http_client)
        got = client.routing.put_config("project-1", CONFIG)
        assert got.guide_agent.agent_id == "guide-1"


async def test_async_routing_list_permanent_routes() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/projects/project-1/permanent-routes"
        return httpx.Response(200, json={"routes": [], "total": 0}, request=request)

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://api.test"
    ) as http_client:
        client = AsyncSonzai(api_key="test", base_url="https://api.test", http_client=http_client)
        got = await client.routing.list_permanent_routes("project-1")
        assert got.total == 0
