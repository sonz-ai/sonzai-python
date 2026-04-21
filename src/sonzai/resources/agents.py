"""Agent-scoped resources for the Sonzai SDK."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any
from urllib.parse import quote

from .._http import AsyncHTTPClient, HTTPClient
from ..types import (
    Agent,
    AgentCapabilities,
    AgentKBSearchResponse,
    AgentListResponse,
    GetToolSchemasResponse,
    ToolSchemasResponse,
    BreakthroughsResponse,
    ChatMessage,
    ChatResponse,
    ChatStreamEvent,
    ConsolidateResponse,
    ConstellationNode,
    ConstellationResponse,
    CustomToolDefinition,
    CustomToolListResponse,
    DeleteResponse,
    DeleteWisdomResponse,
    DialogueResponse,
    DiaryResponse,
    EnrichedContextResponse,
    EvaluationResult,
    ForkResponse,
    ForkStatusResponse,
    GenerateAvatarResponse,
    Goal,
    GoalsResponse,
    Habit,
    HabitsResponse,
    InterestsResponse,
    ModelsResponse,
    MoodAggregateResponse,
    MoodHistoryResponse,
    MoodResponse,
    ProcessResponse,
    RelationshipResponse,
    RunRef,
    ScheduledWakeup,
    SetStatusResponse,
    SimulationEvent,
    SummariesResponse,
    TimeMachineResponse,
    TriggerEventResponse,
    UpdateProjectResponse,
    UsersResponse,
    WakeupsResponse,
    WisdomAuditResponse,
)
from .custom_states import AsyncCustomStates, CustomStates
from .generation import AsyncGeneration, Generation
from .instances import AsyncInstances, Instances
from .inventory import AsyncInventory, Inventory
from .memory import AsyncMemory, Memory
from .notifications import AsyncNotifications, Notifications
from .personality import AsyncPersonality, Personality
from .priming import AsyncPriming, Priming
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
        self.priming = Priming(http)
        self.inventory = Inventory(http)

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
        initial_goals: list[dict[str, Any]] | None = None,
        generate_avatar: bool | None = None,
        capabilities: dict[str, Any] | None = None,
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
        if initial_goals is not None:
            body["initial_goals"] = initial_goals
        if generate_avatar is not None:
            body["generate_avatar"] = generate_avatar
        if capabilities is not None:
            body["capabilities"] = capabilities

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

        data = self._http.patch(f"/api/v1/agents/{agent_id}/profile", json_data=body)
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
        *,
        agent_id: str,  # UUID or agent name (names resolved server-side)
        messages: list[ChatMessage | dict[str, str]],
        user_id: str | None = None,
        user_display_name: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        continuation_token: str | None = None,
        request_type: str | None = None,
        language: str | None = None,
        compiled_system_prompt: str | None = None,
        interaction_role: str | None = None,
        timezone: str | None = None,
        tool_capabilities: dict[str, bool] | None = None,
        tool_definitions: list[dict[str, Any]] | None = None,
        stream: bool = False,
    ) -> ChatResponse | Iterator[ChatStreamEvent]:
        """Send a chat message to an agent.

        Args:
            agent_id: The agent to chat with.
            messages: List of messages (dicts with 'role' and 'content').
            user_id: Optional user identifier (defaults to 'api-user' server-side).
            user_display_name: Optional display name for the user.
            session_id: Optional session ID (auto-created if omitted).
            instance_id: Optional instance ID for scoped sessions.
            provider: Optional LLM provider override.
            model: Optional model override.
            continuation_token: Optional token for multi-turn continuation.
            request_type: Optional request type hint.
            language: Optional language code.
            compiled_system_prompt: Optional pre-compiled system prompt.
            interaction_role: Optional interaction role.
            timezone: Optional user timezone.
            tool_capabilities: Optional built-in tool toggles.
            tool_definitions: Optional external tool definitions.
            stream: If True, return an iterator of ChatStreamEvent.

        Returns:
            ChatResponse if stream=False, Iterator[ChatStreamEvent] if stream=True.
        """
        msgs = [m.model_dump() if isinstance(m, ChatMessage) else m for m in messages]
        body: dict[str, Any] = {"messages": msgs}
        if user_id is not None:
            body["user_id"] = user_id
        if user_display_name is not None:
            body["user_display_name"] = user_display_name
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if continuation_token is not None:
            body["continuation_token"] = continuation_token
        if request_type is not None:
            body["request_type"] = request_type
        if language is not None:
            body["language"] = language
        if compiled_system_prompt is not None:
            body["compiled_system_prompt"] = compiled_system_prompt
        if interaction_role is not None:
            body["interaction_role"] = interaction_role
        if timezone is not None:
            body["timezone"] = timezone
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities
        if tool_definitions is not None:
            body["tool_definitions"] = tool_definitions

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
            # Capture session_id from whichever event supplies it; the server
            # sets it on the session-start frame but also echoes it on later
            # events. Read from the raw event dict because ChatStreamEvent
            # doesn't define a typed session_id field (extras flow through
            # model_config={"extra": "allow"}) and the server emits the key
            # as either session_id (snake_case) or sessionId (camelCase).
            sid = event.get("session_id") or event.get("sessionId") or ""
            if sid:
                session_id = sid

        return ChatResponse(
            content="".join(content_parts),
            session_id=session_id,
            usage=usage,
        )

    def _stream_chat(self, path: str, body: dict[str, Any]) -> Iterator[ChatStreamEvent]:
        for event in self._http.stream_sse("POST", path, json_data=body):
            yield ChatStreamEvent.model_validate(event)

    # -- Dialogue --

    def dialogue(
        self,
        agent_id: str,
        *,
        user_id: str | None = None,
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
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]
        if request_type is not None:
            body["request_type"] = request_type
        if scene_guidance is not None:
            body["scene_guidance"] = scene_guidance
        if tool_config is not None:
            body["tool_config"] = tool_config
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = self._http.post(f"/api/v1/agents/{agent_id}/dialogue", json_data=body)
        return DialogueResponse.model_validate(data)

    # -- Events --

    def trigger_backend_event(
        self,
        agent_id: str,
        *,
        user_id: str,
        event_type: str,
        event_description: str | None = None,
        metadata: dict[str, str] | None = None,
        language: str | None = None,
        instance_id: str | None = None,
        messages: list[ChatMessage | dict[str, str]] | None = None,
    ) -> TriggerEventResponse:
        """Trigger a backend event / activity for an agent.

        Args:
            messages: Optional recent conversation messages passed alongside
                the event. When provided, the Platform API uses them directly
                as conversation history (e.g. for daily_summary / diary
                generation) instead of reconstructing from consolidation
                summaries. Older Platform servers ignore the field.
        """
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
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]

        data = self._http.post(f"/api/v1/agents/{agent_id}/events", json_data=body)
        return TriggerEventResponse.model_validate(data)

    # -- Wakeup Scheduling --

    def schedule_wakeup(
        self,
        agent_id: str,
        *,
        user_id: str,
        check_type: str,
        intent: str,
        delay_hours: int | None = None,
    ) -> ScheduledWakeup:
        """Schedule a wakeup for the agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "check_type": check_type,
            "intent": intent,
        }
        if delay_hours is not None:
            body["delay_hours"] = delay_hours

        data = self._http.post(f"/api/v1/agents/{agent_id}/wakeups", json_data=body)
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
        msgs = [m.model_dump() if isinstance(m, ChatMessage) else m for m in messages]
        body: dict[str, Any] = {"messages": msgs, "template_id": template_id}
        if config_override:
            body["config_override"] = config_override

        data = self._http.post(f"/api/v1/agents/{agent_id}/evaluate", json_data=body)
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
        """Run a simulation, then stream events until completion."""
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

        # Step 1: POST to start the run
        data = self._http.post(f"/api/v1/agents/{agent_id}/simulate", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        for event in self._http.stream_sse("GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"):
            yield SimulationEvent.model_validate(event)

    def simulate_async(
        self,
        agent_id: str,
        *,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
    ) -> RunRef:
        """Start a simulation and return a RunRef without waiting for completion."""
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

        data = self._http.post(f"/api/v1/agents/{agent_id}/simulate", json_data=body)
        return RunRef.model_validate(data)

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
        quality_only: bool | None = None,
    ) -> Iterator[SimulationEvent]:
        """Run simulation + evaluation combined, then stream events."""
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
        if quality_only is not None:
            body["quality_only"] = quality_only

        # Step 1: POST to start the run
        data = self._http.post(f"/api/v1/agents/{agent_id}/run-eval", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        for event in self._http.stream_sse("GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"):
            yield SimulationEvent.model_validate(event)

    def run_eval_async(
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
        quality_only: bool | None = None,
    ) -> RunRef:
        """Start simulation + evaluation and return a RunRef without waiting."""
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
        if quality_only is not None:
            body["quality_only"] = quality_only

        data = self._http.post(f"/api/v1/agents/{agent_id}/run-eval", json_data=body)
        return RunRef.model_validate(data)

    def eval_only(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
        quality_only: bool | None = None,
    ) -> Iterator[SimulationEvent]:
        """Re-evaluate an existing run, then stream events."""
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id
        if quality_only is not None:
            body["quality_only"] = quality_only

        # Step 1: POST to start the eval
        data = self._http.post(f"/api/v1/agents/{agent_id}/eval-only", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        for event in self._http.stream_sse("GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"):
            yield SimulationEvent.model_validate(event)

    def eval_only_async(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
        quality_only: bool | None = None,
    ) -> RunRef:
        """Start re-evaluation and return a RunRef without waiting."""
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id
        if quality_only is not None:
            body["quality_only"] = quality_only

        data = self._http.post(f"/api/v1/agents/{agent_id}/eval-only", json_data=body)
        return RunRef.model_validate(data)

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
    ) -> MoodHistoryResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/mood-history", params=params)
        return MoodHistoryResponse.model_validate(data)

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

    def list_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        """List habits for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/habits", params=params)
        return HabitsResponse.model_validate(data)

    def get_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        """.. deprecated:: Use :meth:`list_habits` instead."""
        return self.list_habits(agent_id, user_id=user_id, instance_id=instance_id)

    def create_habit(
        self,
        agent_id: str,
        *,
        name: str,
        user_id: str | None = None,
        category: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        strength: float | None = None,
    ) -> Habit:
        """Create a habit for an agent. Set user_id for a per-user habit."""
        body: dict[str, Any] = {"name": name}
        if user_id is not None:
            body["user_id"] = user_id
        if category is not None:
            body["category"] = category
        if description is not None:
            body["description"] = description
        if display_name is not None:
            body["display_name"] = display_name
        if strength is not None:
            body["strength"] = strength
        data = self._http.post(f"/api/v1/agents/{agent_id}/habits", json_data=body)
        return Habit.model_validate(data)

    def update_habit(
        self,
        agent_id: str,
        habit_name: str,
        *,
        user_id: str | None = None,
        category: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        strength: float | None = None,
    ) -> Habit:
        """Update an existing habit by name."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if category is not None:
            body["category"] = category
        if description is not None:
            body["description"] = description
        if display_name is not None:
            body["display_name"] = display_name
        if strength is not None:
            body["strength"] = strength
        data = self._http.put(
            f"/api/v1/agents/{agent_id}/habits/{quote(habit_name, safe='')}", json_data=body
        )
        return Habit.model_validate(data)

    def delete_habit(
        self,
        agent_id: str,
        habit_name: str,
        *,
        user_id: str | None = None,
    ) -> None:
        """Delete a habit. Set user_id for per-user habits."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        self._http.delete(
            f"/api/v1/agents/{agent_id}/habits/{quote(habit_name, safe='')}", params=params
        )

    def list_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        """List goals for an agent. Pass user_id to get combined agent-global + per-user goals."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/goals", params=params)
        return GoalsResponse.model_validate(data)

    def get_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        """.. deprecated:: Use :meth:`list_goals` instead."""
        return self.list_goals(agent_id, user_id=user_id, instance_id=instance_id)

    def create_goal(
        self,
        agent_id: str,
        *,
        title: str,
        description: str,
        user_id: str | None = None,
        type: str | None = None,
        priority: int | None = None,
        related_traits: list[str] | None = None,
    ) -> Goal:
        """Create a goal for an agent. Set user_id to create a per-user goal."""
        body: dict[str, Any] = {
            "title": title,
            "description": description,
        }
        if user_id is not None:
            body["user_id"] = user_id
        if type is not None:
            body["type"] = type
        if priority is not None:
            body["priority"] = priority
        if related_traits is not None:
            body["related_traits"] = related_traits

        data = self._http.post(f"/api/v1/agents/{agent_id}/goals", json_data=body)
        return Goal.model_validate(data)

    def update_goal(
        self,
        agent_id: str,
        goal_id: str,
        *,
        user_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
        priority: int | None = None,
        status: str | None = None,
        related_traits: list[str] | None = None,
    ) -> Goal:
        """Update an existing goal. Set user_id for per-user goals."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if title is not None:
            body["title"] = title
        if description is not None:
            body["description"] = description
        if priority is not None:
            body["priority"] = priority
        if status is not None:
            body["status"] = status
        if related_traits is not None:
            body["related_traits"] = related_traits

        data = self._http.put(f"/api/v1/agents/{agent_id}/goals/{goal_id}", json_data=body)
        return Goal.model_validate(data)

    def delete_goal(
        self,
        agent_id: str,
        goal_id: str,
        *,
        user_id: str | None = None,
    ) -> None:
        """Delete (soft-abandon) a goal. Set user_id for per-user goals."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        self._http.delete(f"/api/v1/agents/{agent_id}/goals/{goal_id}", params=params)

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

    def respond_to_tool_call(
        self,
        agent_id: str,
        *,
        session_id: str,
        tool_call_id: str,
        result: Any,
        user_id: str | None = None,
    ) -> ChatResponse:
        body: dict[str, Any] = {
            "session_id": session_id,
            "tool_call_id": tool_call_id,
            "result": result,
        }
        if user_id is not None:
            body["user_id"] = user_id
        data = self._http.post(f"/api/v1/agents/{agent_id}/tools/respond", json_data=body)
        return ChatResponse.model_validate(data)

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

    def create_constellation_node(
        self,
        agent_id: str,
        *,
        label: str,
        user_id: str | None = None,
        node_type: str | None = None,
        description: str | None = None,
        significance: float | None = None,
    ) -> ConstellationNode:
        """Create a constellation node (lore) for an agent."""
        body: dict[str, Any] = {"label": label}
        if user_id is not None:
            body["user_id"] = user_id
        if node_type is not None:
            body["node_type"] = node_type
        if description is not None:
            body["description"] = description
        if significance is not None:
            body["significance"] = significance
        data = self._http.post(f"/api/v1/agents/{agent_id}/constellation/nodes", json_data=body)
        return ConstellationNode.model_validate(data)

    def update_constellation_node(
        self,
        agent_id: str,
        node_id: str,
        *,
        label: str | None = None,
        description: str | None = None,
        significance: float | None = None,
        node_type: str | None = None,
    ) -> ConstellationNode:
        """Update an existing constellation node."""
        body: dict[str, Any] = {}
        if label is not None:
            body["label"] = label
        if description is not None:
            body["description"] = description
        if significance is not None:
            body["significance"] = significance
        if node_type is not None:
            body["node_type"] = node_type
        data = self._http.put(
            f"/api/v1/agents/{agent_id}/constellation/nodes/{node_id}",
            json_data=body,
        )
        return ConstellationNode.model_validate(data)

    def delete_constellation_node(
        self,
        agent_id: str,
        node_id: str,
    ) -> None:
        """Delete a constellation node."""
        self._http.delete(f"/api/v1/agents/{agent_id}/constellation/nodes/{node_id}")

    def list_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """List breakthroughs for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = self._http.get(f"/api/v1/agents/{agent_id}/breakthroughs", params=params)
        return BreakthroughsResponse.model_validate(data)

    def get_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """.. deprecated:: Use :meth:`list_breakthroughs` instead."""
        return self.list_breakthroughs(agent_id, user_id=user_id, instance_id=instance_id)

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

    # -- Agent List --

    def list(
        self,
        *,
        page_size: int | None = None,
        cursor: str | None = None,
        search: str | None = None,
        project_id: str | None = None,
    ) -> AgentListResponse:
        """List agents with optional pagination and filtering."""
        params: dict[str, str] = {}
        if page_size is not None:
            params["page_size"] = str(page_size)
        if cursor is not None:
            params["cursor"] = cursor
        if search is not None:
            params["search"] = search
        if project_id is not None:
            params["project_id"] = project_id
        return AgentListResponse.model_validate(self._http.get("/api/v1/agents", params=params))

    # -- Agent Status --

    def set_status(self, agent_id: str, *, is_active: bool) -> SetStatusResponse:
        """Set an agent's active status."""
        return SetStatusResponse.model_validate(
            self._http.patch(
                f"/api/v1/agents/{agent_id}/status", json_data={"is_active": is_active}
            )
        )

    # -- Update Project --

    def update_project(self, agent_id: str, *, project_id: str) -> UpdateProjectResponse:
        """Update the project assignment for an agent."""
        return UpdateProjectResponse.model_validate(
            self._http.patch(
                f"/api/v1/agents/{agent_id}/project", json_data={"project_id": project_id}
            )
        )

    # -- Capabilities --

    def get_capabilities(self, agent_id: str) -> AgentCapabilities:
        """Get an agent's capabilities."""
        return AgentCapabilities.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/capabilities")
        )

    def update_capabilities(
        self,
        agent_id: str,
        *,
        web_search: bool | None = None,
        remember_name: bool | None = None,
        image_generation: bool | None = None,
        inventory: bool | None = None,
    ) -> AgentCapabilities:
        """Update an agent's capabilities."""
        body: dict[str, Any] = {}
        if web_search is not None:
            body["webSearch"] = web_search
        if remember_name is not None:
            body["rememberName"] = remember_name
        if image_generation is not None:
            body["imageGeneration"] = image_generation
        if inventory is not None:
            body["inventory"] = inventory
        return AgentCapabilities.model_validate(
            self._http.patch(f"/api/v1/agents/{agent_id}/capabilities", json_data=body)
        )

    # -- Post-processing model override (layer 1 of cascade) --

    def update_post_processing_model(
        self,
        agent_id: str,
        *,
        provider: str,
        model: str,
    ) -> dict[str, Any]:
        """Set the agent-level post-processing model override.

        Short-circuits the cascade — when set, project / account /
        system-default layers are not consulted. Both ``provider`` and
        ``model`` must be non-empty for the override to take effect.
        """
        return self._http.patch(  # type: ignore[return-value]
            f"/api/v1/agents/{agent_id}/post-processing-model",
            json_data={
                "post_processing_provider": provider,
                "post_processing_model": model,
            },
        )

    def clear_post_processing_model(self, agent_id: str) -> dict[str, Any]:
        """Remove the agent-level override so the cascade falls through
        to project / account / system-default layers."""
        return self.update_post_processing_model(agent_id, provider="", model="")

    def effective_post_processing_model(
        self, agent_id: str, chat_model: str
    ) -> dict[str, Any]:
        """Run the cascade server-side for ``chat_model`` on this agent,
        without firing inference. Returns ``{provider, model,
        temperature?, max_tokens?}`` — the full resolved config the
        resolver would hand to the Provider.

        When the server has ``ENABLE_POST_PROCESSING_MODEL_MAP=false``,
        the response echoes the chat model itself.
        """
        return self._http.get(  # type: ignore[return-value]
            f"/api/v1/agents/{agent_id}/effective-post-processing-model",
            params={"chat_model": chat_model},
        )

    # -- Custom Tools --

    def list_custom_tools(self, agent_id: str) -> CustomToolListResponse:
        """List custom tools for an agent."""
        return CustomToolListResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/tools")
        )

    def create_custom_tool(
        self,
        agent_id: str,
        *,
        name: str,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> CustomToolDefinition:
        """Create a custom tool for an agent."""
        body: dict[str, Any] = {"name": name, "description": description}
        if parameters is not None:
            body["parameters"] = parameters
        return CustomToolDefinition.model_validate(
            self._http.post(f"/api/v1/agents/{agent_id}/tools", json_data=body)
        )

    def update_custom_tool(
        self,
        agent_id: str,
        tool_name: str,
        *,
        description: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a custom tool for an agent."""
        body: dict[str, Any] = {}
        if description is not None:
            body["description"] = description
        if parameters is not None:
            body["parameters"] = parameters
        return self._http.put(f"/api/v1/agents/{agent_id}/tools/{tool_name}", json_data=body)

    def delete_custom_tool(self, agent_id: str, tool_name: str) -> None:
        """Delete a custom tool from an agent."""
        self._http.delete(f"/api/v1/agents/{agent_id}/tools/{tool_name}")

    # -- Consolidation --

    def consolidate(
        self,
        agent_id: str,
        *,
        period: str = "daily",
        user_id: str | None = None,
    ) -> ConsolidateResponse:
        """Trigger memory consolidation for an agent."""
        body: dict[str, Any] = {"period": period}
        if user_id is not None:
            body["user_id"] = user_id
        return ConsolidateResponse.model_validate(
            self._http.post(f"/api/v1/agents/{agent_id}/consolidate", json_data=body)
        )

    # -- Summaries --

    def get_summaries(
        self,
        agent_id: str,
        *,
        period: str | None = None,
        limit: int | None = None,
    ) -> SummariesResponse:
        """Get memory summaries for an agent."""
        params: dict[str, str] = {}
        if period is not None:
            params["period"] = period
        if limit is not None:
            params["limit"] = str(limit)
        return SummariesResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/summaries", params=params)
        )

    # -- Process --

    def process(
        self,
        agent_id: str,
        *,
        user_id: str,
        messages: list[dict[str, str]],
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        include_extractions: bool | None = None,
    ) -> ProcessResponse:
        """Run the full Context Engine pipeline without generating a chat response."""
        body: dict[str, Any] = {"userId": user_id, "messages": messages}
        if session_id is not None:
            body["sessionId"] = session_id
        if instance_id is not None:
            body["instanceId"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if include_extractions is not None:
            body["include_extractions"] = include_extractions
        return ProcessResponse.model_validate(
            self._http.post(f"/api/v1/agents/{agent_id}/process", json_data=body)
        )

    # -- Models --

    def get_models(self, agent_id: str) -> ModelsResponse:
        """Get available LLM providers and models."""
        return ModelsResponse.model_validate(self._http.get(f"/api/v1/agents/{agent_id}/models"))

    # -- Context --

    def get_context(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str | None = None,
        instance_id: str | None = None,
        query: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> EnrichedContextResponse:
        """Get the full enriched agent context in a single call."""
        params: dict[str, str] = {"userId": user_id}
        if session_id is not None:
            params["sessionId"] = session_id
        if instance_id is not None:
            params["instanceId"] = instance_id
        if query is not None:
            params["query"] = query
        if language is not None:
            params["language"] = language
        if timezone is not None:
            params["timezone"] = timezone
        return EnrichedContextResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/context", params=params)
        )

    # -- Avatar --

    def generate_avatar(
        self,
        agent_id: str,
        *,
        style: str | None = None,
    ) -> GenerateAvatarResponse:
        """Trigger avatar generation for an agent."""
        body: dict[str, Any] = {}
        if style is not None:
            body["style"] = style
        return GenerateAvatarResponse.model_validate(
            self._http.post(f"/api/v1/agents/{agent_id}/avatar/generate", json_data=body)
        )

    # -- Time Machine --

    def get_time_machine(
        self,
        agent_id: str,
        *,
        at: str,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> TimeMachineResponse:
        """Get an agent's personality and mood state at a specific point in time."""
        params: dict[str, str] = {"at": at}
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id
        return TimeMachineResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/timemachine", params=params)
        )

    # -- Knowledge Search (tool endpoint) --

    def knowledge_search(
        self,
        agent_id: str,
        *,
        query: str,
        limit: int | None = None,
    ) -> AgentKBSearchResponse:
        """Search the knowledge base for an agent."""
        body: dict[str, Any] = {"query": query}
        if limit is not None:
            body["limit"] = limit
        return AgentKBSearchResponse.model_validate(
            self._http.post(
                f"/api/v1/agents/{agent_id}/tools/kb-search",
                json_data=body,
            )
        )

    # -- Tool Schemas (BYO-LLM) --

    def get_tools(self, agent_id: str) -> ToolSchemasResponse:
        """Return tool schemas available for an agent (for BYO-LLM integrations)."""
        return ToolSchemasResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/tools")
        )

    def get_tool_schemas(self, agent_id: str) -> GetToolSchemasResponse:
        """Return OpenAPI-style tool schemas for BYO-LLM tool calling."""
        return GetToolSchemasResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/tools/schemas")
        )

    # -- Fork --

    def fork(
        self,
        agent_id: str,
        *,
        name: str | None = None,
    ) -> ForkResponse:
        """Fork an agent (create a copy with a new ID)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        return ForkResponse.model_validate(
            self._http.post(f"/api/v1/agents/{agent_id}/fork", json_data=body)
        )

    def get_fork_status(self, agent_id: str) -> ForkStatusResponse:
        """Check the status of a fork operation."""
        return ForkStatusResponse.model_validate(
            self._http.get(f"/api/v1/agents/{agent_id}/fork/status")
        )

    # -- Playground Chat --

    def playground_chat(
        self,
        agent_id: str,
        *,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        language: str | None = None,
    ) -> ChatResponse:
        """Send a playground chat message (non-streaming). Same as chat but via the playground endpoint."""
        body: dict[str, Any] = {"messages": messages}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if language is not None:
            body["language"] = language

        parts: list[str] = []
        for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/playground/chat", json_data=body
        ):
            parsed = ChatStreamEvent.model_validate(event)
            if parsed.choices and parsed.choices[0].delta.get("content"):
                parts.append(parsed.choices[0].delta["content"])
        return ChatResponse(content="".join(parts))

    def playground_chat_stream(
        self,
        agent_id: str,
        *,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        language: str | None = None,
    ) -> Iterator[ChatStreamEvent]:
        """Send a playground chat message and stream events."""
        body: dict[str, Any] = {"messages": messages}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if language is not None:
            body["language"] = language

        for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/playground/chat", json_data=body
        ):
            yield ChatStreamEvent.model_validate(event)

    # -- Knowledge Search GET --

    def knowledge_search_get(
        self,
        agent_id: str,
        *,
        query: str,
        limit: int | None = None,
    ) -> AgentKBSearchResponse:
        """Search the knowledge base using a GET request with query parameters."""
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        return AgentKBSearchResponse.model_validate(
            self._http.get(
                f"/api/v1/agents/{agent_id}/tools/kb-search",
                params=params,
            )
        )


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
        self.priming = AsyncPriming(http)
        self.inventory = AsyncInventory(http)

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
        initial_goals: list[dict[str, Any]] | None = None,
        generate_avatar: bool | None = None,
        capabilities: dict[str, Any] | None = None,
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
        if initial_goals is not None:
            body["initial_goals"] = initial_goals
        if generate_avatar is not None:
            body["generate_avatar"] = generate_avatar
        if capabilities is not None:
            body["capabilities"] = capabilities

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

        data = await self._http.patch(f"/api/v1/agents/{agent_id}/profile", json_data=body)
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
        agent_id: str,  # UUID or agent name (names resolved server-side)
        *,
        messages: list[ChatMessage | dict[str, str]],
        user_id: str | None = None,
        user_display_name: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        continuation_token: str | None = None,
        request_type: str | None = None,
        language: str | None = None,
        compiled_system_prompt: str | None = None,
        interaction_role: str | None = None,
        timezone: str | None = None,
        tool_capabilities: dict[str, bool] | None = None,
        tool_definitions: list[dict[str, Any]] | None = None,
        stream: bool = False,
    ) -> ChatResponse | AsyncIterator[ChatStreamEvent]:
        """Send a chat message to an agent.

        Returns ChatResponse if stream=False, async iterator if stream=True.
        """
        msgs = [m.model_dump() if isinstance(m, ChatMessage) else m for m in messages]
        body: dict[str, Any] = {"messages": msgs}
        if user_id is not None:
            body["user_id"] = user_id
        if user_display_name is not None:
            body["user_display_name"] = user_display_name
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if continuation_token is not None:
            body["continuation_token"] = continuation_token
        if request_type is not None:
            body["request_type"] = request_type
        if language is not None:
            body["language"] = language
        if compiled_system_prompt is not None:
            body["compiled_system_prompt"] = compiled_system_prompt
        if interaction_role is not None:
            body["interaction_role"] = interaction_role
        if timezone is not None:
            body["timezone"] = timezone
        if tool_capabilities is not None:
            body["tool_capabilities"] = tool_capabilities
        if tool_definitions is not None:
            body["tool_definitions"] = tool_definitions

        path = f"/api/v1/agents/{agent_id}/chat"

        if stream:
            return self._stream_chat(path, body)

        return await self._chat_aggregate(path, body)

    async def _chat_aggregate(self, path: str, body: dict[str, Any]) -> ChatResponse:
        content_parts: list[str] = []
        usage = None
        session_id = ""

        async for event in self._http.stream_sse("POST", path, json_data=body):
            parsed = ChatStreamEvent.model_validate(event)
            if parsed.content:
                content_parts.append(parsed.content)
            if parsed.usage:
                usage = parsed.usage
            # See _chat_sync — read session_id directly from the raw event
            # dict (ChatStreamEvent has no typed session_id field; the server
            # emits the key as session_id or sessionId).
            sid = event.get("session_id") or event.get("sessionId") or ""
            if sid:
                session_id = sid

        return ChatResponse(
            content="".join(content_parts),
            session_id=session_id,
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
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]
        if request_type is not None:
            body["request_type"] = request_type
        if scene_guidance is not None:
            body["scene_guidance"] = scene_guidance
        if tool_config is not None:
            body["tool_config"] = tool_config
        if instance_id is not None:
            body["instance_id"] = instance_id

        data = await self._http.post(f"/api/v1/agents/{agent_id}/dialogue", json_data=body)
        return DialogueResponse.model_validate(data)

    # -- Events --

    async def trigger_backend_event(
        self,
        agent_id: str,
        *,
        user_id: str,
        event_type: str,
        event_description: str | None = None,
        metadata: dict[str, str] | None = None,
        language: str | None = None,
        instance_id: str | None = None,
        messages: list[ChatMessage | dict[str, str]] | None = None,
    ) -> TriggerEventResponse:
        """Trigger a backend event / activity for an agent.

        Args:
            messages: Optional recent conversation messages passed alongside
                the event. When provided, the Platform API uses them directly
                as conversation history (e.g. for daily_summary / diary
                generation) instead of reconstructing from consolidation
                summaries. Older Platform servers ignore the field.
        """
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
        if messages is not None:
            body["messages"] = [
                m.model_dump() if isinstance(m, ChatMessage) else m for m in messages
            ]

        data = await self._http.post(f"/api/v1/agents/{agent_id}/events", json_data=body)
        return TriggerEventResponse.model_validate(data)

    # -- Wakeup Scheduling --

    async def schedule_wakeup(
        self,
        agent_id: str,
        *,
        user_id: str,
        check_type: str,
        intent: str,
        delay_hours: int | None = None,
    ) -> ScheduledWakeup:
        """Schedule a wakeup for the agent."""
        body: dict[str, Any] = {
            "user_id": user_id,
            "check_type": check_type,
            "intent": intent,
        }
        if delay_hours is not None:
            body["delay_hours"] = delay_hours

        data = await self._http.post(f"/api/v1/agents/{agent_id}/wakeups", json_data=body)
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
        msgs = [m.model_dump() if isinstance(m, ChatMessage) else m for m in messages]
        body: dict[str, Any] = {"messages": msgs, "template_id": template_id}
        if config_override:
            body["config_override"] = config_override

        data = await self._http.post(f"/api/v1/agents/{agent_id}/evaluate", json_data=body)
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
        """Run a simulation, then stream events until completion."""
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

        # Step 1: POST to start the run
        data = await self._http.post(f"/api/v1/agents/{agent_id}/simulate", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        async for event in self._http.stream_sse(
            "GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"
        ):
            yield SimulationEvent.model_validate(event)

    async def simulate_async(
        self,
        agent_id: str,
        *,
        sessions: list[dict[str, Any]] | None = None,
        user_persona: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        model: str | None = None,
        config_override: dict[str, Any] | None = None,
    ) -> RunRef:
        """Start a simulation and return a RunRef without waiting for completion."""
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

        data = await self._http.post(f"/api/v1/agents/{agent_id}/simulate", json_data=body)
        return RunRef.model_validate(data)

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
        quality_only: bool | None = None,
    ) -> AsyncIterator[SimulationEvent]:
        """Run simulation + evaluation combined, then stream events."""
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
        if quality_only is not None:
            body["quality_only"] = quality_only

        # Step 1: POST to start the run
        data = await self._http.post(f"/api/v1/agents/{agent_id}/run-eval", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        async for event in self._http.stream_sse(
            "GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"
        ):
            yield SimulationEvent.model_validate(event)

    async def run_eval_async(
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
        quality_only: bool | None = None,
    ) -> RunRef:
        """Start simulation + evaluation and return a RunRef without waiting."""
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
        if quality_only is not None:
            body["quality_only"] = quality_only

        data = await self._http.post(f"/api/v1/agents/{agent_id}/run-eval", json_data=body)
        return RunRef.model_validate(data)

    async def eval_only(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
        quality_only: bool | None = None,
    ) -> AsyncIterator[SimulationEvent]:
        """Re-evaluate an existing run, then stream events."""
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id
        if quality_only is not None:
            body["quality_only"] = quality_only

        # Step 1: POST to start the eval
        data = await self._http.post(f"/api/v1/agents/{agent_id}/eval-only", json_data=body)
        ref = RunRef.model_validate(data)
        # Step 2: Stream events from the run
        async for event in self._http.stream_sse(
            "GET", f"/api/v1/eval-runs/{ref.run_id}/events?from=0"
        ):
            yield SimulationEvent.model_validate(event)

    async def eval_only_async(
        self,
        agent_id: str,
        *,
        template_id: str,
        source_run_id: str,
        adaptation_template_id: str | None = None,
        quality_only: bool | None = None,
    ) -> RunRef:
        """Start re-evaluation and return a RunRef without waiting."""
        body: dict[str, Any] = {
            "template_id": template_id,
            "source_run_id": source_run_id,
        }
        if adaptation_template_id is not None:
            body["adaptation_template_id"] = adaptation_template_id
        if quality_only is not None:
            body["quality_only"] = quality_only

        data = await self._http.post(f"/api/v1/agents/{agent_id}/eval-only", json_data=body)
        return RunRef.model_validate(data)

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
    ) -> MoodHistoryResponse:
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/mood-history", params=params)
        return MoodHistoryResponse.model_validate(data)

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

    async def list_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        """List habits for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/habits", params=params)
        return HabitsResponse.model_validate(data)

    async def get_habits(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> HabitsResponse:
        """.. deprecated:: Use :meth:`list_habits` instead."""
        return await self.list_habits(agent_id, user_id=user_id, instance_id=instance_id)

    async def create_habit(
        self,
        agent_id: str,
        *,
        name: str,
        user_id: str | None = None,
        category: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        strength: float | None = None,
    ) -> Habit:
        """Create a habit for an agent. Set user_id for a per-user habit."""
        body: dict[str, Any] = {"name": name}
        if user_id is not None:
            body["user_id"] = user_id
        if category is not None:
            body["category"] = category
        if description is not None:
            body["description"] = description
        if display_name is not None:
            body["display_name"] = display_name
        if strength is not None:
            body["strength"] = strength
        data = await self._http.post(f"/api/v1/agents/{agent_id}/habits", json_data=body)
        return Habit.model_validate(data)

    async def update_habit(
        self,
        agent_id: str,
        habit_name: str,
        *,
        user_id: str | None = None,
        category: str | None = None,
        description: str | None = None,
        display_name: str | None = None,
        strength: float | None = None,
    ) -> Habit:
        """Update an existing habit by name."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if category is not None:
            body["category"] = category
        if description is not None:
            body["description"] = description
        if display_name is not None:
            body["display_name"] = display_name
        if strength is not None:
            body["strength"] = strength
        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/habits/{quote(habit_name, safe='')}", json_data=body
        )
        return Habit.model_validate(data)

    async def delete_habit(
        self,
        agent_id: str,
        habit_name: str,
        *,
        user_id: str | None = None,
    ) -> None:
        """Delete a habit. Set user_id for per-user habits."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        await self._http.delete(
            f"/api/v1/agents/{agent_id}/habits/{quote(habit_name, safe='')}", params=params
        )

    async def list_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        """List goals for an agent. Pass user_id to get combined agent-global + per-user goals."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/goals", params=params)
        return GoalsResponse.model_validate(data)

    async def get_goals(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> GoalsResponse:
        """.. deprecated:: Use :meth:`list_goals` instead."""
        return await self.list_goals(agent_id, user_id=user_id, instance_id=instance_id)

    async def create_goal(
        self,
        agent_id: str,
        *,
        title: str,
        description: str,
        user_id: str | None = None,
        type: str | None = None,
        priority: int | None = None,
        related_traits: list[str] | None = None,
    ) -> Goal:
        """Create a goal for an agent. Set user_id to create a per-user goal."""
        body: dict[str, Any] = {
            "title": title,
            "description": description,
        }
        if user_id is not None:
            body["user_id"] = user_id
        if type is not None:
            body["type"] = type
        if priority is not None:
            body["priority"] = priority
        if related_traits is not None:
            body["related_traits"] = related_traits

        data = await self._http.post(f"/api/v1/agents/{agent_id}/goals", json_data=body)
        return Goal.model_validate(data)

    async def update_goal(
        self,
        agent_id: str,
        goal_id: str,
        *,
        user_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
        priority: int | None = None,
        status: str | None = None,
        related_traits: list[str] | None = None,
    ) -> Goal:
        """Update an existing goal. Set user_id for per-user goals."""
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
        if title is not None:
            body["title"] = title
        if description is not None:
            body["description"] = description
        if priority is not None:
            body["priority"] = priority
        if status is not None:
            body["status"] = status
        if related_traits is not None:
            body["related_traits"] = related_traits

        data = await self._http.put(f"/api/v1/agents/{agent_id}/goals/{goal_id}", json_data=body)
        return Goal.model_validate(data)

    async def delete_goal(
        self,
        agent_id: str,
        goal_id: str,
        *,
        user_id: str | None = None,
    ) -> None:
        """Delete (soft-abandon) a goal. Set user_id for per-user goals."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["userId"] = user_id
        await self._http.delete(f"/api/v1/agents/{agent_id}/goals/{goal_id}", params=params)

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

    async def respond_to_tool_call(
        self,
        agent_id: str,
        *,
        session_id: str,
        tool_call_id: str,
        result: Any,
        user_id: str | None = None,
    ) -> ChatResponse:
        body: dict[str, Any] = {
            "session_id": session_id,
            "tool_call_id": tool_call_id,
            "result": result,
        }
        if user_id is not None:
            body["user_id"] = user_id
        data = await self._http.post(f"/api/v1/agents/{agent_id}/tools/respond", json_data=body)
        return ChatResponse.model_validate(data)

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

    async def create_constellation_node(
        self,
        agent_id: str,
        *,
        label: str,
        user_id: str | None = None,
        node_type: str | None = None,
        description: str | None = None,
        significance: float | None = None,
    ) -> ConstellationNode:
        """Create a constellation node (lore) for an agent."""
        body: dict[str, Any] = {"label": label}
        if user_id is not None:
            body["user_id"] = user_id
        if node_type is not None:
            body["node_type"] = node_type
        if description is not None:
            body["description"] = description
        if significance is not None:
            body["significance"] = significance
        data = await self._http.post(
            f"/api/v1/agents/{agent_id}/constellation/nodes", json_data=body
        )
        return ConstellationNode.model_validate(data)

    async def update_constellation_node(
        self,
        agent_id: str,
        node_id: str,
        *,
        label: str | None = None,
        description: str | None = None,
        significance: float | None = None,
        node_type: str | None = None,
    ) -> ConstellationNode:
        """Update an existing constellation node."""
        body: dict[str, Any] = {}
        if label is not None:
            body["label"] = label
        if description is not None:
            body["description"] = description
        if significance is not None:
            body["significance"] = significance
        if node_type is not None:
            body["node_type"] = node_type
        data = await self._http.put(
            f"/api/v1/agents/{agent_id}/constellation/nodes/{node_id}",
            json_data=body,
        )
        return ConstellationNode.model_validate(data)

    async def delete_constellation_node(
        self,
        agent_id: str,
        node_id: str,
    ) -> None:
        """Delete a constellation node."""
        await self._http.delete(f"/api/v1/agents/{agent_id}/constellation/nodes/{node_id}")

    async def list_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """List breakthroughs for an agent."""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if instance_id:
            params["instance_id"] = instance_id
        data = await self._http.get(f"/api/v1/agents/{agent_id}/breakthroughs", params=params)
        return BreakthroughsResponse.model_validate(data)

    async def get_breakthroughs(
        self, agent_id: str, *, user_id: str | None = None, instance_id: str | None = None
    ) -> BreakthroughsResponse:
        """.. deprecated:: Use :meth:`list_breakthroughs` instead."""
        return await self.list_breakthroughs(agent_id, user_id=user_id, instance_id=instance_id)

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

    # -- Agent List --

    async def list(
        self,
        *,
        page_size: int | None = None,
        cursor: str | None = None,
        search: str | None = None,
        project_id: str | None = None,
    ) -> AgentListResponse:
        """List agents with optional pagination and filtering."""
        params: dict[str, str] = {}
        if page_size is not None:
            params["page_size"] = str(page_size)
        if cursor is not None:
            params["cursor"] = cursor
        if search is not None:
            params["search"] = search
        if project_id is not None:
            params["project_id"] = project_id
        return AgentListResponse.model_validate(
            await self._http.get("/api/v1/agents", params=params)
        )

    # -- Agent Status --

    async def set_status(self, agent_id: str, *, is_active: bool) -> SetStatusResponse:
        """Set an agent's active status."""
        return SetStatusResponse.model_validate(
            await self._http.patch(
                f"/api/v1/agents/{agent_id}/status", json_data={"is_active": is_active}
            )
        )

    # -- Update Project --

    async def update_project(self, agent_id: str, *, project_id: str) -> UpdateProjectResponse:
        """Update the project assignment for an agent."""
        return UpdateProjectResponse.model_validate(
            await self._http.patch(
                f"/api/v1/agents/{agent_id}/project", json_data={"project_id": project_id}
            )
        )

    # -- Capabilities --

    async def get_capabilities(self, agent_id: str) -> AgentCapabilities:
        """Get an agent's capabilities."""
        return AgentCapabilities.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/capabilities")
        )

    async def update_capabilities(
        self,
        agent_id: str,
        *,
        web_search: bool | None = None,
        remember_name: bool | None = None,
        image_generation: bool | None = None,
        inventory: bool | None = None,
    ) -> AgentCapabilities:
        """Update an agent's capabilities."""
        body: dict[str, Any] = {}
        if web_search is not None:
            body["webSearch"] = web_search
        if remember_name is not None:
            body["rememberName"] = remember_name
        if image_generation is not None:
            body["imageGeneration"] = image_generation
        if inventory is not None:
            body["inventory"] = inventory
        return AgentCapabilities.model_validate(
            await self._http.patch(f"/api/v1/agents/{agent_id}/capabilities", json_data=body)
        )

    # -- Post-processing model override (layer 1 of cascade) --

    async def update_post_processing_model(
        self,
        agent_id: str,
        *,
        provider: str,
        model: str,
    ) -> dict[str, Any]:
        """Set the agent-level post-processing model override. Async.

        See :meth:`Agents.update_post_processing_model` for semantics.
        """
        return await self._http.patch(  # type: ignore[return-value]
            f"/api/v1/agents/{agent_id}/post-processing-model",
            json_data={
                "post_processing_provider": provider,
                "post_processing_model": model,
            },
        )

    async def clear_post_processing_model(self, agent_id: str) -> dict[str, Any]:
        """Remove the agent-level override. Async."""
        return await self.update_post_processing_model(
            agent_id, provider="", model=""
        )

    async def effective_post_processing_model(
        self, agent_id: str, chat_model: str
    ) -> dict[str, Any]:
        """Run the cascade server-side for ``chat_model`` on this agent,
        without firing inference. Async."""
        return await self._http.get(  # type: ignore[return-value]
            f"/api/v1/agents/{agent_id}/effective-post-processing-model",
            params={"chat_model": chat_model},
        )

    # -- Custom Tools --

    async def list_custom_tools(self, agent_id: str) -> CustomToolListResponse:
        """List custom tools for an agent."""
        return CustomToolListResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/tools")
        )

    async def create_custom_tool(
        self,
        agent_id: str,
        *,
        name: str,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> CustomToolDefinition:
        """Create a custom tool for an agent."""
        body: dict[str, Any] = {"name": name, "description": description}
        if parameters is not None:
            body["parameters"] = parameters
        return CustomToolDefinition.model_validate(
            await self._http.post(f"/api/v1/agents/{agent_id}/tools", json_data=body)
        )

    async def update_custom_tool(
        self,
        agent_id: str,
        tool_name: str,
        *,
        description: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update a custom tool for an agent."""
        body: dict[str, Any] = {}
        if description is not None:
            body["description"] = description
        if parameters is not None:
            body["parameters"] = parameters
        return await self._http.put(f"/api/v1/agents/{agent_id}/tools/{tool_name}", json_data=body)

    async def delete_custom_tool(self, agent_id: str, tool_name: str) -> None:
        """Delete a custom tool from an agent."""
        await self._http.delete(f"/api/v1/agents/{agent_id}/tools/{tool_name}")

    # -- Consolidation --

    async def consolidate(
        self,
        agent_id: str,
        *,
        period: str = "daily",
        user_id: str | None = None,
    ) -> ConsolidateResponse:
        """Trigger memory consolidation for an agent."""
        body: dict[str, Any] = {"period": period}
        if user_id is not None:
            body["user_id"] = user_id
        return ConsolidateResponse.model_validate(
            await self._http.post(f"/api/v1/agents/{agent_id}/consolidate", json_data=body)
        )

    # -- Summaries --

    async def get_summaries(
        self,
        agent_id: str,
        *,
        period: str | None = None,
        limit: int | None = None,
    ) -> SummariesResponse:
        """Get memory summaries for an agent."""
        params: dict[str, str] = {}
        if period is not None:
            params["period"] = period
        if limit is not None:
            params["limit"] = str(limit)
        return SummariesResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/summaries", params=params)
        )

    # -- Process --

    async def process(
        self,
        agent_id: str,
        *,
        user_id: str,
        messages: list[dict[str, str]],
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        include_extractions: bool | None = None,
    ) -> ProcessResponse:
        """Run the full Context Engine pipeline without generating a chat response."""
        body: dict[str, Any] = {"userId": user_id, "messages": messages}
        if session_id is not None:
            body["sessionId"] = session_id
        if instance_id is not None:
            body["instanceId"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if include_extractions is not None:
            body["include_extractions"] = include_extractions
        return ProcessResponse.model_validate(
            await self._http.post(f"/api/v1/agents/{agent_id}/process", json_data=body)
        )

    # -- Models --

    async def get_models(self, agent_id: str) -> ModelsResponse:
        """Get available LLM providers and models."""
        return ModelsResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/models")
        )

    # -- Context --

    async def get_context(
        self,
        agent_id: str,
        *,
        user_id: str,
        session_id: str | None = None,
        instance_id: str | None = None,
        query: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> EnrichedContextResponse:
        """Get the full enriched agent context in a single call."""
        params: dict[str, str] = {"userId": user_id}
        if session_id is not None:
            params["sessionId"] = session_id
        if instance_id is not None:
            params["instanceId"] = instance_id
        if query is not None:
            params["query"] = query
        if language is not None:
            params["language"] = language
        if timezone is not None:
            params["timezone"] = timezone
        return EnrichedContextResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/context", params=params)
        )

    # -- Avatar --

    async def generate_avatar(
        self,
        agent_id: str,
        *,
        style: str | None = None,
    ) -> GenerateAvatarResponse:
        """Trigger avatar generation for an agent."""
        body: dict[str, Any] = {}
        if style is not None:
            body["style"] = style
        return GenerateAvatarResponse.model_validate(
            await self._http.post(f"/api/v1/agents/{agent_id}/avatar/generate", json_data=body)
        )

    # -- Time Machine --

    async def get_time_machine(
        self,
        agent_id: str,
        *,
        at: str,
        user_id: str | None = None,
        instance_id: str | None = None,
    ) -> TimeMachineResponse:
        """Get an agent's personality and mood state at a specific point in time."""
        params: dict[str, str] = {"at": at}
        if user_id is not None:
            params["user_id"] = user_id
        if instance_id is not None:
            params["instance_id"] = instance_id
        return TimeMachineResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/timemachine", params=params)
        )

    # -- Knowledge Search (tool endpoint) --

    async def knowledge_search(
        self,
        agent_id: str,
        *,
        query: str,
        limit: int | None = None,
    ) -> AgentKBSearchResponse:
        """Search the knowledge base for an agent."""
        body: dict[str, Any] = {"query": query}
        if limit is not None:
            body["limit"] = limit
        return AgentKBSearchResponse.model_validate(
            await self._http.post(
                f"/api/v1/agents/{agent_id}/tools/kb-search",
                json_data=body,
            )
        )

    # -- Tool Schemas (BYO-LLM) --

    async def get_tools(self, agent_id: str) -> ToolSchemasResponse:
        """Return tool schemas available for an agent (for BYO-LLM integrations)."""
        return ToolSchemasResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/tools")
        )

    async def get_tool_schemas(self, agent_id: str) -> GetToolSchemasResponse:
        """Return OpenAPI-style tool schemas for BYO-LLM tool calling."""
        return GetToolSchemasResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/tools/schemas")
        )

    # -- Fork --

    async def fork(
        self,
        agent_id: str,
        *,
        name: str | None = None,
    ) -> ForkResponse:
        """Fork an agent (create a copy with a new ID)."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        return ForkResponse.model_validate(
            await self._http.post(f"/api/v1/agents/{agent_id}/fork", json_data=body)
        )

    async def get_fork_status(self, agent_id: str) -> ForkStatusResponse:
        """Check the status of a fork operation."""
        return ForkStatusResponse.model_validate(
            await self._http.get(f"/api/v1/agents/{agent_id}/fork/status")
        )

    # -- Playground Chat --

    async def playground_chat(
        self,
        agent_id: str,
        *,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        language: str | None = None,
    ) -> ChatResponse:
        """Send a playground chat message (non-streaming). Same as chat but via the playground endpoint."""
        body: dict[str, Any] = {"messages": messages}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if language is not None:
            body["language"] = language

        parts: list[str] = []
        async for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/playground/chat", json_data=body
        ):
            parsed = ChatStreamEvent.model_validate(event)
            if parsed.choices and parsed.choices[0].delta.get("content"):
                parts.append(parsed.choices[0].delta["content"])
        return ChatResponse(content="".join(parts))

    async def playground_chat_stream(
        self,
        agent_id: str,
        *,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        session_id: str | None = None,
        instance_id: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        language: str | None = None,
    ) -> AsyncIterator[ChatStreamEvent]:
        """Send a playground chat message and stream events."""
        body: dict[str, Any] = {"messages": messages}
        if user_id is not None:
            body["user_id"] = user_id
        if session_id is not None:
            body["session_id"] = session_id
        if instance_id is not None:
            body["instance_id"] = instance_id
        if provider is not None:
            body["provider"] = provider
        if model is not None:
            body["model"] = model
        if language is not None:
            body["language"] = language

        async for event in self._http.stream_sse(
            "POST", f"/api/v1/agents/{agent_id}/playground/chat", json_data=body
        ):
            yield ChatStreamEvent.model_validate(event)

    # -- Knowledge Search GET --

    async def knowledge_search_get(
        self,
        agent_id: str,
        *,
        query: str,
        limit: int | None = None,
    ) -> AgentKBSearchResponse:
        """Search the knowledge base using a GET request with query parameters."""
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        return AgentKBSearchResponse.model_validate(
            await self._http.get(
                f"/api/v1/agents/{agent_id}/tools/kb-search",
                params=params,
            )
        )
