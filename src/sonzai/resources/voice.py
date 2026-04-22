"""Voice resource for the Sonzai SDK."""

from __future__ import annotations

import asyncio
import json as _json
import struct
from typing import Any, Iterator

from .._generated.models import (
    SpeechToTextInputBody,
    TextToSpeechInputBody,
    VoiceLiveWSTokenInputBody,
)
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import (
    VoiceListResponse,
    VoiceStreamEvent,
    VoiceStreamToken,
    TTSResponse,
    STTResponse,
)


class VoiceResource:
    """Sync per-agent voice live operations (duplex WebSocket streaming via Gemini Live)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get_token(
        self,
        agent_id: str,
        *,
        voice_name: str | None = None,
        language: str | None = None,
        user_id: str | None = None,
        compiled_system_prompt: str | None = None,
    ) -> VoiceStreamToken:
        """Get a short-lived token for voice live WebSocket streaming.

        The token expires in 60 seconds and is single-use.
        """
        raw: dict[str, Any] = {}
        if voice_name is not None:
            raw["voice_name"] = voice_name
        if language is not None:
            raw["language"] = language
        if user_id is not None:
            raw["user_id"] = user_id
        if compiled_system_prompt is not None:
            raw["compiled_system_prompt"] = compiled_system_prompt
        body = encode_body(VoiceLiveWSTokenInputBody, raw)

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/live-ws-token", json_data=body
        )
        return VoiceStreamToken.model_validate(data)

    def stream(self, token: VoiceStreamToken) -> VoiceStream:
        """Open a bidirectional WebSocket for real-time voice chat via Gemini Live.

        Usage::

            token = client.agents.voice.get_token(agent_id)
            stream = client.agents.voice.stream(token)

            # Send PCM audio chunks (16kHz, 16-bit, mono)
            stream.send_audio(audio_bytes)

            # Or send text input instead of audio
            stream.send_text("Hello!")

            for event in stream:
                if event.type == "input_transcript":
                    print("User:", event.text)
                elif event.type == "output_transcript":
                    print("Agent:", event.text)
                elif event.type == "audio":
                    play_pcm_audio(event.audio)  # 24kHz PCM
                elif event.type == "session_ended":
                    break

            stream.close()
        """
        return VoiceStream(token)

    def tts(
        self,
        agent_id: str,
        *,
        text: str,
        voice_name: str | None = None,
        language: str | None = None,
        output_format: str | None = None,
    ) -> TTSResponse:
        """Convert text to speech audio.

        Returns a :class:`TTSResponse` with base64-encoded audio data.
        """
        raw: dict[str, Any] = {"text": text}
        if voice_name is not None:
            raw["voice_name"] = voice_name
        if language is not None:
            raw["language"] = language
        if output_format is not None:
            raw["output_format"] = output_format
        body = encode_body(TextToSpeechInputBody, raw)

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/tts", json_data=body
        )
        return TTSResponse.model_validate(data)

    def stt(
        self,
        agent_id: str,
        *,
        audio: str,
        audio_format: str,
        language: str | None = None,
    ) -> STTResponse:
        """Transcribe audio to text.

        Returns a :class:`STTResponse` with the transcript.
        """
        raw: dict[str, Any] = {"audio": audio, "audio_format": audio_format}
        if language is not None:
            raw["language"] = language
        body = encode_body(SpeechToTextInputBody, raw)

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/stt", json_data=body
        )
        return STTResponse.model_validate(data)


class VoiceStream:
    """Bidirectional WebSocket connection for real-time voice chat.

    Implements ``__iter__`` so you can iterate over incoming events.
    Uses the stdlib ``socket`` + minimal WebSocket framing to avoid
    requiring a third-party WebSocket dependency.
    """

    def __init__(self, token: VoiceStreamToken) -> None:
        import socket as _socket
        import ssl as _ssl
        from urllib.parse import urlparse

        parsed = urlparse(token.ws_url)
        host = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "wss" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"

        raw = _socket.create_connection((host, port), timeout=10)
        # Any failure below must close the socket (or the TLS wrapper around it)
        # — otherwise a raised ConnectionError leaks an open file descriptor, and
        # long-running callers eventually exhaust the process's fd limit.
        sock: _socket.socket | None = None
        try:
            if parsed.scheme == "wss":
                ctx = _ssl.create_default_context()
                sock = ctx.wrap_socket(raw, server_hostname=host)
            else:
                sock = raw
            self._sock: _socket.socket = sock

            # WebSocket handshake
            import base64
            import os

            key = base64.b64encode(os.urandom(16)).decode()
            handshake = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                f"Sec-WebSocket-Version: 13\r\n"
                f"\r\n"
            )
            self._sock.sendall(handshake.encode())

            # Read handshake response
            response = b""
            while b"\r\n\r\n" not in response:
                chunk = self._sock.recv(4096)
                if not chunk:
                    raise ConnectionError("WebSocket handshake failed: connection closed")
                response += chunk

            if b"101" not in response.split(b"\r\n")[0]:
                raise ConnectionError(f"WebSocket handshake failed: {response.split(b'\r\n')[0]!r}")

            self._closed = False

            # Send auth token as first text message
            self._send_text(token.auth_token)
        except BaseException:
            # Close whichever socket we ended up holding. If ssl.wrap_socket
            # itself raised, `sock` is None — fall back to the raw socket.
            target = sock if sock is not None else raw
            try:
                target.close()
            except Exception:
                pass
            raise

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        """Send a WebSocket frame (client-to-server, masked)."""
        import os

        header = bytearray()
        header.append(0x80 | opcode)  # FIN + opcode

        length = len(payload)
        if length < 126:
            header.append(0x80 | length)  # MASK bit set
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))

        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self._sock.sendall(bytes(header) + masked)

    def _send_text(self, text: str) -> None:
        self._send_frame(0x01, text.encode())

    def _recv_exact(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self._sock.recv(n - len(data))
            if not chunk:
                raise EOFError("WebSocket connection closed")
            data += chunk
        return data

    def _recv_frame(self) -> tuple[int, bytes]:
        """Receive a WebSocket frame. Returns (opcode, payload)."""
        b0, b1 = self._recv_exact(2)
        opcode = b0 & 0x0F
        masked = bool(b1 & 0x80)
        length = b1 & 0x7F

        if length == 126:
            length = struct.unpack("!H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._recv_exact(8))[0]

        if masked:
            mask = self._recv_exact(4)
            data = self._recv_exact(length)
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        else:
            data = self._recv_exact(length)

        # Handle control frames
        if opcode == 0x08:  # Close
            raise EOFError("WebSocket closed by server")
        if opcode == 0x09:  # Ping
            self._send_frame(0x0A, data)  # Pong
            return self._recv_frame()

        return opcode, data

    def recv(self) -> VoiceStreamEvent:
        """Read the next event from the voice stream.

        Raises ``EOFError`` when the connection is closed.
        """
        opcode, data = self._recv_frame()

        # Binary frames are PCM audio
        if opcode == 0x02:
            return VoiceStreamEvent(type="audio", audio=data)

        # Text frames are JSON events
        return VoiceStreamEvent.model_validate(_json.loads(data))

    def send_audio(self, audio: bytes) -> None:
        """Send a binary audio chunk to the server."""
        self._send_frame(0x02, audio)

    def send_text(self, text: str) -> None:
        """Send a text message to the agent instead of audio."""
        self._send_text(_json.dumps({"type": "text_input", "text": text}))

    def end_session(self) -> None:
        """Gracefully end the voice session."""
        self._send_text('{"type":"end_session"}')

    def configure(
        self,
        *,
        audio_format: str | None = None,
        sample_rate: int | None = None,
    ) -> None:
        """Change audio format or sample rate mid-session."""
        msg: dict[str, Any] = {"type": "config"}
        if audio_format is not None:
            msg["audioFormat"] = audio_format
        if sample_rate is not None:
            msg["sampleRate"] = sample_rate
        self._send_text(_json.dumps(msg))

    def close(self) -> None:
        """Close the voice stream."""
        if not self._closed:
            self._closed = True
            try:
                self._send_frame(0x08, b"")  # Close frame
            except Exception:
                pass
            self._sock.close()

    def __iter__(self) -> Iterator[VoiceStreamEvent]:
        """Iterate over incoming events until the connection closes."""
        try:
            while not self._closed:
                yield self.recv()
        except EOFError:
            return

    def __enter__(self) -> VoiceStream:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncVoiceStream:
    """Async bidirectional WebSocket connection for real-time voice chat.

    Uses ``asyncio`` streams to avoid requiring a third-party WebSocket dependency.
    """

    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self._reader = reader
        self._writer = writer
        self._closed = False

    @classmethod
    async def connect(cls, token: VoiceStreamToken) -> AsyncVoiceStream:
        """Establish the WebSocket connection and authenticate."""
        import base64
        import os
        import ssl as _ssl
        from urllib.parse import urlparse

        parsed = urlparse(token.ws_url)
        host = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "wss" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"

        ssl_ctx: _ssl.SSLContext | None = None
        if parsed.scheme == "wss":
            ssl_ctx = _ssl.create_default_context()

        reader, writer = await asyncio.open_connection(host, port, ssl=ssl_ctx)

        key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n"
            f"\r\n"
        )
        writer.write(handshake.encode())
        await writer.drain()

        response = b""
        while b"\r\n\r\n" not in response:
            chunk = await reader.read(4096)
            if not chunk:
                raise ConnectionError("WebSocket handshake failed: connection closed")
            response += chunk

        if b"101" not in response.split(b"\r\n")[0]:
            raise ConnectionError(f"WebSocket handshake failed: {response.split(b'\r\n')[0]!r}")

        stream = cls(reader, writer)

        # Send auth token as first text message
        await stream._send_text(token.auth_token)
        return stream

    async def _send_frame(self, opcode: int, payload: bytes) -> None:
        import os

        header = bytearray()
        header.append(0x80 | opcode)

        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))

        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self._writer.write(bytes(header) + masked)
        await self._writer.drain()

    async def _send_text(self, text: str) -> None:
        await self._send_frame(0x01, text.encode())

    async def _recv_exact(self, n: int) -> bytes:
        data = await self._reader.readexactly(n)
        return data

    async def _recv_frame(self) -> tuple[int, bytes]:
        header = await self._recv_exact(2)
        b0, b1 = header[0], header[1]
        opcode = b0 & 0x0F
        masked = bool(b1 & 0x80)
        length = b1 & 0x7F

        if length == 126:
            length = struct.unpack("!H", await self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", await self._recv_exact(8))[0]

        if masked:
            mask = await self._recv_exact(4)
            data = await self._recv_exact(length)
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        else:
            data = await self._recv_exact(length)

        if opcode == 0x08:
            raise EOFError("WebSocket closed by server")
        if opcode == 0x09:
            await self._send_frame(0x0A, data)
            return await self._recv_frame()

        return opcode, data

    async def recv(self) -> VoiceStreamEvent:
        """Read the next event from the voice stream."""
        opcode, data = await self._recv_frame()
        if opcode == 0x02:
            return VoiceStreamEvent(type="audio", audio=data)
        return VoiceStreamEvent.model_validate(_json.loads(data))

    async def send_audio(self, audio: bytes) -> None:
        """Send a binary audio chunk to the server."""
        await self._send_frame(0x02, audio)

    async def send_text(self, text: str) -> None:
        """Send a text message to the agent instead of audio."""
        await self._send_text(_json.dumps({"type": "text_input", "text": text}))

    async def end_session(self) -> None:
        """Gracefully end the voice session."""
        await self._send_text('{"type":"end_session"}')

    async def configure(
        self,
        *,
        audio_format: str | None = None,
        sample_rate: int | None = None,
    ) -> None:
        """Change audio format or sample rate mid-session."""
        msg: dict[str, Any] = {"type": "config"}
        if audio_format is not None:
            msg["audioFormat"] = audio_format
        if sample_rate is not None:
            msg["sampleRate"] = sample_rate
        await self._send_text(_json.dumps(msg))

    async def close(self) -> None:
        """Close the voice stream."""
        if not self._closed:
            self._closed = True
            try:
                await self._send_frame(0x08, b"")
            except Exception:
                pass
            self._writer.close()

    async def __aiter__(self):
        try:
            while not self._closed:
                yield await self.recv()
        except (EOFError, asyncio.IncompleteReadError):
            return

    async def __aenter__(self) -> AsyncVoiceStream:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class Voices:
    """Sync global voice catalog operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        tier: int | None = None,
        gender: str | None = None,
        language: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> VoiceListResponse:
        """List available voices from the catalog."""
        params: dict[str, Any] = {}
        if tier is not None:
            params["tier"] = tier
        if gender is not None:
            params["gender"] = gender
        if language is not None:
            params["language"] = language
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        data = self._http.get("/api/v1/voices", params=params)
        return VoiceListResponse.model_validate(data)


