"""HTTP transport layer for the Sonzai SDK."""

from __future__ import annotations

import json
import logging
import time
import uuid
from collections.abc import AsyncIterator, Generator, Iterator
from datetime import datetime
from typing import Any

import httpx
from pydantic import ValidationError as _PydanticValidationError

logger = logging.getLogger(__name__)

from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ErrorBody,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)
from ._customizations.chat import (
    ChatCompleteEvent,
    ChatContextReadyEvent,
    ChatDeltaEvent,
    ChatErrorEvent,
    ChatMessageBoundaryEvent,
    ChatSideEffectsEvent,
)
from ._retry import RetryPolicy


def _raise_for_status(response: httpx.Response) -> None:
    """Raise the typed exception matching the response status. Never returns on failure."""
    if response.is_success:
        return

    # For streaming responses, read the body first
    if not hasattr(response, "_content"):
        try:
            response.read()
        except Exception as e:
            logger.debug("Failed to read response: %s", e)

    status = response.status_code
    body = _parse_error_body(response)
    message = _message_from(body, default=f"HTTP {status}")
    code = body.code if body else None

    if status == 401:
        raise AuthenticationError(message, code=code, body=body)
    if status == 403:
        scope = body.model_extra.get("required_scope") if body and body.model_extra else None
        raise PermissionDeniedError(message, required_scope=scope, code=code, body=body)
    if status == 404:
        resource = body.model_extra.get("resource") if body and body.model_extra else None
        raise NotFoundError(message, resource=resource, code=code, body=body)
    if status == 409:
        resource = body.model_extra.get("resource") if body and body.model_extra else None
        raise ConflictError(message, resource=resource, code=code, body=body)
    if status == 422:
        errors = body.errors if body else None
        raise ValidationError(message, errors=errors, body=body)
    if status == 429:
        raise RateLimitError(
            message,
            retry_after=_parse_int(response.headers.get("Retry-After")),
            limit=_parse_int(response.headers.get("X-RateLimit-Limit")),
            remaining=_parse_int(response.headers.get("X-RateLimit-Remaining")),
            reset_at=_parse_reset(response.headers.get("X-RateLimit-Reset")),
            code=code,
            body=body,
        )
    if status == 400:
        raise BadRequestError(message, code=code, body=body)
    if 500 <= status < 600:
        raise InternalServerError(message, status_code=status, code=code, body=body)
    raise APIError(status, message, code=code, body=body)


def _classify_chat_frame(frame: dict[str, Any]) -> Any:
    """Classify a raw SSE frame dict into the correct ChatXxxEvent subclass."""
    if frame.get("error"):
        return ChatErrorEvent.model_validate(frame)
    frame_type = frame.get("type")
    if frame_type == "context_ready":
        return ChatContextReadyEvent.model_validate(frame)
    if frame_type == "side_effects":
        return ChatSideEffectsEvent.model_validate(frame)
    if frame_type == "message_boundary":
        return ChatMessageBoundaryEvent.model_validate(frame)
    if frame.get("finish_reason") or frame.get("full_content"):
        return ChatCompleteEvent.model_validate(frame)
    choices = frame.get("choices") or []
    if choices and isinstance(choices[0], dict) and choices[0].get("finish_reason"):
        return ChatCompleteEvent.model_validate(frame)
    return ChatDeltaEvent.model_validate(frame)


def _parse_error_body(response: httpx.Response) -> ErrorBody | None:
    if not response.content:
        return None
    try:
        data = response.json()
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    try:
        return ErrorBody.model_validate(data)
    except _PydanticValidationError:
        return None


def _message_from(body: ErrorBody | None, *, default: str) -> str:
    if body and body.message:
        return body.message
    return default


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_reset(value: str | None) -> datetime | None:
    ts = _parse_int(value)
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(ts)
    except (OSError, OverflowError, ValueError):
        return None


