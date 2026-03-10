"""Public types for the Sonzai SDK."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatChoice(BaseModel):
    delta: Dict[str, str] = Field(default_factory=dict)
    finish_reason: Optional[str] = None
    index: int = 0


class ChatUsage(BaseModel):
    prompt_tokens: int = Field(alias="promptTokens", default=0)
    completion_tokens: int = Field(alias="completionTokens", default=0)
    total_tokens: int = Field(alias="totalTokens", default=0)

    model_config = {"populate_by_name": True}


class ChatStreamEvent(BaseModel):
    """A single SSE event from the chat stream."""

    choices: List[ChatChoice] = Field(default_factory=list)
    usage: Optional[ChatUsage] = None
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None

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
    usage: Optional[ChatUsage] = None


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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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
    created_at: Optional[str] = None


class MemoryResponse(BaseModel):
    nodes: List[MemoryNode] = Field(default_factory=list)
    contents: Dict[str, List[AtomicFact]] = Field(default_factory=dict)


class MemorySearchResult(BaseModel):
    fact_id: str = ""
    content: str = ""
    fact_type: str = ""
    score: float = 0.0


class MemorySearchResponse(BaseModel):
    results: List[MemorySearchResult] = Field(default_factory=list)


class TimelineSession(BaseModel):
    session_id: str = ""
    facts: List[AtomicFact] = Field(default_factory=list)
    first_fact_at: Optional[str] = None
    last_fact_at: Optional[str] = None
    fact_count: int = 0


class MemoryTimelineResponse(BaseModel):
    sessions: List[TimelineSession] = Field(default_factory=list)
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
    speech_patterns: List[str] = Field(default_factory=list)
    true_interests: List[str] = Field(default_factory=list)
    true_dislikes: List[str] = Field(default_factory=list)
    primary_traits: List[str] = Field(default_factory=list)
    temperature: float = 0.0
    big5: Big5 = Field(default_factory=Big5)
    dimensions: PersonalityDimensions = Field(default_factory=PersonalityDimensions)
    preferences: PersonalityPreferences = Field(default_factory=PersonalityPreferences)
    behaviors: PersonalityBehaviors = Field(default_factory=PersonalityBehaviors)
    emotional_tendencies: Dict[str, float] = Field(default_factory=dict)
    created_at: Optional[str] = None


class PersonalityDelta(BaseModel):
    delta_id: str = ""
    change: str = ""
    reason: str = ""
    created_at: Optional[str] = None


class PersonalityResponse(BaseModel):
    profile: PersonalityProfile = Field(default_factory=PersonalityProfile)
    evolution: List[PersonalityDelta] = Field(default_factory=list)


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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class InstanceListResponse(BaseModel):
    instances: List[AgentInstance] = Field(default_factory=list)


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
    consumed_at: Optional[str] = None
    created_at: Optional[str] = None


class NotificationListResponse(BaseModel):
    notifications: List[Notification] = Field(default_factory=list)


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
    categories: List[EvalCategory] = Field(default_factory=list)


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
    categories: List[EvalTemplateCategory] = Field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class EvalTemplateListResponse(BaseModel):
    templates: List[EvalTemplate] = Field(default_factory=list)


class EvalRun(BaseModel):
    id: str = ""
    tenant_id: str = ""
    agent_id: str = ""
    agent_name: str = ""
    status: str = ""
    character_config: Dict[str, Any] = Field(default_factory=dict)
    template_id: str = ""
    template_snapshot: Dict[str, Any] = Field(default_factory=dict)
    simulation_config: Dict[str, Any] = Field(default_factory=dict)
    simulation_model: str = ""
    user_persona: Dict[str, Any] = Field(default_factory=dict)
    transcript: List[Any] = Field(default_factory=list)
    evaluation_result: Dict[str, Any] = Field(default_factory=dict)
    adaptation_result: Dict[str, Any] = Field(default_factory=dict)
    simulation_state: Dict[str, Any] = Field(default_factory=dict)
    total_sessions: int = 0
    total_turns: int = 0
    simulated_minutes: int = 0
    total_cost_usd: float = 0.0
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


class EvalRunListResponse(BaseModel):
    runs: List[EvalRun] = Field(default_factory=list)
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
    eval_result: Optional[Dict[str, Any]] = None
    adaptation_result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# User Persona
# ---------------------------------------------------------------------------


class UserPersona(BaseModel):
    id: str = ""
    name: str = ""
    background: str = ""
    personality_traits: List[str] = Field(default_factory=list)
    communication_style: str = ""

    model_config = {"extra": "allow"}