class AsyncVoiceResource:
    """Async per-agent voice live operations (duplex WebSocket streaming via Gemini Live)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get_token(
        self,
        agent_id: str,
        *,
        voice_name: str | None = None,
        language: str | None = None,
        user_id: str | None = None,
        compiled_system_prompt: str | None = None,
    ) -> VoiceStreamToken:
        """Get a short-lived token for voice live WebSocket streaming."""
        raw: dict[str, Any] = {}
        if voice_name is not None:
            raw["voice_name"] = voice_name
        if language is not None:
            raw["language"] = language
        if user_id is not None:
            raw["user_id"] = user_id
        if compiled_system_prompt is not None:
            raw["compiled_system_prompt"] = compiled_system_prompt
        body = encode_body(VoiceLiveWSTokenInputBody, raw)

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/live-ws-token", json_data=body
        )
        return VoiceStreamToken.model_validate(data)

    async def stream(self, token: VoiceStreamToken) -> AsyncVoiceStream:
        """Open a bidirectional WebSocket for real-time voice chat via Gemini Live.

        Usage::

            token = await client.agents.voice.get_token(agent_id)
            async with await client.agents.voice.stream(token) as stream:
                await stream.send_audio(audio_bytes)
                async for event in stream:
                    if event.type == "audio":
                        play_pcm_audio(event.audio)
        """
        return await AsyncVoiceStream.connect(token)

    async def tts(
        self,
        agent_id: str,
        *,
        text: str,
        voice_name: str | None = None,
        language: str | None = None,
        output_format: str | None = None,
    ) -> TTSResponse:
        """Convert text to speech audio."""
        raw: dict[str, Any] = {"text": text}
        if voice_name is not None:
            raw["voice_name"] = voice_name
        if language is not None:
            raw["language"] = language
        if output_format is not None:
            raw["output_format"] = output_format
        body = encode_body(TextToSpeechInputBody, raw)

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/tts", json_data=body
        )
        return TTSResponse.model_validate(data)

    async def stt(
        self,
        agent_id: str,
        *,
        audio: str,
        audio_format: str,
        language: str | None = None,
    ) -> STTResponse:
        """Transcribe audio to text."""
        raw: dict[str, Any] = {"audio": audio, "audio_format": audio_format}
        if language is not None:
            raw["language"] = language
        body = encode_body(SpeechToTextInputBody, raw)

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/stt", json_data=body
        )
        return STTResponse.model_validate(data)


class AsyncVoices:
    """Async global voice catalog operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        tier: int | None = None,
        gender: str | None = None,
        language: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> VoiceListResponse:
        """List available voices from the catalog."""
        params: dict[str, Any] = {}
        if tier is not None:
            params["tier"] = tier
        if gender is not None:
            params["gender"] = gender
        if language is not None:
            params["language"] = language
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        data = await self._http.get("/api/v1/voices", params=params)
        return VoiceListResponse.model_validate(data)
