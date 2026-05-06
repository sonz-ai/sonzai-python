"""Tests for SSE chunked-payload producer and consumer."""

from __future__ import annotations

import json

import httpx
import respx

from sonzai import DEFAULT_MAX_CHUNK_SIZE, AsyncSonzai, Sonzai, chunk_payload
from sonzai._http import _parse_sse_stream

# ---------------------------------------------------------------------------
# Producer: chunk_payload
# ---------------------------------------------------------------------------


class TestChunkPayloadSmall:
    """Payloads that fit in a single frame should NOT be chunked."""

    def test_single_frame_no_envelope(self) -> None:
        payload = {"msg": "hello"}
        frames = chunk_payload(payload)
        assert len(frames) == 1
        # Must be a plain data: line — no __chunk wrapper
        data = json.loads(frames[0].removeprefix("data: ").strip())
        assert "__chunk" not in data
        assert data == payload

    def test_single_frame_format(self) -> None:
        frames = chunk_payload({"x": 1})
        assert frames[0].startswith("data: ")
        assert frames[0].endswith("\n\n")

    def test_exact_boundary_no_chunk(self) -> None:
        """A payload whose JSON is exactly max_chunk_size bytes stays in one frame."""
        target = 64
        # {"k":"..."} with compact separators is 8 chars of overhead ({"k":""})
        filler = "x" * (target - 8)
        payload = {"k": filler}
        raw = json.dumps(payload, separators=(",", ":"))
        assert len(raw.encode("utf-8")) == target
        frames = chunk_payload(payload, max_chunk_size=target)
        assert len(frames) == 1


class TestChunkPayloadLarge:
    """Payloads exceeding the threshold must be split into chunk-enveloped frames."""

    def test_multiple_chunks_produced(self) -> None:
        # Use a tiny threshold so even a small dict triggers chunking
        payload = {"key": "A" * 200}
        frames = chunk_payload(payload, max_chunk_size=64)
        assert len(frames) > 1

    def test_chunk_envelope_structure(self) -> None:
        payload = {"key": "B" * 200}
        frames = chunk_payload(payload, max_chunk_size=64)
        for i, frame in enumerate(frames):
            data = json.loads(frame.removeprefix("data: ").strip())
            assert "__chunk" in data
            assert data["__chunk"]["index"] == i
            assert data["__chunk"]["total"] == len(frames)
            assert "data" in data

    def test_indices_contiguous(self) -> None:
        payload = {"key": "C" * 500}
        frames = chunk_payload(payload, max_chunk_size=64)
        indices = [json.loads(f.removeprefix("data: ").strip())["__chunk"]["index"] for f in frames]
        assert indices == list(range(len(frames)))

    def test_default_threshold_is_256k(self) -> None:
        assert DEFAULT_MAX_CHUNK_SIZE == 256 * 1024


# ---------------------------------------------------------------------------
# Roundtrip: chunk_payload -> _parse_sse_stream reassembly
# ---------------------------------------------------------------------------


class TestChunkRoundtrip:
    def test_small_payload_roundtrip(self) -> None:
        payload = {"hello": "world", "n": 42}
        frames = chunk_payload(payload)
        # Simulate the raw SSE lines that _parse_sse_stream expects
        lines = [line for frame in frames for line in frame.strip().split("\n") if line]
        results = list(_parse_sse_stream(iter(lines)))
        assert len(results) == 1
        assert results[0] == payload

    def test_large_payload_roundtrip(self) -> None:
        payload = {"big": "X" * 1000, "nested": {"a": list(range(50))}}
        frames = chunk_payload(payload, max_chunk_size=128)
        assert len(frames) > 1  # sanity: actually chunked
        lines = [line for frame in frames for line in frame.strip().split("\n") if line]
        results = list(_parse_sse_stream(iter(lines)))
        assert len(results) == 1
        assert results[0] == payload

    def test_roundtrip_preserves_unicode(self) -> None:
        payload = {"emoji": "\U0001f600\U0001f389", "cjk": "你好"}
        frames = chunk_payload(payload, max_chunk_size=32)
        lines = [line for frame in frames for line in frame.strip().split("\n") if line]
        results = list(_parse_sse_stream(iter(lines)))
        assert len(results) == 1
        assert results[0] == payload


# ---------------------------------------------------------------------------
# Consumer: _parse_sse_stream with chunked events
# ---------------------------------------------------------------------------


class TestParseSSEStreamChunked:
    def _make_chunk_lines(
        self, payload: dict, *, max_chunk_size: int = 64
    ) -> list[str]:
        """Build raw SSE lines (without trailing blank lines) from a payload."""
        frames = chunk_payload(payload, max_chunk_size=max_chunk_size)
        return [line for frame in frames for line in frame.strip().split("\n") if line]

    def test_chunked_reassembly(self) -> None:
        payload = {"data": "Z" * 300}
        lines = self._make_chunk_lines(payload)
        results = list(_parse_sse_stream(iter(lines)))
        assert results == [payload]

    def test_non_chunked_passthrough(self) -> None:
        """A normal SSE event without __chunk is yielded as-is."""
        lines = ['data: {"foo":"bar"}']
        results = list(_parse_sse_stream(iter(lines)))
        assert results == [{"foo": "bar"}]

    def test_done_sentinel_stops(self) -> None:
        lines = ['data: {"a":1}', "data: [DONE]", 'data: {"b":2}']
        results = list(_parse_sse_stream(iter(lines)))
        assert results == [{"a": 1}]

    def test_malformed_line_skipped(self) -> None:
        lines = ["data: {bad-json", 'data: {"ok":true}']
        results = list(_parse_sse_stream(iter(lines)))
        assert results == [{"ok": True}]


