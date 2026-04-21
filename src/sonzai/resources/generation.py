"""Generation resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    GenerateBioResponse,
    GenerateCharacterResponse,
    GenerateSeedMemoriesResponse,
    ImageGenerateResponse,
)


class Generation:
    """Sync AI content generation operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def generate_bio(
        self,
        agent_id: str,
        *,
        name: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        user_id: str | None = None,
        current_bio: str | None = None,
        style: str | None = None,
        instance_id: str | None = None,
    ) -> GenerateBioResponse:
        """Generate a bio for an agent using AI."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if user_id is not None:
            body["user_id"] = user_id
        if current_bio is not None:
            body["current_bio"] = current_bio
        if style is not None:
            body["style"] = style
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/bio/generate", json_data=body
        )
        return GenerateBioResponse.model_validate(data)

    def generate_image(
        self,
        agent_id: str,
        *,
        prompt: str,
        negative_prompt: str | None = None,
        model: str | None = None,
        provider: str | None = None,
    ) -> ImageGenerateResponse:
        """Generate an image using the agent's context."""
        body: dict[str, Any] = {"prompt": prompt}
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if model is not None:
            body["model"] = model
        if provider is not None:
            body["provider"] = provider

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/image/generate", json_data=body
        )
        return ImageGenerateResponse.model_validate(data)

    def generate_character(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        fields: list[str] | None = None,
    ) -> GenerateCharacterResponse:
        """Generate a full character profile from a description.

        If an agent with the resolved ID already exists, the LLM is skipped
        and the existing profile is returned.
        """
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields

        data = self._http.post(
            "/api/v1/agents/generate-character", json_data=body
        )
        return GenerateCharacterResponse.model_validate(data)

    def generate_and_create(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        fields: list[str] | None = None,
        project_id: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        """Generate a character and create the agent in one idempotent call.

        If the agent already exists, the LLM is skipped and the existing
        agent is returned. Safe to call on every app startup.
        """
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        if project_id is not None:
            body["project_id"] = project_id
        if language is not None:
            body["language"] = language

        return self._http.post(
            "/api/v1/agents/generate-and-create", json_data=body
        )

    def generate_seed_memories(
        self,
        agent_id: str,
        *,
        agent_name: str | None = None,
        big5: dict[str, Any] | None = None,
        personality_prompt: str | None = None,
        primary_traits: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        speech_patterns: list[str] | None = None,
        creator_display_name: str | None = None,
        static_lore_memories: list[dict[str, Any]] | None = None,
        lore_generation_context: dict[str, Any] | None = None,
        identity_memory_templates: list[dict[str, Any]] | None = None,
        generate_origin_story: bool | None = None,
        generate_personalized_memories: bool | None = None,
    ) -> GenerateSeedMemoriesResponse:
        """Generate seed memories for an agent using AI."""
        body: dict[str, Any] = {}
        if agent_name is not None:
            body["agentName"] = agent_name
        if big5 is not None:
            body["big5"] = big5
        if personality_prompt is not None:
            body["personalityPrompt"] = personality_prompt
        if primary_traits is not None:
            body["primaryTraits"] = primary_traits
        if true_interests is not None:
            body["trueInterests"] = true_interests
        if true_dislikes is not None:
            body["trueDislikes"] = true_dislikes
        if speech_patterns is not None:
            body["speechPatterns"] = speech_patterns
        if creator_display_name is not None:
            body["creatorDisplayName"] = creator_display_name
        if static_lore_memories is not None:
            body["staticLoreMemories"] = static_lore_memories
        if lore_generation_context is not None:
            body["loreGenerationContext"] = lore_generation_context
        if identity_memory_templates is not None:
            body["identityMemoryTemplates"] = identity_memory_templates
        if generate_origin_story is not None:
            body["generateOriginStory"] = generate_origin_story
        if generate_personalized_memories is not None:
            body["generatePersonalizedMemories"] = generate_personalized_memories

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return GenerateSeedMemoriesResponse.model_validate(data)


class AsyncGeneration:
    """Async AI content generation operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def generate_bio(
        self,
        agent_id: str,
        *,
        name: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        user_id: str | None = None,
        current_bio: str | None = None,
        style: str | None = None,
        instance_id: str | None = None,
    ) -> GenerateBioResponse:
        """Generate a bio for an agent using AI."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if user_id is not None:
            body["user_id"] = user_id
        if current_bio is not None:
            body["current_bio"] = current_bio
        if style is not None:
            body["style"] = style
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/bio/generate", json_data=body
        )
        return GenerateBioResponse.model_validate(data)

    async def generate_image(
        self,
        agent_id: str,
        *,
        prompt: str,
        negative_prompt: str | None = None,
        model: str | None = None,
        provider: str | None = None,
    ) -> ImageGenerateResponse:
        """Generate an image using the agent's context."""
        body: dict[str, Any] = {"prompt": prompt}
        if negative_prompt is not None:
            body["negative_prompt"] = negative_prompt
        if model is not None:
            body["model"] = model
        if provider is not None:
            body["provider"] = provider

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/image/generate", json_data=body
        )
        return ImageGenerateResponse.model_validate(data)

    async def generate_character(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        fields: list[str] | None = None,
    ) -> GenerateCharacterResponse:
        """Generate a full character profile from a description.

        If an agent with the resolved ID already exists, the LLM is skipped
        and the existing profile is returned.
        """
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields

        data = await self._http.post(
            "/api/v1/agents/generate-character", json_data=body
        )
        return GenerateCharacterResponse.model_validate(data)

    async def generate_and_create(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        gender: str | None = None,
        description: str | None = None,
        fields: list[str] | None = None,
        project_id: str | None = None,
        language: str | None = None,
    ) -> dict[str, Any]:
        """Generate a character and create the agent in one idempotent call.

        If the agent already exists, the LLM is skipped and the existing
        agent is returned. Safe to call on every app startup.
        """
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if gender is not None:
            body["gender"] = gender
        if description is not None:
            body["description"] = description
        if fields is not None:
            body["fields"] = fields
        if project_id is not None:
            body["project_id"] = project_id
        if language is not None:
            body["language"] = language

        return await self._http.post(
            "/api/v1/agents/generate-and-create", json_data=body
        )

    async def generate_seed_memories(
        self,
        agent_id: str,
        *,
        agent_name: str | None = None,
        big5: dict[str, Any] | None = None,
        personality_prompt: str | None = None,
        primary_traits: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        speech_patterns: list[str] | None = None,
        creator_display_name: str | None = None,
        static_lore_memories: list[dict[str, Any]] | None = None,
        lore_generation_context: dict[str, Any] | None = None,
        identity_memory_templates: list[dict[str, Any]] | None = None,
        generate_origin_story: bool | None = None,
        generate_personalized_memories: bool | None = None,
    ) -> GenerateSeedMemoriesResponse:
        """Generate seed memories for an agent using AI."""
        body: dict[str, Any] = {}
        if agent_name is not None:
            body["agentName"] = agent_name
        if big5 is not None:
            body["big5"] = big5
        if personality_prompt is not None:
            body["personalityPrompt"] = personality_prompt
        if primary_traits is not None:
            body["primaryTraits"] = primary_traits
        if true_interests is not None:
            body["trueInterests"] = true_interests
        if true_dislikes is not None:
            body["trueDislikes"] = true_dislikes
        if speech_patterns is not None:
            body["speechPatterns"] = speech_patterns
        if creator_display_name is not None:
            body["creatorDisplayName"] = creator_display_name
        if static_lore_memories is not None:
            body["staticLoreMemories"] = static_lore_memories
        if lore_generation_context is not None:
            body["loreGenerationContext"] = lore_generation_context
        if identity_memory_templates is not None:
            body["identityMemoryTemplates"] = identity_memory_templates
        if generate_origin_story is not None:
            body["generateOriginStory"] = generate_origin_story
        if generate_personalized_memories is not None:
            body["generatePersonalizedMemories"] = generate_personalized_memories

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/memory/seed", json_data=body
        )
        return GenerateSeedMemoriesResponse.model_validate(data)
