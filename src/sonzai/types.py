"""Public types for the Sonzai SDK."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._customizations import AgentCapabilities, ChatStreamEvent, StoredFact  # noqa: F401
from ._generated.models import (  # noqa: F401
    AdvanceTimeDiaryEntry,
    AtomicFact,
    BatchPersonalityEntry,
    Big5,
    Big5Trait,
    DiaryEntry,
    Goal,
    GoalsResponse,
    Habit,
    HabitsResponse,
    InterestsResponse,
    ListAllFactsResponse,
    MemoryNode,
    MemoryResponse,
    MemorySummary,
    MoodAggregateResponse,
    MoodHistoryEntry,
    MoodHistoryResponse,
    MoodResponse,
    MoodState,
    PersonalityDelta,
    PersonalityDimensions,
    PersonalityProfile,
    PersonalityResponse,
    PersonalityShift,
    RecentShiftsResponse,
    SignificantMoment,
    SignificantMomentsResponse,
    SummariesResponse,
    TimeMachineMoodSnapshot,
    TimeMachineResponse,
    TimelineSession,
    TraitPrecision,
)

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
    """Token-usage counters attached to SSE stream events.

    Not part of the ChatSSEChunk spec; populated by the stream consumer
    from usage frames emitted by the server and preserved here for
    backward compatibility with existing callers.
    """

    model_config = ConfigDict(populate_by_name=True)

    prompt_tokens: int = Field(alias="promptTokens", default=0)
    completion_tokens: int = Field(alias="completionTokens", default=0)
    total_tokens: int = Field(alias="totalTokens", default=0)


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



class MemorySearchResult(BaseModel):
    fact_id: str = ""
    content: str = ""
    fact_type: str = ""
    score: float = 0.0


class MemorySearchResponse(BaseModel):
    results: list[MemorySearchResult] = Field(default_factory=list)


class MemoryTimelineResponse(BaseModel):
    sessions: list[TimelineSession] = Field(default_factory=list)
    total_facts: int = 0


# ---------------------------------------------------------------------------
# Personality
# ---------------------------------------------------------------------------


class PersonalityPreferences(BaseModel):
    conversation_pace: str = ""
    formality: str = ""
    humor_style: str = ""
    emotional_expression: str = ""


class PersonalityBehaviors(BaseModel):
    response_length: str = ""
    question_frequency: str = ""
    empathy_style: str = ""
    conflict_approach: str = ""


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


class RelationshipData(BaseModel):
    """A relationship between an agent and a user."""

    user_id: str = ""
    love_score: float = 0.0
    chemistry_score: float = 0.0
    narrative: str = ""
    last_update: str = ""
    updated_at: str = ""

    model_config = {"extra": "allow"}


class RelationshipResponse(BaseModel):
    relationships: list[RelationshipData] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class HabitData(BaseModel):
    """A behavioral habit with a strength score."""

    name: str = ""
    strength: float = 0.0
    category: str = ""
    description: str = ""
    display_name: str = ""
    formed: bool = False
    daily_reinforced: float = 0.0
    last_update: str = ""

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


class InitialGoal(BaseModel):
    """Goal definition used when creating an agent with initial goals."""

    type: str = ""
    title: str = ""
    description: str = ""
    priority: int = 0
    related_traits: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class InterestData(BaseModel):
    """A single agent interest with score."""

    topic: str = ""
    score: float = 0.0  # Deprecated: use confidence instead.
    category: str = ""
    agent_id: str = ""
    user_id: str = ""
    confidence: float = 0.0
    engagement_level: float = 0.0
    mention_count: int = 0
    research_status: str = ""
    research_findings: str = ""
    last_mentioned_at: str = ""
    created_at: str = ""
    updated_at: str = ""

    model_config = {"extra": "allow"}


class DiaryResponse(BaseModel):
    entries: list[DiaryEntry] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class UsersResponse(BaseModel):
    # Users are returned as open-shaped dicts by the API today;
    # keep them flexible here rather than forcing a schema.
    users: list[dict] = Field(default_factory=list)

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
    """SDK alias. The spec wire name is run_id."""
    run_id: str = ""
    tenant_id: str = ""
    project_id: str = ""
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
    started_at: str | None = None
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


class ConstellationEdge(BaseModel):
    """An edge between two constellation nodes."""

    edge_id: str = ""
    agent_id: str = ""
    source_id: str = ""
    target_id: str = ""
    relation: str = ""
    weight: float = 0.0
    metadata: dict = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class ConstellationInsight(BaseModel):
    """An insight derived from the knowledge graph."""

    insight_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    content: str = ""
    type: str = ""
    surfaced: bool = False
    metadata: dict = Field(default_factory=dict)
    created_at: str = ""

    model_config = {"extra": "allow"}


class ConstellationResponse(BaseModel):
    nodes: list[ConstellationNode] = Field(default_factory=list)
    edges: list[ConstellationEdge] = Field(default_factory=list)
    insights: list[ConstellationInsight] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class Breakthrough(BaseModel):
    """A personality breakthrough moment for an agent."""

    breakthrough_id: str = ""
    agent_id: str = ""
    user_id: str = ""
    breakthrough_number: int = 0
    level_at_breakthrough: int = 0
    narrative: str = ""
    personality_shifts: list[str] = Field(default_factory=list)
    trait_evolved: str = ""
    new_goals: list[str] = Field(default_factory=list)
    achieved_goals: list[str] = Field(default_factory=list)
    skill_points_awarded: int = 0
    acknowledged: bool = False
    created_at: str = ""

    model_config = {"extra": "allow"}


class BreakthroughsResponse(BaseModel):
    breakthroughs: list[Breakthrough] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class WakeupsResponse(BaseModel):
    # Forward reference: ScheduledWakeup is defined later in this module.
    wakeups: list["ScheduledWakeup"] = Field(default_factory=list)

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
    session_id: str = ""
    source_id: str = ""
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
# Account Config (tenant-scoped)
# ---------------------------------------------------------------------------


class AccountConfigEntry(BaseModel):
    """Tenant-scoped config entry. Shape mirrors ``ProjectConfigEntry`` so
    callers that already handle project config can reuse their serialisation.
    """

    key: str
    value: Any = None
    updated_at: str | None = None


class AccountConfigListResponse(BaseModel):
    configs: list[AccountConfigEntry] = []


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
    research_summary: str = ""
    executed_at: str | None = None
    created_at: str | None = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Schedules (recurring, per-user)
# ---------------------------------------------------------------------------


class Schedule(BaseModel):
    schedule_id: str = ""
    cadence_type: str = ""
    cadence: str = ""
    active_window: str = ""
    timezone: str = ""
    next_fire_at: str = ""
    inventory_item_id: str = ""
    intent: str = ""
    check_type: str = ""
    metadata: str = ""
    enabled: bool = False
    starts_at: str = ""
    ends_at: str = ""
    created_at: str = ""
    updated_at: str = ""

    model_config = {"extra": "allow"}


class ScheduleListResponse(BaseModel):
    schedules: list[Schedule] = Field(default_factory=list)


class ScheduleCreateResponse(BaseModel):
    schedule_id: str = ""
    next_fire_at: str = ""
    next_fire_at_local: str = ""
    enabled: bool = False


class ScheduleUpcomingResponse(BaseModel):
    upcoming: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Agent List (paginated)
# ---------------------------------------------------------------------------


class AgentIndex(BaseModel):
    model_config = {"extra": "allow"}
    id: str = ""
    agent_id: str = ""
    tenant_id: str = ""
    name: str = ""
    bio: str = ""
    gender: str = ""
    avatar_url: str = ""
    status: str = ""
    is_active: bool = False
    project_id: str = ""
    instance_count: int = 0
    last_seen_at: str = ""
    owner_user_id: str = ""
    owner_display_name: str = ""
    owner_email: str = ""
    created_at: str = ""


class AgentListResponse(BaseModel):
    items: list[AgentIndex] = Field(default_factory=list)
    next_cursor: str | None = None
    has_more: bool = False
    total_count: int = 0


# ---------------------------------------------------------------------------
# Batch Personality
# ---------------------------------------------------------------------------


class BatchPersonalityResponse(BaseModel):
    personalities: dict[str, BatchPersonalityEntry] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Personality Extensions
# ---------------------------------------------------------------------------


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


class PendingCapability(BaseModel):
    capability: str = ""
    context: str = ""
    model_config = {"extra": "allow"}


class CustomToolListResponse(BaseModel):
    tools: list[CustomToolDefinition] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Consolidation
# ---------------------------------------------------------------------------


class ConsolidateResponse(BaseModel):
    success: bool = False


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


# ----------------------------------------------------------------------------
# Organization-global KB (see docs/ORGANIZATION_GLOBAL_KB.md)
# ----------------------------------------------------------------------------


class KBScope(str, Enum):
    """Scope mode for agent knowledge_search reads.

    Wire values match sonzai-go + sonzai-typescript SDKs so the same enum
    round-trips cleanly through the platform API.
    """

    PROJECT_ONLY = "project_only"
    ORG_ONLY = "org_only"
    CASCADE = "cascade"
    UNION = "union"


class CreateOrgNodeOptions(BaseModel):
    """Request body for Knowledge.create_org_node."""

    node_type: str
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)
    # Defaults to 1.0 server-side for hand-authored org knowledge.
    confidence: float = 0.0


class KBNodeWithScope(KBNode):
    """KBNode with scope provenance — returned by cascade reads + promote."""

    scope_type: str = ""  # "project" | "organization"
    relevance: float = 0.0


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
    display_name: str | None = None
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
    last_run_at: str = ""
    last_run_status: str = ""
    last_run_duration_ms: int = 0
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


class JobUser(BaseModel):
    job_id: str = ""
    user_id: str = ""
    status: str = ""
    facts_stored: int = 0
    facts_deduped: int = 0
    warmth_score: int = 0
    updated_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    error_message: str = ""


class ListImportJobUsersResponse(BaseModel):
    users: list[JobUser] = Field(default_factory=list)
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
    inventory_item_id: str | None = None
    kb_resolution: KBResolutionInfo | None = None
    candidates: list[KBCandidate] = Field(default_factory=list)
    error: str = ""


class InventoryItem(BaseModel):
    fact_id: str = ""
    inventory_item_id: str | None = None
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


# ---------------------------------------------------------------------------
# Input option models (Wave 3 — Python parity with TS/Go)
# These models let Python callers pass typed structures instead of bare dicts.
# All models use `extra=allow` to stay forward-compatible with server fields.
# Resource methods continue to accept both these models and **kwargs.
# ---------------------------------------------------------------------------


class SeedMemory(BaseModel):
    """A pre-written lore memory to seed verbatim into the agent's memory."""

    content: str = ""
    fact_type: str | None = None
    importance: float | None = None
    entities: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class LoreGenerationContext(BaseModel):
    """World-building context for LLM-generated origin stories and personalized memories."""

    world_description: str = ""
    entity_terminology: dict[str, str] = Field(default_factory=dict)
    origin_prompt_instructions: str | None = None

    model_config = {"extra": "allow"}


