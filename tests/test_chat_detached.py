"""Tests for ``chat_detached`` / ``chat_stream_detached`` (sonzai-go parity).

Python port of sonzai-go's detached_test.go. The detached helpers shield
the upstream AI streaming call from caller-task cancellation, so a
short-lived NATS handler / queue worker / asyncio task that cancels mid-
generation does not abort the AI call.

Three contracts:

1. Baseline trap: the regular ``chat`` honours caller cancellation and
   aborts the in-flight request when the caller's task is cancelled.
2. Fix: ``chat_detached`` survives caller cancellation and runs to
   completion. The watchdog logs a warning (or fires the
   ``on_parent_cancel`` callback) when the caller cancels mid-call.
3. No-warning happy path: when the caller's task outlives the call, the
   watchdog must not log spurious warnings.
"""

from __future__ import annotations

import asyncio
import logging

import httpx
import pytest
import respx

from sonzai import DEFAULT_DETACHED_TIMEOUT_SECONDS, AsyncSonzai, DetachOptions


@pytest.fixture
def base_url() -> str:
    return "https://api.test.sonz.ai"


@pytest.fixture
def async_client(base_url: str):
    return AsyncSonzai(api_key="test-key", base_url=base_url)


_SIMPLE_SSE_BODY = (
    'data: {"choices":[{"delta":{"content":"hi"},"finish_reason":"stop","index":0}]}\n\n'
    "data: [DONE]\n\n"
)


# -----------------------------------------------------------------------------
# Module-level smoke tests for the DetachOptions dataclass and helpers.
# -----------------------------------------------------------------------------


class TestDetachOptions:
    def test_default_values(self) -> None:
        opts = DetachOptions()
        assert opts.timeout_seconds is None
        assert opts.logger is None
        assert opts.on_parent_cancel is None

    def test_frozen(self) -> None:
        opts = DetachOptions(timeout_seconds=10.0)
        # frozen=True — mutation must raise.
        with pytest.raises(Exception):  # FrozenInstanceError subclasses AttributeError
            opts.timeout_seconds = 20.0  # type: ignore[misc]

    def test_default_timeout_constant(self) -> None:
        assert DEFAULT_DETACHED_TIMEOUT_SECONDS == 300.0


# -----------------------------------------------------------------------------
# chat_detached — aggregate variant.
# -----------------------------------------------------------------------------


class TestChatDetachedAggregate:
    @pytest.mark.asyncio
    @respx.mock
    async def test_completes_normally_when_parent_lives(
        self, async_client, base_url
    ) -> None:
        """Happy path: caller doesn't cancel, call returns aggregated content."""
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_SIMPLE_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )

        resp = await async_client.agents.chat_detached(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
        )
        assert resp.content == "hi"
        await async_client.close()

    @pytest.mark.asyncio
    @respx.mock
    async def test_no_warning_when_parent_lives(
        self, async_client, base_url, caplog
    ) -> None:
        """Well-behaved caller — no spurious misuse warnings."""
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=_SIMPLE_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )
        )

        with caplog.at_level(logging.WARNING, logger="sonzai._customizations.detached"):
            await async_client.agents.chat_detached(
                "agent-1",
                messages=[{"role": "user", "content": "hi"}],
            )

        # Give the watchdog a tick to observe done_event and exit cleanly.
        await asyncio.sleep(0.05)
        warning_records = [
            r for r in caplog.records if "parent task cancelled" in r.getMessage()
        ]
        assert warning_records == [], f"expected no warnings, got {warning_records}"
        await async_client.close()

    @pytest.mark.asyncio
    @respx.mock
    async def test_survives_caller_cancel(self, async_client, base_url) -> None:
        """The fix: caller task.cancel() does NOT abort the upstream call.

        We start chat_detached inside a child task, cancel the child mid-
        flight, and observe that the upstream HTTP handler is allowed to
        complete (signalled via ``handler_completed``). Without the
        shield, httpx would tear down the connection when the child task
        cancels and the handler would not get to record completion.
        """
        # Hold the response until we release it — simulates a slow LLM.
        release = asyncio.Event()
        handler_entered = asyncio.Event()
        handler_completed = asyncio.Event()

        async def slow_response(request: httpx.Request) -> httpx.Response:
            handler_entered.set()
            await release.wait()
            handler_completed.set()
            return httpx.Response(
                200,
                content=_SIMPLE_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )

        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            side_effect=slow_response
        )

        callback_hits: list[BaseException | None] = []

        async def caller() -> None:
            await async_client.agents.chat_detached(
                "agent-1",
                messages=[{"role": "user", "content": "hi"}],
                on_parent_cancel=lambda exc: callback_hits.append(exc),
                timeout_seconds=10.0,
            )

        child = asyncio.create_task(caller())
        # Wait for the handler to actually run — this is the moment of
        # truth: the request is in flight and parked inside the mock.
        await asyncio.wait_for(handler_entered.wait(), timeout=2.0)

        child.cancel()
        try:
            await child
        except asyncio.CancelledError:
            pass

        # Give the watchdog a tick to observe the cancel and fire the callback.
        await asyncio.sleep(0.05)
        assert callback_hits, "on_parent_cancel should have fired once"
        assert len(callback_hits) == 1

        # The cancelled caller has returned. The handler is still parked.
        # Release the upstream — if the shield works, the handler runs to
        # completion and sets handler_completed even though no one is
        # awaiting the response.
        assert not handler_completed.is_set(), (
            "handler should still be parked at release.wait()"
        )
        release.set()
        # Allow the orphan inner task to finish reading the response.
        await asyncio.wait_for(handler_completed.wait(), timeout=2.0)
        # Give the orphan task a moment to drain the body and tidy up.
        await asyncio.sleep(0.05)
        await async_client.close()

    @pytest.mark.asyncio
    @respx.mock
    async def test_timeout_fires(self, async_client, base_url) -> None:
        """Hard timeout is enforced even though caller cancel is shielded."""
        never_returns = asyncio.Event()

        async def hangs_forever(request: httpx.Request) -> httpx.Response:
            await never_returns.wait()
            return httpx.Response(200, json={})  # pragma: no cover

        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            side_effect=hangs_forever
        )

        with pytest.raises((asyncio.TimeoutError, TimeoutError)):
            await async_client.agents.chat_detached(
                "agent-1",
                messages=[{"role": "user", "content": "hi"}],
                timeout_seconds=0.1,
            )

        # Release the mock so it can be torn down cleanly.
        never_returns.set()
        await asyncio.sleep(0.05)
        await async_client.close()


