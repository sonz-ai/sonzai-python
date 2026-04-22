"""Eval template resource for the Sonzai SDK."""

from __future__ import annotations

import builtins
from typing import Any

from .._generated.models import CreateEvalTemplateInputBody
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body
from ..types import EvalTemplate, EvalTemplateCategory, EvalTemplateListResponse, SessionResponse

# Alias to avoid shadowing by the ``list`` method on resource classes.
_list = builtins.list


class EvalTemplates:
    """Sync eval template operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, *, template_type: str | None = None) -> EvalTemplateListResponse:
        """List all eval templates."""
        params: dict[str, Any] = {}
        if template_type:
            params["type"] = template_type

        data = self._http.get("/api/v1/eval-templates", params=params)
        return EvalTemplateListResponse.model_validate(data)

    def get(self, template_id: str) -> EvalTemplate:
        """Get a specific eval template."""
        data = self._http.get(f"/api/v1/eval-templates/{template_id}")
        return EvalTemplate.model_validate(data)

    def create(
        self,
        *,
        name: str,
        description: str = "",
        template_type: str = "",
        judge_model: str = "gemini-3.1-pro-preview",
        temperature: float = 0.3,
        max_tokens: int = 8192,
        scoring_rubric: str = "",
        categories: _list[dict[str, Any]] | None = None,
    ) -> EvalTemplate:
        """Create a new eval template."""
        raw: dict[str, Any] = {
            "name": name,
            "description": description,
            "template_type": template_type,
            "judge_model": judge_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "scoring_rubric": scoring_rubric,
        }
        if categories:
            raw["categories"] = categories
        body = encode_body(CreateEvalTemplateInputBody, raw)

        data = self._http.post("/api/v1/eval-templates", json_data=body)
        return EvalTemplate.model_validate(data)

    def update(
        self,
        template_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        template_type: str | None = None,
        judge_model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        scoring_rubric: str | None = None,
        categories: _list[dict[str, Any]] | None = None,
    ) -> EvalTemplate:
        """Update an eval template."""
        # NOTE: not routed through encode_body — UpdateEvalTemplateInputBody lacks
        # the ``template_type`` field that this method exposes.
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if template_type is not None:
            body["template_type"] = template_type
        if judge_model is not None:
            body["judge_model"] = judge_model
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if scoring_rubric is not None:
            body["scoring_rubric"] = scoring_rubric
        if categories is not None:
            body["categories"] = categories

        data = self._http.put(
            f"/api/v1/eval-templates/{template_id}", json_data=body
        )
        return EvalTemplate.model_validate(data)

    def delete(self, template_id: str) -> SessionResponse:
        """Delete an eval template."""
        data = self._http.delete(f"/api/v1/eval-templates/{template_id}")
        return SessionResponse.model_validate(data)


class AsyncEvalTemplates:
    """Async eval template operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, *, template_type: str | None = None) -> EvalTemplateListResponse:
        params: dict[str, Any] = {}
        if template_type:
            params["type"] = template_type
        data = await self._http.get("/api/v1/eval-templates", params=params)
        return EvalTemplateListResponse.model_validate(data)

    async def get(self, template_id: str) -> EvalTemplate:
        data = await self._http.get(f"/api/v1/eval-templates/{template_id}")
        return EvalTemplate.model_validate(data)

    async def create(
        self,
        *,
        name: str,
        description: str = "",
        template_type: str = "",
        judge_model: str = "gemini-3.1-pro-preview",
        temperature: float = 0.3,
        max_tokens: int = 8192,
        scoring_rubric: str = "",
        categories: _list[dict[str, Any]] | None = None,
    ) -> EvalTemplate:
        raw: dict[str, Any] = {
            "name": name,
            "description": description,
            "template_type": template_type,
            "judge_model": judge_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "scoring_rubric": scoring_rubric,
        }
        if categories:
            raw["categories"] = categories
        body = encode_body(CreateEvalTemplateInputBody, raw)
        data = await self._http.post("/api/v1/eval-templates", json_data=body)
        return EvalTemplate.model_validate(data)

    async def update(
        self,
        template_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        template_type: str | None = None,
        judge_model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        scoring_rubric: str | None = None,
        categories: _list[dict[str, Any]] | None = None,
    ) -> EvalTemplate:
        # NOTE: not routed through encode_body — UpdateEvalTemplateInputBody lacks
        # the ``template_type`` field that this method exposes.
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if template_type is not None:
            body["template_type"] = template_type
        if judge_model is not None:
            body["judge_model"] = judge_model
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if scoring_rubric is not None:
            body["scoring_rubric"] = scoring_rubric
        if categories is not None:
            body["categories"] = categories
        data = await self._http.put(
            f"/api/v1/eval-templates/{template_id}", json_data=body
        )
        return EvalTemplate.model_validate(data)

    async def delete(self, template_id: str) -> SessionResponse:
        data = await self._http.delete(f"/api/v1/eval-templates/{template_id}")
        return SessionResponse.model_validate(data)