class IdentityMemory(BaseModel):
    """Template string for an identity memory with {{agentName}} and {{creatorName}} placeholders."""

    template: str = ""
    fact_type: str | None = None
    importance: float | None = None
    entities: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ModelConfig(BaseModel):
    """LLM provider/model configuration for seed memory generation."""

    provider: str = ""
    model: str = ""
    temperature: float | None = None
    max_tokens: int | None = None

    model_config = {"extra": "allow"}


class Big5Scores(BaseModel):
    openness: float = 0.0
    conscientiousness: float = 0.0
    extraversion: float = 0.0
    agreeableness: float = 0.0
    neuroticism: float = 0.0
    confidence: float | None = None

    model_config = {"extra": "allow"}


class SDKPersonalityDimensions(BaseModel):
    intellect: float = 0.0
    aesthetic: float = 0.0
    industriousness: float = 0.0
    orderliness: float = 0.0
    enthusiasm: float = 0.0
    assertiveness: float = 0.0
    compassion: float = 0.0
    politeness: float = 0.0
    withdrawal: float = 0.0
    volatility: float = 0.0

    model_config = {"extra": "allow"}


class SDKInteractionPreferences(BaseModel):
    conversation_pace: str = ""
    formality: str = ""
    humor_style: str = ""
    emotional_expression: str = ""

    model_config = {"extra": "allow"}