# ---------------------------------------------------------------------------
# Mixed chunked + normal events
# ---------------------------------------------------------------------------


class TestMixedEvents:
    def test_normal_then_chunked_then_normal(self) -> None:
        """Interleaved normal and chunked events should all be delivered."""
        normal1 = 'data: {"type":"delta","content":"Hi"}'
        # A chunked event
        big_payload = {"type": "context_ready", "data": "Y" * 400}
        chunk_frames = chunk_payload(big_payload, max_chunk_size=128)
        chunk_lines = [
            line
            for frame in chunk_frames
            for line in frame.strip().split("\n")
            if line
        ]
        normal2 = 'data: {"type":"delta","content":"!"}'

        all_lines = [normal1] + chunk_lines + [normal2]
        results = list(_parse_sse_stream(iter(all_lines)))

        assert len(results) == 3
        assert results[0] == {"type": "delta", "content": "Hi"}
        assert results[1] == big_payload
        assert results[2] == {"type": "delta", "content": "!"}

    def test_multiple_chunked_sequences(self) -> None:
        """Two consecutive chunked payloads should each reassemble independently."""
        p1 = {"seq": 1, "val": "A" * 200}
        p2 = {"seq": 2, "val": "B" * 200}

        lines: list[str] = []
        for payload in (p1, p2):
            frames = chunk_payload(payload, max_chunk_size=64)
            for frame in frames:
                for line in frame.strip().split("\n"):
                    if line:
                        lines.append(line)

        results = list(_parse_sse_stream(iter(lines)))
        assert len(results) == 2
        assert results[0] == p1
        assert results[1] == p2


# ---------------------------------------------------------------------------
# Sync HTTPClient.stream_sse — end-to-end with respx
# ---------------------------------------------------------------------------


class TestSyncStreamSSEChunked:
    @respx.mock
    def test_chunked_events_reassembled(self) -> None:
        base_url = "https://api.test.sonz.ai"
        payload = {"type": "context_ready", "ctx": "Q" * 500}
        frames = chunk_payload(payload, max_chunk_size=128)
        sse_body = "".join(frames) + "data: [DONE]\n\n"

        respx.post(f"{base_url}/api/v1/agents/a1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        client = Sonzai(api_key="test-key", base_url=base_url)
        try:
            events = list(
                client._http.stream_sse("POST", "/api/v1/agents/a1/chat")
            )
            assert len(events) == 1
            assert events[0] == payload
        finally:
            client.close()

    @respx.mock
    def test_mixed_normal_and_chunked(self) -> None:
        base_url = "https://api.test.sonz.ai"

        normal_event = '{"choices":[{"delta":{"content":"Hi"}}]}'
        big_payload = {"type": "context_ready", "data": "R" * 400}
        chunk_frames = chunk_payload(big_payload, max_chunk_size=128)

        sse_body = f"data: {normal_event}\n\n"
        sse_body += "".join(chunk_frames)
        sse_body += "data: [DONE]\n\n"

        respx.post(f"{base_url}/api/v1/agents/a1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        client = Sonzai(api_key="test-key", base_url=base_url)
        try:
            events = list(
                client._http.stream_sse("POST", "/api/v1/agents/a1/chat")
            )
            assert len(events) == 2
            assert events[0] == json.loads(normal_event)
            assert events[1] == big_payload
        finally:
            client.close()


# ---------------------------------------------------------------------------
# Async AsyncHTTPClient.stream_sse — end-to-end with respx
# ---------------------------------------------------------------------------


class TestAsyncStreamSSEChunked:
    @respx.mock
    async def test_async_chunked_events_reassembled(self) -> None:
        base_url = "https://api.test.sonz.ai"
        payload = {"type": "side_effects", "data": {"facts": ["W" * 300]}}
        frames = chunk_payload(payload, max_chunk_size=128)
        sse_body = "".join(frames) + "data: [DONE]\n\n"

        respx.post(f"{base_url}/api/v1/agents/a1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            events: list[dict] = []
            async for event in client._http.stream_sse(
                "POST", "/api/v1/agents/a1/chat"
            ):
                events.append(event)
            assert len(events) == 1
            assert events[0] == payload
        finally:
            await client.close()

    @respx.mock
    async def test_async_mixed_normal_and_chunked(self) -> None:
        base_url = "https://api.test.sonz.ai"

        delta = '{"choices":[{"delta":{"content":"yo"}}]}'
        big = {"type": "context_ready", "blob": "S" * 600}
        chunk_frames = chunk_payload(big, max_chunk_size=128)

        sse_body = f"data: {delta}\n\n"
        sse_body += "".join(chunk_frames)
        sse_body += f"data: {delta}\n\n"
        sse_body += "data: [DONE]\n\n"

        respx.post(f"{base_url}/api/v1/agents/a1/chat").mock(
            return_value=httpx.Response(
                200,
                content=sse_body,
                headers={"content-type": "text/event-stream"},
            )
        )

        client = AsyncSonzai(api_key="test-key", base_url=base_url)
        try:
            events: list[dict] = []
            async for event in client._http.stream_sse(
                "POST", "/api/v1/agents/a1/chat"
            ):
                events.append(event)
            assert len(events) == 3
            assert events[0] == json.loads(delta)
            assert events[1] == big
            assert events[2] == json.loads(delta)
        finally:
            await client.close()
