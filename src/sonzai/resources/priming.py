"""User priming resource for the Sonzai SDK."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    AddContentResponse,
    BatchImportResponse,
    ImportJob,
    ImportJobListResponse,
    ListImportJobUsersResponse,
    PrimeUserResponse,
    UpdateMetadataResponse,
    UserPrimingMetadata,
)


class Priming:
    """Sync user priming operations for an agent."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def prime_user(
        self,
        agent_id: str,
        user_id: str,
        *,
        display_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        content: list[dict[str, str]] | None = None,
        source: str | None = None,
    ) -> PrimeUserResponse:
        """Prime a user with metadata and content."""
        body: dict[str, Any] = {}
        if display_name is not None:
            body["display_name"] = display_name
        if metadata is not None:
            body["metadata"] = metadata
        if content is not None:
            body["content"] = content
        if source is not None:
            body["source"] = source
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/prime",
            json_data=body,
        )
        return PrimeUserResponse.model_validate(data)

    def get_prime_status(self, agent_id: str, user_id: str, job_id: str) -> ImportJob:
        """Get the status of a priming job."""
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/prime/{job_id}"
        )
        return ImportJob.model_validate(data)

    def add_content(
        self,
        agent_id: str,
        user_id: str,
        *,
        content: list[dict[str, str]],
        source: str | None = None,
    ) -> AddContentResponse:
        """Add content blocks for async LLM extraction."""
        body: dict[str, Any] = {"content": content}
        if source is not None:
            body["source"] = source
        data = self._http.post(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/content",
            json_data=body,
        )
        return AddContentResponse.model_validate(data)

    def get_metadata(self, agent_id: str, user_id: str) -> UserPrimingMetadata:
        """Get priming metadata for a user."""
        data = self._http.get(f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/metadata")
        return UserPrimingMetadata.model_validate(data)

    def update_metadata(self, agent_id: str, user_id: str, **kwargs: Any) -> UpdateMetadataResponse:
        """Partially update priming metadata.

        Custom fields in the ``custom`` dict are merged with existing values,
        not replaced. Omit ``custom`` to leave it unchanged.
        """
        data = self._http.patch(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/metadata",
            json_data=kwargs,
        )
        return UpdateMetadataResponse.model_validate(data)

    def batch_import(
        self,
        agent_id: str,
        *,
        users: list[dict[str, Any]],
        source: str | None = None,
    ) -> BatchImportResponse:
        """Batch import multiple users."""
        body: dict[str, Any] = {"users": users}
        if source is not None:
            body["source"] = source
        data = self._http.post(f"/api/v1/agents/{agent_id}/users/import", json_data=body)
        return BatchImportResponse.model_validate(data)

    def get_import_status(self, agent_id: str, job_id: str) -> ImportJob:
        """Get the status of a batch import job."""
        data = self._http.get(f"/api/v1/agents/{agent_id}/users/import/{job_id}")
        return ImportJob.model_validate(data)

    def list_import_jobs(self, agent_id: str, *, limit: int | None = None) -> ImportJobListResponse:
        """List recent import jobs."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(f"/api/v1/agents/{agent_id}/users/imports", params=params)
        return ImportJobListResponse.model_validate(data)

    def list_import_job_users(
        self, agent_id: str, job_id: str, *, limit: int | None = None
    ) -> ListImportJobUsersResponse:
        """List per-user progress rows for a batch import job.

        Returns one row per user the priming worker has started, with status,
        fact counts, warmth score, and any error message — useful for
        diagnosing stuck or failed users during a large migration.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = self._http.get(
            f"/api/v1/agents/{agent_id}/users/import/{job_id}/users", params=params
        )
        return ListImportJobUsersResponse.model_validate(data)


class AsyncPriming:
    """Async user priming operations for an agent."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def prime_user(self, agent_id: str, user_id: str, **kwargs: Any) -> PrimeUserResponse:
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/prime",
            json_data=kwargs,
        )
        return PrimeUserResponse.model_validate(data)

    async def get_prime_status(self, agent_id: str, user_id: str, job_id: str) -> ImportJob:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/prime/{job_id}"
        )
        return ImportJob.model_validate(data)

    async def add_content(self, agent_id: str, user_id: str, **kwargs: Any) -> AddContentResponse:
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/content",
            json_data=kwargs,
        )
        return AddContentResponse.model_validate(data)

    async def get_metadata(self, agent_id: str, user_id: str) -> UserPrimingMetadata:
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/metadata"
        )
        return UserPrimingMetadata.model_validate(data)

    async def update_metadata(
        self, agent_id: str, user_id: str, **kwargs: Any
    ) -> UpdateMetadataResponse:
        data = await self._http.patch(
            f"/api/v1/agents/{agent_id}/users/{quote(user_id, safe='')}/metadata",
            json_data=kwargs,
        )
        return UpdateMetadataResponse.model_validate(data)

    async def batch_import(self, agent_id: str, **kwargs: Any) -> BatchImportResponse:
        data = await self._http.post(f"/api/v1/agents/{agent_id}/users/import", json_data=kwargs)
        return BatchImportResponse.model_validate(data)

    async def get_import_status(self, agent_id: str, job_id: str) -> ImportJob:
        data = await self._http.get(f"/api/v1/agents/{agent_id}/users/import/{job_id}")
        return ImportJob.model_validate(data)

    async def list_import_jobs(
        self, agent_id: str, *, limit: int | None = None
    ) -> ImportJobListResponse:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(f"/api/v1/agents/{agent_id}/users/imports", params=params)
        return ImportJobListResponse.model_validate(data)

    async def list_import_job_users(
        self, agent_id: str, job_id: str, *, limit: int | None = None
    ) -> ListImportJobUsersResponse:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        data = await self._http.get(
            f"/api/v1/agents/{agent_id}/users/import/{job_id}/users", params=params
        )
        return ListImportJobUsersResponse.model_validate(data)