class SDKBehavioralTraits(BaseModel):
    response_length: str = ""
    question_frequency: str = ""
    empathy_style: str = ""
    conflict_approach: str = ""

    model_config = {"extra": "allow"}


class AgentToolCapabilities(BaseModel):
    web_search: bool = False
    remember_name: bool = False
    image_generation: bool = False
    inventory: bool = False

    model_config = {"extra": "allow"}


class InitialGoal(BaseModel):
    type: str | None = None
    title: str = ""
    description: str = ""
    priority: int | None = None
    related_traits: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class AgentFeatureCapabilities(BaseModel):
    """Feature capabilities for an agent (image generation, inventory, etc.)."""

    image_generation: bool = False
    inventory: bool = False

    model_config = {"extra": "allow"}


class CreateAgentOptions(BaseModel):
    agent_id: str | None = None
    user_id: str | None = None
    user_display_name: str | None = None
    name: str = ""
    gender: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    project_id: str | None = None
    personality_prompt: str | None = None
    speech_patterns: list[str] = Field(default_factory=list)
    true_interests: list[str] = Field(default_factory=list)
    true_dislikes: list[str] = Field(default_factory=list)
    primary_traits: list[str] = Field(default_factory=list)
    big5: Big5Scores | None = None
    dimensions: SDKPersonalityDimensions | None = None
    preferences: dict[str, str] = Field(default_factory=dict)
    behaviors: dict[str, str] = Field(default_factory=dict)
    capabilities: AgentFeatureCapabilities | None = None
    tool_capabilities: AgentToolCapabilities | None = None
    generate_avatar: bool | None = None
    language: str | None = None
    seed_memories: list[SeedMemory] = Field(default_factory=list)
    lore_context: dict[str, Any] = Field(default_factory=dict)
    generate_origin_story: bool | None = None
    generate_personalized_memories: bool | None = None
    initial_goals: list[InitialGoal] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class UpdateAgentOptions(BaseModel):
    name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    personality_prompt: str | None = None
    speech_patterns: list[str] | None = None
    true_interests: list[str] | None = None
    true_dislikes: list[str] | None = None
    big5: Big5Scores | None = None
    dimensions: SDKPersonalityDimensions | None = None
    tool_capabilities: AgentToolCapabilities | None = None

    model_config = {"extra": "allow"}


class AgentListOptions(BaseModel):
    page_size: int | None = None
    cursor: str | None = None
    search: str | None = None
    project_id: str | None = None

    model_config = {"extra": "allow"}


class GameContext(BaseModel):
    """Game-specific context for chat requests."""

    custom_fields: dict[str, str] = Field(default_factory=dict)
    game_state_json: Any = None

    model_config = {"extra": "allow"}


class ChatOptions(BaseModel):
    """Input model for chat. `agent` accepts UUID or agent name."""

    agent: str = ""
    messages: list[ChatMessage] = Field(default_factory=list)
    user_id: str | None = None
    user_display_name: str | None = None
    session_id: str | None = None
    instance_id: str | None = None
    provider: str | None = None
    model: str | None = None
    continuation_token: str | None = None
    request_type: str | None = None
    language: str | None = None
    compiled_system_prompt: str | None = None
    interaction_role: str | None = None
    timezone: str | None = None
    tool_capabilities: AgentToolCapabilities | None = None
    tool_definitions: list[dict[str, Any]] = Field(default_factory=list)
    max_turns: int | None = None
    skip_context_build: bool | None = None
    game_context: GameContext | None = None

    model_config = {"extra": "allow"}


class SessionStartOptions(BaseModel):
    user_id: str = ""
    user_display_name: str | None = None
    session_id: str = ""
    instance_id: str | None = None
    tool_definitions: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class SessionEndOptions(BaseModel):
    user_id: str = ""
    session_id: str = ""
    instance_id: str | None = None
    total_messages: int | None = None
    duration_seconds: float | None = None
    messages: list[ChatMessage] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class MemoryListOptions(BaseModel):
    user_id: str | None = None
    instance_id: str | None = None
    parent_id: str | None = None
    include_contents: bool | None = None
    limit: int | None = None
    memory_type: str | None = None

    model_config = {"extra": "allow"}


