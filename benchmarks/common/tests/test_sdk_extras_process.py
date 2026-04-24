"""Tests for async_process() — the forward-compat shim over POST /process."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from benchmarks.common.sdk_extras import async_process


@pytest.mark.asyncio
async def test_async_process_falls_back_to_raw_transport():
    """When client.process isn't present, go through client._http.post."""
    client = MagicMock()
    client.process = None  # simulate pre-regen SDK
    client._http = MagicMock()
    client._http.post = AsyncMock(
        return_value={"success": True, "facts_extracted": 3, "side_effects": {}}
    )

    resp = await async_process(
        client,
        agent_id="agent-1",
        user_id="user-1",
        messages=[
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ],
        session_id="sess-1",
    )

    client._http.post.assert_awaited_once()
    path, = client._http.post.call_args.args
    kwargs = client._http.post.call_args.kwargs
    assert path == "/api/v1/agents/agent-1/process"
    assert kwargs["json_data"]["userId"] == "user-1"
    assert kwargs["json_data"]["sessionId"] == "sess-1"
    assert len(kwargs["json_data"]["messages"]) == 2
    assert resp["facts_extracted"] == 3


@pytest.mark.asyncio
async def test_async_process_uses_native_binding_when_present():
    client = MagicMock()
    client.process = AsyncMock(return_value={"success": True, "facts_extracted": 1})

    resp = await async_process(
        client,
        agent_id="agent-1",
        user_id="user-1",
        messages=[{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}],
    )

    client.process.assert_awaited_once()
    assert resp["facts_extracted"] == 1


@pytest.mark.asyncio
async def test_async_process_requires_min_2_messages():
    """The server requires >=2 messages; we validate client-side to fail fast."""
    client = MagicMock()
    client.process = None
    client._http = MagicMock()

    with pytest.raises(ValueError, match="at least 2 messages"):
        await async_process(
            client,
            agent_id="agent-1",
            user_id="user-1",
            messages=[{"role": "user", "content": "only one"}],
        )
