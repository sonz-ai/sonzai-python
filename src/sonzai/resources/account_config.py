"""Account (tenant-scoped) config resource for the Sonzai SDK.

Mirror of :mod:`sonzai.resources.project_config` at the tenant scope. The
tenant is resolved from the API key or Clerk session on the server — never
from a URL parameter — so callers can only read or write config for the
tenant they are currently authenticated to.

Use for settings that should apply to every project inside the tenant
without per-project duplication: for example, the default post-processing
model map (:const:`POST_PROCESSING_MODEL_MAP_KEY`).
"""

from __future__ import annotations

from typing import Any

from .._generated.resources.account_config import AccountConfig as _GenAccountConfig
from .._generated.resources.account_config import AsyncAccountConfig as _GenAsyncAccountConfig
from .._http import AsyncHTTPClient, HTTPClient
from ..post_processing_model import (
    POST_PROCESSING_MODEL_MAP_KEY,
    PostProcessingModelMap,
    decode_post_processing_map,
)
from ..types import AccountConfigEntry, AccountConfigListResponse


class AccountConfig(_GenAccountConfig):
    """Sync account-scope configuration (key-value store)."""

    def __init__(self, http: HTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    def list(self) -> AccountConfigListResponse:
        """List all config entries for the authenticated tenant."""
        data = self._http.get("/api/v1/account/config")
        return AccountConfigListResponse.model_validate(data)

    def get(self, key: str) -> AccountConfigEntry:
        """Get a config value by key."""
        data = self._http.get(f"/api/v1/account/config/{key}")
        return AccountConfigEntry.model_validate(data)

    def set(self, key: str, value: Any) -> dict[str, bool]:
        """Set a config value. Body must be valid JSON."""
        data = self._http.put(
            f"/api/v1/account/config/{key}",
            json_data=value,
        )
        return data  # type: ignore[return-value]

    def delete(self, key: str) -> None:
        """Delete a config entry."""
        self._http.delete(f"/api/v1/account/config/{key}")

    # ------------------------------------------------------------------
    # Typed helpers: post-processing model map
    # ------------------------------------------------------------------

    def get_post_processing_model_map(self) -> PostProcessingModelMap | None:
        """Read the tenant-level post-processing model map.

        Returns ``None`` when no map is configured for the tenant —
        callers can then rely on the system-default layer.
        """
        entry = self.get(POST_PROCESSING_MODEL_MAP_KEY)
        return decode_post_processing_map(entry.value)

    def set_post_processing_model_map(
        self, mapping: PostProcessingModelMap
    ) -> dict[str, bool]:
        """Write the tenant-level post-processing map (full replace)."""
        return self.set(POST_PROCESSING_MODEL_MAP_KEY, mapping)

    def delete_post_processing_model_map(self) -> None:
        """Remove the tenant-level map so the cascade falls through."""
        self.delete(POST_PROCESSING_MODEL_MAP_KEY)


class AsyncAccountConfig(_GenAsyncAccountConfig):
    """Async account-scope configuration (key-value store)."""

    def __init__(self, http: AsyncHTTPClient) -> None:  # TODO(B.3-followup): typed HTTP client
        self._http = http

    async def list(self) -> AccountConfigListResponse:
        data = await self._http.get("/api/v1/account/config")
        return AccountConfigListResponse.model_validate(data)

    async def get(self, key: str) -> AccountConfigEntry:
        data = await self._http.get(f"/api/v1/account/config/{key}")
        return AccountConfigEntry.model_validate(data)

    async def set(self, key: str, value: Any) -> dict[str, bool]:
        data = await self._http.put(
            f"/api/v1/account/config/{key}",
            json_data=value,
        )
        return data  # type: ignore[return-value]

    async def delete(self, key: str) -> None:
        await self._http.delete(f"/api/v1/account/config/{key}")

    async def get_post_processing_model_map(
        self,
    ) -> PostProcessingModelMap | None:
        entry = await self.get(POST_PROCESSING_MODEL_MAP_KEY)
        return decode_post_processing_map(entry.value)

    async def set_post_processing_model_map(
        self, mapping: PostProcessingModelMap
    ) -> dict[str, bool]:
        return await self.set(POST_PROCESSING_MODEL_MAP_KEY, mapping)

    async def delete_post_processing_model_map(self) -> None:
        await self.delete(POST_PROCESSING_MODEL_MAP_KEY)
