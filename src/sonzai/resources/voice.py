"""Voice resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    TTSResponse,
    Voice,
    VoiceChatResponse,
    VoiceListResponse,
    VoiceMatchResponse,
)


class VoiceResource:
    """Sync per-agent voice operations (TTS, match, chat)."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def text_to_speech(
        self,
        agent_id: str,
        *,
        text: str,
        voice_name: str | None = None,
        language: str | None = None,
        emotional_context: dict[str, Any] | None = None,
    ) -> TTSResponse:
        """Convert text to speech using the agent's voice."""
        body: dict[str, Any] = {"text": text}
        if voice_name is not None:
            body["voice_name"] = voice_name
        if language is not None:
            body["language"] = language
        if emotional_context is not None:
            body["emotional_context"] = emotional_context

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/tts", json_data=body
        )
        return TTSResponse.model_validate(data)

    def voice_match(
        self,
        agent_id: str,
        *,
        big5: dict[str, Any] | None = None,
        preferred_gender: str | None = None,
    ) -> VoiceMatchResponse:
        """Find the best matching voice for an agent based on personality."""
        body: dict[str, Any] = {}
        if big5 is not None:
            body["big5"] = big5
        if preferred_gender is not None:
            body["preferred_gender"] = preferred_gender

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/match", json_data=body
        )
        return VoiceMatchResponse.model_validate(data)

    def voice_chat(
        self,
        agent_id: str,
        *,
        audio: str,
        user_id: str | None = None,
        audio_format: str | None = None,
        voice_name: str | None = None,
        continuation_token: str | None = None,
        language: str | None = None,
    ) -> VoiceChatResponse:
        """Perform a single-turn voice chat: send audio, receive text + audio response."""
        body: dict[str, Any] = {"audio": audio}
        if user_id is not None:
            body["user_id"] = user_id
        if audio_format is not None:
            body["audio_format"] = audio_format
        if voice_name is not None:
            body["voice_name"] = voice_name
        if continuation_token is not None:
            body["continuation_token"] = continuation_token
        if language is not None:
            body["language"] = language

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/voice/chat", json_data=body
        )
        return VoiceChatResponse.model_validate(data)


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
    """Async per-agent voice operations (TTS, match, chat)."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def text_to_speech(
        self,
        agent_id: str,
        *,
        text: str,
        voice_name: str | None = None,
        language: str | None = None,
        emotional_context: dict[str, Any] | None = None,
    ) -> TTSResponse:
        """Convert text to speech using the agent's voice."""
        body: dict[str, Any] = {"text": text}
        if voice_name is not None:
            body["voice_name"] = voice_name
        if language is not None:
            body["language"] = language
        if emotional_context is not None:
            body["emotional_context"] = emotional_context

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/tts", json_data=body
        )
        return TTSResponse.model_validate(data)

    async def voice_match(
        self,
        agent_id: str,
        *,
        big5: dict[str, Any] | None = None,
        preferred_gender: str | None = None,
    ) -> VoiceMatchResponse:
        """Find the best matching voice for an agent based on personality."""
        body: dict[str, Any] = {}
        if big5 is not None:
            body["big5"] = big5
        if preferred_gender is not None:
            body["preferred_gender"] = preferred_gender

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/match", json_data=body
        )
        return VoiceMatchResponse.model_validate(data)

    async def voice_chat(
        self,
        agent_id: str,
        *,
        audio: str,
        user_id: str | None = None,
        audio_format: str | None = None,
        voice_name: str | None = None,
        continuation_token: str | None = None,
        language: str | None = None,
    ) -> VoiceChatResponse:
        """Perform a single-turn voice chat: send audio, receive text + audio response."""
        body: dict[str, Any] = {"audio": audio}
        if user_id is not None:
            body["user_id"] = user_id
        if audio_format is not None:
            body["audio_format"] = audio_format
        if voice_name is not None:
            body["voice_name"] = voice_name
        if continuation_token is not None:
            body["continuation_token"] = continuation_token
        if language is not None:
            body["language"] = language

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/voice/chat", json_data=body
        )
        return VoiceChatResponse.model_validate(data)


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
