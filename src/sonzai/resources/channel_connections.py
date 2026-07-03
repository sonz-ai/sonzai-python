"""Meta channel connections resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any, Literal
from urllib.parse import quote

from .._generated.models import (
    ChannelConnectionDTO,
    ChannelConnectionsOutputBody,
    CreateChannelConnectionInputBody,
    PatchChannelConnectionInputBody,
    TestChannelConnectionInputBody,
)
from .._generated.resources.channel_connections import (
    AsyncChannelConnections as _GenAsyncChannelConnections,
)
from .._generated.resources.channel_connections import ChannelConnections as _GenChannelConnections
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body

ChannelConnectionType = Literal["whatsapp", "messenger", "instagram"]
ChannelProviderMode = Literal["byo_app", "embedded_signup"]
ChannelConnectionStatus = Literal["active", "disabled", "error"]

_SECRET_FIELDS = frozenset({"access_token", "app_secret"})
_REDACTED_SECRET = "redacted"


class ChannelConnections(_GenChannelConnections):
    """Sync Meta channel connection management."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(self, project_id: str) -> list[ChannelConnectionDTO]:
        """List channel connections for a project."""
        data = self._http.get(f"/api/v1/projects/{quote(project_id, safe='')}/channel-connections")
        result = ChannelConnectionsOutputBody.model_validate(_redact_secrets(data))
        return list(result.connections or result.items or [])

    def create(
        self,
        project_id: str,
        *,
        channel_type: ChannelConnectionType | str,
        provider_mode: ChannelProviderMode | str = "byo_app",
        app_id: str | None = None,
        app_secret: str | None = None,
        phone_number_id: str | None = None,
        waba_id: str | None = None,
        page_id: str | None = None,
        ig_account_id: str | None = None,
        access_token: str | None = None,
        verify_token: str | None = None,
        display_name: str | None = None,
        code: str | None = None,
        default_agent_id: str | None = None,
        templates: Any | None = None,
        test_to: str | None = None,
        test_message: str | None = None,
    ) -> ChannelConnectionDTO:
        """Create a channel connection."""
        body = _create_body(
            channel_type=channel_type,
            provider_mode=provider_mode,
            app_id=app_id,
            app_secret=app_secret,
            phone_number_id=phone_number_id,
            waba_id=waba_id,
            page_id=page_id,
            ig_account_id=ig_account_id,
            access_token=access_token,
            verify_token=verify_token,
            display_name=display_name,
            code=code,
            default_agent_id=default_agent_id,
            templates=templates,
            test_to=test_to,
            test_message=test_message,
        )
        data = self._http.post(
            f"/api/v1/projects/{quote(project_id, safe='')}/channel-connections",
            json_data=body,
        )
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    def get(self, project_id: str, connection_id: str) -> ChannelConnectionDTO:
        """Fetch a channel connection."""
        data = self._http.get(_connection_path(project_id, connection_id))
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    def update(
        self,
        project_id: str,
        connection_id: str,
        *,
        default_agent_id: str | None = None,
        status: ChannelConnectionStatus | str | None = None,
        templates: Any | None = None,
    ) -> ChannelConnectionDTO:
        """Patch mutable channel connection fields."""
        body = encode_body(
            PatchChannelConnectionInputBody,
            {
                "default_agent_id": default_agent_id,
                "status": status,
                "templates": templates,
            },
        )
        data = self._http.patch(_connection_path(project_id, connection_id), json_data=body)
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    def delete(self, project_id: str, connection_id: str) -> None:
        """Delete a channel connection."""
        self._http.delete(_connection_path(project_id, connection_id))

    def test(
        self,
        project_id: str,
        connection_id: str,
        *,
        to: str,
        message: str,
    ) -> ChannelConnectionDTO:
        """Send a test message through a channel connection."""
        body = encode_body(TestChannelConnectionInputBody, {"to": to, "message": message})
        data = self._http.post(
            f"{_connection_path(project_id, connection_id)}/test", json_data=body
        )
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))


