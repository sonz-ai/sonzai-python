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
    ChatPhaseEvent,
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
    if frame_type == "phase":
        # iter-140u-1: progressive elaboration. Surfaces the agentic
        # loop's lifecycle stage. Naive consumers can drop these via
        # `if isinstance(event, ChatPhaseEvent): continue`.
        return ChatPhaseEvent.model_validate(frame)
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
                    "User-Agent": "sonzai-python/1.8.0",
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
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # Build per-request headers; add Idempotency-Key for mutating methods
        extra_headers: dict[str, str] = {}
        if headers:
            extra_headers.update(headers)
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
                    timeout=_per_request_timeout(timeout),
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

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return self.request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        return self.request(
            "POST",
            path,
            json_data=json_data,
            params=params,
            headers=headers,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

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

    def stream_sse_named(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> Iterator[tuple[str, dict[str, Any]]]:
        """Send a request and yield ``(event_name, data)`` tuples.

        Unlike :meth:`stream_sse` (which discards ``event:`` lines), this
        variant tracks the SSE event name so callers can dispatch on named
        frames such as ``event: update`` / ``event: result`` / ``event: error``.
        Frames without an explicit ``event:`` line are reported with the SSE
        default name ``"message"``.
        """
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        with self._client.stream(
            method,
            path,
            json=json_data,
            params=params,
            headers={"Accept": "text/event-stream"},
            timeout=_per_request_timeout(timeout),
        ) as response:
            _raise_for_status(response)
            yield from _parse_named_sse_stream(response.iter_lines())

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
                    "User-Agent": "sonzai-python/1.8.0",
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
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        import asyncio

        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # Build per-request headers; add Idempotency-Key for mutating methods
        extra_headers: dict[str, str] = {}
        if headers:
            extra_headers.update(headers)
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
                    timeout=_per_request_timeout(timeout),
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

    async def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        return await self.request("GET", path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        return await self.request(
            "POST",
            path,
            json_data=json_data,
            params=params,
            headers=headers,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

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
        """Send a request and yield parsed SSE events asynchronously.

        Supports the ``__chunk`` envelope protocol — see
        :func:`_parse_sse_stream` for the full description.
        """
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
            chunk_buffer: list[str] = []
            chunk_total: int = 0

            async for line in response.aiter_lines():
                line = line.strip()
                if not line:
                    continue
                if line == "data: [DONE]":
                    return
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        parsed = json.loads(data)
                    except json.JSONDecodeError as e:
                        logger.warning("Malformed SSE event: %s", e)
                        continue

                    if isinstance(parsed, dict) and "__chunk" in parsed:
                        chunk_meta = parsed["__chunk"]
                        idx = chunk_meta["index"]
                        total = chunk_meta["total"]
                        piece = parsed["data"]

                        if idx == 0:
                            chunk_buffer = [""] * total
                            chunk_total = total

                        if idx < len(chunk_buffer):
                            chunk_buffer[idx] = piece

                        if (
                            len([p for p in chunk_buffer if p]) == chunk_total
                            and chunk_total > 0
                        ):
                            assembled = "".join(chunk_buffer)
                            chunk_buffer = []
                            chunk_total = 0
                            try:
                                yield json.loads(assembled)
                            except json.JSONDecodeError as e:
                                logger.warning(
                                    "Malformed reassembled chunk payload: %s", e
                                )
                        continue

                    yield parsed

    async def stream_sse_named(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        """Send a request and yield ``(event_name, data)`` tuples asynchronously.

        Async mirror of :meth:`HTTPClient.stream_sse_named` — tracks ``event:``
        lines so callers can dispatch on named frames such as ``event: update``
        / ``event: result`` / ``event: error``. Frames without an explicit
        ``event:`` line are reported with the SSE default name ``"message"``.
        """
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        async with self._client.stream(
            method,
            path,
            json=json_data,
            params=params,
            headers={"Accept": "text/event-stream"},
            timeout=_per_request_timeout(timeout),
        ) as response:
            _raise_for_status(response)
            event_name = _SSE_DEFAULT_EVENT
            async for line in response.aiter_lines():
                item, event_name = _consume_named_sse_line(line, event_name)
                if item is _SSE_STREAM_DONE:
                    return
                if item is not None:
                    yield item  # type: ignore[misc]

    async def close(self) -> None:
        await self._client.aclose()


def _parse_sse_stream(lines: Iterator[str]) -> Generator[dict[str, Any], None, None]:
    """Parse SSE lines into JSON dicts.

    Supports the ``__chunk`` envelope protocol: when a payload is too large for
    a single SSE frame the producer splits it across multiple ``data:`` lines,
    each carrying a ``{"__chunk": {"index": N, "total": M}, "data": "..."}``
    wrapper.  This function buffers the fragments and yields the reassembled
    JSON object once all pieces have arrived.

    Non-chunked events pass through unchanged (backward compatible).
    """
    chunk_buffer: list[str] = []
    chunk_total: int = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "data: [DONE]":
            return
        if line.startswith("data: "):
            data = line[6:]
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError as e:
                logger.warning("Malformed SSE event: %s", e)
                continue

            if isinstance(parsed, dict) and "__chunk" in parsed:
                chunk_meta = parsed["__chunk"]
                idx = chunk_meta["index"]
                total = chunk_meta["total"]
                piece = parsed["data"]

                if idx == 0:
                    chunk_buffer = [""] * total
                    chunk_total = total

                if idx < len(chunk_buffer):
                    chunk_buffer[idx] = piece

                if len([p for p in chunk_buffer if p]) == chunk_total and chunk_total > 0:
                    assembled = "".join(chunk_buffer)
                    chunk_buffer = []
                    chunk_total = 0
                    try:
                        yield json.loads(assembled)
                    except json.JSONDecodeError as e:
                        logger.warning("Malformed reassembled chunk payload: %s", e)
                continue

            yield parsed


def _per_request_timeout(timeout: float | None) -> httpx.Timeout | Any:
    """Map an optional per-request timeout override to the httpx argument.

    ``None`` means "use whatever the client was constructed with". A float
    sets the total/read/write/pool timeout while keeping the same 10s connect
    budget the client-level default uses — long-running calls (e.g. built-in
    agent invocations) need a generous read timeout, not a slow handshake.
    """
    if timeout is None:
        return httpx.USE_CLIENT_DEFAULT
    return httpx.Timeout(timeout, connect=10.0)


# Named-event SSE parsing (event:/data: pairs) -------------------------------
#
# `_parse_sse_stream` above predates endpoints that dispatch on the SSE event
# name (it drops `event:` lines entirely). The built-in agents endpoints frame
# their streams as `event: update` / `event: result` / `event: error`, so the
# helpers below track the most recent `event:` line and pair it with the next
# `data:` payload. Per the SSE spec the event name applies to the dispatch it
# precedes, then resets to the default ("message").

_SSE_DEFAULT_EVENT = "message"

# Sentinel distinguishing "stream finished" ([DONE]) from "no event yet".
_SSE_STREAM_DONE: tuple[str, dict[str, Any]] = ("__done__", {})


def _consume_named_sse_line(
    line: str, event_name: str
) -> tuple[tuple[str, dict[str, Any]] | None, str]:
    """Consume one SSE line; return ``(item, next_event_name)``.

    ``item`` is ``None`` when the line carries no dispatchable payload (blank
    line, ``event:`` line, malformed JSON), ``_SSE_STREAM_DONE`` on the
    ``data: [DONE]`` terminator, and a ``(event_name, payload)`` tuple when a
    ``data:`` line completes a frame.
    """
    line = line.strip()
    if not line:
        # Frame boundary — the pending event name (if any) was already
        # consumed by its data line; reset defensively per the SSE spec.
        return None, _SSE_DEFAULT_EVENT
    if line.startswith("event:"):
        return None, line[len("event:") :].strip() or _SSE_DEFAULT_EVENT
    if line == "data: [DONE]":
        return _SSE_STREAM_DONE, _SSE_DEFAULT_EVENT
    if line.startswith("data:"):
        data = line[len("data:") :].strip()
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as e:
            logger.warning("Malformed SSE event: %s", e)
            return None, event_name
        if not isinstance(parsed, dict):
            logger.warning("Ignoring non-object SSE payload: %r", parsed)
            return None, event_name
        # Dispatch resets the event name to the default per the SSE spec.
        return (event_name, parsed), _SSE_DEFAULT_EVENT
    # Comments (`: keepalive`) and unknown fields are ignored.
    return None, event_name


def _parse_named_sse_stream(
    lines: Iterator[str],
) -> Generator[tuple[str, dict[str, Any]], None, None]:
    """Parse named-event SSE lines into ``(event_name, payload)`` tuples."""
    event_name = _SSE_DEFAULT_EVENT
    for line in lines:
        item, event_name = _consume_named_sse_line(line, event_name)
        if item is _SSE_STREAM_DONE:
            return
        if item is not None:
            yield item