class MemorySearchOptions(BaseModel):
    query: str = ""
    instance_id: str | None = None
    limit: int | None = None

    model_config = {"extra": "allow"}


class MemoryTimelineOptions(BaseModel):
    user_id: str | None = None
    instance_id: str | None = None
    start: str | None = None
    end: str | None = None

    model_config = {"extra": "allow"}


class MemoryResetOptions(BaseModel):
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class FactListOptions(BaseModel):
    user_id: str | None = None
    category: str | None = None
    limit: int | None = None
    offset: int | None = None

    model_config = {"extra": "allow"}


class CreateFactOptions(BaseModel):
    content: str = ""
    user_id: str | None = None
    fact_type: str | None = None
    importance: float | None = None
    confidence: float | None = None
    entities: list[str] = Field(default_factory=list)
    node_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class UpdateFactOptions(BaseModel):
    content: str | None = None
    fact_type: str | None = None
    importance: float | None = None
    confidence: float | None = None
    entities: list[str] | None = None
    metadata: dict[str, Any] | None = None

    model_config = {"extra": "allow"}


class CreateHabitOptions(BaseModel):
    user_id: str | None = None
    name: str = ""
    category: str | None = None
    description: str | None = None
    display_name: str | None = None
    strength: float | None = None

    model_config = {"extra": "allow"}


class UpdateHabitOptions(BaseModel):
    user_id: str | None = None
    category: str | None = None
    description: str | None = None
    display_name: str | None = None
    strength: float | None = None

    model_config = {"extra": "allow"}


class DeleteHabitOptions(BaseModel):
    user_id: str | None = None

    model_config = {"extra": "allow"}


class CreateGoalOptions(BaseModel):
    user_id: str | None = None
    type: str | None = None
    title: str = ""
    description: str = ""
    priority: int | None = None
    related_traits: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class UpdateGoalOptions(BaseModel):
    user_id: str | None = None
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    status: str | None = None
    related_traits: list[str] | None = None

    model_config = {"extra": "allow"}


class DeleteGoalOptions(BaseModel):
    user_id: str | None = None

    model_config = {"extra": "allow"}


class CreateConstellationNodeOptions(BaseModel):
    user_id: str | None = None
    node_type: str | None = None
    label: str = ""
    description: str | None = None
    significance: float | None = None

    model_config = {"extra": "allow"}


class UpdateConstellationNodeOptions(BaseModel):
    label: str | None = None
    description: str | None = None
    significance: float | None = None
    node_type: str | None = None

    model_config = {"extra": "allow"}


class ScheduleWakeupOptions(BaseModel):
    user_id: str = ""
    scheduled_at: str = ""
    check_type: str = ""
    intent: str | None = None
    occasion: str | None = None
    interest_topic: str | None = None
    event_description: str | None = None

    model_config = {"extra": "allow"}


class TriggerEventOptions(BaseModel):
    user_id: str = ""
    event_type: str = ""
    event_description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    language: str | None = None
    instance_id: str | None = None
    messages: list[ChatMessage] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class DialogueOptions(BaseModel):
    user_id: str | None = None
    messages: list[ChatMessage] = Field(default_factory=list)
    request_type: str | None = None
    scene_guidance: str | None = None
    tool_config: dict[str, Any] = Field(default_factory=dict)
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class GenerateBioOptions(BaseModel):
    name: str | None = None
    gender: str | None = None
    description: str | None = None
    user_id: str | None = None
    enriched_context_json: dict[str, Any] | None = None
    current_bio: str | None = None
    style: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class GenerateCharacterOptions(BaseModel):
    agent_id: str | None = None
    name: str = ""
    gender: str | None = None
    description: str | None = None
    fields: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class GenerateAndCreateOptions(BaseModel):
    agent_id: str | None = None
    name: str = ""
    gender: str | None = None
    description: str | None = None
    fields: list[str] = Field(default_factory=list)
    project_id: str | None = None
    language: str | None = None

    model_config = {"extra": "allow"}


class GenerateAvatarOptions(BaseModel):
    style: str | None = None
    gender: str | None = None
    description: str | None = None

    model_config = {"extra": "allow"}


class ImageGenerateOptions(BaseModel):
    prompt: str = ""
    negative_prompt: str | None = None
    model: str | None = None
    provider: str | None = None

    model_config = {"extra": "allow"}


class CustomStateListOptions(BaseModel):
    scope: str | None = None
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class CustomStateCreateOptions(BaseModel):
    key: str = ""
    value: Any = None
    scope: str | None = None
    content_type: str | None = None
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class CustomStateUpdateOptions(BaseModel):
    value: Any = None
    content_type: str | None = None

    model_config = {"extra": "allow"}


class CustomStateUpsertOptions(BaseModel):
    key: str = ""
    value: Any = None
    scope: str | None = None
    content_type: str | None = None
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class CustomStateGetByKeyOptions(BaseModel):
    key: str = ""
    scope: str | None = None
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class CustomStateDeleteByKeyOptions(BaseModel):
    key: str = ""
    scope: str | None = None
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class WebhookRegisterOptions(BaseModel):
    webhook_url: str = ""
    auth_header: str | None = None

    model_config = {"extra": "allow"}


