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


class GoalsResponse(BaseModel):
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
    created_at: str | None = None
    completed_at: str | None = None


class EvalRunListResponse(BaseModel):
    runs: list[EvalRun] = Field(default_factory=list)
    total_count: int = 0


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


class VoiceMatchResponse(BaseModel):
    voice_id: str = ""
    voice_name: str = ""
    match_score: float = 0.0
    reasoning: str = ""

    model_config = {"extra": "allow"}


class TTSResponse(BaseModel):
    audio: str = ""
    content_type: str = ""
    voice_name: str = ""
    duration_ms: int = 0

    model_config = {"extra": "allow"}


class VoiceChatResponse(BaseModel):
    transcript: str = ""
    response: str = ""
    audio: str = ""
    content_type: str = ""
    continuation_token: str = ""

    model_config = {"extra": "allow"}


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


class GenerateCharacterResponse(BaseModel):
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


class InsertFactsResponse(BaseModel):
    processed: int = 0
    created: int = 0
    updated: int = 0
    details: list[InsertFactDetail] = Field(default_factory=list)


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
