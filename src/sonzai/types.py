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