class TTSOptions(BaseModel):
    text: str = ""
    voice: str | None = None
    voice_id: str | None = None
    model: str | None = None
    provider: str | None = None
    output_format: str | None = None
    language: str | None = None

    model_config = {"extra": "allow"}


class STTOptions(BaseModel):
    audio: Any = None
    audio_url: str | None = None
    model: str | None = None
    provider: str | None = None
    language: str | None = None

    model_config = {"extra": "allow"}


class VoiceTokenOptions(BaseModel):
    provider: str | None = None
    voice: str | None = None
    voice_id: str | None = None

    model_config = {"extra": "allow"}


class VoiceListOptions(BaseModel):
    provider: str | None = None
    language: str | None = None

    model_config = {"extra": "allow"}


class ForkResponse(BaseModel):
    agent_id: str = ""
    source_agent_id: str = ""
    status: str = ""
    name: str = ""

    model_config = {"extra": "allow"}


class ForkStatusResponse(BaseModel):
    status: str = ""
    source_agent_id: str = ""
    started_at: str | None = None
    completed_at: str | None = None
    tables_copied: int = 0
    tables_total: int = 0
    error_message: str | None = None

    model_config = {"extra": "allow"}


class DeleteWisdomResponse(BaseModel):
    success: bool = False
    fact_id: str = ""

    model_config = {"extra": "allow"}


class WisdomAuditResponse(BaseModel):
    fact_id: str = ""
    content: str = ""
    target_path: str | None = None
    derived_from_hashes: list[str] = Field(default_factory=list)
    source_user_count: int = 0
    promotion_confidence: float = 0.0
    promoted_at: str | None = None

    model_config = {"extra": "allow"}


class AgentKBSearchOptions(BaseModel):
    query: str = ""
    limit: int | None = None

    model_config = {"extra": "allow"}


class SetStatusOptions(BaseModel):
    status: str = ""

    model_config = {"extra": "allow"}


