"""HTTP transport layer for the Sonzai SDK."""

from __future__ import annotations

import json
import logging
import time
from collections.abc import AsyncIterator, Generator, Iterator
from typing import Any

import httpx

logger = logging.getLogger(__name__)

from ._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return

    # For streaming responses, read the body first
    if not hasattr(response, "_content"):
        try:
            response.read()
        except Exception as e:
            logger.debug("Failed to read response: %s", e)

    try:
        body = response.json()
        message = body.get("error", response.text)
    except Exception as e:
        logger.debug("Failed to read response: %s", e)
        try:
            message = response.text
        except Exception as e:
            logger.debug("Failed to read response: %s", e)
            message = f"HTTP {response.status_code}"

    status = response.status_code
    if status == 401:
        raise AuthenticationError(message)
    elif status == 403:
        raise PermissionDeniedError(message)
    elif status == 404:
        raise NotFoundError(message)
    elif status == 400:
        raise BadRequestError(message)
    elif status == 429:
        raise RateLimitError(message)
    elif status >= 500:
        raise InternalServerError(message)
    else:
        raise APIError(status, message)


class HTTPClient:
    """Synchronous HTTP client wrapping httpx."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
        max_retries: int = 2,
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
                    "User-Agent": "sonzai-python/1.2.0",
                },
                timeout=httpx.Timeout(timeout, connect=10.0),
                follow_redirects=True,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        self._max_retries = max_retries

    _RETRYABLE_METHODS = frozenset({"GET", "DELETE"})

    def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        retries = self._max_retries if method.upper() in self._RETRYABLE_METHODS else 0

        for attempt in range(retries + 1):
            try:
                response = self._client.request(
                    method,
                    path,
                    json=json_data,
                    params=params,
                )
                if response.status_code >= 500 and attempt < retries:
                    logger.debug(
                        "Retrying %s %s (attempt %d/%d) after %d status",
                        method,
                        path,
                        attempt + 1,
                        retries,
                        response.status_code,
                    )
                    time.sleep(0.5 * 2**attempt)
                    continue
                _raise_for_status(response)

                if response.headers.get("content-type", "").startswith("application/json"):
                    return response.json()
                return response.text
            except httpx.TransportError as exc:
                if attempt < retries:
                    logger.debug(
                        "Retrying %s %s (attempt %d/%d) after transport error: %s",
                        method,
                        path,
                        attempt + 1,
                        retries,
                        exc,
                    )
                    time.sleep(0.5 * 2**attempt)
                    continue
                raise

        # Unreachable, but satisfies type checkers
        raise InternalServerError("Max retries exceeded")  # pragma: no cover

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return self.request("POST", path, json_data=json_data, params=params)

    def put(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        return self.request("PUT", path, json_data=json_data)

    def patch(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        return self.request("PATCH", path, json_data=json_data)

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

        files = {"file": (file_name, io.BytesIO(file_data), content_type)}
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
                    "User-Agent": "sonzai-python/1.2.0",
                },
                timeout=httpx.Timeout(timeout, connect=10.0),
                follow_redirects=True,
                limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            )
        self._max_retries = max_retries

    _RETRYABLE_METHODS = frozenset({"GET", "DELETE"})

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        retries = self._max_retries if method.upper() in self._RETRYABLE_METHODS else 0
        import asyncio

        for attempt in range(retries + 1):
            try:
                response = await self._client.request(
                    method,
                    path,
                    json=json_data,
                    params=params,
                )
                if response.status_code >= 500 and attempt < retries:
                    logger.debug(
                        "Retrying %s %s (attempt %d/%d) after %d status",
                        method,
                        path,
                        attempt + 1,
                        retries,
                        response.status_code,
                    )
                    await asyncio.sleep(0.5 * 2**attempt)
                    continue
                _raise_for_status(response)

                if response.headers.get("content-type", "").startswith("application/json"):
                    return response.json()
                return response.text
            except httpx.TransportError as exc:
                if attempt < retries:
                    logger.debug(
                        "Retrying %s %s (attempt %d/%d) after transport error: %s",
                        method,
                        path,
                        attempt + 1,
                        retries,
                        exc,
                    )
                    await asyncio.sleep(0.5 * 2**attempt)
                    continue
                raise

        # Unreachable, but satisfies type checkers
        raise InternalServerError("Max retries exceeded")  # pragma: no cover

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("POST", path, json_data=json_data, params=params)

    async def put(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("PUT", path, json_data=json_data)

    async def patch(
        self,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("PATCH", path, json_data=json_data)

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

        files = {"file": (file_name, io.BytesIO(file_data), content_type)}
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
