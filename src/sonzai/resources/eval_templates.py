"""Eval template resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._http import AsyncHTTPClient, HTTPClient
from ..types import EvalTemplate, EvalTemplateCategory, EvalTemplateListResponse, SessionResponse


class EvalTemplates:
    """Sync eval template operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, *, template_type: Optional[str] = None) -> EvalTemplateListResponse:
        """List all eval templates."""
        params: Dict[str, Any] = {}
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
        categories: Optional[List[Dict[str, Any]]] = None,
    ) -> EvalTemplate:
        """Create a new eval template."""
        body: Dict[str, Any] = {
            "name": name,
            "description": description,
            "template_type": template_type,
            "judge_model": judge_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "scoring_rubric": scoring_rubric,
        }
        if categories:
            body["categories"] = categories

        data = self._http.post("/api/v1/eval-templates", json_data=body)
        return EvalTemplate.model_validate(data)

    def update(
        self,
        template_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        template_type: Optional[str] = None,
        judge_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        scoring_rubric: Optional[str] = None,
        categories: Optional[List[Dict[str, Any]]] = None,
    ) -> EvalTemplate:
        """Update an eval template."""
        body: Dict[str, Any] = {}
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

    async def list(self, *, template_type: Optional[str] = None) -> EvalTemplateListResponse:
        params: Dict[str, Any] = {}
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
        categories: Optional[List[Dict[str, Any]]] = None,
    ) -> EvalTemplate:
        body: Dict[str, Any] = {
            "name": name,
            "description": description,
            "template_type": template_type,
            "judge_model": judge_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "scoring_rubric": scoring_rubric,
        }
        if categories:
            body["categories"] = categories
        data = await self._http.post("/api/v1/eval-templates", json_data=body)
        return EvalTemplate.model_validate(data)

    async def update(
        self,
        template_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        template_type: Optional[str] = None,
        judge_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        scoring_rubric: Optional[str] = None,
        categories: Optional[List[Dict[str, Any]]] = None,
    ) -> EvalTemplate:
        body: Dict[str, Any] = {}
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
