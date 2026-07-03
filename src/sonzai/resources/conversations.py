"""Omnichannel conversations resource for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, Literal, cast
from urllib.parse import quote, urlencode

from .._generated.models import (
    ConversationBody,
    ConversationDetailBody,
    OmnichannelConversationDTO,
    OmnichannelMessageDTO,
    PatchConversationInputBody,
    SendConversationMessageInputBody,
)
from .._generated.resources.conversations import AsyncConversations as _GenAsyncConversations
from .._generated.resources.conversations import Conversations as _GenConversations
from .._http import AsyncHTTPClient, HTTPClient
from .._pagination import AsyncPage, Page
from .._request_helpers import encode_body

ConversationController = Literal["agent", "human"]
ConversationStatus = Literal["open", "snoozed", "closed"]


class Conversations(_GenConversations):
    """Sync omnichannel conversation operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        project_id: str | None = None,
        channel: str | None = None,
        agent_id: str | None = None,
        user_id: str | None = None,
        controller: ConversationController | str | None = None,
        status: ConversationStatus | str | None = None,
        q: str | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> Page[ConversationBody]:
        """List conversations with cursor pagination."""
        params = _conversation_params(
            project_id=project_id,
            channel=channel,
            agent_id=agent_id,
            user_id=user_id,
            controller=controller,
            status=status,
            q=q,
            cursor=cursor,
            limit=limit,
        )
        return Page(
            fetcher=lambda p: self._http.get("/api/v1/conversations", params=p),
            params=params,
            item_key="conversations",
            item_parser=ConversationBody.model_validate,
            mode="cursor",
            total_key="total",
        )

    def get(self, conversation_id: str) -> ConversationDetailBody:
        """Fetch a single conversation."""
        data = self._http.get(f"/api/v1/conversations/{quote(conversation_id, safe='')}")
        return ConversationDetailBody.model_validate(data)

    def messages(
        self,
        conversation_id: str,
        *,
        cursor: str | None = None,
        limit: int = 100,
    ) -> Page[OmnichannelMessageDTO]:
        """List conversation messages with cursor pagination."""
        params: dict[str, Any] = {"limit": limit, "cursor": cursor}
        path = f"/api/v1/conversations/{quote(conversation_id, safe='')}/messages"
        return Page(
            fetcher=lambda p: self._http.get(path, params=p),
            params=params,
            item_key="items",
            item_parser=OmnichannelMessageDTO.model_validate,
            mode="cursor",
        )

    def stream(self, *, project_id: str | None = None) -> Iterator[dict[str, Any]]:
        """Stream conversation events over SSE."""
        yield from self._http.stream_sse("GET", _stream_path(project_id=project_id))

    def take_over(
        self,
        conversation_id: str,
        *,
        operator_id: str | None = None,
        force: bool | None = None,
    ) -> OmnichannelConversationDTO:
        """Take over a conversation for a human operator."""
        params: dict[str, Any] = {}
        if operator_id is not None:
            params["operator_id"] = operator_id
        if force is not None:
            params["force"] = force
        data = self._http.post(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/takeover",
            params=params,
        )
        return OmnichannelConversationDTO.model_validate(data)

    def release(self, conversation_id: str) -> OmnichannelConversationDTO:
        """Release a human takeover back to the agent."""
        data = self._http.delete(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/takeover"
        )
        if isinstance(data, dict):
            return OmnichannelConversationDTO.model_validate(data)
        return OmnichannelConversationDTO.model_construct()

    def send_as_agent(
        self,
        conversation_id: str,
        *,
        content: str,
        attachments: Any | None = None,
    ) -> OmnichannelConversationDTO:
        """Send an agent/operator-authored conversation message."""
        body = encode_body(
            SendConversationMessageInputBody,
            {"content": content, "attachments": attachments},
        )
        data = self._http.post(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/messages",
            json_data=body,
        )
        return OmnichannelConversationDTO.model_validate(data)

    def mark_read(self, conversation_id: str) -> OmnichannelConversationDTO:
        """Mark a conversation read."""
        data = self._http.post(f"/api/v1/conversations/{quote(conversation_id, safe='')}/read")
        return OmnichannelConversationDTO.model_validate(data)

    def update(
        self,
        conversation_id: str,
        *,
        agent_id: str | None = None,
        status: ConversationStatus | str | None = None,
    ) -> OmnichannelConversationDTO:
        """Patch mutable conversation fields."""
        body = encode_body(PatchConversationInputBody, {"agent_id": agent_id, "status": status})
        data = self._http.patch(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}",
            json_data=body,
        )
        return OmnichannelConversationDTO.model_validate(data)