class HTTPClient:
    """Synchronous HTTP client wrapping httpx."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 2,
        retry: RetryPolicy | None = None,
        httpx_client: httpx.Client | None = None,
    ) -> None:
        if httpx_client is not None:
            self._client = httpx_client
        else:
            self._client = httpx.Client(
                base_url=base_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "sonzai-python/1.4.3",
                },
                timeout=httpx.Timeout(timeout, connect=10.0),
                follow_redirects=True,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        # retry= takes precedence; fall back to legacy max_retries kwarg
        if retry is not None:
            self._retry = retry
        else:
            self._retry = RetryPolicy(max_attempts=max_retries)

    _MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH"})

    def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # Build per-request headers; add Idempotency-Key for mutating methods
        extra_headers: dict[str, str] = {}
        if method.upper() in self._MUTATING_METHODS:
            extra_headers["Idempotency-Key"] = idempotency_key or uuid.uuid4().hex

        attempt = 0
        last_exc: Exception | None = None
        while attempt < self._retry.max_attempts:
            attempt += 1
            try:
                response = self._client.request(
                    method,
                    path,
                    json=json_data,
                    params=params,
                    headers=extra_headers,
                )
            except Exception as exc:
                if not self._retry.should_retry(attempt=attempt, status=None, exc=exc):
                    raise
                last_exc = exc
                logger.debug(
                    "Retrying %s %s (attempt %d/%d) after network error: %s",
                    method,
                    path,
                    attempt,
                    self._retry.max_attempts,
                    exc,
                )
                time.sleep(self._retry.backoff_seconds(attempt=attempt, retry_after_header=None))
                continue

            if response.is_success:
                if response.headers.get("content-type", "").startswith("application/json"):
                    return response.json()
                return response.text

            if self._retry.should_retry(attempt=attempt, status=response.status_code, exc=None):
                logger.debug(
                    "Retrying %s %s (attempt %d/%d) after %d status",
                    method,
                    path,
                    attempt,
                    self._retry.max_attempts,
                    response.status_code,
                )
                time.sleep(
                    self._retry.backoff_seconds(
                        attempt=attempt,
                        retry_after_header=response.headers.get("Retry-After"),
                    )
                )
                continue

            _raise_for_status(response)

        if last_exc is not None:
            raise last_exc
        raise APIError(0, "retries exhausted")  # pragma: no cover

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self.request("POST", path, json_data=json_data, params=params, idempotency_key=idempotency_key)

    def put(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self.request("PUT", path, json_data=json_data, idempotency_key=idempotency_key)

    def patch(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return self.request("PATCH", path, json_data=json_data, idempotency_key=idempotency_key)

    def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("DELETE", path, params=params)

    def upload_file(
        self,
        path: str,
        *,
        file_name: str,
        file_data: bytes,
        content_type: str = "application/octet-stream",
        params: dict[str, Any] | None = None,
    ) -> Any:
        import io

        # Close the BytesIO explicitly. httpx does not guarantee it closes
        # file-like objects it reads from, so without this the underlying
        # buffer sits around until the GC runs. Using `with` ensures the
        # handle is released even if request() raises.
        with io.BytesIO(file_data) as buf:
            files = {"file": (file_name, buf, content_type)}
            response = self._client.request(
                "POST",
                path,
                files=files,
                params=params,
            )
        _raise_for_status(response)
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.text

    def stream_sse(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Send a request and yield parsed SSE events."""
        with self._client.stream(
            method,
            path,
            json=json_data,
            headers={"Accept": "text/event-stream"},
        ) as response:
            _raise_for_status(response)
            # httpx's iter_lines() / aiter_lines() accumulate chunks via LineDecoder
            # without a hard per-line size limit, so large SSE events such as
            # context_ready (which embeds the full enriched context JSON in a single
            # data: line and can exceed 64 KB) are handled correctly.
            yield from _parse_sse_stream(response.iter_lines())

    def close(self) -> None:
        self._client.close()