class AsyncChannelConnections(_GenAsyncChannelConnections):
    """Async Meta channel connection management."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(self, project_id: str) -> list[ChannelConnectionDTO]:
        """List channel connections for a project."""
        data = await self._http.get(
            f"/api/v1/projects/{quote(project_id, safe='')}/channel-connections"
        )
        result = ChannelConnectionsOutputBody.model_validate(_redact_secrets(data))
        return list(result.connections or result.items or [])

    async def create(
        self,
        project_id: str,
        *,
        channel_type: ChannelConnectionType | str,
        provider_mode: ChannelProviderMode | str = "byo_app",
        app_id: str | None = None,
        app_secret: str | None = None,
        phone_number_id: str | None = None,
        waba_id: str | None = None,
        page_id: str | None = None,
        ig_account_id: str | None = None,
        access_token: str | None = None,
        verify_token: str | None = None,
        display_name: str | None = None,
        code: str | None = None,
        default_agent_id: str | None = None,
        templates: Any | None = None,
        test_to: str | None = None,
        test_message: str | None = None,
    ) -> ChannelConnectionDTO:
        """Create a channel connection."""
        body = _create_body(
            channel_type=channel_type,
            provider_mode=provider_mode,
            app_id=app_id,
            app_secret=app_secret,
            phone_number_id=phone_number_id,
            waba_id=waba_id,
            page_id=page_id,
            ig_account_id=ig_account_id,
            access_token=access_token,
            verify_token=verify_token,
            display_name=display_name,
            code=code,
            default_agent_id=default_agent_id,
            templates=templates,
            test_to=test_to,
            test_message=test_message,
        )
        data = await self._http.post(
            f"/api/v1/projects/{quote(project_id, safe='')}/channel-connections",
            json_data=body,
        )
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    async def get(self, project_id: str, connection_id: str) -> ChannelConnectionDTO:
        """Fetch a channel connection."""
        data = await self._http.get(_connection_path(project_id, connection_id))
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    async def update(
        self,
        project_id: str,
        connection_id: str,
        *,
        default_agent_id: str | None = None,
        status: ChannelConnectionStatus | str | None = None,
        templates: Any | None = None,
    ) -> ChannelConnectionDTO:
        """Patch mutable channel connection fields."""
        body = encode_body(
            PatchChannelConnectionInputBody,
            {
                "default_agent_id": default_agent_id,
                "status": status,
                "templates": templates,
            },
        )
        data = await self._http.patch(_connection_path(project_id, connection_id), json_data=body)
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))

    async def delete(self, project_id: str, connection_id: str) -> None:
        """Delete a channel connection."""
        await self._http.delete(_connection_path(project_id, connection_id))

    async def test(
        self,
        project_id: str,
        connection_id: str,
        *,
        to: str,
        message: str,
    ) -> ChannelConnectionDTO:
        """Send a test message through a channel connection."""
        body = encode_body(TestChannelConnectionInputBody, {"to": to, "message": message})
        data = await self._http.post(
            f"{_connection_path(project_id, connection_id)}/test",
            json_data=body,
        )
        return ChannelConnectionDTO.model_validate(_redact_secrets(data))


def _create_body(
    *,
    channel_type: str,
    provider_mode: str,
    app_id: str | None,
    app_secret: str | None,
    phone_number_id: str | None,
    waba_id: str | None,
    page_id: str | None,
    ig_account_id: str | None,
    access_token: str | None,
    verify_token: str | None,
    display_name: str | None,
    code: str | None,
    default_agent_id: str | None,
    templates: Any | None,
    test_to: str | None,
    test_message: str | None,
) -> dict[str, Any]:
    return encode_body(
        CreateChannelConnectionInputBody,
        {
            "channel_type": channel_type,
            "provider_mode": provider_mode,
            "app_id": app_id,
            "app_secret": app_secret,
            "phone_number_id": phone_number_id,
            "waba_id": waba_id,
            "page_id": page_id,
            "ig_account_id": ig_account_id,
            "access_token": access_token,
            "verify_token": verify_token,
            "display_name": display_name,
            "code": code,
            "default_agent_id": default_agent_id,
            "templates": templates,
            "test_to": test_to,
            "test_message": test_message,
        },
    )


def _connection_path(project_id: str, connection_id: str) -> str:
    return (
        f"/api/v1/projects/{quote(project_id, safe='')}/channel-connections/"
        f"{quote(connection_id, safe='')}"
    )


def _redact_secrets(value: Any) -> Any:
    if isinstance(value, list):
        return [_redact_secrets(item) for item in value]
    if not isinstance(value, dict):
        return value

    redacted: dict[str, Any] = {}
    for key, item in value.items():
        if key in _SECRET_FIELDS:
            continue
        if key == "verify_token" and item is not None:
            redacted[key] = _REDACTED_SECRET
        else:
            redacted[key] = _redact_secrets(item)
    return redacted