class UpdateProjectOptions(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Wave 4 — remaining input models for full TS/Go parity
# ---------------------------------------------------------------------------

# --- Knowledge Base ---


class KBSchemaField(BaseModel):
    name: str = ""
    type: str = ""
    required: bool | None = None
    indexed: bool | None = None

    model_config = {"extra": "allow"}


class KBSimilarityConfig(BaseModel):
    match_fields: list[str] = Field(default_factory=list)
    threshold: float | None = None

    model_config = {"extra": "allow"}


class InsertFactEntry(BaseModel):
    entity_type: str = ""
    label: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class InsertRelEntry(BaseModel):
    from_label: str = ""
    to_label: str = ""
    edge_type: str = ""

    model_config = {"extra": "allow"}


class InsertFactsOptions(BaseModel):
    source: str | None = None
    facts: list[InsertFactEntry] = Field(default_factory=list)
    relationships: list[InsertRelEntry] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class CreateSchemaOptions(BaseModel):
    entity_type: str = ""
    fields: list[KBSchemaField] = Field(default_factory=list)
    description: str | None = None
    similarity_config: KBSimilarityConfig | None = None

    model_config = {"extra": "allow"}


class CreateAnalyticsRuleOptions(BaseModel):
    rule_type: str = ""
    name: str = ""
    config: Any = None
    enabled: bool = False
    schedule: str | None = None

    model_config = {"extra": "allow"}


class UpdateAnalyticsRuleOptions(BaseModel):
    name: str | None = None
    config: Any = None
    enabled: bool = False
    schedule: str | None = None

    model_config = {"extra": "allow"}


class KBSearchOptions(BaseModel):
    query: str = ""
    limit: int | None = None
    include_history: bool | None = None
    entity_types: str | None = None
    filters: str | None = None
    hops: int | None = None

    model_config = {"extra": "allow"}


class KBBulkUpdateOptions(BaseModel):
    source: str | None = None
    updates: list[KBBulkUpdateEntry] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class RecordFeedbackOptions(BaseModel):
    source_node_id: str = ""
    target_node_id: str = ""
    rule_id: str = ""
    converted: bool = False
    score_at_time: float = 0.0
    action: str | None = None

    model_config = {"extra": "allow"}


class ListAllFactsOptions(BaseModel):
    has_metadata: bool | None = None
    item_type: str | None = None
    limit: int | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


# --- KB response/data types needed as field types ---


class KBRelatedNode(BaseModel):
    node_id: str = ""
    label: str = ""
    node_type: str = ""
    edge_type: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class KBTrendAggregation(BaseModel):
    project_id: str = ""
    node_id: str = ""
    rule_id: str = ""
    window: str = ""
    value: float = 0.0
    direction: str = ""

    model_config = {"extra": "allow"}


class KBTrendRanking(BaseModel):
    project_id: str = ""
    node_id: str = ""
    rule_id: str = ""
    type: str = ""
    window: str = ""
    rank: int = 0
    score: float = 0.0

    model_config = {"extra": "allow"}


class KBConversionStats(BaseModel):
    project_id: str = ""
    rule_id: str = ""
    segment_key: str = ""
    target_type: str = ""
    shown_count: int = 0
    conversion_count: int = 0
    conversion_rate: float = 0.0

    model_config = {"extra": "allow"}


# --- User Priming ---


class PrimeContentBlock(BaseModel):
    type: str = ""
    body: str = ""

    model_config = {"extra": "allow"}


class PrimeUserMetadata(BaseModel):
    company: str | None = None
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    timezone: str | None = None
    custom: dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class UpdateMetadataOptions(BaseModel):
    display_name: str | None = None
    company: str | None = None
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    timezone: str | None = None
    custom: dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class PrimeUserOptions(BaseModel):
    display_name: str | None = None
    metadata: PrimeUserMetadata | None = None
    content: list[PrimeContentBlock] = Field(default_factory=list)
    source: str | None = None

    model_config = {"extra": "allow"}


class AddContentOptions(BaseModel):
    content: list[PrimeContentBlock] = Field(default_factory=list)
    source: str | None = None

    model_config = {"extra": "allow"}


class BatchImportUser(BaseModel):
    user_id: str = ""
    display_name: str | None = None
    metadata: PrimeUserMetadata | None = None
    content: list[PrimeContentBlock] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class BatchImportOptions(BaseModel):
    users: list[BatchImportUser] = Field(default_factory=list)
    source: str | None = None

    model_config = {"extra": "allow"}


# --- Inventory ---


class InventoryUpdateOptions(BaseModel):
    action: str = ""
    item_type: str = ""
    description: str | None = None
    kb_node_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    project_id: str | None = None

    model_config = {"extra": "allow"}


class InventoryQueryOptions(BaseModel):
    mode: str | None = None
    item_type: str | None = None
    query: str | None = None
    project_id: str | None = None
    filters: str | None = None
    sort_by: str | None = None
    sort_order: str | None = None
    aggregations: str | None = None
    group_by: str | None = None
    limit: int | None = None
    offset: int | None = None
    cursor: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class InventoryBatchItem(BaseModel):
    item_type: str = ""
    description: str | None = None
    kb_node_id: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class InventoryBatchImportOptions(BaseModel):
    items: list[InventoryBatchItem] = Field(default_factory=list)
    project_id: str | None = None

    model_config = {"extra": "allow"}


class InventoryDirectUpdateOptions(BaseModel):
    properties: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


# --- Eval ---


class EvaluateOptions(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)
    template_id: str = ""
    config_override: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class SimulationSession(BaseModel):
    user_persona: str = ""
    turn_count: int = 0
    opening_message: str = ""

    model_config = {"extra": "allow"}


class SimulationConfig(BaseModel):
    max_sessions: int | None = None
    max_turns_per_session: int | None = None
    simulated_duration_hours: int | None = None
    enable_proactive: bool | None = None
    enable_diary: bool | None = None
    enable_consolidation: bool | None = None

    model_config = {"extra": "allow"}


class SimulateOptions(BaseModel):
    sessions: list[SimulationSession] = Field(default_factory=list)
    user_persona: dict[str, Any] = Field(default_factory=dict)
    config: SimulationConfig | None = None
    model: str | None = None
    config_override: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class RunEvalOptions(BaseModel):
    template_id: str = ""
    sessions: list[SimulationSession] = Field(default_factory=list)
    user_persona: dict[str, Any] = Field(default_factory=dict)
    simulation_config: SimulationConfig | None = None
    model: str | None = None
    config_override: dict[str, Any] = Field(default_factory=dict)
    adaptation_template_id: str | None = None
    quality_only: bool | None = None

    model_config = {"extra": "allow"}


class EvalOnlyOptions(BaseModel):
    template_id: str = ""
    source_run_id: str = ""
    adaptation_template_id: str | None = None
    quality_only: bool | None = None

    model_config = {"extra": "allow"}


class EvalTemplateCreateOptions(BaseModel):
    name: str = ""
    description: str | None = None
    template_type: str | None = None
    judge_model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    scoring_rubric: str | None = None
    categories: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class EvalTemplateUpdateOptions(BaseModel):
    name: str | None = None
    description: str | None = None
    template_type: str | None = None
    judge_model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    scoring_rubric: str | None = None
    categories: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class EvalRunListOptions(BaseModel):
    agent_id: str | None = None
    limit: int | None = None
    offset: int | None = None

    model_config = {"extra": "allow"}


# --- Custom LLM ---


class SetCustomLLMOptions(BaseModel):
    endpoint: str = ""
    api_key: str = ""
    model: str | None = None
    display_name: str | None = None
    is_active: bool | None = None

    model_config = {"extra": "allow"}


# --- Project Config ---


class SetConfigOptions(BaseModel):
    value: Any = None

    model_config = {"extra": "allow"}


# --- Notifications ---


class ProjectNotificationListOptions(BaseModel):
    agent_id: str | None = None
    event_type: str | None = None
    limit: int | None = None

    model_config = {"extra": "allow"}


class AcknowledgeNotificationsOptions(BaseModel):
    notification_ids: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class AcknowledgeAllOptions(BaseModel):
    agent_id: str | None = None
    event_type: str | None = None

    model_config = {"extra": "allow"}


class NotificationListOptions(BaseModel):
    status: str | None = None
    user_id: str | None = None
    limit: int | None = None

    model_config = {"extra": "allow"}


# --- Consolidation & Summaries ---


class ConsolidateOptions(BaseModel):
    period: str | None = None
    user_id: str | None = None

    model_config = {"extra": "allow"}


class SummariesOptions(BaseModel):
    period: str | None = None
    limit: int | None = None

    model_config = {"extra": "allow"}


# --- Time Machine ---


class TimeMachineOptions(BaseModel):
    at: str = ""
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


# --- Capabilities ---


class UpdateCapabilitiesOptions(BaseModel):
    web_search: bool | None = None
    remember_name: bool | None = None
    image_generation: bool | None = None
    inventory: bool | None = None
    knowledge_base: bool | None = None

    model_config = {"extra": "allow"}


# --- Custom Tools ---


class CreateCustomToolOptions(BaseModel):
    name: str = ""
    description: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class UpdateCustomToolOptions(BaseModel):
    description: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


# --- Personality ---


class PersonalityGetOptions(BaseModel):
    history_limit: int | None = None
    since: str | None = None

    model_config = {"extra": "allow"}


class PersonalityUpdateOptions(BaseModel):
    big5: dict[str, Any] = Field(default_factory=dict)
    assessment_method: str | None = None
    total_exchanges: int | None = None

    model_config = {"extra": "allow"}


class UserOverlayOptions(BaseModel):
    instance_id: str | None = None
    since: str | None = None

    model_config = {"extra": "allow"}


# --- Session Tools ---


class SetSessionToolsOptions(BaseModel):
    tools: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"extra": "allow"}