class AsyncHTTPClient:
    """Asynchronous HTTP client wrapping httpx."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 2,
        retry: RetryPolicy | None = None,
        httpx_client: httpx.AsyncClient | None = None,
    ) -> None:
        if httpx_client is not None:
            self._client = httpx_client
        else:
            self._client = httpx.AsyncClient(
                base_url=base_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "sonzai-python/1.4.3",
                },
                timeout=httpx.Timeout(timeout, connect=10.0),
                follow_redirects=True,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        # retry= takes precedence; fall back to legacy max_retries kwarg
        if retry is not None:
            self._retry = retry
        else:
            self._retry = RetryPolicy(max_attempts=max_retries)

    _MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH"})

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        import asyncio

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # Build per-request headers; add Idempotency-Key for mutating methods
        extra_headers: dict[str, str] = {}
        if method.upper() in self._MUTATING_METHODS:
            extra_headers["Idempotency-Key"] = idempotency_key or uuid.uuid4().hex

        attempt = 0
        last_exc: Exception | None = None
        while attempt < self._retry.max_attempts:
            attempt += 1
            try:
                response = await self._client.request(
                    method,
                    path,
                    json=json_data,
                    params=params,
                    headers=extra_headers,
                )
            except Exception as exc:
                if not self._retry.should_retry(attempt=attempt, status=None, exc=exc):
                    raise
                last_exc = exc
                logger.debug(
                    "Retrying %s %s (attempt %d/%d) after network error: %s",
                    method,
                    path,
                    attempt,
                    self._retry.max_attempts,
                    exc,
                )
                await asyncio.sleep(self._retry.backoff_seconds(attempt=attempt, retry_after_header=None))
                continue

            if response.is_success:
                if response.headers.get("content-type", "").startswith("application/json"):
                    return response.json()
                return response.text

            if self._retry.should_retry(attempt=attempt, status=response.status_code, exc=None):
                logger.debug(
                    "Retrying %s %s (attempt %d/%d) after %d status",
                    method,
                    path,
                    attempt,
                    self._retry.max_attempts,
                    response.status_code,
                )
                await asyncio.sleep(
                    self._retry.backoff_seconds(
                        attempt=attempt,
                        retry_after_header=response.headers.get("Retry-After"),
                    )
                )
                continue

            _raise_for_status(response)

        if last_exc is not None:
            raise last_exc
        raise APIError(0, "retries exhausted")  # pragma: no cover

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self.request("POST", path, json_data=json_data, params=params, idempotency_key=idempotency_key)

    async def put(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self.request("PUT", path, json_data=json_data, idempotency_key=idempotency_key)

    async def patch(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        return await self.request("PATCH", path, json_data=json_data, idempotency_key=idempotency_key)

    async def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("DELETE", path, params=params)

    async def upload_file(
        self,
        path: str,
        *,
        file_name: str,
        file_data: bytes,
        content_type: str = "application/octet-stream",
        params: dict[str, Any] | None = None,
    ) -> Any:
        import io

        # See sync upload_file — explicitly close the BytesIO so we don't
        # rely on GC timing for buffer release.
        with io.BytesIO(file_data) as buf:
            files = {"file": (file_name, buf, content_type)}
            response = await self._client.request(
                "POST",
                path,
                files=files,
                params=params,
            )
        _raise_for_status(response)
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return response.text

    async def stream_sse(
        self, method: str, path: str, *, json_data: dict[str, Any] | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """Send a request and yield parsed SSE events asynchronously."""
        async with self._client.stream(
            method,
            path,
            json=json_data,
            headers={"Accept": "text/event-stream"},
        ) as response:
            _raise_for_status(response)
            # httpx's aiter_lines() accumulates chunks via LineDecoder without a hard
            # per-line size limit, so large SSE events such as context_ready (which
            # embeds the full enriched context JSON in a single data: line and can
            # exceed 64 KB) are handled correctly.
            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                if line == "data: [DONE]":
                    return
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError as e:
                        logger.warning("Malformed SSE event: %s", e)
                        continue

    async def close(self) -> None:
        await self._client.aclose()


def _parse_sse_stream(lines: Iterator[str]) -> Generator[dict[str, Any], None, None]:
    """Parse SSE lines into JSON dicts."""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "data: [DONE]":
            return
        if line.startswith("data: "):
            data = line[6:]
            try:
                yield json.loads(data)
            except json.JSONDecodeError as e:
                logger.warning("Malformed SSE event: %s", e)
                continue
