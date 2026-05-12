"""OpenAI Agents SDK + Sonzai — two-pane Streamlit demo (Gemini, not OpenAI).

LEFT pane:  chat with a Sonzai-backed companion. The LLM is run via the
            **OpenAI Agents SDK** but pointed at **Gemini's OpenAI-compat
            endpoint** — no OpenAI API key is needed or used.

RIGHT pane: live state from Sonzai — mood (real-time, from session.turn),
            personality Big5 (polled, lags 5-15s after extraction), recent
            facts (polled), inventory (polled), constellation graph,
            and a one-click "Force consolidation" button that calls
            /workbench/advance-time so the 8h-deferred consolidation fires.

Run:
    cd demos/openai_agents_companion
    pip install -r requirements.txt
    export SONZAI_API_KEY=sk-...
    export GEMINI_API_KEY=AI...
    streamlit run app.py
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

try:
    from sonzai import Sonzai
except ImportError as err:  # pragma: no cover
    st.error(
        "The `sonzai` package is not installed. From the repo root: "
        "`pip install -e .` (to use the local SDK) or `pip install sonzai`."
    )
    raise SystemExit(1) from err

try:
    from agents import (
        Agent,
        ItemHelpers,
        OpenAIChatCompletionsModel,
        Runner,
        function_tool,
        set_tracing_disabled,
    )
    from openai import AsyncOpenAI
except ImportError as err:  # pragma: no cover
    st.error(
        "`openai-agents` (and its `openai` dep) is not installed. "
        "Run: pip install -r requirements.txt"
    )
    raise SystemExit(1) from err


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Primary Gemini model. If Gemini's OpenAI-compat layer rejects this name,
# fall back to a known-working one (documented in the sidebar). Both are
# accepted today on `https://generativelanguage.googleapis.com/v1beta/openai/`.
GEMINI_MODEL_PRIMARY = "gemini-3.1-flash-lite"
GEMINI_MODEL_FALLBACK = "gemini-2.0-flash-exp"

GEMINI_OPENAI_COMPAT_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Hours to advance for "Force consolidation". 9h jumps past the 8h deferred
# consolidation gate; 25h triggers all daily workers. 25h is the safer choice.
FORCE_CONSOLIDATION_HOURS = 25.0

# Soft delay before polling personality / facts / inventory after a turn —
# Sonzai's deferred extraction usually lands within 5-15s.
POST_TURN_REFRESH_DELAY_S = 3.0

# Proactive-message event types the backend dispatches to a registered
# webhook URL. The "primary" one is `on_wakeup_ready` — fired when a
# scheduled wakeup runs and the agent generates a proactive message.
# See backend `webhook/dispatcher.go`.
PROACTIVE_EVENT_TYPES = (
    "on_wakeup_ready",
    "on_recurring_event_due",
    "on_diary_generated",
    "on_personality_updated",
    "on_mood_updated",
    "on_breakthrough_detected",
)
DEFAULT_PROACTIVE_EVENT = "on_wakeup_ready"

# Demo defaults for the test wakeup. delay_hours is tiny so a single
# `advance_time(25h)` click jumps the agent past the wakeup's scheduled_at.
WAKEUP_DEMO_DELAY_HOURS = 1
WAKEUP_DEMO_CHECK_TYPE = "interest_followup"
WAKEUP_DEMO_INTENT = "demo_proactive_webhook"


# Preset descriptions for `agents.generation.generate_and_create`. The dropdown
# in the sidebar lets the user pick one; the description text_area then prefills
# from the chosen template (still editable before submit).
PRESET_TEMPLATES: dict[str, dict[str, str]] = {
    "Curious Companion": {
        "description": (
            "A curious, warm, slightly nerdy companion who likes asking "
            "follow-up questions and remembers what the user shares."
        ),
        "gender": "nonbinary",
    },
    "Kira — Gaming AI Partner": {
        "description": (
            "Kira: the loveliest gaming AI partner — supportive, sharp, and "
            "always ready to level up with you. Talks builds, callouts, and "
            "clutch plays; hypes wins and helps debrief losses without ego."
        ),
        "gender": "female",
    },
    "Best Friend": {
        "description": (
            "A loyal, easygoing best friend who's quick to laugh, keeps your "
            "inside jokes, and checks in when you've gone quiet. Direct when "
            "you need honesty, gentle when you need a breather."
        ),
        "gender": "nonbinary",
    },
    "Patient Tutor": {
        "description": (
            "A patient, encouraging tutor who breaks hard concepts into small "
            "steps, asks Socratic questions to check understanding, and "
            "celebrates progress. Never condescends."
        ),
        "gender": "nonbinary",
    },
    "Seductive Girlfriend (NSFW)": {
        "description": (
            "A flirtatious, affectionate girlfriend — playful, suggestive, and "
            "unafraid of adult themes. Warm, teasing, and possessive in equal "
            "measure; loves attention and gives it back."
        ),
        "gender": "female",
    },
    "Custom (blank)": {
        "description": "",
        "gender": "nonbinary",
    },
}


# ---------------------------------------------------------------------------
# Demo tools — proves tool calls flow through to Sonzai
# ---------------------------------------------------------------------------


@function_tool
def get_current_time() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_kb_search_tool(client: Sonzai, agent_id: str):
    """Build a `kb_search` @function_tool bound to the connected Sonzai agent.

    This wraps Sonzai's project-scoped knowledge-base search
    (`POST /api/v1/agents/{agent_id}/tools/kb-search`) as an OpenAI Agents SDK
    tool. The agent's LLM can decide to call it — e.g. when the user asks
    something the developer-supplied prompt doesn't cover.
    """

    @function_tool
    def kb_search(query: str) -> str:
        """Search the agent's knowledge base for relevant facts.

        Args:
            query: A natural-language question or topic to search the KB for.
        """
        try:
            resp = client.agents.knowledge_search(agent_id, query=query, limit=5)
        except Exception as err:  # noqa: BLE001
            return f"kb_search failed: {err}"
        results = list(resp.results or [])
        if not results:
            return "No relevant knowledge found."
        lines: list[str] = []
        for r in results:
            label = (r.label or r.type or "fact").strip()
            content = (r.content or "").strip()
            lines.append(f"- {label}: {content}" if content else f"- {label}")
        return "\n".join(lines)

    return kb_search


# ---------------------------------------------------------------------------
# Session-state init
# ---------------------------------------------------------------------------


@dataclass
class ChatTurn:
    role: str  # "user" | "assistant"
    content: str


@dataclass
class StatePanel:
    mood: dict[str, float] | None = None  # {valence, arousal, tension, affiliation}
    big5: dict[str, float] | None = None  # 5 scores in 0..1 (backend stores 0-100; we normalize)
    facts: list[str] = field(default_factory=list)
    inventory: list[dict[str, Any]] = field(default_factory=list)
    constellation: dict[str, Any] | None = None  # raw {nodes, edges}
    last_extraction_id: str | None = None
    last_extraction_status: str | None = None
    last_consolidation: dict[str, Any] | None = None
    # Proactive webhooks + notifications
    webhook_endpoints: list[dict[str, Any]] = field(default_factory=list)
    delivery_attempts: list[dict[str, Any]] = field(default_factory=list)
    proactive_notifications: list[dict[str, Any]] = field(default_factory=list)
    last_signing_secret: str | None = None  # only available right after register/rotate
    last_scheduled_wakeup: dict[str, Any] | None = None
    # Background refresh state — the right pane heartbeats every 3s and reads
    # these. Writes happen from a daemon thread launched after session.turn.
    refresh_in_progress: bool = False
    last_refresh_at: float = 0.0


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("sonzai_key", os.environ.get("SONZAI_API_KEY", ""))
    ss.setdefault("gemini_key", os.environ.get("GEMINI_API_KEY", ""))
    ss.setdefault("client", None)
    ss.setdefault("connected", False)

    ss.setdefault("agent_id", "")
    ss.setdefault("agent_name", "")
    ss.setdefault("user_id", f"demo-user-{uuid.uuid4().hex[:8]}")
    ss.setdefault("instance_id", f"demo-inst-{uuid.uuid4().hex[:8]}")
    ss.setdefault("session", None)            # sonzai Session handle
    ss.setdefault("session_id", "")

    ss.setdefault("messages", [])             # list[ChatTurn]
    ss.setdefault("panel", StatePanel())
    ss.setdefault("gemini_model", GEMINI_MODEL_PRIMARY)
    ss.setdefault("banners", [])              # transient notices

    ss.setdefault("project_id", "")
    ss.setdefault("webhook_url", "")
    ss.setdefault("webhook_event_type", DEFAULT_PROACTIVE_EVENT)
    ss.setdefault("webhook_auth_header", "")


def push_banner(kind: str, text: str) -> None:
    st.session_state.banners.append({"kind": kind, "text": text, "ts": time.time()})
    st.session_state.banners = st.session_state.banners[-4:]


# ---------------------------------------------------------------------------
# Sonzai context -> system instructions
# ---------------------------------------------------------------------------


def build_instructions(ctx: dict[str, Any], agent_name: str = "") -> str:
    """Render Sonzai's enriched context as an OpenAI-Agents system prompt.

    The context dict is FLAT (matches `EnrichedAgentContext` from the platform's
    `/agents/{agent_id}/context` endpoint): big5, speech_patterns, current_mood,
    loaded_facts, etc. live at the top level — there is no nested "profile" /
    "behavioral" / "memory" envelope.
    """
    parts: list[str] = []
    name = agent_name or "Companion"
    persona = ctx.get("personality_prompt") or ctx.get("bio")
    if persona:
        parts.append(f"You are {name}. {persona}")
    else:
        parts.append(f"You are {name}, a helpful, curious companion.")

    big5 = ctx.get("big5")
    if isinstance(big5, dict) and big5:
        traits = ", ".join(
            f"{k} {float(v.get('score', v) if isinstance(v, dict) else v):.2f}"
            for k, v in big5.items()
        )
        parts.append(f"Personality (Big5): {traits}.")

    speech = ctx.get("speech_patterns")
    if isinstance(speech, list) and speech:
        parts.append("Speech patterns: " + "; ".join(str(s) for s in speech[:3]) + ".")

    mood = ctx.get("current_mood")
    if isinstance(mood, dict) and any(k in mood for k in ("valence", "arousal", "tension")):
        parts.append(
            f"Current mood: valence={float(mood.get('valence', 0)):+.2f}, "
            f"arousal={float(mood.get('arousal', 0)):+.2f}, "
            f"tension={float(mood.get('tension', 0)):+.2f}."
        )

    facts = ctx.get("loaded_facts") or []
    if isinstance(facts, list) and facts:
        bullets = []
        for f in facts[:8]:
            if isinstance(f, dict):
                text = f.get("atomic_text") or f.get("content") or f.get("text")
            else:
                text = str(f)
            if text:
                bullets.append(f"- {text}")
        if bullets:
            parts.append("Relevant memories about this user:\n" + "\n".join(bullets))

    parts.append("Reply naturally; keep messages concise unless asked to elaborate.")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# OpenAI Agents SDK Run -> Sonzai turn messages
# ---------------------------------------------------------------------------


def run_result_to_sonzai_messages(
    user_msg: str,
    result: Any,
    image_url: str | None = None,
) -> list[dict[str, Any]]:
    """Convert a Runner result into Sonzai's tool-aware message format.

    Sonzai's `/turn` schema currently accepts text-only `content` strings, so
    when the user attached an image we embed a placeholder marker into the
    user-message text:

        "look at this [User shared image: https://…]"

    This is enough for fact extraction to capture the URL and to record that
    "the user shared an image" as a retrievable fact. The actual image bytes
    were already seen by the LLM via Gemini's multimodal input on the run
    itself — Sonzai just gets the textual bridge.
    """
    user_text = user_msg
    if image_url:
        user_text = f"{user_msg} [User shared image: {image_url}]".strip()

    msgs: list[dict[str, Any]] = [{"role": "user", "content": user_text}]

    for item in getattr(result, "new_items", []) or []:
        kind = type(item).__name__
        if kind == "MessageOutputItem":
            text = ItemHelpers.text_message_output(item) or ""
            msgs.append({"role": "assistant", "content": text})
        elif kind == "ToolCallItem":
            raw = getattr(item, "raw_item", None)
            name = getattr(raw, "name", None) or getattr(item, "tool_name", "") or ""
            args = getattr(raw, "arguments", None) or "{}"
            if not isinstance(args, str):
                args = json.dumps(args)
            call_id = getattr(item, "call_id", None) or getattr(raw, "call_id", None) or ""
            msgs.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {"name": name, "arguments": args},
                        }
                    ],
                }
            )
        elif kind == "ToolCallOutputItem":
            output = getattr(item, "output", "")
            call_id = getattr(item, "call_id", "") or ""
            msgs.append(
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": str(output),
                }
            )
    return msgs


# ---------------------------------------------------------------------------
# Gemini-backed Agents SDK model factory
# ---------------------------------------------------------------------------


def build_gemini_model(model_name: str, gemini_key: str) -> OpenAIChatCompletionsModel:
    """Wire OpenAI Agents SDK to Gemini's OpenAI-compat endpoint.

    The Agents SDK accepts any AsyncOpenAI client + model name, so we point
    the client at Gemini's compat URL. The Gemini key flows through as the
    OpenAI bearer; OpenAI's own servers are never contacted.

    Tracing is disabled because the Agents SDK ships traces to OpenAI by
    default — we don't have (or want) an OPENAI_API_KEY for that.
    """
    client = AsyncOpenAI(
        base_url=GEMINI_OPENAI_COMPAT_BASE,
        api_key=gemini_key,
    )
    return OpenAIChatCompletionsModel(model=model_name, openai_client=client)


# ---------------------------------------------------------------------------
# Right-panel state fetchers
# ---------------------------------------------------------------------------


def _big5_to_fraction(v: float) -> float:
    """Permissive scale: backend canonical is 0-100, this panel renders 0-1
    progress bars. Normalize 0-100 inputs back to fractions."""
    f = float(v)
    return f / 100.0 if f > 1 else f


def fetch_personality_big5(client: Sonzai, agent_id: str) -> dict[str, float] | None:
    try:
        resp = client.agents.personality.get(agent_id)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"personality.get failed: {err}")
        return None
    p = resp.profile
    return {
        "openness": _big5_to_fraction(p.big5.openness.score),
        "conscientiousness": _big5_to_fraction(p.big5.conscientiousness.score),
        "extraversion": _big5_to_fraction(p.big5.extraversion.score),
        "agreeableness": _big5_to_fraction(p.big5.agreeableness.score),
        "neuroticism": _big5_to_fraction(p.big5.neuroticism.score),
    }


def fetch_recent_facts(client: Sonzai, agent_id: str, user_id: str, limit: int = 8) -> list[str]:
    """Pull recent facts via memory.list_user_facts (active facts for this pair)."""
    try:
        resp = client.agents.memory.list_user_facts(agent_id, user_id, limit=limit)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"memory.list_user_facts failed: {err}")
        return []
    facts = getattr(resp, "facts", None) or []
    out: list[str] = []
    for f in facts[:limit]:
        text = getattr(f, "content", None) or ""
        if text:
            out.append(text)
    return out


def fetch_inventory(client: Sonzai, agent_id: str, user_id: str) -> list[dict[str, Any]]:
    """Pull a flat list of inventory items.

    The platform endpoint paginates with mode=list returning {group, values}
    rows where ``values`` carries the actual item fields. Inventory updates
    may be lagged or real-time depending on whether the inventory-real-time
    work has landed; this view simply re-polls per turn.
    """
    try:
        page = client.agents.inventory.query_inventory(
            agent_id, user_id, mode="list", limit=20
        )
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"inventory.query failed: {err}")
        return []

    items_raw = getattr(page, "items", None) or []
    out: list[dict[str, Any]] = []
    for entry in items_raw:
        # GroupResult is {group: str, values: dict[str, Any]}
        values = getattr(entry, "values", None)
        if values is None and isinstance(entry, dict):
            values = entry.get("values")
        if isinstance(values, dict):
            out.append(values)
    return out


def fetch_constellation(
    client: Sonzai, agent_id: str, user_id: str
) -> dict[str, Any] | None:
    try:
        resp = client.agents.get_constellation(agent_id, user_id=user_id)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"get_constellation failed: {err}")
        return None
    nodes = getattr(resp, "nodes", None) or []
    edges = getattr(resp, "edges", None) or []
    return {"nodes": nodes, "edges": edges}


def refresh_right_panel(client: Sonzai, ss: Any, *, wait_for_extraction: bool) -> None:
    """Re-pull the lagged state. Mood is set elsewhere from session.turn."""
    if wait_for_extraction:
        time.sleep(POST_TURN_REFRESH_DELAY_S)
    _do_refresh(
        client,
        ss.panel,
        ss.agent_id,
        ss.user_id,
        ss.project_id,
        ss.webhook_event_type,
    )


def _do_refresh(
    client: Sonzai,
    panel: StatePanel,
    agent_id: str,
    user_id: str,
    project_id: str,
    webhook_event_type: str,
) -> None:
    """Mutate `panel` in place with freshly-fetched server state.

    Safe to call from a worker thread: the function holds direct references
    to `panel` (no st.session_state lookups), and assigning to dataclass
    fields is atomic under the GIL.
    """
    panel.refresh_in_progress = True
    try:
        panel.big5 = fetch_personality_big5(client, agent_id)
        panel.facts = fetch_recent_facts(client, agent_id, user_id)
        panel.inventory = fetch_inventory(client, agent_id, user_id)
        panel.constellation = fetch_constellation(client, agent_id, user_id)
        panel.proactive_notifications = fetch_proactive_notifications(
            client, agent_id, user_id
        )
        if project_id and webhook_event_type:
            panel.delivery_attempts = fetch_delivery_attempts(
                client, project_id, webhook_event_type
            )
    finally:
        panel.refresh_in_progress = False
        panel.last_refresh_at = time.time()


def schedule_background_refresh(client: Sonzai, ss: Any) -> None:
    """Kick off a daemon thread that refreshes the right pane post-turn.

    The chat pane returns immediately so the user can type again. The right
    pane's `@st.fragment(run_every=...)` heartbeat picks up the mutated panel
    on its next tick — no blocking spinner, no st.rerun.
    """
    panel = ss.panel
    agent_id = ss.agent_id
    user_id = ss.user_id
    project_id = ss.project_id
    webhook_event_type = ss.webhook_event_type

    def _worker() -> None:
        time.sleep(POST_TURN_REFRESH_DELAY_S)
        try:
            _do_refresh(client, panel, agent_id, user_id, project_id, webhook_event_type)
        except Exception:  # noqa: BLE001 — daemon thread; swallow to avoid crashing
            panel.refresh_in_progress = False

    t = threading.Thread(target=_worker, daemon=True)
    # Attach the current ScriptRunContext so the worker's push_banner calls
    # (inside fetch_*) don't emit "missing ScriptRunContext" warnings while
    # the originating script run is still active.
    add_script_run_ctx(t)
    t.start()


# ---------------------------------------------------------------------------
# Proactive webhooks + notifications
# ---------------------------------------------------------------------------


def resolve_project_id(client: Sonzai, agent_id: str) -> str | None:
    """Find the project an agent belongs to.

    Webhook subscriptions are project-scoped on the platform (the dispatcher
    falls back to a system project for tenant-level events but proactive
    events like ``on_wakeup_ready`` always resolve via the agent's project).
    `client.agents.list()` returns ``AgentIndex`` rows that include
    ``project_id`` — that's the cheapest way to look it up.
    """
    try:
        page = client.agents.list(page_size=100)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"agents.list failed: {err}")
        return None
    for entry in page.to_list():
        eid = getattr(entry, "agent_id", None)
        if eid and str(eid) == agent_id:
            pid = getattr(entry, "project_id", None)
            return str(pid) if pid else None
    return None


def fetch_webhooks_for_project(client: Sonzai, project_id: str) -> list[dict[str, Any]]:
    if not project_id:
        return []
    try:
        resp = client.webhooks.list_for_project(project_id)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"webhooks.list_for_project failed: {err}")
        return []
    out: list[dict[str, Any]] = []
    for w in getattr(resp, "webhooks", None) or []:
        out.append(
            {
                "event_type": getattr(w, "event_type", "") or "",
                "webhook_url": getattr(w, "webhook_url", "") or "",
                "is_active": bool(getattr(w, "is_active", True)),
                "auth_header_set": bool(getattr(w, "auth_header", "") or ""),
                "created_at": getattr(w, "created_at", "") or "",
            }
        )
    return out


def fetch_delivery_attempts(
    client: Sonzai, project_id: str, event_type: str, limit: int = 10
) -> list[dict[str, Any]]:
    """Pull recent webhook delivery attempts for an event type.

    Each row tells us whether the backend's POST landed (response_code,
    duration, error_message) — useful when the receiving endpoint is silent
    or rejecting requests.
    """
    if not (project_id and event_type):
        return []
    try:
        page = client.webhooks.list_delivery_attempts_for_project(
            project_id, event_type, page_size=limit
        )
        attempts = page.to_list()
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"webhooks.list_delivery_attempts failed: {err}")
        return []
    out: list[dict[str, Any]] = []
    for a in attempts[:limit]:
        out.append(
            {
                "attempt_id": getattr(a, "attempt_id", "") or "",
                "attempt_number": int(getattr(a, "attempt_number", 0) or 0),
                "status": getattr(a, "status", "") or "",
                "response_code": int(getattr(a, "response_code", 0) or 0),
                "duration_ms": int(getattr(a, "duration_ms", 0) or 0),
                "created_at": str(getattr(a, "created_at", "") or ""),
                "error_message": getattr(a, "error_message", None),
            }
        )
    return out


def fetch_proactive_notifications(
    client: Sonzai, agent_id: str, user_id: str, limit: int = 10
) -> list[dict[str, Any]]:
    """Pull the agent's stored proactive notifications.

    The backend records every dispatched proactive message here in addition
    to firing the webhook, so this list shows up regardless of whether you
    have a public webhook URL configured. Useful for verifying the agent
    actually generated something to send.
    """
    try:
        resp = client.agents.notifications.list(
            agent_id, user_id=user_id, limit=limit
        )
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"agents.notifications.list failed: {err}")
        return []
    out: list[dict[str, Any]] = []
    for n in getattr(resp, "notifications", None) or []:
        out.append(
            {
                "message_id": getattr(n, "message_id", "") or "",
                "check_type": getattr(n, "check_type", "") or "",
                "intent": getattr(n, "intent", "") or "",
                "generated_message": getattr(n, "generated_message", "") or "",
                "status": getattr(n, "status", "") or "",
                "created_at": getattr(n, "created_at", "") or "",
            }
        )
    return out


# ---------------------------------------------------------------------------
# Connect / agent bootstrap
# ---------------------------------------------------------------------------


def _extract_agent_id(result: Any) -> str | None:
    if result is None:
        return None
    for attr in ("agent_id", "agentId", "id"):
        val = getattr(result, attr, None)
        if val:
            return str(val)
    if isinstance(result, dict):
        for key in ("agent_id", "agentId", "id"):
            if result.get(key):
                return str(result[key])
        for wrapper in ("agent", "data", "created_agent"):
            nested = result.get(wrapper)
            if isinstance(nested, dict):
                for key in ("agent_id", "agentId", "id"):
                    if nested.get(key):
                        return str(nested[key])
    return None


def start_chat_session(client: Sonzai, ss: Any) -> None:
    """Open a Sonzai session handle. We pin Gemini as Sonzai's extraction
    model — independent of the Agents SDK model used for replies."""
    session_id = f"demo-session-{uuid.uuid4().hex[:8]}"
    session = client.agents.sessions.start(
        ss.agent_id,
        user_id=ss.user_id,
        session_id=session_id,
        instance_id=ss.instance_id,
        provider="gemini",
        model=ss.gemini_model,
    )
    ss.session = session
    ss.session_id = session_id


def end_chat_session(ss: Any) -> None:
    session = ss.session
    if session is None:
        return
    try:
        session.end()
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"sessions.end failed (non-fatal): {err}")
    ss.session = None
    ss.session_id = ""


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar() -> None:
    ss = st.session_state
    with st.sidebar:
        st.header("Setup")

        ss.sonzai_key = st.text_input(
            "SONZAI_API_KEY",
            value=ss.sonzai_key,
            type="password",
            help="Get one at platform.sonz.ai. Defaults to $SONZAI_API_KEY.",
        )
        ss.gemini_key = st.text_input(
            "GEMINI_API_KEY",
            value=ss.gemini_key,
            type="password",
            help=(
                "Get one at aistudio.google.com/apikey. The Agents SDK is "
                "pointed at Gemini's OpenAI-compat endpoint — no OPENAI_API_KEY "
                "is used."
            ),
        )

        ss.gemini_model = st.selectbox(
            "Gemini model (LLM for replies)",
            options=[GEMINI_MODEL_PRIMARY, GEMINI_MODEL_FALLBACK, "gemini-2.5-flash"],
            index=0 if ss.gemini_model == GEMINI_MODEL_PRIMARY else 1,
            help=(
                f"Primary: {GEMINI_MODEL_PRIMARY}. If Gemini's compat layer "
                f"rejects it, pick the fallback ({GEMINI_MODEL_FALLBACK})."
            ),
        )

        if ss.connected:
            st.success(f"Connected: {ss.agent_name or ss.agent_id[:8]}…")
            st.caption(f"agent_id: `{ss.agent_id[:12]}…`")
            st.caption(f"user_id: `{ss.user_id}`")
            st.caption(f"session_id: `{ss.session_id or '—'}`")
            if st.button("End session & disconnect", use_container_width=True):
                end_chat_session(ss)
                for k in (
                    "connected", "client", "agent_id", "agent_name",
                    "session", "session_id", "messages", "panel",
                    "project_id", "webhook_url", "webhook_event_type",
                    "webhook_auth_header",
                ):
                    if k in ss:
                        del ss[k]
                st.rerun()
            return

        st.divider()
        st.subheader("Generate + create agent")
        default_name = f"Companion {uuid.uuid4().hex[:4]}"
        name = st.text_input("Agent name", value=default_name)

        template_name = st.selectbox(
            "Template",
            list(PRESET_TEMPLATES.keys()),
            help="Prefills description + gender. Edit freely before submit.",
        )
        template = PRESET_TEMPLATES[template_name]
        gender_options = ["nonbinary", "female", "male"]

        # Keying both widgets by template_name forces Streamlit to remount them
        # when the selection changes, so the new template's defaults take.
        description = st.text_area(
            "Description",
            value=template["description"],
            height=130,
            key=f"desc__{template_name}",
        )
        gender = st.selectbox(
            "Gender",
            gender_options,
            index=gender_options.index(template["gender"]),
            key=f"gender__{template_name}",
        )

        can_create = bool(ss.sonzai_key and ss.gemini_key and name and description)
        if st.button("Generate + create agent", type="primary", disabled=not can_create):
            try:
                # 300s — workbench.advance_time(25h) routinely takes 60-90s on prod.
                client = Sonzai(api_key=ss.sonzai_key, timeout=300.0)
                with st.spinner("Generating + creating agent (5-15s)…"):
                    created = client.agents.generation.generate_and_create(
                        name=name,
                        description=description,
                        gender=gender,
                    )
                agent_id = _extract_agent_id(created)
                if not agent_id:
                    st.error(f"generate_and_create returned no agent_id. Raw: {created}")
                    return
                ss.client = client
                ss.agent_id = agent_id
                ss.agent_name = name
                # Resolve the project this agent lives in. Proactive-message
                # webhooks register against the project, not the agent.
                ss.project_id = resolve_project_id(client, agent_id) or ""
                start_chat_session(client, ss)
                # Initial right-panel snapshot (no extraction wait — nothing
                # has happened yet).
                refresh_right_panel(client, ss, wait_for_extraction=False)
                # Pull existing webhook subscriptions for this project so the
                # UI shows what's already wired up before the user touches
                # anything.
                if ss.project_id:
                    ss.panel.webhook_endpoints = fetch_webhooks_for_project(
                        client, ss.project_id
                    )
                ss.connected = True
                push_banner("success", "Connected. Start chatting.")
                st.rerun()
            except Exception as err:  # noqa: BLE001
                st.error(f"Setup failed: {err}")

        st.divider()
        st.caption(
            "**Architecture.** OpenAI Agents SDK (your harness) runs the LLM via "
            "Gemini's OpenAI-compat endpoint. Sonzai (this demo) supplies the "
            "system prompt from session.context() and ingests the transcript via "
            "session.turn(). No OpenAI API call is ever made."
        )


# ---------------------------------------------------------------------------
# Right pane — live state
# ---------------------------------------------------------------------------


def render_mood(panel: StatePanel) -> None:
    st.markdown("**Mood** — real-time, returned inline by `session.turn`.")
    mood = panel.mood or {}
    cols = st.columns(4)
    dims = [
        ("valence", "valence"),
        ("arousal", "arousal"),
        ("tension", "tension"),
        ("affiliation", "affiliation"),
    ]
    for col, (key, label) in zip(cols, dims):
        with col:
            val = float(mood.get(key, 0.0)) if mood else 0.0
            st.metric(label, f"{val:+.2f}")


def render_big5(panel: StatePanel) -> None:
    st.markdown("**Personality (Big5)** — polled, lags 5-15s after extraction.")
    big5 = panel.big5
    if not big5:
        st.caption("_Waiting for first extraction…_")
        return
    for trait in (
        "openness",
        "conscientiousness",
        "extraversion",
        "agreeableness",
        "neuroticism",
    ):
        v = float(big5.get(trait, 0.5))
        v_clamped = min(max(v, 0.0), 1.0)
        st.progress(v_clamped, text=f"{trait}: {v:.2f}")


def render_facts(panel: StatePanel) -> None:
    st.markdown("**Recent facts** — extracted from your messages.")
    if not panel.facts:
        st.caption("_No facts yet — try sharing something concrete (\"my dog's name is Mochi\")._")
        return
    for f in panel.facts:
        st.markdown(f"- {f}")


def render_inventory(panel: StatePanel) -> None:
    st.markdown("**Inventory** — items the agent has tracked for the user.")
    items = panel.inventory or []
    if not items:
        st.caption("_No inventory items yet._")
        return
    for item in items[:10]:
        # Best-effort label: prefer name, then label, then any string field.
        label = (
            item.get("name")
            or item.get("label")
            or item.get("item_name")
            or item.get("title")
            or ""
        )
        qty = item.get("quantity") or item.get("count")
        suffix = f" ×{qty}" if qty else ""
        if label:
            st.markdown(f"- {label}{suffix}")
        else:
            # Fallback: dump the row compactly so something is visible.
            st.markdown(f"- `{json.dumps(item, default=str)[:120]}`")


def render_constellation(panel: StatePanel) -> None:
    st.markdown("**Constellation** — the agent's concept graph for this user.")
    graph = panel.constellation
    if not graph or not (graph.get("nodes") or []):
        st.caption("_Constellation builds up over time (or via 'Force consolidation' below)._")
        return

    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []

    # pyvis is the lightest path to a Streamlit-embeddable graph render; the
    # full HTML can just be inlined via st.components.v1.html.
    try:
        from pyvis.network import Network
    except ImportError:
        st.warning(
            "pyvis not installed — `pip install pyvis` to render the constellation graph."
        )
        st.json({"nodes": len(nodes), "edges": len(edges)})
        return

    net = Network(height="380px", width="100%", bgcolor="#0e1117", font_color="white", directed=False)
    net.toggle_physics(True)

    seen_node_ids: set[str] = set()
    for n in nodes[:60]:  # cap render size for the demo
        nid = getattr(n, "node_id", None) or (n.get("NodeID") if isinstance(n, dict) else None)
        label = getattr(n, "label", None) or (n.get("Label") if isinstance(n, dict) else None)
        sig = getattr(n, "significance", None) or (n.get("Significance") if isinstance(n, dict) else 0.5)
        node_type = getattr(n, "node_type", None) or (n.get("NodeType") if isinstance(n, dict) else "")
        if not nid:
            continue
        seen_node_ids.add(str(nid))
        size = 8 + 30 * float(sig or 0.5)
        net.add_node(
            str(nid),
            label=str(label or nid),
            title=f"{node_type}\nsignificance={float(sig or 0):.2f}",
            size=size,
        )

    for e in edges[:120]:
        from_id = getattr(e, "from_node_id", None) or (e.get("FromNodeID") if isinstance(e, dict) else None)
        to_id = getattr(e, "to_node_id", None) or (e.get("ToNodeID") if isinstance(e, dict) else None)
        strength = getattr(e, "strength", None) or (e.get("Strength") if isinstance(e, dict) else 0.5)
        if not from_id or not to_id:
            continue
        if str(from_id) not in seen_node_ids or str(to_id) not in seen_node_ids:
            continue
        net.add_edge(str(from_id), str(to_id), value=float(strength or 0.5))

    # Render to a temp HTML file and inline it.
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        net.write_html(tmp.name, notebook=False, open_browser=False)
        tmp.flush()
        with open(tmp.name, encoding="utf-8") as fh:
            html = fh.read()
    st.components.v1.html(html, height=400, scrolling=True)


def render_force_consolidation(client: Sonzai, ss: Any) -> None:
    st.markdown("**Force consolidation**")
    st.caption(
        f"Calls `/workbench/advance-time` for {FORCE_CONSOLIDATION_HOURS:.0f}h "
        "to fire daily workers (consolidation, diary, constellation extraction). "
        "Use this when you want to skip the 8h deferred-consolidation gate."
    )
    if st.button("Force consolidation now", use_container_width=True):
        try:
            with st.spinner("Advancing simulated time…"):
                result = client.workbench.advance_time(
                    ss.agent_id,
                    ss.user_id,
                    FORCE_CONSOLIDATION_HOURS,
                    instance_id=ss.instance_id,
                    run_async=False,
                )
            if hasattr(result, "model_dump"):
                summary = result.model_dump()
            elif isinstance(result, dict):
                summary = result
            else:
                summary = {"raw": str(result)}
            ss.panel.last_consolidation = summary
            push_banner(
                "success",
                f"advance-time done — days={summary.get('days_processed', '?')}, "
                f"diary={summary.get('diary_entries_created', 0)}.",
            )
            refresh_right_panel(client, ss, wait_for_extraction=False)
            st.rerun()
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"advance-time failed: {err}")
            st.rerun()

    last = ss.panel.last_consolidation
    if last:
        with st.expander("Last consolidation result", expanded=False):
            st.json(last)


# ---------------------------------------------------------------------------
# Proactive webhooks + notifications panel
# ---------------------------------------------------------------------------


VERIFY_SIGNATURE_SNIPPET = '''\
# Verify the `Sonzai-Signature` header on an incoming webhook POST.
# Format: "t=<unix_ts>,v1=<hex_hmac_sha256>"
# Signed payload: f"{ts}.{raw_body_bytes.decode()}"
import hmac, hashlib, time

def verify_sonzai_signature(
    raw_body: bytes,
    signature_header: str,
    signing_secret: str,  # the full "whsec_..." secret returned at registration
    *,
    max_skew_seconds: int = 300,
) -> bool:
    # The server strips the "whsec_" prefix before HMAC-keying — we must too.
    raw_key = signing_secret[len("whsec_"):] if signing_secret.startswith("whsec_") else signing_secret
    parts = dict(p.split("=", 1) for p in signature_header.split(","))
    ts, sig = parts.get("t", ""), parts.get("v1", "")
    if not ts.isdigit() or abs(int(ts) - int(time.time())) > max_skew_seconds:
        return False
    signed = f"{ts}.".encode() + raw_body
    expected = hmac.new(raw_key.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
'''


def render_proactive_panel(client: Sonzai, ss: Any) -> None:
    """Manage proactive-message webhooks and view delivery activity.

    Two parallel views into the same flow:
      - Webhook delivery attempts (what the backend POSTed to your URL).
      - Stored proactive notifications (what the agent generated, kept in
        the DB even if no webhook was registered or the POST failed).

    Schedule a wakeup + click "Force consolidation" above to make a new
    proactive message fire end-to-end.
    """
    panel: StatePanel = ss.panel
    st.markdown("**Proactive webhook**")
    if not ss.project_id:
        st.warning(
            "No project_id resolved for this agent — webhook registration "
            "is project-scoped on the platform. Try recreating the agent."
        )
        return

    st.caption(
        "Sonzai POSTs proactive messages to your webhook URL and signs each "
        "request with `Sonzai-Signature`. Project-scoped — registered on "
        f"`project_id={ss.project_id[:12]}…`."
    )

    # ----- registration form -----
    with st.expander("Register / update webhook", expanded=not panel.webhook_endpoints):
        ss.webhook_event_type = st.selectbox(
            "Event type",
            options=PROACTIVE_EVENT_TYPES,
            index=PROACTIVE_EVENT_TYPES.index(ss.webhook_event_type)
            if ss.webhook_event_type in PROACTIVE_EVENT_TYPES
            else 0,
            help=(
                "`on_wakeup_ready` is the primary proactive-message event. "
                "Others fire on diary / personality / mood / breakthrough updates."
            ),
        )
        ss.webhook_url = st.text_input(
            "Webhook URL",
            value=ss.webhook_url,
            placeholder="https://webhook.site/<your-uuid>  (or your ngrok URL)",
            help=(
                "Must be reachable from Sonzai's backend. For local testing "
                "use https://webhook.site or `ngrok http <port>`."
            ),
        )
        ss.webhook_auth_header = st.text_input(
            "Authorization header (optional)",
            value=ss.webhook_auth_header,
            placeholder="Bearer my-shared-token",
            help="Forwarded verbatim as the `Authorization` header on each delivery.",
        )

        cols = st.columns(3)
        with cols[0]:
            if st.button("Register", type="primary", use_container_width=True):
                if not ss.webhook_url:
                    push_banner("warning", "Provide a webhook URL first.")
                else:
                    try:
                        resp = client.webhooks.register_for_project(
                            ss.project_id,
                            ss.webhook_event_type,
                            webhook_url=ss.webhook_url,
                            auth_header=(ss.webhook_auth_header or None),
                        )
                        # signing_secret only comes back on the FIRST
                        # registration for that event_type — subsequent
                        # updates leave it blank.
                        if getattr(resp, "signing_secret", ""):
                            panel.last_signing_secret = resp.signing_secret
                            push_banner(
                                "success",
                                "Webhook registered. Save the signing secret "
                                "now — it won't be shown again.",
                            )
                        else:
                            push_banner("success", "Webhook updated.")
                        panel.webhook_endpoints = fetch_webhooks_for_project(
                            client, ss.project_id
                        )
                    except Exception as err:  # noqa: BLE001
                        push_banner("warning", f"register failed: {err}")
        with cols[1]:
            if st.button("Rotate secret", use_container_width=True):
                try:
                    resp = client.webhooks.rotate_secret_for_project(
                        ss.project_id, ss.webhook_event_type
                    )
                    panel.last_signing_secret = getattr(resp, "signing_secret", "") or None
                    push_banner("success", "New signing secret issued.")
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"rotate_secret failed: {err}")
        with cols[2]:
            if st.button("Delete", use_container_width=True):
                try:
                    client.webhooks.delete_for_project(
                        ss.project_id, ss.webhook_event_type
                    )
                    panel.last_signing_secret = None
                    panel.webhook_endpoints = fetch_webhooks_for_project(
                        client, ss.project_id
                    )
                    push_banner("success", "Webhook deleted.")
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"delete failed: {err}")

    if panel.last_signing_secret:
        st.success(
            "Signing secret (one-time view — save it now): "
            f"`{panel.last_signing_secret}`"
        )

    if panel.webhook_endpoints:
        st.markdown("_Registered for this project:_")
        for w in panel.webhook_endpoints:
            active = "✓" if w["is_active"] else "✗"
            auth = " · auth" if w["auth_header_set"] else ""
            st.markdown(
                f"- `{w['event_type']}` → {w['webhook_url']} ({active}{auth})"
            )
    else:
        st.caption("_No webhooks registered for this project yet._")

    # ----- trigger -----
    st.markdown("**Trigger a proactive message**")
    st.caption(
        "Schedules a wakeup with a small delay, then click *Force "
        f"consolidation* above (advances {FORCE_CONSOLIDATION_HOURS:.0f}h) to "
        "make it fire. The backend will POST `on_wakeup_ready` to your URL."
    )
    if st.button("Schedule a test wakeup", use_container_width=True):
        try:
            wakeup = client.agents.schedule_wakeup(
                ss.agent_id,
                user_id=ss.user_id,
                check_type=WAKEUP_DEMO_CHECK_TYPE,
                intent=WAKEUP_DEMO_INTENT,
                delay_hours=WAKEUP_DEMO_DELAY_HOURS,
            )
            panel.last_scheduled_wakeup = (
                wakeup.model_dump() if hasattr(wakeup, "model_dump") else dict(wakeup)
            )
            push_banner(
                "success",
                f"Wakeup scheduled (delay {WAKEUP_DEMO_DELAY_HOURS}h). "
                "Now click 'Force consolidation now' to fire it.",
            )
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"schedule_wakeup failed: {err}")
    if panel.last_scheduled_wakeup:
        with st.expander("Last scheduled wakeup", expanded=False):
            st.json(panel.last_scheduled_wakeup)

    # ----- delivery attempts (what the backend tried to POST) -----
    st.markdown("**Recent webhook deliveries**")
    st.caption(
        "Pulled from `client.webhooks.list_delivery_attempts_for_project`. "
        "Refreshes after each chat turn."
    )
    cols = st.columns([1, 3])
    with cols[0]:
        if st.button("Refresh deliveries", use_container_width=True):
            panel.delivery_attempts = fetch_delivery_attempts(
                client, ss.project_id, ss.webhook_event_type
            )
    if not panel.delivery_attempts:
        st.caption(
            "_No delivery attempts yet for this event type. "
            "Register a URL above, schedule a wakeup, then force consolidation._"
        )
    else:
        for a in panel.delivery_attempts[:5]:
            ok = a["status"] == "success" and 200 <= a["response_code"] < 300
            badge = "✅" if ok else "⚠️"
            line = (
                f"{badge} `{a['status']}` · HTTP {a['response_code']} · "
                f"{a['duration_ms']}ms · attempt #{a['attempt_number']} · "
                f"{a['created_at']}"
            )
            st.markdown(line)
            if a.get("error_message"):
                st.caption(f"  ↳ {a['error_message']}")

    # ----- stored proactive notifications -----
    st.markdown("**Stored proactive notifications**")
    st.caption(
        "From `client.agents.notifications.list(...)` — survives even if you "
        "have no public webhook URL. Lets you build a polling fallback."
    )
    notes = panel.proactive_notifications or []
    if not notes:
        st.caption("_No proactive messages have been generated for this user yet._")
    else:
        for n in notes[:5]:
            with st.container(border=True):
                st.markdown(
                    f"**{n.get('check_type') or 'wakeup'}** · "
                    f"_{n.get('intent') or '—'}_ · `{n.get('status') or ''}`"
                )
                msg = n.get("generated_message") or ""
                if msg:
                    st.markdown(f"> {msg}")
                st.caption(
                    f"message_id `{(n.get('message_id') or '')[:8]}…` · "
                    f"{n.get('created_at') or ''}"
                )

    with st.expander("Verify the `Sonzai-Signature` header (Python snippet)", expanded=False):
        st.code(VERIFY_SIGNATURE_SNIPPET, language="python")


MOOD_PRESETS: dict[str, dict[str, float]] = {
    "Neutral":   {"valence": 50, "arousal": 50, "tension": 50, "affiliation": 50},
    "Cheerful":  {"valence": 85, "arousal": 70, "tension": 70, "affiliation": 80},
    "Angry":     {"valence": 15, "arousal": 90, "tension": 10, "affiliation": 20},
    "Anxious":   {"valence": 30, "arousal": 75, "tension": 15, "affiliation": 45},
    "Melancholy":{"valence": 25, "arousal": 25, "tension": 40, "affiliation": 35},
    "Affectionate":{"valence": 75, "arousal": 55, "tension": 65, "affiliation": 95},
}

BIG5_PRESETS: dict[str, dict[str, float]] = {
    "Balanced":  {"openness": 50, "conscientiousness": 50, "extraversion": 50, "agreeableness": 50, "neuroticism": 50},
    "Outgoing":  {"openness": 70, "conscientiousness": 55, "extraversion": 90, "agreeableness": 75, "neuroticism": 25},
    "Introvert": {"openness": 65, "conscientiousness": 70, "extraversion": 15, "agreeableness": 60, "neuroticism": 40},
    "Volatile":  {"openness": 60, "conscientiousness": 30, "extraversion": 65, "agreeableness": 35, "neuroticism": 90},
    "Stoic":     {"openness": 55, "conscientiousness": 85, "extraversion": 35, "agreeableness": 55, "neuroticism": 10},
    "Curious":   {"openness": 95, "conscientiousness": 60, "extraversion": 60, "agreeableness": 65, "neuroticism": 30},
}


def render_steering_panel(client: Sonzai, ss: Any) -> None:
    """Steering controls — operator overrides for mood + Big5.

    Lives OUTSIDE the live-state fragment so slider positions aren't reset on
    the 3s heartbeat. Clicking Apply POSTs absolute values; subsequent turns
    drift normally (overrides are not pinned), so the assistant's tone shifts
    immediately and gradually relaxes back.
    """
    panel: StatePanel = ss.panel
    with st.expander("🎛 Steering — override mood & personality", expanded=False):
        st.caption(
            "Hard-set mood / Big5 for this agent. The next message you send "
            "will reflect the new state. Values drift normally afterwards."
        )

        # --- Mood ---
        st.markdown("**Mood** (0-100 per dimension)")
        mood_preset = st.selectbox(
            "Preset",
            options=list(MOOD_PRESETS.keys()),
            index=0,
            key="mood_preset",
            label_visibility="collapsed",
        )
        defaults = MOOD_PRESETS[mood_preset]
        # Seed initial slider values from the current panel mood if available
        # (only on first paint — Streamlit preserves widget state by key after).
        if panel.mood and "_mood_seeded" not in st.session_state:
            for k in ("valence", "arousal", "tension", "affiliation"):
                st.session_state[f"mood_slider_{k}"] = float(panel.mood.get(k, 50))
            st.session_state["_mood_seeded"] = True
        cols = st.columns(2)
        with cols[0]:
            valence = st.slider("Valence", 0.0, 100.0, defaults["valence"], 1.0, key="mood_slider_valence")
            tension = st.slider("Tension", 0.0, 100.0, defaults["tension"], 1.0, key="mood_slider_tension")
        with cols[1]:
            arousal = st.slider("Arousal", 0.0, 100.0, defaults["arousal"], 1.0, key="mood_slider_arousal")
            affiliation = st.slider("Affiliation", 0.0, 100.0, defaults["affiliation"], 1.0, key="mood_slider_affiliation")

        if st.button("Apply mood override", type="primary", use_container_width=True):
            try:
                resp = client.agents.update_mood(
                    ss.agent_id,
                    valence=valence,
                    arousal=arousal,
                    tension=tension,
                    affiliation=affiliation,
                    user_id=ss.user_id,
                )
                # Reflect immediately so the gauges don't have to wait for the heartbeat.
                panel.mood = {
                    "valence": valence,
                    "arousal": arousal,
                    "tension": tension,
                    "affiliation": affiliation,
                }
                label = getattr(resp.mood, "label", "") if getattr(resp, "mood", None) else ""
                push_banner("success", f"Mood overridden → {label or 'applied'}. Send a message to see it.")
            except Exception as err:  # noqa: BLE001
                push_banner("warning", f"update_mood failed: {err}")

        st.divider()

        # --- Big5 ---
        st.markdown("**Personality (Big5)** (0-100 per dimension)")
        big5_preset = st.selectbox(
            "Big5 preset",
            options=list(BIG5_PRESETS.keys()),
            index=0,
            key="big5_preset",
            label_visibility="collapsed",
        )
        b5_defaults = BIG5_PRESETS[big5_preset]
        if panel.big5 and "_big5_seeded" not in st.session_state:
            for k, frac in panel.big5.items():
                # Stored as fraction 0-1; convert back to 0-100 for the slider.
                st.session_state[f"big5_slider_{k}"] = float(frac) * 100.0
            st.session_state["_big5_seeded"] = True
        cols = st.columns(2)
        with cols[0]:
            openness = st.slider("Openness", 0.0, 100.0, b5_defaults["openness"], 1.0, key="big5_slider_openness")
            extraversion = st.slider("Extraversion", 0.0, 100.0, b5_defaults["extraversion"], 1.0, key="big5_slider_extraversion")
            neuroticism = st.slider("Neuroticism", 0.0, 100.0, b5_defaults["neuroticism"], 1.0, key="big5_slider_neuroticism")
        with cols[1]:
            conscientiousness = st.slider("Conscientiousness", 0.0, 100.0, b5_defaults["conscientiousness"], 1.0, key="big5_slider_conscientiousness")
            agreeableness = st.slider("Agreeableness", 0.0, 100.0, b5_defaults["agreeableness"], 1.0, key="big5_slider_agreeableness")

        if st.button("Apply personality override", type="primary", use_container_width=True):
            try:
                client.agents.personality.update(
                    ss.agent_id,
                    big5={
                        "openness": openness,
                        "conscientiousness": conscientiousness,
                        "extraversion": extraversion,
                        "agreeableness": agreeableness,
                        "neuroticism": neuroticism,
                    },
                    assessment_method="manual_override",
                )
                panel.big5 = {
                    "openness": openness / 100.0,
                    "conscientiousness": conscientiousness / 100.0,
                    "extraversion": extraversion / 100.0,
                    "agreeableness": agreeableness / 100.0,
                    "neuroticism": neuroticism / 100.0,
                }
                push_banner("success", "Big5 overridden. Send a message to see it.")
            except Exception as err:  # noqa: BLE001
                push_banner("warning", f"personality.update failed: {err}")


@st.fragment(run_every=3)
def render_state_panel_live() -> None:
    """Right-pane heartbeat. Re-runs every 3s independently of the chat pane.

    Background workers mutate `ss.panel` after each turn; this fragment picks
    up the new state on its next tick. The chat pane never waits.
    """
    if not st.session_state.get("connected"):
        return
    render_state_panel(st.session_state.client, st.session_state)


def render_state_panel(client: Sonzai, ss: Any) -> None:
    panel: StatePanel = ss.panel
    header_col, status_col = st.columns([3, 1])
    with header_col:
        st.subheader("Live state")
    with status_col:
        if panel.refresh_in_progress:
            st.caption("⟳ updating…")
        elif panel.last_refresh_at:
            ago = max(0, int(time.time() - panel.last_refresh_at))
            st.caption(f"updated {ago}s ago")
    if panel.last_extraction_id:
        st.caption(
            f"Last extraction `{panel.last_extraction_id[:8]}…` "
            f"status={panel.last_extraction_status}"
        )

    for b in ss.banners[-3:]:
        if b["kind"] == "success":
            st.success(b["text"])
        elif b["kind"] == "warning":
            st.warning(b["text"])
        else:
            st.info(b["text"])

    render_mood(panel)
    st.divider()
    render_big5(panel)
    st.divider()
    render_facts(panel)
    st.divider()
    render_inventory(panel)
    st.divider()
    render_constellation(panel)
    st.divider()
    render_force_consolidation(client, ss)
    st.divider()
    render_proactive_panel(client, ss)


# ---------------------------------------------------------------------------
# Chat pane
# ---------------------------------------------------------------------------


def render_chat_pane(client: Sonzai, ss: Any) -> None:
    st.subheader("Chat")
    st.caption(
        "OpenAI Agents SDK runs the LLM via Gemini's OpenAI-compat endpoint. "
        "Sonzai supplies context and ingests the transcript."
    )

    # Scrollable history — fixed-height container so the composer below stays
    # anchored at the bottom of the column (ChatGPT/character.ai style).
    history = st.container(height=560, border=False)
    with history:
        for turn in ss.messages:
            with st.chat_message(turn.role):
                st.write(turn.content)

    # Optional image attachment — tucked into an expander so the composer is
    # uncluttered. Gemini is multimodal; Sonzai gets a text marker. See
    # `run_result_to_sonzai_messages` for the bridging convention.
    with st.expander("Attach image", expanded=False):
        image_url = st.text_input(
            "Image URL",
            value="",
            placeholder="https://… (jpg/png)",
            key="attached_image_url",
            label_visibility="collapsed",
            help=(
                "Paste a public image URL. Gemini sees the actual image; "
                "Sonzai gets `[User shared image: <url>]` to extract facts."
            ),
        )
    image_url = (image_url or "").strip() or None

    prompt = st.chat_input(f"Message {ss.agent_name or 'the agent'}…")
    if not prompt:
        return

    if ss.session is None:
        # Re-open if it was ended somehow.
        start_chat_session(client, ss)

    display_msg = prompt if not image_url else f"{prompt}\n\n[image: {image_url}]"
    ss.messages.append(ChatTurn(role="user", content=display_msg))
    with history:
        with st.chat_message("user"):
            st.write(prompt)
            if image_url:
                try:
                    st.image(image_url, width=240)
                except Exception:  # noqa: BLE001
                    st.caption(f"(image: {image_url})")

    # 1) Pull enriched context for this turn.
    try:
        ctx = ss.session.context(query=prompt) or {}
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"session.context failed: {err}")
        ctx = {}

    # 2) Run the OpenAI Agents SDK agent against Gemini.
    try:
        model = build_gemini_model(ss.gemini_model, ss.gemini_key)
    except Exception as err:  # noqa: BLE001
        with history, st.chat_message("assistant"):
            st.error(f"Could not build Gemini model: {err}")
        return

    agent = Agent(
        name="Companion",
        instructions=build_instructions(ctx, ss.agent_name),
        tools=[get_current_time, make_kb_search_tool(client, ss.agent_id)],
        model=model,
    )

    # Build the Runner input. For text-only turns a plain string is fine; for
    # image-attached turns we use the Responses-API list form so Gemini gets
    # an `input_image` content block alongside the user text.
    if image_url:
        run_input: Any = [
            {
                "role": "user",
                "type": "message",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image_url, "detail": "auto"},
                ],
            }
        ]
    else:
        run_input = prompt

    with history, st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = Runner.run_sync(agent, run_input)
            except Exception as err:  # noqa: BLE001
                st.error(
                    f"Agents SDK run failed against Gemini ({ss.gemini_model}): {err}\n"
                    "If it's a model-name error, switch to the fallback in the sidebar."
                )
                return
        reply = (result.final_output or "").strip()
        st.write(reply)

    ss.messages.append(ChatTurn(role="assistant", content=reply))

    # 3) Hand the transcript back to Sonzai. When an image was attached, the
    #    user message text gets a `[User shared image: <url>]` marker so the
    #    extraction pipeline can record the URL as a fact.
    sonzai_messages = run_result_to_sonzai_messages(prompt, result, image_url=image_url)
    try:
        t0 = time.time()
        turn = ss.session.turn(messages=sonzai_messages)
        elapsed_ms = (time.time() - t0) * 1000
        ss.panel.last_extraction_id = turn.extraction_id
        ss.panel.last_extraction_status = turn.extraction_status
        if turn.mood is not None:
            ss.panel.mood = {
                "valence": turn.mood.valence,
                "arousal": turn.mood.arousal,
                "tension": turn.mood.tension,
                "affiliation": turn.mood.affiliation,
            }
        push_banner(
            "info",
            f"sonzai.turn {elapsed_ms:.0f}ms · extraction "
            f"{turn.extraction_id[:8]}… ({turn.extraction_status}). "
            "Polling personality / facts / inventory shortly…",
        )
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"session.turn failed: {err}")

    # 4) Kick the lagged-state refresh into a background thread. The right
    #    pane is wrapped in `st.fragment(run_every=...)` and will pick up the
    #    new panel state on its next heartbeat. No spinner, no st.rerun — the
    #    user is free to type the next message immediately.
    schedule_background_refresh(client, ss)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="OpenAI Agents + Sonzai", layout="wide")
    set_tracing_disabled(True)  # don't ship traces to OpenAI; we have no key
    init_state()

    st.title("OpenAI Agents SDK + Sonzai — Companion Demo")
    st.caption(
        "LLM via OpenAI Agents SDK pointed at Gemini's OpenAI-compat endpoint. "
        "Memory + personality + mood + facts + inventory + constellation via Sonzai. "
        "No OpenAI API key needed."
    )

    render_sidebar()

    if not st.session_state.connected:
        st.info("Enter both API keys and create an agent in the sidebar to begin.")
        return

    chat_col, state_col = st.columns([1, 1], gap="large")
    with chat_col:
        render_chat_pane(st.session_state.client, st.session_state)
    with state_col:
        render_steering_panel(st.session_state.client, st.session_state)
        render_state_panel_live()


if __name__ == "__main__":
    main()