# --- Fork ---


class ForkAgentOptions(BaseModel):
    name: str | None = None

    model_config = {"extra": "allow"}


# --- Context ---


class ContextDataOptions(BaseModel):
    user_id: str | None = None
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class GetContextOptions(BaseModel):
    user_id: str = ""
    session_id: str | None = None
    instance_id: str | None = None
    query: str | None = None
    language: str | None = None
    timezone: str | None = None

    model_config = {"extra": "allow"}


# --- Context data types (used in enriched context) ---


class ContextLoadedFact(BaseModel):
    fact_id: str | None = None
    atomic_text: str | None = None
    fact_type: str | None = None
    importance: float | None = None
    session_id: str | None = None
    created_at: str | None = None

    model_config = {"extra": "allow"}


class ContextLongTermSummary(BaseModel):
    summary_type: str | None = None
    period_start: str | None = None
    summary: str | None = None
    topics: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ContextProactiveMemory(BaseModel):
    fact: ContextLoadedFact | None = None
    urgency: float | None = None
    template: str | None = None

    model_config = {"extra": "allow"}


class ContextConstellationPattern(BaseModel):
    type: str | None = None
    description: str | None = None
    significance: float | None = None
    mention_count: int | None = None

    model_config = {"extra": "allow"}


# --- Process ---


class ProcessOptions(BaseModel):
    user_id: str = ""
    session_id: str | None = None
    instance_id: str | None = None
    messages: list[ChatMessage] = Field(default_factory=list)
    provider: str | None = None
    model: str | None = None

    model_config = {"extra": "allow"}


# --- Instances ---


class InstanceCreateOptions(BaseModel):
    name: str = ""
    description: str | None = None

    model_config = {"extra": "allow"}


