"""Webhooks resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    DeleteResponse,
    DeliveryAttemptsResponse,
    WebhookListResponse,
    WebhookRegisterResponse,
)


class Webhooks:
    """Sync webhook management operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def register(
        self,
        event_type: str,
        *,
        webhook_url: str,
        auth_header: str | None = None,
    ) -> WebhookRegisterResponse:
        """Register (or update) a webhook URL for an event type."""
        body: dict[str, Any] = {"webhook_url": webhook_url}
        if auth_header is not None:
            body["auth_header"] = auth_header

        data = self._http.put(
            f"/api/v1/webhooks/{event_type}", json_data=body
        )
        return WebhookRegisterResponse.model_validate(data)

    def list(self) -> WebhookListResponse:
        """List all registered webhooks."""
        data = self._http.get("/api/v1/webhooks")
        return WebhookListResponse.model_validate(data)

    def delete(self, event_type: str) -> DeleteResponse:
        """Remove a webhook for an event type."""
        data = self._http.delete(f"/api/v1/webhooks/{event_type}")
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    def list_delivery_attempts(
        self, event_type: str
    ) -> DeliveryAttemptsResponse:
        """List recent delivery attempts for a specific event type."""
        data = self._http.get(
            f"/api/v1/webhooks/{event_type}/attempts"
        )
        return DeliveryAttemptsResponse.model_validate(data)

    def rotate_secret(self, event_type: str) -> WebhookRegisterResponse:
        """Generate a new signing secret for a webhook event type."""
        data = self._http.post(
            f"/api/v1/webhooks/{event_type}/rotate-secret"
        )
        return WebhookRegisterResponse.model_validate(data)

    # -- Project-scoped webhooks --

    def register_for_project(
        self,
        project_id: str,
        event_type: str,
        *,
        webhook_url: str,
        auth_header: str | None = None,
    ) -> WebhookRegisterResponse:
        """Register (or update) a webhook for a project event type."""
        body: dict[str, Any] = {"webhook_url": webhook_url}
        if auth_header is not None:
            body["auth_header"] = auth_header
        data = self._http.put(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}",
            json_data=body,
        )
        return WebhookRegisterResponse.model_validate(data)

    def list_for_project(self, project_id: str) -> WebhookListResponse:
        """List all webhooks for a project."""
        data = self._http.get(f"/api/v1/projects/{project_id}/webhooks")
        return WebhookListResponse.model_validate(data)

    def delete_for_project(
        self, project_id: str, event_type: str
    ) -> DeleteResponse:
        """Remove a webhook for a project event type."""
        data = self._http.delete(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    def list_delivery_attempts_for_project(
        self, project_id: str, event_type: str
    ) -> DeliveryAttemptsResponse:
        """List delivery attempts for a project webhook event type."""
        data = self._http.get(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}/attempts"
        )
        return DeliveryAttemptsResponse.model_validate(data)

    def rotate_secret_for_project(
        self, project_id: str, event_type: str
    ) -> WebhookRegisterResponse:
        """Rotate signing secret for a project webhook event type."""
        data = self._http.post(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}/rotate-secret"
        )
        return WebhookRegisterResponse.model_validate(data)


class AsyncWebhooks:
    """Async webhook management operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def register(
        self,
        event_type: str,
        *,
        webhook_url: str,
        auth_header: str | None = None,
    ) -> WebhookRegisterResponse:
        """Register (or update) a webhook URL for an event type."""
        body: dict[str, Any] = {"webhook_url": webhook_url}
        if auth_header is not None:
            body["auth_header"] = auth_header

        data = await self._http.put(
            f"/api/v1/webhooks/{event_type}", json_data=body
        )
        return WebhookRegisterResponse.model_validate(data)

    async def list(self) -> WebhookListResponse:
        """List all registered webhooks."""
        data = await self._http.get("/api/v1/webhooks")
        return WebhookListResponse.model_validate(data)

    async def delete(self, event_type: str) -> DeleteResponse:
        """Remove a webhook for an event type."""
        data = await self._http.delete(f"/api/v1/webhooks/{event_type}")
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    async def list_delivery_attempts(
        self, event_type: str
    ) -> DeliveryAttemptsResponse:
        """List recent delivery attempts for a specific event type."""
        data = await self._http.get(
            f"/api/v1/webhooks/{event_type}/attempts"
        )
        return DeliveryAttemptsResponse.model_validate(data)

    async def rotate_secret(
        self, event_type: str
    ) -> WebhookRegisterResponse:
        """Generate a new signing secret for a webhook event type."""
        data = await self._http.post(
            f"/api/v1/webhooks/{event_type}/rotate-secret"
        )
        return WebhookRegisterResponse.model_validate(data)

    # -- Project-scoped webhooks --

    async def register_for_project(
        self,
        project_id: str,
        event_type: str,
        *,
        webhook_url: str,
        auth_header: str | None = None,
    ) -> WebhookRegisterResponse:
        """Register (or update) a webhook for a project event type."""
        body: dict[str, Any] = {"webhook_url": webhook_url}
        if auth_header is not None:
            body["auth_header"] = auth_header
        data = await self._http.put(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}",
            json_data=body,
        )
        return WebhookRegisterResponse.model_validate(data)

    async def list_for_project(
        self, project_id: str
    ) -> WebhookListResponse:
        """List all webhooks for a project."""
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/webhooks"
        )
        return WebhookListResponse.model_validate(data)

    async def delete_for_project(
        self, project_id: str, event_type: str
    ) -> DeleteResponse:
        """Remove a webhook for a project event type."""
        data = await self._http.delete(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}"
        )
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    async def list_delivery_attempts_for_project(
        self, project_id: str, event_type: str
    ) -> DeliveryAttemptsResponse:
        """List delivery attempts for a project webhook event type."""
        data = await self._http.get(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}/attempts"
        )
        return DeliveryAttemptsResponse.model_validate(data)

    async def rotate_secret_for_project(
        self, project_id: str, event_type: str
    ) -> WebhookRegisterResponse:
        """Rotate signing secret for a project webhook event type."""
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/webhooks/{event_type}/rotate-secret"
        )
        return WebhookRegisterResponse.model_validate(data)