class AsyncConversations(_GenAsyncConversations):
    """Async omnichannel conversation operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        project_id: str | None = None,
        channel: str | None = None,
        agent_id: str | None = None,
        user_id: str | None = None,
        controller: ConversationController | str | None = None,
        status: ConversationStatus | str | None = None,
        q: str | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> AsyncPage[ConversationBody]:
        """List conversations with cursor pagination."""
        params = _conversation_params(
            project_id=project_id,
            channel=channel,
            agent_id=agent_id,
            user_id=user_id,
            controller=controller,
            status=status,
            q=q,
            cursor=cursor,
            limit=limit,
        )

        async def fetcher(p: dict[str, Any]) -> dict[str, Any]:
            return cast(dict[str, Any], await self._http.get("/api/v1/conversations", params=p))

        return AsyncPage(
            fetcher=fetcher,
            params=params,
            item_key="conversations",
            item_parser=ConversationBody.model_validate,
            mode="cursor",
            total_key="total",
        )

    async def get(self, conversation_id: str) -> ConversationDetailBody:
        """Fetch a single conversation."""
        data = await self._http.get(f"/api/v1/conversations/{quote(conversation_id, safe='')}")
        return ConversationDetailBody.model_validate(data)

    async def messages(
        self,
        conversation_id: str,
        *,
        cursor: str | None = None,
        limit: int = 100,
    ) -> AsyncPage[OmnichannelMessageDTO]:
        """List conversation messages with cursor pagination."""
        params: dict[str, Any] = {"limit": limit, "cursor": cursor}
        path = f"/api/v1/conversations/{quote(conversation_id, safe='')}/messages"

        async def fetcher(p: dict[str, Any]) -> dict[str, Any]:
            return cast(dict[str, Any], await self._http.get(path, params=p))

        return AsyncPage(
            fetcher=fetcher,
            params=params,
            item_key="items",
            item_parser=OmnichannelMessageDTO.model_validate,
            mode="cursor",
        )

    async def stream(self, *, project_id: str | None = None) -> AsyncIterator[dict[str, Any]]:
        """Stream conversation events over SSE."""
        async for event in self._http.stream_sse("GET", _stream_path(project_id=project_id)):
            yield event

    async def take_over(
        self,
        conversation_id: str,
        *,
        operator_id: str | None = None,
        force: bool | None = None,
    ) -> OmnichannelConversationDTO:
        """Take over a conversation for a human operator."""
        params: dict[str, Any] = {}
        if operator_id is not None:
            params["operator_id"] = operator_id
        if force is not None:
            params["force"] = force
        data = await self._http.post(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/takeover",
            params=params,
        )
        return OmnichannelConversationDTO.model_validate(data)

    async def release(self, conversation_id: str) -> OmnichannelConversationDTO:
        """Release a human takeover back to the agent."""
        data = await self._http.delete(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/takeover"
        )
        if isinstance(data, dict):
            return OmnichannelConversationDTO.model_validate(data)
        return OmnichannelConversationDTO.model_construct()

    async def send_as_agent(
        self,
        conversation_id: str,
        *,
        content: str,
        attachments: Any | None = None,
    ) -> OmnichannelConversationDTO:
        """Send an agent/operator-authored conversation message."""
        body = encode_body(
            SendConversationMessageInputBody,
            {"content": content, "attachments": attachments},
        )
        data = await self._http.post(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/messages",
            json_data=body,
        )
        return OmnichannelConversationDTO.model_validate(data)

    async def mark_read(self, conversation_id: str) -> OmnichannelConversationDTO:
        """Mark a conversation read."""
        data = await self._http.post(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}/read"
        )
        return OmnichannelConversationDTO.model_validate(data)

    async def update(
        self,
        conversation_id: str,
        *,
        agent_id: str | None = None,
        status: ConversationStatus | str | None = None,
    ) -> OmnichannelConversationDTO:
        """Patch mutable conversation fields."""
        body = encode_body(PatchConversationInputBody, {"agent_id": agent_id, "status": status})
        data = await self._http.patch(
            f"/api/v1/conversations/{quote(conversation_id, safe='')}",
            json_data=body,
        )
        return OmnichannelConversationDTO.model_validate(data)


def _conversation_params(
    *,
    project_id: str | None,
    channel: str | None,
    agent_id: str | None,
    user_id: str | None,
    controller: str | None,
    status: str | None,
    q: str | None,
    cursor: str | None,
    limit: int,
) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "channel": channel,
        "agent_id": agent_id,
        "user_id": user_id,
        "controller": controller,
        "status": status,
        "q": q,
        "cursor": cursor,
        "limit": limit,
    }


def _stream_path(*, project_id: str | None) -> str:
    path = "/api/v1/conversations/stream"
    if project_id is None:
        return path
    return f"{path}?{urlencode({'project_id': project_id})}"