class UpdateInstanceOptions(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None

    model_config = {"extra": "allow"}


# --- Seed Memories ---


class SeedMemoriesOptions(BaseModel):
    user_id: str = ""
    memories: list[dict[str, Any]] = Field(default_factory=list)
    instance_id: str | None = None

    model_config = {"extra": "allow"}


class GenerateSeedMemoriesOptions(BaseModel):
    user_id: str | None = None
    agent_name: str | None = None
    big5: dict[str, Any] = Field(default_factory=dict)
    personality_prompt: str | None = None
    guide_summary: str | None = None
    true_interests: list[str] = Field(default_factory=list)
    true_dislikes: list[str] = Field(default_factory=list)
    speech_patterns: list[str] = Field(default_factory=list)
    creator_display_name: str | None = None
    static_lore_memories: list[dict[str, Any]] = Field(default_factory=list)
    lore_generation_context: dict[str, Any] = Field(default_factory=dict)
    identity_memory_templates: list[dict[str, Any]] = Field(default_factory=list)
    generate_origin_story: bool | None = None
    generate_personalized_memories: bool | None = None
    store_memories: bool | None = None

    model_config = {"extra": "allow"}


# --- Voice ---


class VoiceEntry(BaseModel):
    voice_id: str = ""
    voice_name: str = ""
    gender: str = ""
    tier: int = 0
    provider: str = ""
    language: str = ""
    accent: str | None = None
    age_profile: str | None = None
    description: str | None = None
    sample_audio_url: str | None = None
    availability: str = ""

    model_config = {"extra": "allow"}


# --- Tool Definition ---


class ToolDefinition(BaseModel):
    name: str = ""
    description: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

class Project(BaseModel):
    project_id: str = ""
    tenant_id: str = ""
    name: str = ""
    game_name: str = ""
    environment: str = ""
    created_at: str = ""
    is_active: bool = True

    model_config = {"extra": "allow"}


class ProjectList(BaseModel):
    projects: list[Project] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ProjectAPIKey(BaseModel):
    key_id: str = ""
    project_id: str = ""
    tenant_id: str = ""
    name: str = ""
    key_prefix: str = ""
    created_by: str = ""
    created_at: str = ""
    expires_at: str | None = None
    last_used_at: str | None = None
    is_active: bool = True
    is_admin_managed: bool = False
    scopes: list[str] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class ProjectAPIKeyList(BaseModel):
    keys: list[ProjectAPIKey] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class CreateAPIKeyResponse(BaseModel):
    key_id: str = ""
    project_id: str = ""
    tenant_id: str = ""
    name: str = ""
    key_prefix: str = ""
    key: str = ""
    is_active: bool = True
    scopes: list[str] = Field(default_factory=list)
    created_at: str = ""
    created_by: str = ""
    expires_at: str | None = None

    model_config = {"extra": "allow"}


class RevokeAPIKeyResponse(BaseModel):
    success: bool = False

    model_config = {"extra": "allow"}


class DeleteProjectResponse(BaseModel):
    status: str = ""

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# User Personas (API resource — distinct from simulation UserPersona)
# ---------------------------------------------------------------------------

class UserPersonaRecord(BaseModel):
    persona_id: str = ""
    name: str = ""
    description: str = ""
    style: str = ""
    is_default: bool = False
    created_at: str = ""
    updated_at: str = ""
    tenant_id: str = ""

    model_config = {"extra": "allow"}


class UserPersonaList(BaseModel):
    personas: list[UserPersonaRecord] = Field(default_factory=list)

    model_config = {"extra": "allow"}


class DeleteUserPersonaResponse(BaseModel):
    success: bool = False

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Tool Schemas (distinct from custom tool list)
# ---------------------------------------------------------------------------

class ToolSchemaEntry(BaseModel):
    name: str = ""
    description: str = ""
    endpoint: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow"}


class GetToolSchemasResponse(BaseModel):
    tools: list[ToolSchemaEntry] = Field(default_factory=list)

    model_config = {"extra": "allow"}

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Workbench / AdvanceTime
# ---------------------------------------------------------------------------

# NOTE: ``DiaryEntry`` is defined earlier in this module as the canonical diary
# type (covers every field the diary API returns). The advance-time handler's
# ``advanceTimeDiaryEntry`` is a strict subset of those fields — reusing the
# same model means callers who import ``sonzai.types.DiaryEntry`` via either
# surface get the same class.


class WakeupExecution(BaseModel):
    """A wakeup that fired during the workbench advance-time window.

    Fields mirror the Go handler ``advanceTimeWakeup`` struct.
    ``generated_message`` is populated only when the platform has wired in
    the proactive message generator (production parity with the game-side
    post-wakeup Chat call).
    """

    wakeup_id: str = ""
    check_type: str = ""
    intent: str = ""
    user_id: str = ""
    agent_id: str = ""
    generated_message: str = ""

    model_config = {"extra": "allow"}


class AdvanceTimeResponse(BaseModel):
    """Result of ``POST /workbench/advance-time``.

    Mirrors the Go handler ``workbenchAdvanceTimeResponse`` struct. All
    counters default to 0 and lists default to empty so callers can safely
    ignore fields that aren't populated in a given run.
    """

    days_processed: int = 0
    consolidation_ran: bool = False
    weekly_consolidations: int = 0
    diary_entries_created: int = 0
    diary_entries: list[AdvanceTimeDiaryEntry] = Field(default_factory=list)
    wakeups_executed: list[WakeupExecution] = Field(default_factory=list)
    consolidation_processed: int = 0

    model_config = {"extra": "allow"}

    @field_validator("diary_entries", "wakeups_executed", mode="before")
    @classmethod
    def _none_is_empty_list(cls, v: Any) -> Any:
        # Go marshals empty slices as JSON `null` — coerce to [] for Python callers.
        return [] if v is None else v


# ---------------------------------------------------------------------------
# Support tickets
# ---------------------------------------------------------------------------


class SupportTicketComment(BaseModel):
    """A single comment on a support ticket thread."""

    comment_id: str = ""
    ticket_id: str = ""
    author_id: str = ""
    author_email: str = ""
    author_type: str = ""
    content: str = ""
    is_internal: bool = False
    created_at: str | None = None

    model_config = {"extra": "allow"}


class SupportTicketHistory(BaseModel):
    """A single audit-log entry describing a change to a support ticket."""

    history_id: str = ""
    ticket_id: str = ""
    changed_by: str = ""
    changed_by_email: str = ""
    field_changed: str = ""
    old_value: str = ""
    new_value: str = ""
    created_at: str | None = None

    model_config = {"extra": "allow"}


class SupportTicket(BaseModel):
    """A support ticket owned by a tenant."""

    ticket_id: str = ""
    tenant_id: str = ""
    created_by: str = ""
    created_by_email: str = ""
    assigned_to: str = ""
    assigned_to_email: str = ""
    title: str = ""
    description: str = ""
    type: str = ""
    status: str = ""
    priority: str = ""
    comment_count: int = 0
    comments: list[SupportTicketComment] | None = None
    resolved_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    model_config = {"extra": "allow"}


class TicketSummary(BaseModel):
    """Compact ticket representation used by list endpoints."""

    ticket_id: str = ""
    title: str = ""
    type: str = ""
    status: str = ""
    priority: str = ""
    created_by_email: str = ""
    assigned_to_email: str = ""
    comment_count: int = 0
    created_at: str | None = None
    updated_at: str | None = None

    model_config = {"extra": "allow"}


class TicketListResponse(BaseModel):
    """Paginated list of the caller's support tickets."""

    tickets: list[TicketSummary] = Field(default_factory=list)
    total: int = 0
    has_more: bool = False

    model_config = {"extra": "allow"}


class TicketDetailResponse(BaseModel):
    """A single support ticket with its change history."""

    ticket: SupportTicket = Field(default_factory=lambda: SupportTicket())
    history: list[SupportTicketHistory] | None = None


# ---------------------------------------------------------------------------
# Resolve forward references
# ---------------------------------------------------------------------------
# ChatStreamEvent (in _customizations/chat.py) has `usage: "ChatUsage | None"`
# as a forward reference to avoid a circular import at definition time.
# Now that ChatUsage is defined above, tell Pydantic to resolve it.
from sonzai._customizations.chat import ChatStreamEvent as _ChatStreamEvent  # noqa: E402

_ChatStreamEvent.model_rebuild(_types_namespace={"ChatUsage": ChatUsage})
