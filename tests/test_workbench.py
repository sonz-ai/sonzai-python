"""Tests for the Workbench resource — especially ``advance_time`` which the
benchmark suite relies on. Confirms:

- The sync and async clients expose ``workbench.advance_time`` with the
  documented keyword-argument signature.
- The request body matches the shape declared by the Go handler
  (``agent_id``, ``user_id``, ``simulated_hours``, ``simulated_base_offset_hours``,
  ``character_config``, ``instance_id``).
- The response parses into :class:`sonzai.types.AdvanceTimeResponse`.
"""

from __future__ import annotations

import json

import httpx
import pytest
import respx

from sonzai import AsyncSonzai, Sonzai
from sonzai.types import AdvanceTimeResponse


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


SAMPLE_RESPONSE = {
    "days_processed": 1,
    "consolidation_ran": True,
    "weekly_consolidations": 0,
    "diary_entries_created": 1,
    "diary_entries": [
        {
            "date": "2026-04-21",
            "content": "Learned about Rust.",
            "mood": "curious",
            "topics": ["rust"],
        }
    ],
    "wakeups_executed": [
        {
            "wakeup_id": "w-1",
            "check_type": "followup",
            "intent": "ask about the trip",
            "user_id": "bench-user",
            "agent_id": "agent-123",
            "generated_message": "Hey, how was the trip?",
        }
    ],
    "consolidation_processed": 3,
}


class TestAdvanceTime:
    @respx.mock
    def test_advance_time_request_body_shape(self, client: Sonzai, base_url: str) -> None:
        route = respx.post(f"{base_url}/api/v1/workbench/advance-time").mock(
            return_value=httpx.Response(200, json=SAMPLE_RESPONSE)
        )

        resp = client.workbench.advance_time(
            agent_id="agent-123",
            user_id="bench-user",
            simulated_hours=25.0,
        )

        assert route.called
        sent = json.loads(route.calls.last.request.content)
        # Hand-handler-driven shape — the benchmark depends on exactly these keys.
        assert sent["agent_id"] == "agent-123"
        assert sent["user_id"] == "bench-user"
        assert sent["simulated_hours"] == 25.0
        assert sent["simulated_base_offset_hours"] == 0.0
        # character_config and instance_id must be present even when omitted.
        assert sent["character_config"] == {}
        assert sent["instance_id"] == ""

        assert isinstance(resp, AdvanceTimeResponse)
        assert resp.days_processed == 1
        assert resp.consolidation_ran is True
        assert resp.consolidation_processed == 3
        assert len(resp.diary_entries) == 1
        assert resp.diary_entries[0].content == "Learned about Rust."
        assert len(resp.wakeups_executed) == 1
        assert resp.wakeups_executed[0].generated_message == "Hey, how was the trip?"

    @respx.mock
    def test_advance_time_passes_optional_kwargs(
        self, client: Sonzai, base_url: str
    ) -> None:
        route = respx.post(f"{base_url}/api/v1/workbench/advance-time").mock(
            return_value=httpx.Response(200, json=SAMPLE_RESPONSE)
        )

        client.workbench.advance_time(
            agent_id="agent-123",
            user_id="bench-user",
            simulated_hours=12.5,
            simulated_base_offset_hours=12.0,
            instance_id="inst-7",
            character_config={"name": "Luna"},
        )

        assert route.called
        sent = json.loads(route.calls.last.request.content)
        assert sent["simulated_base_offset_hours"] == 12.0
        assert sent["instance_id"] == "inst-7"
        assert sent["character_config"] == {"name": "Luna"}

    @respx.mock
    async def test_advance_time_async(
        self, async_client: AsyncSonzai, base_url: str
    ) -> None:
        route = respx.post(f"{base_url}/api/v1/workbench/advance-time").mock(
            return_value=httpx.Response(200, json=SAMPLE_RESPONSE)
        )

        resp = await async_client.workbench.advance_time(
            agent_id="agent-123",
            user_id="bench-user",
            simulated_hours=25.0,
        )
        await async_client.close()

        assert route.called
        assert isinstance(resp, AdvanceTimeResponse)
        assert resp.diary_entries_created == 1


class TestWorkbenchWiredUp:
    """Confirm the new resource is wired on the client (class-level attr type)."""

    def test_sync_client_exposes_workbench(self, client: Sonzai) -> None:
        assert client.workbench is not None
        # Compile-time check: the documented signature is present.
        assert callable(client.workbench.advance_time)

    def test_async_client_exposes_workbench(
        self, async_client: AsyncSonzai
    ) -> None:
        assert async_client.workbench is not None
        assert callable(async_client.workbench.advance_time)
