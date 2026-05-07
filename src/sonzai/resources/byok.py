"""BYOK (Bring-Your-Own-Key) resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Literal

from .._generated.models import (
    BYOKKeyResponse,
    ListBYOKKeysOutputBody,
    PutBYOKKeyInputBody,
    SetBYOKActiveInputBody,
)
from .._generated.resources.byok import AsyncByok as _GenAsyncByok
from .._generated.resources.byok import Byok as _GenByok
from .._http import AsyncHTTPClient, HTTPClient
from .._request_helpers import encode_body

BYOKProvider = Literal["openai", "gemini", "xai", "openrouter"]


class BYOK(_GenByok):
    """Sync BYOK key management for a project."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def list(self, project_id: str) -> list[BYOKKeyResponse]:
        """List BYOK keys configured for a project."""
        data = self._http.get(f"/api/v1/projects/{project_id}/byok-keys")
        result = ListBYOKKeysOutputBody.model_validate(data)
        return list(result.keys or [])

    def set(
        self,
        project_id: str,
        provider: BYOKProvider,
        *,
        api_key: str,
    ) -> BYOKKeyResponse:
        """Create or replace a BYOK key for a provider."""
        body = encode_body(PutBYOKKeyInputBody, {"api_key": api_key})
        data = self._http.put(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}",
            json_data=body,
        )
        return BYOKKeyResponse.model_validate(data)

    def delete(self, project_id: str, provider: BYOKProvider) -> None:
        """Delete a stored BYOK key."""
        self._http.delete(f"/api/v1/projects/{project_id}/byok-keys/{provider}")

    def set_active(
        self,
        project_id: str,
        provider: BYOKProvider,
        *,
        is_active: bool,
    ) -> BYOKKeyResponse:
        """Enable or disable a BYOK key without rotating it."""
        body = encode_body(SetBYOKActiveInputBody, {"is_active": is_active})
        data = self._http.patch(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}",
            json_data=body,
        )
        return BYOKKeyResponse.model_validate(data)

    def test(self, project_id: str, provider: BYOKProvider) -> BYOKKeyResponse:
        """Re-test a stored BYOK key against the provider."""
        data = self._http.post(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}/test"
        )
        return BYOKKeyResponse.model_validate(data)


class AsyncBYOK(_GenAsyncByok):
    """Async BYOK key management for a project."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def list(self, project_id: str) -> list[BYOKKeyResponse]:
        """List BYOK keys configured for a project."""
        data = await self._http.get(f"/api/v1/projects/{project_id}/byok-keys")
        result = ListBYOKKeysOutputBody.model_validate(data)
        return list(result.keys or [])

    async def set(
        self,
        project_id: str,
        provider: BYOKProvider,
        *,
        api_key: str,
    ) -> BYOKKeyResponse:
        """Create or replace a BYOK key for a provider."""
        body = encode_body(PutBYOKKeyInputBody, {"api_key": api_key})
        data = await self._http.put(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}",
            json_data=body,
        )
        return BYOKKeyResponse.model_validate(data)

    async def delete(self, project_id: str, provider: BYOKProvider) -> None:
        """Delete a stored BYOK key."""
        await self._http.delete(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}"
        )

    async def set_active(
        self,
        project_id: str,
        provider: BYOKProvider,
        *,
        is_active: bool,
    ) -> BYOKKeyResponse:
        """Enable or disable a BYOK key without rotating it."""
        body = encode_body(SetBYOKActiveInputBody, {"is_active": is_active})
        data = await self._http.patch(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}",
            json_data=body,
        )
        return BYOKKeyResponse.model_validate(data)

    async def test(self, project_id: str, provider: BYOKProvider) -> BYOKKeyResponse:
        """Re-test a stored BYOK key against the provider."""
        data = await self._http.post(
            f"/api/v1/projects/{project_id}/byok-keys/{provider}/test"
        )
        return BYOKKeyResponse.model_validate(data)
