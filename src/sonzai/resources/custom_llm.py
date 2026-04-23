"""Custom LLM config resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._generated.models import SetCustomLLMConfigInputBody
from .._generated.resources.custom_llm import AsyncCustomLlm as _GenAsyncCustomLlm
from .._generated.resources.custom_llm import CustomLlm as _GenCustomLlm
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import CustomLLMConfigResponse


class CustomLLM(_GenCustomLlm):
    """Sync custom LLM configuration operations."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def get(self, project_id: str) -> CustomLLMConfigResponse:
        """Get the custom LLM config for a project."""
        data = self._http.get(
            f"/api/v1/projects/{project_id}/custom-llm"
        )
        return CustomLLMConfigResponse.model_validate(data)

    def set(
        self,
        project_id: str,
        *,
        endpoint: str,
        api_key: str,
        model: str | None = None,
        display_name: str | None = None,
        is_active: bool | None = None,
    ) -> CustomLLMConfigResponse:
        """Set or update the custom LLM config."""
        raw: dict[str, Any] = {"endpoint": endpoint, "api_key": api_key}
        if model is not None:
            raw["model"] = model
        if display_name is not None:
            raw["display_name"] = display_name
        if is_active is not None:
            raw["is_active"] = is_active
        body = encode_body(SetCustomLLMConfigInputBody, raw)

        data = self._http.put(
            f"/api/v1/projects/{project_id}/custom-llm",
            json_data=body,
        )
        return CustomLLMConfigResponse.model_validate(data)

    def delete(self, project_id: str) -> None:
        """Delete the custom LLM config."""
        self._http.delete(f"/api/v1/projects/{project_id}/custom-llm")


class AsyncCustomLLM(_GenAsyncCustomLlm):
    """Async custom LLM configuration operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def get(self, project_id: str) -> CustomLLMConfigResponse:
        """Get the custom LLM config for a project."""
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/custom-llm"
        )
        return CustomLLMConfigResponse.model_validate(data)

    async def set(
        self,
        project_id: str,
        *,
        endpoint: str,
        api_key: str,
        model: str | None = None,
        display_name: str | None = None,
        is_active: bool | None = None,
    ) -> CustomLLMConfigResponse:
        """Set or update the custom LLM config."""
        raw: dict[str, Any] = {"endpoint": endpoint, "api_key": api_key}
        if model is not None:
            raw["model"] = model
        if display_name is not None:
            raw["display_name"] = display_name
        if is_active is not None:
            raw["is_active"] = is_active
        body = encode_body(SetCustomLLMConfigInputBody, raw)

        data = await self._http.put(
            f"/api/v1/projects/{project_id}/custom-llm",
            json_data=body,
        )
        return CustomLLMConfigResponse.model_validate(data)

    async def delete(self, project_id: str) -> None:
        """Delete the custom LLM config."""
        await self._http.delete(
            f"/api/v1/projects/{project_id}/custom-llm"
        )
