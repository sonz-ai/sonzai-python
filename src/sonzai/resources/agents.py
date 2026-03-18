"""Agent-scoped resources for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    Agent,
    BreakthroughsResponse,
    ChatMessage,
    ChatResponse,
    ChatStreamEvent,
    ChatUsage,
    ConstellationResponse,
    DeleteResponse,
    DialogueResponse,
    DiaryResponse,
    EvaluationResult,
    GoalsResponse,
    HabitsResponse,
    InterestsResponse,
    MoodAggregateResponse,
    MoodResponse,
    RelationshipResponse,
    ScheduledWakeup,
    SimulationEvent,
    TriggerEventResponse,
    UsersResponse,
    WakeupsResponse,
)
from .custom_states import AsyncCustomStates, CustomStates
from .generation import AsyncGeneration, Generation
from .instances import AsyncInstances, Instances
from .memory import AsyncMemory, Memory
from .notifications import AsyncNotifications, Notifications
from .personality import AsyncPersonality, Personality
from .sessions import AsyncSessions, Sessions
from .voice import AsyncVoiceResource, VoiceResource


class Agents:
    """Sync agent operations: CRUD, chat, evaluate, simulate, and sub-resources."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http
        self.memory = Memory(http)
        self.personality = Personality(http)
        self.sessions = Sessions(http)
        self.instances = Instances(http)
        self.notifications = Notifications(http)
        self.custom_states = CustomStates(http)
        self.generation = Generation(http)
        self.voice = VoiceResource(http)

    # -- Agent CRUD --

    def create(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        user_id: str | None = None,
        user_display_name: str | None = None,
        gender: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
        project_id: str | None = None,
        personality_prompt: str | None = None,
        speech_patterns: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        primary_traits: list[str] | None = None,
        big5: dict[str, Any] | None = None,
        dimensions: dict[str, Any] | None = None,
        preferences: dict[str, str] | None = None,
        behaviors: dict[str, str] | None = None,
        tool_capabilities: dict[str, bool] | None = None,
        language: str | None = None,
        seed_memories: list[dict[str, Any]] | None = None,
        lore_generation_context: dict[str, Any] | None = None,
        generate_origin_story: bool | None = None,
        generate_personalized_memories: bool | None = None,
    ) -> Agent:
        """Create a new agent."""
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if user_id is not None:
            body["user_id"] = user_id
        if user_display_name is not None:
            body["user_display_name"] = user_display_name
        if gender is not None:
            body["gender"] = gender
        if bio is not None:
            body["bio"] = bio
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if project_id is not None:
            body["project_id"] = project_id
        if personality_prompt is not None:
            body["personality_prompt"] = personality_prompt
        if speech_patterns is not None:
            body["speech_patterns"] = speech_patterns
        if true_interests is not None:
            body["true_interests"] = true_interests
        if true_dislikes is not None:
            body["true_dislikes"] = true_dislikes
        if primary_traits is not None:
            body["primary_traits"] = primary_traits
        if big5 is not None:
            body["big5"] = big5
        if dimensions is not None:
            body["dimensions"] = dimensions
        if preferences is not None:
            body["preferences"] = preferences
        if behaviors is not None:
            body["behaviors"] = behaviors
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities
        if language is not None:
            body["language"] = language
        if seed_memories is not None:
            body["seed_memories"] = seed_memories
        if lore_generation_context is not None:
            body["lore_generation_context"] = lore_generation_context
        if generate_origin_story is not None:
            body["generate_origin_story"] = generate_origin_story
        if generate_personalized_memories is not None:
            body["generate_personalized_memories"] = generate_personalized_memories

        data = self._http.post("/api/v1/agents", json_data=body)
        return Agent.model_validate(data)

    def get(self, agent_id: str) -> Agent:
        """Get an agent by ID."""
        data = self._http.get(f"/api/v1/agents/{agent_id}")
        return Agent.model_validate(data)

    def update(
        self,
        agent_id: str,
        *,
        name: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
        personality_prompt: str | None = None,
        speech_patterns: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        big5: dict[str, Any] | None = None,
        dimensions: dict[str, Any] | None = None,
        tool_capabilities: dict[str, bool] | None = None,
    ) -> Agent:
        """Update an agent's profile."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if bio is not None:
            body["bio"] = bio
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if personality_prompt is not None:
            body["personality_prompt"] = personality_prompt
        if speech_patterns is not None:
            body["speech_patterns"] = speech_patterns
        if true_interests is not None:
            body["true_interests"] = true_interests
        if true_dislikes is not None:
            body["true_dislikes"] = true_dislikes
        if big5 is not None:
            body["big5"] = big5
        if dimensions is not None:
            body["dimensions"] = dimensions
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities

        data = self._http.patch(
            f"/api/v1/agents/{agent_id}/profile", json_data=body
        )
        return Agent.model_validate(data)

    def delete(self, agent_id: str) -> DeleteResponse:
        """Delete an agent."""
        data = self._http.delete(f"/api/v1/agents/{agent_id}")
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    # -- Chat --

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

    # -- Dialogue --

    def dialogue(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        enriched_context: dict[str, Any] | None = None,
        messages: list[ChatMessage | dict[str, str]] | None = None,
        request_type: str | None = None,
        scene_guidance: str | None = None,
        tool_config: dict[str, Any] | None = None,
        instance_id: str | None = None,
    ) -> DialogueResponse:
        """Initiate a dialogue with an agent."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if enriched_context is not None:
            body["enriched_context"] = enriched_context
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m
                for m in messages
            ]
        if request_type is not None:
            body["request_type"] = request_type
        if scene_guidance is not None:
            body["scene_guidance"] = scene_guidance
        if tool_config is not None:
            body["tool_config"] = tool_config
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/dialogue", json_data=body
        )
        return DialogueResponse.model_validate(data)

    # -- Events --

    def trigger_game_event(
        self,
        agent_id: str,
        *,
        user_id: str,
        event_type: str,
        event_description: str | None = None,
        metadata: dict[str, str] | None = None,
        language: str | None = None,
        instance_id: str | None = None,
    ) -> TriggerEventResponse:
        """Trigger a game event / activity for an agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "event_type": event_type,
        }
        if event_description is not None:
            body["event_description"] = event_description
        if metadata is not None:
            body["metadata"] = metadata
        if language is not None:
            body["language"] = language
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/events", json_data=body
        )
        return TriggerEventResponse.model_validate(data)

    # -- Wakeup Scheduling --

    def schedule_wakeup(
        self,
        agent_id: str,
        *,
        user_id: str,
        scheduled_at: str,
        check_type: str,
        intent: str | None = None,
        occasion: str | None = None,
        interest_topic: str | None = None,
        event_description: str | None = None,
    ) -> ScheduledWakeup:
        """Schedule a wakeup for the agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "scheduled_at": scheduled_at,
            "check_type": check_type,
        }
        if intent is not None:
            body["intent"] = intent
        if occasion is not None:
            body["occasion"] = occasion
        if interest_topic is not None:
            body["interest_topic"] = interest_topic
        if event_description is not None:
            body["event_description"] = event_description

        data = self._http.post(
            f"/api/v1/agents/{agent_id}/wakeups", json_data=body
        )
        return ScheduledWakeup.model_validate(data)

    # -- Evaluate / Simulate --

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

    def get_mood_aggregate(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodAggregateResponse:
        """Get aggregated mood statistics for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/mood/aggregate", params=params)
        return MoodAggregateResponse.model_validate(data)

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

    def get_constellation(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> ConstellationResponse:
        """Get the constellation graph for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/constellation", params=params)
        return ConstellationResponse.model_validate(data)

    def get_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """Get breakthroughs for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/breakthroughs", params=params)
        return BreakthroughsResponse.model_validate(data)

    def get_wakeups(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> WakeupsResponse:
        """Get wakeups for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/wakeups", params=params)
        return WakeupsResponse.model_validate(data)


class AsyncAgents:
    """Async agent operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http
        self.memory = AsyncMemory(http)
        self.personality = AsyncPersonality(http)
        self.sessions = AsyncSessions(http)
        self.instances = AsyncInstances(http)
        self.notifications = AsyncNotifications(http)
        self.custom_states = AsyncCustomStates(http)
        self.generation = AsyncGeneration(http)
        self.voice = AsyncVoiceResource(http)

    # -- Agent CRUD --

    async def create(
        self,
        *,
        name: str,
        agent_id: str | None = None,
        user_id: str | None = None,
        user_display_name: str | None = None,
        gender: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
        project_id: str | None = None,
        personality_prompt: str | None = None,
        speech_patterns: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        primary_traits: list[str] | None = None,
        big5: dict[str, Any] | None = None,
        dimensions: dict[str, Any] | None = None,
        preferences: dict[str, str] | None = None,
        behaviors: dict[str, str] | None = None,
        tool_capabilities: dict[str, bool] | None = None,
        language: str | None = None,
        seed_memories: list[dict[str, Any]] | None = None,
        lore_generation_context: dict[str, Any] | None = None,
        generate_origin_story: bool | None = None,
        generate_personalized_memories: bool | None = None,
    ) -> Agent:
        """Create a new agent."""
        body: dict[str, Any] = {"name": name}
        if agent_id is not None:
            body["agent_id"] = agent_id
        if user_id is not None:
            body["user_id"] = user_id
        if user_display_name is not None:
            body["user_display_name"] = user_display_name
        if gender is not None:
            body["gender"] = gender
        if bio is not None:
            body["bio"] = bio
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if project_id is not None:
            body["project_id"] = project_id
        if personality_prompt is not None:
            body["personality_prompt"] = personality_prompt
        if speech_patterns is not None:
            body["speech_patterns"] = speech_patterns
        if true_interests is not None:
            body["true_interests"] = true_interests
        if true_dislikes is not None:
            body["true_dislikes"] = true_dislikes
        if primary_traits is not None:
            body["primary_traits"] = primary_traits
        if big5 is not None:
            body["big5"] = big5
        if dimensions is not None:
            body["dimensions"] = dimensions
        if preferences is not None:
            body["preferences"] = preferences
        if behaviors is not None:
            body["behaviors"] = behaviors
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities
        if language is not None:
            body["language"] = language
        if seed_memories is not None:
            body["seed_memories"] = seed_memories
        if lore_generation_context is not None:
            body["lore_generation_context"] = lore_generation_context
        if generate_origin_story is not None:
            body["generate_origin_story"] = generate_origin_story
        if generate_personalized_memories is not None:
            body["generate_personalized_memories"] = generate_personalized_memories

        data = await self._http.post("/api/v1/agents", json_data=body)
        return Agent.model_validate(data)

    async def get(self, agent_id: str) -> Agent:
        """Get an agent by ID."""
        data = await self._http.get(f"/api/v1/agents/{agent_id}")
        return Agent.model_validate(data)

    async def update(
        self,
        agent_id: str,
        *,
        name: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
        personality_prompt: str | None = None,
        speech_patterns: list[str] | None = None,
        true_interests: list[str] | None = None,
        true_dislikes: list[str] | None = None,
        big5: dict[str, Any] | None = None,
        dimensions: dict[str, Any] | None = None,
        tool_capabilities: dict[str, bool] | None = None,
    ) -> Agent:
        """Update an agent's profile."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if bio is not None:
            body["bio"] = bio
        if avatar_url is not None:
            body["avatar_url"] = avatar_url
        if personality_prompt is not None:
            body["personality_prompt"] = personality_prompt
        if speech_patterns is not None:
            body["speech_patterns"] = speech_patterns
        if true_interests is not None:
            body["true_interests"] = true_interests
        if true_dislikes is not None:
            body["true_dislikes"] = true_dislikes
        if big5 is not None:
            body["big5"] = big5
        if dimensions is not None:
            body["dimensions"] = dimensions
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities

        data = await self._http.patch(
            f"/api/v1/agents/{agent_id}/profile", json_data=body
        )
        return Agent.model_validate(data)

    async def delete(self, agent_id: str) -> DeleteResponse:
        """Delete an agent."""
        data = await self._http.delete(f"/api/v1/agents/{agent_id}")
        if isinstance(data, dict):
            return DeleteResponse.model_validate(data)
        return DeleteResponse(success=True)

    # -- Chat --

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

    async def _stream_chat(self, path: str, body: dict[str, Any]) -> AsyncIterator[ChatStreamEvent]:
        async for event in self._http.stream_sse("POST", path, json_data=body):
            yield ChatStreamEvent.model_validate(event)

    # -- Dialogue --

    async def dialogue(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
        enriched_context: dict[str, Any] | None = None,
        messages: list[ChatMessage | dict[str, str]] | None = None,
        request_type: str | None = None,
        scene_guidance: str | None = None,
        tool_config: dict[str, Any] | None = None,
        instance_id: str | None = None,
    ) -> DialogueResponse:
        """Initiate a dialogue with an agent."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if enriched_context is not None:
            body["enriched_context"] = enriched_context
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m
                for m in messages
            ]
        if request_type is not None:
            body["request_type"] = request_type
        if scene_guidance is not None:
            body["scene_guidance"] = scene_guidance
        if tool_config is not None:
            body["tool_config"] = tool_config
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/dialogue", json_data=body
        )
        return DialogueResponse.model_validate(data)

    # -- Events --

    async def trigger_game_event(
        self,
        agent_id: str,
        *,
        user_id: str,
        event_type: str,
        event_description: str | None = None,
        metadata: dict[str, str] | None = None,
        language: str | None = None,
        instance_id: str | None = None,
    ) -> TriggerEventResponse:
        """Trigger a game event / activity for an agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "event_type": event_type,
        }
        if event_description is not None:
            body["event_description"] = event_description
        if metadata is not None:
            body["metadata"] = metadata
        if language is not None:
            body["language"] = language
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/events", json_data=body
        )
        return TriggerEventResponse.model_validate(data)

    # -- Wakeup Scheduling --

    async def schedule_wakeup(
        self,
        agent_id: str,
        *,
        user_id: str,
        scheduled_at: str,
        check_type: str,
        intent: str | None = None,
        occasion: str | None = None,
        interest_topic: str | None = None,
        event_description: str | None = None,
    ) -> ScheduledWakeup:
        """Schedule a wakeup for the agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "scheduled_at": scheduled_at,
            "check_type": check_type,
        }
        if intent is not None:
            body["intent"] = intent
        if occasion is not None:
            body["occasion"] = occasion
        if interest_topic is not None:
            body["interest_topic"] = interest_topic
        if event_description is not None:
            body["event_description"] = event_description

        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/wakeups", json_data=body
        )
        return ScheduledWakeup.model_validate(data)

    # -- Evaluate / Simulate --

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
    ) -> AsyncIterator[SimulationEvent]:
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
    ) -> AsyncIterator[SimulationEvent]:
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
    ) -> AsyncIterator[SimulationEvent]:
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

    # -- Context Engine convenience accessors --

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

    async def get_mood_aggregate(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> MoodAggregateResponse:
        """Get aggregated mood statistics for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/mood/aggregate", params=params)
        return MoodAggregateResponse.model_validate(data)

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

    async def get_constellation(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> ConstellationResponse:
        """Get the constellation graph for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/constellation", params=params)
        return ConstellationResponse.model_validate(data)

    async def get_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """Get breakthroughs for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/breakthroughs", params=params)
        return BreakthroughsResponse.model_validate(data)

    async def get_wakeups(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> WakeupsResponse:
        """Get wakeups for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/wakeups", params=params)
        return WakeupsResponse.model_validate(data)
