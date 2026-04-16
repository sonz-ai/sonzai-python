"""Public types for the Sonzai SDK."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatChoice(BaseModel):
    delta: dict[str, str] = Field(default_factory=dict)
    finish_reason: str | None = None
    index: int = 0


class ChatUsage(BaseModel):
    prompt_tokens: int = Field(alias="promptTokens", default=0)
    completion_tokens: int = Field(alias="completionTokens", default=0)
    total_tokens: int = Field(alias="totalTokens", default=0)

    model_config = {"populate_by_name": True}


class ChatStreamEvent(BaseModel):
    """A single SSE event from the chat stream."""

    choices: list[ChatChoice] = Field(default_factory=list)
    usage: ChatUsage | None = None
    type: str | None = None
    data: dict[str, Any] | None = None
    error: dict[str, str] | None = None

    # Rich event fields (populated based on type)
    message_index: int = 0
    is_follow_up: bool = False
    replacement: bool = False
    full_content: str = ""
    finish_reason: str = ""
    continuation_token: str = ""
    message_count: int = 0
    side_effects: dict[str, Any] | None = None
    external_tool_calls: list[ExternalToolCall] = Field(default_factory=list)
    error_message: str = ""
    error_code: str = ""
    is_token_error: bool = False

    model_config = {"extra": "allow"}

    @property
    def content(self) -> str:
        if self.choices:
            return self.choices[0].delta.get("content", "")
        return ""

    @property
    def is_finished(self) -> bool:
        return bool(self.choices and self.choices[0].finish_reason == "stop")


class ChatResponse(BaseModel):
    """Aggregated chat response (non-streaming)."""

    content: str
    session_id: str
    usage: ChatUsage | None = None


class ExternalToolCall(BaseModel):
    id: str = ""
    name: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolCallResponseOptions(BaseModel):
    session_id: str = ""
    user_id: str = ""
    tool_call_id: str = ""
    result: Any = None


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------


class MemoryNode(BaseModel):
    node_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    parent_id: str = ""
    title: str = ""
    summary: str = ""
    importance: float = 0.0
    created_at: str | None = None
    updated_at: str | None = None


class AtomicFact(BaseModel):
    fact_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    node_id: str = ""
    atomic_text: str = ""
    fact_type: str = ""
    importance: float = 0.0
    supersedes_id: str = ""
    session_id: str = ""
    metadata: dict[str, Any] | None = None
    created_at: str | None = None


class MemoryResponse(BaseModel):
    nodes: list[MemoryNode] = Field(default_factory=list)
    contents: dict[str, list[AtomicFact]] = Field(default_factory=dict)


class MemorySearchResult(BaseModel):
    fact_id: str = ""
    content: str = ""
    fact_type: str = ""
    score: float = 0.0


class MemorySearchResponse(BaseModel):
    results: list[MemorySearchResult] = Field(default_factory=list)


class TimelineSession(BaseModel):
    session_id: str = ""
    facts: list[AtomicFact] = Field(default_factory=list)
    first_fact_at: str | None = None
    last_fact_at: str | None = None
    fact_count: int = 0


class MemoryTimelineResponse(BaseModel):
    sessions: list[TimelineSession] = Field(default_factory=list)
    total_facts: int = 0


# ---------------------------------------------------------------------------
# Personality
# ---------------------------------------------------------------------------


class Big5Trait(BaseModel):
    score: float = 0.0
    percentile: int = 0
    confidence: float = 0.0


class Big5(BaseModel):
    openness: Big5Trait = Field(default_factory=Big5Trait)
    conscientiousness: Big5Trait = Field(default_factory=Big5Trait)
    extraversion: Big5Trait = Field(default_factory=Big5Trait)
    agreeableness: Big5Trait = Field(default_factory=Big5Trait)
    neuroticism: Big5Trait = Field(default_factory=Big5Trait)


class PersonalityDimensions(BaseModel):
    warmth: int = 5
    energy: int = 5
    openness: int = 5
    emotional_depth: int = 5
    playfulness: int = 5
    supportiveness: int = 5
    curiosity: int = 5
    wisdom: int = 5


class PersonalityPreferences(BaseModel):
    pace: str = ""
    formality: str = ""
    humor_style: str = ""
    emotional_expression: str = ""


class PersonalityBehaviors(BaseModel):
    proactivity: str = ""
    reliability: str = ""
    humor: str = ""


class PersonalityProfile(BaseModel):
    agent_id: str = ""
    name: str = ""
    gender: str = ""
    bio: str = ""
    avatar_url: str = ""
    personality_prompt: str = ""
    speech_patterns: list[str] = Field(default_factory=list)
    true_interests: list[str] = Field(default_factory=list)
    true_dislikes: list[str] = Field(default_factory=list)
    primary_traits: list[str] = Field(default_factory=list)
    temperature: float = 0.0
    big5: Big5 = Field(default_factory=Big5)
    dimensions: PersonalityDimensions = Field(default_factory=PersonalityDimensions)
    preferences: PersonalityPreferences = Field(default_factory=PersonalityPreferences)
    behaviors: PersonalityBehaviors = Field(default_factory=PersonalityBehaviors)
    emotional_tendencies: dict[str, float] = Field(default_factory=dict)
    created_at: str | None = None


class PersonalityDelta(BaseModel):
    delta_id: str = ""
    change: str = ""
    reason: str = ""
    created_at: str | None = None


class PersonalityResponse(BaseModel):
    profile: PersonalityProfile = Field(default_factory=PersonalityProfile)
    evolution: list[PersonalityDelta] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


class SessionResponse(BaseModel):
    success: bool = False


# ---------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------


class AgentInstance(BaseModel):
    instance_id: str = ""
    agent_id: str = ""
    name: str = ""
    description: str = ""
    status: str = ""
    is_default: bool = False
    created_at: str | None = None
    updated_at: str | None = None


class InstanceListResponse(BaseModel):
    instances: list[AgentInstance] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------


class Notification(BaseModel):
    message_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    wakeup_id: str = ""
    check_type: str = ""
    intent: str = ""
    generated_message: str = ""
    status: str = ""
    consumed_at: str | None = None
    created_at: str | None = None


class NotificationListResponse(BaseModel):
    notifications: list[Notification] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Context Engine Data
# ---------------------------------------------------------------------------


class MoodResponse(BaseModel):
    """Raw mood data from the API."""

    model_config = {"extra": "allow"}


class RelationshipResponse(BaseModel):
    model_config = {"extra": "allow"}


class HabitsResponse(BaseModel):
    model_config = {"extra": "allow"}


class Habit(BaseModel):
    """Full habit entity returned from create/update endpoints."""

    id: str = ""
    agent_id: str = ""
    user_id: str = ""
    name: str = ""
    category: str = ""
    description: str = ""
    display_name: str = ""
    strength: float = 0.0
    formed: bool = False
    observation_count: int = 0
    last_reinforced_at: str | None = None
    formed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    model_config = {"extra": "allow"}


class ConstellationNode(BaseModel):
    """Full constellation node entity returned from create/update endpoints."""

    node_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    node_type: str = ""
    label: str = ""
    description: str = ""
    significance: float = 0.0
    mention_count: int = 0
    brightness: float = 0.0
    first_mentioned_at: str | None = None
    last_mentioned_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    model_config = {"extra": "allow"}


GoalType = str
"""One of: personal_growth, skill_mastery, relationship, learning_discovery."""

GoalStatus = str
"""One of: active, achieved, abandoned."""

GoalPriority = int
"""0 = low, 1 = medium, 2 = high."""


class Goal(BaseModel):
    goal_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    type: str = ""
    title: str = ""
    description: str = ""
    priority: int = 0
    status: str = ""
    related_traits: list[str] = Field(default_factory=list)
    created_at: str | None = None
    achieved_at: str | None = None
    updated_at: str | None = None

    model_config = {"extra": "allow"}


class GoalsResponse(BaseModel):
    goals: list[Goal] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class InitialGoal(BaseModel):
    """Goal definition used when creating an agent with initial goals."""

    type: str = ""
    title: str = ""
    description: str = ""
    priority: int = 0
    related_traits: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class InterestsResponse(BaseModel):
    model_config = {"extra": "allow"}


class DiaryResponse(BaseModel):
    model_config = {"extra": "allow"}


class UsersResponse(BaseModel):
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


class EvalCategory(BaseModel):
    name: str = ""
    score: float = 0.0
    feedback: str = ""


class EvaluationResult(BaseModel):
    score: float = 0.0
    feedback: str = ""
    categories: list[EvalCategory] = Field(default_factory=list)


class EvalTemplateCategory(BaseModel):
    name: str = ""
    weight: float = 0.0
    criteria: str = ""


class EvalTemplate(BaseModel):
    id: str = ""
    tenant_id: str = ""
    name: str = ""
    description: str = ""
    template_type: str = ""
    judge_model: str = ""
    temperature: float = 0.3
    max_tokens: int = 8192
    scoring_rubric: str = ""
    categories: list[EvalTemplateCategory] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class EvalTemplateListResponse(BaseModel):
    templates: list[EvalTemplate] = Field(default_factory=list)


class EvalRun(BaseModel):
    id: str = ""
    tenant_id: str = ""
    agent_id: str = ""
    agent_name: str = ""
    status: str = ""
    character_config: dict[str, Any] = Field(default_factory=dict)
    template_id: str = ""
    template_snapshot: dict[str, Any] = Field(default_factory=dict)
    simulation_config: dict[str, Any] = Field(default_factory=dict)
    simulation_model: str = ""
    user_persona: dict[str, Any] = Field(default_factory=dict)
    transcript: list[Any] = Field(default_factory=list)
    evaluation_result: dict[str, Any] = Field(default_factory=dict)
    adaptation_result: dict[str, Any] = Field(default_factory=dict)
    simulation_state: dict[str, Any] = Field(default_factory=dict)
    total_sessions: int = 0
    total_turns: int = 0
    simulated_minutes: int = 0
    total_cost_usd: float = 0.0
    error_reason: str = ""
    simulation_cost_usd: float = 0.0
    evaluation_cost_usd: float = 0.0
    adaptation_template_id: str = ""
    adaptation_template_snapshot: Any = None
    created_at: str | None = None
    completed_at: str | None = None


class EvalRunListResponse(BaseModel):
    runs: list[EvalRun] = Field(default_factory=list)
    total_count: int = 0


# ---------------------------------------------------------------------------
# Run Reference (async run pattern)
# ---------------------------------------------------------------------------


class RunRef(BaseModel):
    """Reference returned when starting an async simulation/eval run."""

    run_id: str = ""
    status: str = ""
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Simulation / RunEval streaming
# ---------------------------------------------------------------------------


class SimulationEvent(BaseModel):
    """A single SSE event from simulation or run-eval streams."""

    type: str = ""
    session_index: int = 0
    total_sessions: int = 0
    total_turns: int = 0
    total_cost_usd: float = 0.0
    message: str = ""
    eval_result: dict[str, Any] | None = None
    adaptation_result: dict[str, Any] | None = None
    error: dict[str, str] | None = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# User Persona
# ---------------------------------------------------------------------------


class UserPersona(BaseModel):
    id: str = ""
    name: str = ""
    background: str = ""
    personality_traits: list[str] = Field(default_factory=list)
    communication_style: str = ""

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Agent CRUD
# ---------------------------------------------------------------------------


class Agent(BaseModel):
    agent_id: str = ""
    name: str = ""
    bio: str = ""
    gender: str = ""
    avatar_url: str = ""
    status: str = ""
    personality_prompt: str = ""
    speech_patterns: list[str] = Field(default_factory=list)
    true_interests: list[str] = Field(default_factory=list)
    true_dislikes: list[str] = Field(default_factory=list)
    created_at: str | None = None

    model_config = {"extra": "allow"}


class DeleteResponse(BaseModel):
    success: bool = False

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Events / Dialogue
# ---------------------------------------------------------------------------


class TriggerEventResponse(BaseModel):
    accepted: bool = False
    event_id: str = ""

    model_config = {"extra": "allow"}


class DialogueResponse(BaseModel):
    response: str = ""
    side_effects: dict[str, Any] | None = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Constellation / Breakthroughs / Wakeups / Mood Aggregate
# ---------------------------------------------------------------------------


class ConstellationResponse(BaseModel):
    model_config = {"extra": "allow"}


class BreakthroughsResponse(BaseModel):
    model_config = {"extra": "allow"}


class WakeupsResponse(BaseModel):
    model_config = {"extra": "allow"}


class MoodAggregateResponse(BaseModel):
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Memory Facts / Reset / Seed
# ---------------------------------------------------------------------------


class Fact(BaseModel):
    fact_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    content: str = ""
    category: str = ""
    confidence: float = 0.0
    mention_count: int = 0
    created_at: str | None = None
    last_mentioned_at: str | None = None
    context_examples: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class FactListResponse(BaseModel):
    facts: list[Fact] = Field(default_factory=list)
    total_count: int = 0
    has_more: bool = False


class MemoryResetResponse(BaseModel):
    agent_id: str = ""
    user_id: str = ""
    status: str = ""
    facts_deleted: int = 0
    relationships_deleted: int = 0

    model_config = {"extra": "allow"}


class SeedMemoriesResponse(BaseModel):
    memories_created: int = 0

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Personality Update
# ---------------------------------------------------------------------------


class PersonalityUpdateResponse(BaseModel):
    agent_id: str = ""
    status: str = ""

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Voice
# ---------------------------------------------------------------------------


class Voice(BaseModel):
    voice_id: str = ""
    voice_name: str = ""
    gender: str = ""
    tier: int = 0
    provider: str = ""
    language: str = ""
    accent: str = ""
    age_profile: str = ""
    description: str = ""
    sample_audio_url: str = ""
    availability: str = ""

    model_config = {"extra": "allow"}


class VoiceListResponse(BaseModel):
    voices: list[Voice] = Field(default_factory=list)
    total_count: int = 0
    has_more: bool = False


class VoiceStreamToken(BaseModel):
    """Token for establishing a voice live WebSocket connection."""

    ws_url: str = Field(default="", alias="wsUrl")
    auth_token: str = Field(default="", alias="authToken")

    model_config = {"populate_by_name": True, "extra": "allow"}


class VoiceUsage(BaseModel):
    """Usage statistics from a voice session."""

    prompt_tokens: int = Field(default=0, alias="promptTokens")
    completion_tokens: int = Field(default=0, alias="completionTokens")
    total_tokens: int = Field(default=0, alias="totalTokens")

    model_config = {"populate_by_name": True, "extra": "allow"}


class VoiceStreamEvent(BaseModel):
    """Server event from the voice live WebSocket stream.

    Event types: "ready", "session_ready", "input_transcript",
    "output_transcript", "agent_state", "turn_complete", "tool_activity",
    "side_effects", "usage", "session_ended", "error", or "audio".
    """

    type: str = ""
    session_id: str = Field(default="", alias="sessionId")
    text: str = ""
    is_final: bool | None = Field(default=None, alias="isFinal")
    speaking: bool | None = None
    turn_index: int | None = Field(default=None, alias="turnIndex")
    # tool_activity fields
    name: str = ""
    status: str = ""
    # side_effects fields
    facts: list | None = None
    emotions: dict | None = None
    relationship_delta: dict | None = Field(default=None, alias="relationshipDelta")
    # usage fields
    prompt_tokens: int = Field(default=0, alias="promptTokens")
    completion_tokens: int = Field(default=0, alias="completionTokens")
    total_tokens: int = Field(default=0, alias="totalTokens")
    # session_ended fields
    reason: str = ""
    total_usage: VoiceUsage | None = Field(default=None, alias="totalUsage")
    turn_count: int = Field(default=0, alias="turnCount")
    # session_ready fields
    voice_name: str = Field(default="", alias="voiceName")
    # error fields
    error: str = ""
    error_code: str = Field(default="", alias="errorCode")
    # audio (binary, set when type is "audio")
    audio: bytes = b""

    model_config = {"populate_by_name": True, "extra": "allow"}


# ---------------------------------------------------------------------------
# Voice TTS/STT
# ---------------------------------------------------------------------------


class TTSResponse(BaseModel):
    """Response from text-to-speech synthesis."""

    audio: str = ""
    content_type: str = Field(default="", alias="contentType")
    duration_ms: int = Field(default=0, alias="durationMs")
    usage: dict = Field(default_factory=dict)

    model_config = {"populate_by_name": True, "extra": "allow"}


class STTResponse(BaseModel):
    """Response from speech-to-text transcription."""

    transcript: str = ""
    confidence: float = 0.0
    language_code: str = Field(default="", alias="languageCode")

    model_config = {"populate_by_name": True, "extra": "allow"}


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------


class GenerateBioResponse(BaseModel):
    bio: str = ""
    tone: str = ""
    confidence: float = 0.0

    model_config = {"extra": "allow"}


class ImageGenerateResponse(BaseModel):
    image_id: str = ""
    public_url: str = ""
    mime_type: str = ""
    generation_time_ms: int = 0

    model_config = {"extra": "allow"}


class GeneratedGoal(BaseModel):
    """A goal generated as part of character generation."""

    type: str = ""
    title: str = ""
    description: str = ""
    priority: int = 0

    model_config = {"extra": "allow"}


class GenerateCharacterResponse(BaseModel):
    agent_id: str = ""
    """The resolved agent ID (provided or derived from name)."""
    existing: bool = False
    """True when the agent already existed and the LLM was not called."""
    bio: str = ""
    personality_prompt: str = ""
    big5: dict[str, Any] = Field(default_factory=dict)
    speech_patterns: list[str] = Field(default_factory=list)
    true_interests: list[str] = Field(default_factory=list)
    true_dislikes: list[str] = Field(default_factory=list)
    primary_traits: list[str] = Field(default_factory=list)
    dimensions: dict[str, Any] = Field(default_factory=dict)
    preferences: dict[str, Any] = Field(default_factory=dict)
    behaviors: dict[str, Any] = Field(default_factory=dict)
    initial_goals: list[GeneratedGoal] = Field(default_factory=list)
    world_description: str = ""
    origin_prompt_instructions: str = ""

    model_config = {"extra": "allow"}


class GenerateSeedMemoriesResponse(BaseModel):
    memories: list[dict[str, Any]] = Field(default_factory=list)
    memories_stored: int = 0

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Custom States
# ---------------------------------------------------------------------------


class CustomState(BaseModel):
    state_id: str = ""
    agent_id: str = ""
    scope: str = ""
    key: str = ""
    value: Any = None
    content_type: str = ""
    user_id: str = ""
    instance_id: str = ""
    created_at: str | None = None
    updated_at: str | None = None

    model_config = {"extra": "allow"}


class CustomStateListResponse(BaseModel):
    states: list[CustomState] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


class WebhookEndpoint(BaseModel):
    event_type: str = ""
    webhook_url: str = ""
    auth_header: str = ""
    is_active: bool = True
    created_at: str = ""

    model_config = {"extra": "allow"}


class WebhookRegisterResponse(BaseModel):
    success: bool = False
    signing_secret: str = ""

    model_config = {"extra": "allow"}


class WebhookListResponse(BaseModel):
    webhooks: list[WebhookEndpoint] = Field(default_factory=list)


class WebhookDeliveryAttempt(BaseModel):
    attempt_id: str = ""
    event_type: str = ""
    webhook_url: str = ""
    response_code: int = 0
    response_body: str = ""
    error_message: str = ""
    duration_ms: int = 0
    attempt_number: int = 0
    status: str = ""
    created_at: str = ""

    model_config = {"extra": "allow"}


class DeliveryAttemptsResponse(BaseModel):
    attempts: list[WebhookDeliveryAttempt] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Project Config
# ---------------------------------------------------------------------------


class ProjectConfigEntry(BaseModel):
    key: str
    value: Any = None
    updated_at: str | None = None


class ProjectConfigListResponse(BaseModel):
    configs: list[ProjectConfigEntry] = []


# ---------------------------------------------------------------------------
# Custom LLM
# ---------------------------------------------------------------------------


class CustomLLMConfigResponse(BaseModel):
    endpoint: str = ""
    api_key_prefix: str = ""
    model: str = ""
    display_name: str = ""
    is_active: bool = False
    configured: bool = False


# ---------------------------------------------------------------------------
# Project Notifications
# ---------------------------------------------------------------------------


class ProjectNotificationListResponse(BaseModel):
    notifications: list[Notification] = []
    count: int = 0


class AcknowledgeResponse(BaseModel):
    acknowledged: int = 0


# ---------------------------------------------------------------------------
# Wakeup Scheduling
# ---------------------------------------------------------------------------


class ScheduledWakeup(BaseModel):
    wakeup_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    scheduled_at: str = ""
    check_type: str = ""
    status: str = ""
    intent: str = ""
    last_topic: str = ""
    event_description: str = ""
    occasion: str = ""
    interest_topic: str = ""
    executed_at: str | None = None
    created_at: str | None = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Agent List (paginated)
# ---------------------------------------------------------------------------


class AgentIndex(BaseModel):
    model_config = {"extra": "allow"}
    id: str = ""
    tenant_id: str = ""
    name: str = ""
    bio: str = ""
    gender: str = ""
    avatar_url: str = ""
    status: str = ""
    project_id: str = ""
    created_at: str = ""


class AgentListResponse(BaseModel):
    items: list[AgentIndex] = Field(default_factory=list)
    next_cursor: str | None = None
    has_more: bool = False


# ---------------------------------------------------------------------------
# Batch Personality
# ---------------------------------------------------------------------------


class BatchPersonalityEntry(BaseModel):
    model_config = {"extra": "allow"}
    profile: PersonalityProfile = Field(default_factory=PersonalityProfile)
    evolution_count: int = 0


class BatchPersonalityResponse(BaseModel):
    personalities: dict[str, BatchPersonalityEntry] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Personality Extensions
# ---------------------------------------------------------------------------


class SignificantMoment(BaseModel):
    model_config = {"extra": "allow"}
    agent_id: str = ""
    moment_id: str = ""
    timestamp: str = ""
    description: str = ""
    significance_score: float = 0.0


class SignificantMomentsResponse(BaseModel):
    moments: list[SignificantMoment] = Field(default_factory=list)


class PersonalityShift(BaseModel):
    model_config = {"extra": "allow"}
    agent_id: str = ""
    trait_name: str = ""
    trait_category: str = ""
    old_value: float = 0.0
    new_value: float = 0.0
    delta: float = 0.0
    timestamp: str = ""
    reason: str = ""


class RecentShiftsResponse(BaseModel):
    shifts: list[PersonalityShift] = Field(default_factory=list)


class UserPersonalityOverlay(BaseModel):
    model_config = {"extra": "allow"}
    agent_id: str = ""
    user_id: str = ""
    big5: Big5 | None = None
    dimensions: PersonalityDimensions | None = None
    preferences: PersonalityPreferences | None = None
    behaviors: PersonalityBehaviors | None = None
    primary_traits: list[str] = Field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


class UserOverlaysListResponse(BaseModel):
    overlays: list[UserPersonalityOverlay] = Field(default_factory=list)


class UserOverlayDetailResponse(BaseModel):
    overlay: UserPersonalityOverlay = Field(default_factory=UserPersonalityOverlay)
    base: PersonalityProfile = Field(default_factory=PersonalityProfile)
    evolution: list[PersonalityShift] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Fact History
# ---------------------------------------------------------------------------


class FactHistoryResponse(BaseModel):
    current: AtomicFact = Field(default_factory=AtomicFact)
    previous_versions: list[AtomicFact] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Process (full pipeline)
# ---------------------------------------------------------------------------


class ProcessSideEffectsSummary(BaseModel):
    model_config = {"extra": "allow"}
    mood_updated: bool = False
    personality_updated: bool = False
    habits_observed: int = 0
    interests_detected: int = 0


class ExtractionFact(BaseModel):
    text: str = ""
    fact_type: str = ""
    importance: float = 0.0
    entities: list[str] = Field(default_factory=list)
    sentiment: str = ""
    topic_tags: list[str] = Field(default_factory=list)


class ExtractionPersonalityDelta(BaseModel):
    trait: str = ""
    delta: float = 0.0
    reason: str = ""


class ExtractionDimensionDelta(BaseModel):
    dimension: str = ""
    delta: float = 0.0
    reason: str = ""


class ExtractionMoodDelta(BaseModel):
    happiness: float = 0.0
    energy: float = 0.0
    calmness: float = 0.0
    affection: float = 0.0
    reason: str = ""


class ExtractionHabit(BaseModel):
    name: str = ""
    category: str = ""
    description: str = ""
    is_reinforcement: bool = False


class ExtractionInterest(BaseModel):
    topic: str = ""
    category: str = ""
    confidence: float = 0.0
    engagement_level: float = 0.0


class ExtractionRelationshipDelta(BaseModel):
    score_change: int = 0
    reason: str = ""


class ExtractionProactive(BaseModel):
    type: str = ""
    description: str = ""
    delay_hours: int = 0
    intent: str = ""


class ExtractionRecurring(BaseModel):
    description: str = ""
    pattern: str = ""
    confidence: float = 0.0


class ExtractionInnerThoughts(BaseModel):
    diary: str = ""
    reflection: str = ""


class SideEffectExtraction(BaseModel):
    memory_facts: list[ExtractionFact] = Field(default_factory=list)
    personality_deltas: list[ExtractionPersonalityDelta] = Field(default_factory=list)
    dimension_deltas: list[ExtractionDimensionDelta] = Field(default_factory=list)
    mood_delta: ExtractionMoodDelta | None = None
    habit_observations: list[ExtractionHabit] = Field(default_factory=list)
    interests_detected: list[ExtractionInterest] = Field(default_factory=list)
    relationship_delta: ExtractionRelationshipDelta | None = None
    proactive_suggestions: list[ExtractionProactive] = Field(default_factory=list)
    recurring_events: list[ExtractionRecurring] = Field(default_factory=list)
    inner_thoughts: ExtractionInnerThoughts | None = None
    emotional_themes: list[str] = Field(default_factory=list)


class ProcessResponse(BaseModel):
    model_config = {"extra": "allow"}
    success: bool = False
    memories_created: int = 0
    facts_extracted: int = 0
    side_effects: ProcessSideEffectsSummary = Field(default_factory=ProcessSideEffectsSummary)
    extractions: SideEffectExtraction | None = None


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ModelVariant(BaseModel):
    """A single model variant offered by a provider."""

    id: str = ""
    display_name: str = ""


class ModelsProviderEntry(BaseModel):
    provider: str = ""
    provider_name: str = ""
    default_model: str = ""
    models: list[ModelVariant] = Field(default_factory=list)


class ModelsResponse(BaseModel):
    default_provider: str = ""
    default_model: str = ""
    providers: list[ModelsProviderEntry] = Field(default_factory=list)


class PlatformModelsResponse(BaseModel):
    """Response from ``GET /api/v1/models``."""

    default_model: str = ""
    providers: list[ModelsProviderEntry] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Context (single-call enriched context)
# ---------------------------------------------------------------------------


class EnrichedContextResponse(BaseModel):
    model_config = {"extra": "allow", "populate_by_name": True}
    # Layer 1: Core Identity
    bio: str | None = None
    personality_prompt: str | None = None
    speech_patterns: list[str] | None = None
    true_interests: list[str] | None = None
    true_dislikes: list[str] | None = None
    primary_traits: list[str] | None = None
    # Layer 2: Personality
    big5: dict[str, Any] | None = None
    dimensions: dict[str, Any] | None = None
    preferences: dict[str, Any] | None = None
    behaviors: dict[str, Any] | None = None
    # Layer 3: Evolution
    recent_personality_shifts: list[Any] | None = None
    significant_moments: list[Any] | None = None
    active_goals: list[Any] | None = None
    habits: list[Any] | None = None
    breakthrough_count: int | None = None
    # Layer 4: Relationship
    relationship_narrative: str | None = None
    shared_memory_summary: str | None = None
    chemistry_score: float | None = None
    love_from_agent: float | None = None
    love_from_user: float | None = None
    relationship_status: str | None = None
    days_since_last_chat: int | None = None
    # Layer 5: Current State
    current_mood: dict[str, Any] | None = None
    emotional_state: str | None = None
    capabilities: dict[str, Any] | None = None
    # Layer 6: Memory
    loaded_facts: list[dict[str, Any]] | None = None
    long_term_summaries: list[Any] | None = None
    # Layer 6b: Proactive
    proactive_memories: list[Any] | None = None
    # Layer 6c: Constellation
    constellation_patterns: list[Any] | None = None
    # Layer 7: Backend Context
    backend_context: dict[str, Any] | None = Field(default=None, alias="game_context")


# ---------------------------------------------------------------------------
# Avatar Generation
# ---------------------------------------------------------------------------


class GenerateAvatarResponse(BaseModel):
    model_config = {"extra": "allow"}
    success: bool = False
    avatar_url: str = ""
    prompt: str = ""
    generation_time_ms: int = 0


# ---------------------------------------------------------------------------
# Time Machine
# ---------------------------------------------------------------------------


class TimeMachineMoodSnapshot(BaseModel):
    model_config = {"extra": "allow"}
    valence: float = 0.0
    arousal: float = 0.0
    tension: float = 0.0
    affiliation: float = 0.0
    label: str = ""


class TimeMachineResponse(BaseModel):
    model_config = {"extra": "allow"}
    personality_at: dict[str, Any] | None = None
    current_personality: dict[str, Any] | None = None
    evolution_events: list[PersonalityShift] = Field(default_factory=list)
    mood_at: TimeMachineMoodSnapshot | None = None
    requested_at: str = ""


# ---------------------------------------------------------------------------
# Agent Status
# ---------------------------------------------------------------------------


class SetStatusResponse(BaseModel):
    success: bool = False
    agent_id: str = ""
    is_active: bool = False


# ---------------------------------------------------------------------------
# Capabilities
# ---------------------------------------------------------------------------


class CustomToolDefinition(BaseModel):
    name: str = ""
    description: str = ""
    parameters: dict[str, Any] | None = None


class AgentCapabilities(BaseModel):
    model_config = {"extra": "allow"}
    webSearch: bool = False
    rememberName: bool = False
    imageGeneration: bool = False
    inventory: bool = False
    customTools: list[CustomToolDefinition] = Field(default_factory=list)


class CustomToolListResponse(BaseModel):
    tools: list[CustomToolDefinition] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Consolidation
# ---------------------------------------------------------------------------


class ConsolidateResponse(BaseModel):
    success: bool = False


# ---------------------------------------------------------------------------
# Summaries
# ---------------------------------------------------------------------------


class MemorySummary(BaseModel):
    model_config = {"extra": "allow"}
    agent_id: str = ""
    stage: str = ""
    summary_text: str = ""
    timestamp: str = ""
    fact_count: int = 0
    confidence: float = 0.0


class SummariesResponse(BaseModel):
    summaries: list[MemorySummary] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Update Project
# ---------------------------------------------------------------------------


class UpdateProjectResponse(BaseModel):
    success: bool = False
    agent_id: str = ""
    project_id: str = ""


# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------


class KBDocument(BaseModel):
    project_id: str = ""
    document_id: str = ""
    file_name: str = ""
    content_type: str = ""
    file_size: int = 0
    gcs_path: str = ""
    checksum: str = ""
    status: str = ""
    uploaded_by: str = ""
    extraction_tokens: int = 0
    created_at: str = ""
    updated_at: str = ""


class KBDocumentListResponse(BaseModel):
    documents: list[KBDocument] = Field(default_factory=list)
    total: int = 0


class KBNode(BaseModel):
    project_id: str = ""
    node_id: str = ""
    node_type: str = ""
    label: str = ""
    norm_label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    source_type: str = ""
    version: int = 0
    is_active: bool = True
    confidence: float = 0.0
    created_at: str = ""
    updated_at: str = ""


class KBNodeListResponse(BaseModel):
    nodes: list[KBNode] = Field(default_factory=list)
    total: int = 0
    next_cursor: str = ""


class KBEdge(BaseModel):
    project_id: str = ""
    edge_id: str = ""
    from_node_id: str = ""
    to_node_id: str = ""
    edge_type: str = ""
    confidence: float = 0.0
    created_at: str = ""
    updated_at: str = ""


class KBNodeHistory(BaseModel):
    project_id: str = ""
    node_id: str = ""
    version: int = 0
    properties: dict[str, Any] = Field(default_factory=dict)
    changed_by: str = ""
    change_type: str = ""
    changed_at: str = ""


class KBNodeDetailResponse(BaseModel):
    node: KBNode | None = None
    outgoing: list[KBEdge] = Field(default_factory=list)
    incoming: list[KBEdge] = Field(default_factory=list)
    history: list[KBNodeHistory] = Field(default_factory=list)


class KBNodeHistoryResponse(BaseModel):
    history: list[KBNodeHistory] = Field(default_factory=list)
    total: int = 0


class KBSearchResult(BaseModel):
    node_id: str = ""
    node_type: str = ""
    label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)
    source: str = ""
    updated_at: str = ""
    score: float = 0.0
    related: list[dict[str, Any]] = Field(default_factory=list)
    history: list[KBNodeHistory] = Field(default_factory=list)


class KBSearchResponse(BaseModel):
    query: str = ""
    results: list[KBSearchResult] = Field(default_factory=list)
    total: int = 0


class KBEntitySchema(BaseModel):
    project_id: str = ""
    schema_id: str = ""
    entity_type: str = ""
    fields: list[dict[str, Any]] = Field(default_factory=list)
    description: str = ""
    similarity_config: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


class KBSchemaListResponse(BaseModel):
    schemas: list[KBEntitySchema] = Field(default_factory=list)
    total: int = 0


class KBStats(BaseModel):
    documents: dict[str, int] = Field(default_factory=dict)
    nodes: dict[str, int] = Field(default_factory=dict)
    edges: int = 0
    extraction_tokens: int = 0


class InsertFactDetail(BaseModel):
    label: str = ""
    type: str = ""
    action: str = ""
    node_id: str = ""
    version: int = 0


class InsertFactEdgeDetail(BaseModel):
    edge_id: str = ""
    from_node: str = ""
    to_node: str = ""
    relation: str = ""


class InsertFactsResponse(BaseModel):
    processed: int = 0
    created: int = 0
    updated: int = 0
    details: list[InsertFactDetail] = Field(default_factory=list)
    edges: list[InsertFactEdgeDetail] = Field(default_factory=list)


class KBAnalyticsRule(BaseModel):
    project_id: str = ""
    rule_id: str = ""
    rule_type: str = ""
    name: str = ""
    config: Any = None
    enabled: bool = False
    schedule: str = ""
    created_at: str = ""
    updated_at: str = ""


class KBAnalyticsRuleListResponse(BaseModel):
    rules: list[KBAnalyticsRule] = Field(default_factory=list)
    total: int = 0


class KBRecommendationScore(BaseModel):
    project_id: str = ""
    rule_id: str = ""
    source_id: str = ""
    target_id: str = ""
    target_type: str = ""
    score: float = 0.0


class KBRecommendationsResponse(BaseModel):
    recommendations: list[KBRecommendationScore] = Field(default_factory=list)
    total: int = 0


class KBTrendsResponse(BaseModel):
    trends: list[dict[str, Any]] = Field(default_factory=list)
    total: int = 0


class KBTrendRankingsResponse(BaseModel):
    rankings: list[dict[str, Any]] = Field(default_factory=list)
    total: int = 0


class KBConversionsResponse(BaseModel):
    conversions: list[dict[str, Any]] = Field(default_factory=list)
    total: int = 0


# ---------------------------------------------------------------------------
# User Priming
# ---------------------------------------------------------------------------


class PrimeUserResponse(BaseModel):
    job_id: str = ""
    status: str = ""
    facts_created: int = 0
    rows_parsed: int | None = None
    kb_resolved: int | None = None
    unresolved: int | None = None


class AddContentResponse(BaseModel):
    job_id: str = ""
    status: str = ""


class UserPrimingMetadata(BaseModel):
    agent_id: str = ""
    user_id: str = ""
    display_name: str = ""
    company: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    timezone: str = ""
    """IANA timezone (e.g., 'Asia/Singapore')."""
    source_type: str = ""
    custom_fields: dict[str, str] = Field(default_factory=dict)
    primed_at: str = ""


class UpdateMetadataResponse(BaseModel):
    metadata: UserPrimingMetadata | None = None
    facts_created: int = 0


class BatchImportResponse(BaseModel):
    job_id: str = ""
    status: str = ""
    total_users: int = 0
    facts_created: int = 0


class ImportJob(BaseModel):
    job_id: str = ""
    tenant_id: str = ""
    agent_id: str = ""
    job_type: str = ""
    user_id: str = ""
    source: str = ""
    status: str = ""
    total_users: int = 0
    processed_users: int = 0
    facts_created: int = 0
    error_message: str = ""
    created_at: str = ""
    updated_at: str = ""


class ImportJobListResponse(BaseModel):
    jobs: list[ImportJob] = Field(default_factory=list)
    count: int = 0


# ---------------------------------------------------------------------------
# Structured Import (Priming)
# ---------------------------------------------------------------------------


class StructuredColumnMapping(BaseModel):
    property: str = ""
    is_label: bool = False
    type: str = ""


class StructuredImportSpec(BaseModel):
    entity_type: str = ""
    content_csv: str = ""
    column_mapping: dict[str, StructuredColumnMapping] = Field(default_factory=dict)
    project_id: str = ""


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------


class KBResolutionInfo(BaseModel):
    resolved: bool = False
    kb_node_id: str = ""
    kb_label: str = ""
    kb_properties: dict[str, Any] = Field(default_factory=dict)


class KBCandidate(BaseModel):
    kb_node_id: str = ""
    label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)


class InventoryUpdateResponse(BaseModel):
    status: str = ""
    fact_id: str = ""
    kb_resolution: KBResolutionInfo | None = None
    candidates: list[KBCandidate] = Field(default_factory=list)
    error: str = ""


class InventoryItem(BaseModel):
    fact_id: str = ""
    item_label: str = ""
    kb_node_id: str = ""
    user_properties: dict[str, Any] = Field(default_factory=dict)
    market_properties: dict[str, Any] = Field(default_factory=dict)
    gain_loss: float | None = None


class InventoryGroupResult(BaseModel):
    group: str = ""
    values: dict[str, Any] = Field(default_factory=dict)


class InventoryQueryResponse(BaseModel):
    items: list[InventoryItem] = Field(default_factory=list)
    total_items: int = 0
    next_cursor: str = ""
    totals: dict[str, Any] = Field(default_factory=dict)
    groups: list[InventoryGroupResult] = Field(default_factory=list)


class InventoryBatchImportResponse(BaseModel):
    status: str = ""
    added: int = 0
    failed: int = 0
    total: int = 0
    error: str = ""


class InventoryDirectUpdateResponse(BaseModel):
    status: str = ""
    fact_id: str = ""
    error: str = ""


class StoredFact(BaseModel):
    fact_id: str = ""
    content: str = ""
    fact_type: str = ""
    importance: float = 0.0
    confidence: float = 0.0
    entity: str = ""
    source_type: str = ""
    mention_count: int = 0
    metadata: dict[str, Any] | None = None
    created_at: str = ""
    updated_at: str = ""


class ListAllFactsResponse(BaseModel):
    facts: list[StoredFact] = Field(default_factory=list)
    total: int = 0


# ---------------------------------------------------------------------------
# KB Bulk Update
# ---------------------------------------------------------------------------


class AgentKBSearchResult(BaseModel):
    content: str = ""
    label: str = ""
    type: str = ""
    source: str = ""
    score: float = 0.0


class AgentKBSearchResponse(BaseModel):
    query: str = ""
    results: list[AgentKBSearchResult] = Field(default_factory=list)


class KBBulkUpdateEntry(BaseModel):
    entity_type: str = ""
    label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)


class KBBulkUpdateResponse(BaseModel):
    processed: int = 0
    updated: int = 0
    not_found: int = 0
    created: int = 0
    status: str = ""
    count: int = 0


# ---------------------------------------------------------------------------
# Tool Schemas (BYO-LLM)
# ---------------------------------------------------------------------------


class ToolSchema(BaseModel):
    """Describes a single tool available for an agent (BYO-LLM integrations)."""

    name: str = ""
    description: str = ""
    endpoint: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolSchemasResponse(BaseModel):
    """Response from the get_tools endpoint."""

    tools: list[ToolSchema] = Field(default_factory=list)
