"""Workbench resource for the Sonzai SDK.

Interactive testing sandbox: prepare a workbench session, simulate users,
advance time, and inspect state. Request/response shapes are currently
untyped on the server side — pass plain dicts for bodies, receive dicts
back. When Huma adds schemas, we can tighten these.
"""

from __future__ import annotations

from typing import Any

from .._http import AsyncHTTPClient, HTTPClient


class Workbench:
    """Sync workbench operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def prepare(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Prepare the workbench for a run."""
        return self._http.post("/api/v1/workbench/prepare", json_data=body or {})

    def get_state(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get current workbench state."""
        return self._http.post("/api/v1/workbench/state", json_data=body or {})

    def advance_time(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Advance simulated time in the workbench."""
        return self._http.post("/api/v1/workbench/advance-time", json_data=body or {})

    def chat(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a workbench chat turn (non-streaming)."""
        return self._http.post("/api/v1/workbench/chat", json_data=body or {})

    def simulate_user(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate a simulated user turn."""
        return self._http.post("/api/v1/workbench/simulate-user", json_data=body or {})

    def session_end(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Trigger session-end processing."""
        return self._http.post("/api/v1/workbench/session-end", json_data=body or {})

    def reset_agent(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Reset the workbench agent's data."""
        return self._http.post("/api/v1/workbench/reset-agent", json_data=body or {})

    def generate_bio(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate an agent bio from current workbench context."""
        return self._http.post("/api/v1/workbench/generate-bio", json_data=body or {})

    def generate_character(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate a full character (personality + bio + seed memories)."""
        return self._http.post("/api/v1/workbench/generate-character", json_data=body or {})

    def generate_seed_memories(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate agent seed memories."""
        return self._http.post("/api/v1/workbench/generate-seed-memories", json_data=body or {})


class AsyncWorkbench:
    """Async workbench operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def prepare(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Prepare the workbench for a run."""
        return await self._http.post("/api/v1/workbench/prepare", json_data=body or {})

    async def get_state(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get current workbench state."""
        return await self._http.post("/api/v1/workbench/state", json_data=body or {})

    async def advance_time(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Advance simulated time in the workbench."""
        return await self._http.post("/api/v1/workbench/advance-time", json_data=body or {})

    async def chat(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a workbench chat turn (non-streaming)."""
        return await self._http.post("/api/v1/workbench/chat", json_data=body or {})

    async def simulate_user(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate a simulated user turn."""
        return await self._http.post("/api/v1/workbench/simulate-user", json_data=body or {})

    async def session_end(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Trigger session-end processing."""
        return await self._http.post("/api/v1/workbench/session-end", json_data=body or {})

    async def reset_agent(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Reset the workbench agent's data."""
        return await self._http.post("/api/v1/workbench/reset-agent", json_data=body or {})

    async def generate_bio(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate an agent bio from current workbench context."""
        return await self._http.post("/api/v1/workbench/generate-bio", json_data=body or {})

    async def generate_character(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate a full character (personality + bio + seed memories)."""
        return await self._http.post("/api/v1/workbench/generate-character", json_data=body or {})

    async def generate_seed_memories(self, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generate agent seed memories."""
        return await self._http.post("/api/v1/workbench/generate-seed-memories", json_data=body or {})