# -----------------------------------------------------------------------------
# chat_stream_detached — streaming variant.
# -----------------------------------------------------------------------------


class TestChatStreamDetached:
    @pytest.mark.asyncio
    @respx.mock
    async def test_yields_events(self, async_client, base_url) -> None:
        sse_body = (
            'data: {"choices":[{"delta":{"content":"hel"},"finish_reason":null,"index":0}]}\n\n'
            'data: {"choices":[{"delta":{"content":"lo"},"finish_reason":"stop","index":0}]}\n\n'
            "data: [DONE]\n\n"
        )
        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        events = []
        async for event in async_client.agents.chat_stream_detached(
            "agent-1",
            messages=[{"role": "user", "content": "hi"}],
        ):
            events.append(event)

        assert [e.content for e in events] == ["hel", "lo"]
        await async_client.close()


# -----------------------------------------------------------------------------
# Watchdog warning emission.
# -----------------------------------------------------------------------------


class TestWatchdogWarning:
    @pytest.mark.asyncio
    @respx.mock
    async def test_warning_logged_when_parent_cancelled(
        self, async_client, base_url, caplog
    ) -> None:
        """No callback supplied → watchdog logs a warning."""
        release = asyncio.Event()
        handler_entered = asyncio.Event()

        async def slow_response(request: httpx.Request) -> httpx.Response:
            handler_entered.set()
            await release.wait()
            return httpx.Response(
                200,
                content=_SIMPLE_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )

        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            side_effect=slow_response
        )

        async def caller() -> None:
            await async_client.agents.chat_detached(
                "agent-1",
                messages=[{"role": "user", "content": "hi"}],
                timeout_seconds=10.0,
            )

        with caplog.at_level(logging.WARNING, logger="sonzai._customizations.detached"):
            child = asyncio.create_task(caller())
            await asyncio.wait_for(handler_entered.wait(), timeout=2.0)
            child.cancel()
            try:
                await child
            except asyncio.CancelledError:
                pass
            # Give the watchdog a tick.
            await asyncio.sleep(0.05)

        assert any(
            "parent task cancelled" in r.getMessage() for r in caplog.records
        ), f"expected parent-cancel warning, got: {[r.getMessage() for r in caplog.records]}"

        release.set()
        await asyncio.sleep(0.1)
        await async_client.close()

    @pytest.mark.asyncio
    @respx.mock
    async def test_callback_overrides_warning(
        self, async_client, base_url, caplog
    ) -> None:
        """When on_parent_cancel is set, no log warning is emitted."""
        release = asyncio.Event()
        handler_entered = asyncio.Event()

        async def slow_response(request: httpx.Request) -> httpx.Response:
            handler_entered.set()
            await release.wait()
            return httpx.Response(
                200,
                content=_SIMPLE_SSE_BODY,
                headers={"content-type": "text/event-stream"},
            )

        respx.post(f"{base_url}/api/v1/agents/agent-1/chat").mock(
            side_effect=slow_response
        )

        hits = 0

        def cb(exc: BaseException | None) -> None:
            nonlocal hits
            hits += 1

        async def caller() -> None:
            await async_client.agents.chat_detached(
                "agent-1",
                messages=[{"role": "user", "content": "hi"}],
                on_parent_cancel=cb,
                timeout_seconds=10.0,
            )

        with caplog.at_level(logging.WARNING, logger="sonzai._customizations.detached"):
            child = asyncio.create_task(caller())
            await asyncio.wait_for(handler_entered.wait(), timeout=2.0)
            child.cancel()
            try:
                await child
            except asyncio.CancelledError:
                pass
            await asyncio.sleep(0.05)

        assert hits == 1, f"expected callback to fire once, got {hits}"
        warning_records = [
            r for r in caplog.records if "parent task cancelled" in r.getMessage()
        ]
        assert warning_records == [], "callback path should suppress the log warning"

        release.set()
        await asyncio.sleep(0.1)
        await async_client.close()


# -----------------------------------------------------------------------------
# Sync parity surface — delegates to the cancellation-honouring path but
# the API symbol must exist so callers can write provider-neutral code.
# -----------------------------------------------------------------------------


class TestSyncParitySurface:
    def test_sync_chat_detached_exists(self) -> None:
        from sonzai.resources.agents import Agents

        assert hasattr(Agents, "chat_detached")
        assert hasattr(Agents, "chat_stream_detached")
