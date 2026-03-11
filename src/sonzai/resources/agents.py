"""Agent-scoped resources for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    ChatMessage,
    ChatResponse,
    ChatStreamEvent,
    ChatUsage,
    DiaryResponse,
    EvaluationResult,
    GoalsResponse,
    HabitsResponse,
    InterestsResponse,
    MoodResponse,
    RelationshipResponse,
    SimulationEvent,
    UsersResponse,
)
from .instances import AsyncInstances, Instances
from .memory import AsyncMemory, Memory
from .notifications import AsyncNotifications, Notifications
from .personality import AsyncPersonality, Personality
from .sessions import AsyncSessions, Sessions


class Agents:
    """Sync agent operations: chat, evaluate, simulate, and sub-resources."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http
        self.memory = Memory(http)
        self.personality = Personality(http)
        self.sessions = Sessions(http)
        self.instances = Instances(http)
        self.notifications = Notifications(http)

    def chat(
        self,
        agent_id: str,
        *,
        messages: list[ChatMessage | dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        stream: bool = False,
    ) -> ChatResponse | Iterator[ChatStreamEvent]:
        """Send a chat message to an agent.

        Args:
            agent_id: The agent to chat with.
            messages: List of messages (dicts with 'role' and 'content').
            user_id: Optional user identifier (defaults to 'api-user' server-side).
            session_id: Optional session ID (auto-created if omitted).
            instance_id: Optional instance ID for scoped sessions.
            stream: If True, return an iterator of ChatStreamEvent.

        Returns:
            ChatResponse if stream=False, Iterator[ChatStreamEvent] if stream=True.
        """
        msgs = [
            m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
        ]
        body: dict[str, Any] = {"messages": msgs}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id

        path = f"/api/v1/agents/{agent_id}/chat"

        if stream:
            return self._stream_chat(path, body)

        return self._chat_sync(path, body)

    def _chat_sync(self, path: str, body: dict[str, Any]) -> ChatResponse:
        """Consume SSE stream and return aggregated response."""
        content_parts: list[str] = []
        usage = None
        session_id = ""

        for event in self._http.stream_sse("POST", path, json_data=body):
            parsed = ChatStreamEvent.model_validate(event)
            if parsed.content:
                content_parts.append(parsed.content)
            if parsed.usage:
                usage = parsed.usage

        return ChatResponse(
            content="".join(content_parts),
            session_id=session_id,
            usage=usage,
        )

    def _stream_chat(
        self, path: str, body: dict[str, Any]
    ) -> Iterator[ChatStreamEvent]:
        for event in self._http.stream_sse("POST", path, json_data=body):
            yield ChatStreamEvent.model_validate(event)

    def evaluate(
        self,
        agent_id: str,
        *,
        messages: list[ChatMessage | dict[str, str]],
        template_id: str,
        config_override: dict[str, Any] | None = None,
    ) -> EvaluationResult:
        """Evaluate an agent against a template."""
        msgs = [
            m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
        ]
        body: dict[str, Any] = {"messages": msgs, "template_id": template_id}
        if config_override:
            body["config_override"] = config_override

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/evaluate", json_data=body
        )
        return EvaluationResult.model_validate(data)

    def simulate(
        self,
        agent_id: str,
        *,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
    ) -> Iterator[SimulationEvent]:
        """Run a simulation and stream events."""
        body: dict[str, Any] = {}
        if sessions is not None:
            body["sessions"] = sessions
        if user_persona is not None:
            body["user_persona"] = user_persona
        if config is not None:
            body["config"] = config
        if model is not None:
            body["model"] = model
        if config_override is not None:
            body["config_override"] = config_override

        for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/simulate", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    def run_eval(
        self,
        agent_id: str,
        *,
        template_id: str,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        simulation_config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
        adaptation_template_id: str | None = None,
    ) -> Iterator[SimulationEvent]:
        """Run simulation + evaluation combined."""
        body: dict[str, Any] = {"template_id": template_id}
        if sessions is not None:
            body["sessions"] = sessions
        if user_persona is not None:
            body["user_persona"] = user_persona
        if simulation_config is not None:
            body["simulation_config"] = simulation_config
        if model is not None:
            body["model"] = model
        if config_override is not None:
            body["config_override"] = config_override
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id

        for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/run-eval", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    def eval_only(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
    ) -> Iterator[SimulationEvent]:
        """Re-evaluate an existing run."""
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id

        for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/eval-only", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    # -- Context Engine convenience accessors --

    def get_mood(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/mood", params=params)
        return MoodResponse.model_validate(data)

    def get_mood_history(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/mood-history", params=params)
        return MoodResponse.model_validate(data)

    def get_relationships(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> RelationshipResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/relationships", params=params)
        return RelationshipResponse.model_validate(data)

    def get_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/habits", params=params)
        return HabitsResponse.model_validate(data)

    def get_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/goals", params=params)
        return GoalsResponse.model_validate(data)

    def get_interests(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> InterestsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/interests", params=params)
        return InterestsResponse.model_validate(data)

    def get_diary(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> DiaryResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/diary", params=params)
        return DiaryResponse.model_validate(data)

    def get_users(self, agent_id: str) -> UsersResponse:
        data = self._http.get(f"/api/v1/agents/{agent_id}/users")
        return UsersResponse.model_validate(data)


class AsyncAgents:
    """Async agent operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http
        self.memory = AsyncMemory(http)
        self.personality = AsyncPersonality(http)
        self.sessions = AsyncSessions(http)
        self.instances = AsyncInstances(http)
        self.notifications = AsyncNotifications(http)

    async def chat(
        self,
        agent_id: str,
        *,
        messages: list[ChatMessage | dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        stream: bool = False,
    ) -> Any:
        """Send a chat message to an agent.

        Returns ChatResponse if stream=False, async iterator if stream=True.
        """
        msgs = [
            m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
        ]
        body: dict[str, Any] = {"messages": msgs}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id

        path = f"/api/v1/agents/{agent_id}/chat"

        if stream:
            return self._stream_chat(path, body)

        return await self._chat_aggregate(path, body)

    async def _chat_aggregate(self, path: str, body: dict[str, Any]) -> ChatResponse:
        content_parts: list[str] = []
        usage = None

        async for event in self._http.stream_sse("POST", path, json_data=body):
            parsed = ChatStreamEvent.model_validate(event)
            if parsed.content:
                content_parts.append(parsed.content)
            if parsed.usage:
                usage = parsed.usage

        return ChatResponse(
            content="".join(content_parts),
            session_id="",
            usage=usage,
        )

    async def _stream_chat(self, path: str, body: dict[str, Any]):  # type: ignore[no-untyped-def]
        async for event in self._http.stream_sse("POST", path, json_data=body):
            yield ChatStreamEvent.model_validate(event)

    async def evaluate(
        self,
        agent_id: str,
        *,
        messages: list[ChatMessage | dict[str, str]],
        template_id: str,
        config_override: dict[str, Any] | None = None,
    ) -> EvaluationResult:
        msgs = [
            m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
        ]
        body: dict[str, Any] = {"messages": msgs, "template_id": template_id}
        if config_override:
            body["config_override"] = config_override

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/evaluate", json_data=body
        )
        return EvaluationResult.model_validate(data)

    async def simulate(
        self,
        agent_id: str,
        *,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
    ):  # type: ignore[no-untyped-def]
        body: dict[str, Any] = {}
        if sessions is not None:
            body["sessions"] = sessions
        if user_persona is not None:
            body["user_persona"] = user_persona
        if config is not None:
            body["config"] = config
        if model is not None:
            body["model"] = model
        if config_override is not None:
            body["config_override"] = config_override

        async for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/simulate", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    async def run_eval(
        self,
        agent_id: str,
        *,
        template_id: str,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        simulation_config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
        adaptation_template_id: str | None = None,
    ):  # type: ignore[no-untyped-def]
        body: dict[str, Any] = {"template_id": template_id}
        if sessions is not None:
            body["sessions"] = sessions
        if user_persona is not None:
            body["user_persona"] = user_persona
        if simulation_config is not None:
            body["simulation_config"] = simulation_config
        if model is not None:
            body["model"] = model
        if config_override is not None:
            body["config_override"] = config_override
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id

        async for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/run-eval", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    async def eval_only(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
    ):  # type: ignore[no-untyped-def]
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id

        async for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/eval-only", json_data=body
        ):
            yield SimulationEvent.model_validate(event)

    async def get_mood(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/mood", params=params)
        return MoodResponse.model_validate(data)

    async def get_mood_history(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/mood-history", params=params)
        return MoodResponse.model_validate(data)

    async def get_relationships(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> RelationshipResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/relationships", params=params)
        return RelationshipResponse.model_validate(data)

    async def get_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/habits", params=params)
        return HabitsResponse.model_validate(data)

    async def get_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/goals", params=params)
        return GoalsResponse.model_validate(data)

    async def get_interests(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> InterestsResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/interests", params=params)
        return InterestsResponse.model_validate(data)

    async def get_diary(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> DiaryResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/diary", params=params)
        return DiaryResponse.model_validate(data)

    async def get_users(self, agent_id: str) -> UsersResponse:
        data = await self._http.get(f"/api/v1/agents/{agent_id}/users")
        return UsersResponse.model_validate(data)
