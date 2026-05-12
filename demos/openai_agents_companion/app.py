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

import http.server
import json
import os
import socket
import socketserver
import tempfile
import threading
import time

# Auto-load .env so `streamlit run app.py` Just Works without an explicit
# `export $(grep -v '^#' .env | xargs)` step. python-dotenv is optional —
# if missing, fall back to the manual-export instructions in README.md.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import uuid
from collections import deque
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

# Local webhook receiver: bounded ring buffer of the most recent deliveries
# we observed on 127.0.0.1. 20 entries is enough to see retries from
# dispatcher.go (4 attempts per event) and a few events back.
LOCAL_RECEIVER_MAX_DELIVERIES = 20
LOCAL_RECEIVER_BODY_PREVIEW_BYTES = 2048


class _ReuseAddrServer(socketserver.TCPServer):
    # SO_REUSEADDR so a quick Stop → Start cycle doesn't hit TIME_WAIT.
    allow_reuse_address = True


@dataclass
class LocalReceiver:
    """Per-session HTTP receiver for webhook deliveries.

    Lives in `st.session_state` across Streamlit reruns. The handler runs
    in a daemon thread and pushes every POST into `deliveries` (a
    thread-safe `deque` — `append` is atomic in CPython and `maxlen`
    keeps it bounded so a long session can't OOM).

    Reachability is the caller's problem — Sonzai's dispatcher
    (`webhook/dispatcher.go`) POSTs from the cloud, so 127.0.0.1 is not
    reachable without a tunnel (ngrok / cloudflared). The UI surfaces
    the local URL and tells the user how to expose it.
    """

    server: socketserver.TCPServer | None = None
    thread: threading.Thread | None = None
    port: int = 0
    deliveries: "deque[dict[str, Any]]" = field(
        default_factory=lambda: deque(maxlen=LOCAL_RECEIVER_MAX_DELIVERIES)
    )

    @property
    def running(self) -> bool:
        return self.server is not None

    @property
    def local_url(self) -> str:
        return f"http://127.0.0.1:{self.port}" if self.port else ""


def _pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _make_receiver_handler(
    deliveries: "deque[dict[str, Any]]",
) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0") or 0)
            body = self.rfile.read(length) if length else b""
            sig = (
                self.headers.get("Sonzai-Signature")
                or self.headers.get("sonzai-signature")
                or ""
            )
            deliveries.append(
                {
                    "path": self.path,
                    "signature": sig,
                    "body": body[:LOCAL_RECEIVER_BODY_PREVIEW_BYTES],
                    "body_len": len(body),
                    "ts": time.time(),
                }
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        def log_message(self, *_a: Any, **_k: Any) -> None:  # silence stderr
            return

    return Handler


def start_local_receiver() -> LocalReceiver:
    port = _pick_free_port()
    state = LocalReceiver(port=port)
    handler = _make_receiver_handler(state.deliveries)
    state.server = _ReuseAddrServer(("127.0.0.1", port), handler)
    state.thread = threading.Thread(
        target=state.server.serve_forever, daemon=True, name=f"sonzai-webhook-receiver-{port}"
    )
    state.thread.start()
    return state


def stop_local_receiver(state: LocalReceiver) -> None:
    if state.server is None:
        return
    # shutdown() blocks until serve_forever returns; server_close() releases
    # the socket so the port is immediately reusable.
    state.server.shutdown()
    state.server.server_close()
    state.server = None
    state.thread = None


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
    # Mood label that was in effect at the moment THIS turn was generated.
    # Rendered next to assistant replies so it's obvious which mood drove
    # which reply — kills the "I changed the mood but the reply is wrong"
    # confusion when the user clicked Apply AFTER the reply landed.
    mood_label: str | None = None


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
    # Previous snapshots so the steering UI can render +/- deltas next to each
    # current value. Captured immediately before mood/big5 are overwritten.
    prev_mood: dict[str, float] | None = None
    prev_big5: dict[str, float] | None = None


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
    ss.setdefault("local_receiver", None)  # LocalReceiver | None — populated when Start clicked

    # Steering: sliders track the live backend value by default. Picking a
    # preset or dragging a slider flips tracking off; "Resume" turns it back
    # on. Default slider values are neutral so first paint isn't all-zero.
    ss.setdefault("track_mood", True)
    ss.setdefault("track_big5", True)
    for dim in ("valence", "arousal", "tension", "affiliation"):
        ss.setdefault(f"mood_slider_{dim}", 50.0)
    for trait in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"):
        ss.setdefault(f"big5_slider_{trait}", 50.0)


def push_banner(kind: str, text: str) -> None:
    st.session_state.banners.append({"kind": kind, "text": text, "ts": time.time()})
    st.session_state.banners = st.session_state.banners[-4:]


# ---------------------------------------------------------------------------
# Sonzai context -> system instructions
# ---------------------------------------------------------------------------


def build_instructions(ctx: dict[str, Any], agent_name: str = "") -> str:
    """Return the system prompt for the OpenAI Agents SDK.

    The platform's /context endpoint now returns a fully-rendered behavioral
    `system_prompt` (persona + Big5 traits as behavior phrases + mood as a
    'RESPOND AS X' directive + relationship + facts + …) — SDK consumers
    should paste it as-is instead of stitching structured fields in their
    own language. We honour that contract here.

    The legacy stitching path remains as a fallback for older platform
    builds that don't emit `system_prompt` yet, so the demo doesn't break
    against a stale backend.
    """
    rendered = ctx.get("system_prompt")
    if isinstance(rendered, str) and rendered.strip():
        return rendered

    # Fallback for old platforms — minimal, no mood-to-tone translation
    # (the new path does this server-side; we don't want to drift).
    parts: list[str] = []
    name = agent_name or "Companion"
    persona = ctx.get("personality_prompt") or ctx.get("bio")
    parts.append(f"You are {name}. {persona}" if persona else f"You are {name}.")
    mood = ctx.get("current_mood")
    if isinstance(mood, dict) and mood.get("label"):
        parts.append(f"Current mood: {mood['label']}.")
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


def fetch_current_mood(client: Sonzai, agent_id: str, user_id: str) -> dict[str, float] | None:
    """Absolute mood state on the 0-100 scale via `agents.get_mood`.

    Distinct from `turn.mood`, which session.turn returns as a per-turn delta
    (~-1..+1 range). The sliders / gauges want the absolute current value, so
    we fetch from the dedicated endpoint.
    """
    try:
        resp = client.agents.get_mood(agent_id, user_id=user_id)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"get_mood failed: {err}")
        return None
    m = getattr(resp, "mood", None)
    if m is None:
        return None
    out: dict[str, float] = {}
    for k in ("valence", "arousal", "tension", "affiliation"):
        v = getattr(m, k, None)
        if v is not None:
            # Clamp defensively — backend guarantees [0, 100] but a stale row
            # or migration glitch shouldn't crash the slider.
            out[k] = max(0.0, min(100.0, float(v)))
    return out or None


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
        new_mood = fetch_current_mood(client, agent_id, user_id)
        if new_mood is not None and panel.mood:
            panel.prev_mood = dict(panel.mood)
        if new_mood is not None:
            panel.mood = new_mood
        new_big5 = fetch_personality_big5(client, agent_id)
        if new_big5 is not None and panel.big5:
            panel.prev_big5 = dict(panel.big5)
        panel.big5 = new_big5
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


def _disable_mood_tracking() -> None:
    """Slider on_change handler — user grabbed a slider, freeze auto-sync."""
    st.session_state["track_mood"] = False


def _disable_big5_tracking() -> None:
    st.session_state["track_big5"] = False


def _on_mood_preset_pick() -> None:
    """Selectbox on_change — load preset values into sliders + freeze tracking."""
    preset = st.session_state.get("mood_preset")
    if preset and preset in MOOD_PRESETS:
        for k, v in MOOD_PRESETS[preset].items():
            st.session_state[f"mood_slider_{k}"] = float(v)
        st.session_state["track_mood"] = False


def _on_big5_preset_pick() -> None:
    preset = st.session_state.get("big5_preset")
    if preset and preset in BIG5_PRESETS:
        for k, v in BIG5_PRESETS[preset].items():
            st.session_state[f"big5_slider_{k}"] = float(v)
        st.session_state["track_big5"] = False


def _delta_str(current: float, prev: float | None) -> str:
    """' (+5)' / ' (−3)' / ''  — empty when delta is tiny so it doesn't shout."""
    if prev is None:
        return ""
    d = current - prev
    if abs(d) < 0.5:
        return ""
    return f" ({d:+.0f})"


def render_mood_section(client: Sonzai, ss: Any) -> None:
    """Mood gauges merged with override sliders.

    When `track_mood` is on (default), each fragment heartbeat writes the
    current backend mood into the slider session_state — so the sliders
    visibly animate as the agent's mood drifts. Dragging a slider or
    picking a preset flips tracking off and freezes the sliders at the
    chosen values; "Apply" POSTs them and re-enables tracking so you can
    watch the override decay over subsequent turns.
    """
    panel: StatePanel = ss.panel
    track = st.session_state.get("track_mood", True)

    # Sanitize any stale slider state (defends against an older app version
    # that wrote a delta like -0.9 into session_state). Always idempotent.
    for k in ("valence", "arousal", "tension", "affiliation"):
        key = f"mood_slider_{k}"
        if key in st.session_state:
            st.session_state[key] = max(0.0, min(100.0, float(st.session_state[key])))

    # === Live mirror: backend → slider state, before slider widgets render. ===
    if track and panel.mood:
        for k in ("valence", "arousal", "tension", "affiliation"):
            v = panel.mood.get(k)
            if v is not None:
                st.session_state[f"mood_slider_{k}"] = max(0.0, min(100.0, float(v)))

    badge = "🔄 tracking" if track else "✏️ editing"
    st.markdown(f"**Mood** &nbsp; <span style='font-size:0.8em;opacity:0.7'>{badge}</span>", unsafe_allow_html=True)
    if panel.mood:
        prev = panel.prev_mood or {}
        cur = panel.mood
        st.caption(
            "Current → "
            f"V {cur.get('valence', 0):.0f}{_delta_str(cur.get('valence', 0), prev.get('valence'))} · "
            f"A {cur.get('arousal', 0):.0f}{_delta_str(cur.get('arousal', 0), prev.get('arousal'))} · "
            f"T {cur.get('tension', 0):.0f}{_delta_str(cur.get('tension', 0), prev.get('tension'))} · "
            f"Af {cur.get('affiliation', 0):.0f}{_delta_str(cur.get('affiliation', 0), prev.get('affiliation'))}"
        )
    else:
        st.caption("Current → (no mood yet — send a message)")

    preset_col, resume_col = st.columns([3, 1])
    with preset_col:
        st.selectbox(
            "Mood preset",
            options=list(MOOD_PRESETS.keys()),
            index=0,
            key="mood_preset",
            label_visibility="collapsed",
            on_change=_on_mood_preset_pick,
        )
    with resume_col:
        if st.button("↺ Track", key="resume_mood", disabled=track, use_container_width=True, help="Resume auto-sync to live values"):
            st.session_state["track_mood"] = True

    cols = st.columns(2)
    with cols[0]:
        st.slider("Valence", 0.0, 100.0, step=1.0, key="mood_slider_valence", on_change=_disable_mood_tracking)
        st.slider("Tension", 0.0, 100.0, step=1.0, key="mood_slider_tension", on_change=_disable_mood_tracking)
    with cols[1]:
        st.slider("Arousal", 0.0, 100.0, step=1.0, key="mood_slider_arousal", on_change=_disable_mood_tracking)
        st.slider("Affiliation", 0.0, 100.0, step=1.0, key="mood_slider_affiliation", on_change=_disable_mood_tracking)

    if st.button("Apply mood override", type="primary", use_container_width=True, key="apply_mood", disabled=track, help="Freeze a slider first (drag or pick a preset) to enable"):
        try:
            valence = float(st.session_state["mood_slider_valence"])
            arousal = float(st.session_state["mood_slider_arousal"])
            tension = float(st.session_state["mood_slider_tension"])
            affiliation = float(st.session_state["mood_slider_affiliation"])
            resp = client.agents.update_mood(
                ss.agent_id,
                valence=valence,
                arousal=arousal,
                tension=tension,
                affiliation=affiliation,
                user_id=ss.user_id,
            )
            # Snapshot prev BEFORE we overwrite, so deltas show the jump.
            if panel.mood:
                panel.prev_mood = dict(panel.mood)
            panel.mood = {"valence": valence, "arousal": arousal, "tension": tension, "affiliation": affiliation}
            label = getattr(resp.mood, "label", "") if getattr(resp, "mood", None) else ""
            push_banner("success", f"Mood overridden → {label or 'applied'}. Resuming live tracking.")
            # Re-enable tracking so the user can watch the override drift over subsequent turns.
            st.session_state["track_mood"] = True
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"update_mood failed: {err}")


def render_big5_section(client: Sonzai, ss: Any) -> None:
    """Big5 bars merged with override sliders. Same tracking pattern as mood."""
    panel: StatePanel = ss.panel
    track = st.session_state.get("track_big5", True)

    # Live mirror: panel.big5 stores fractions (0-1); sliders use 0-100.
    if track and panel.big5:
        for k in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"):
            v = panel.big5.get(k)
            if v is not None:
                st.session_state[f"big5_slider_{k}"] = float(v) * 100.0

    badge = "🔄 tracking" if track else "✏️ editing"
    st.markdown(f"**Personality (Big5)** &nbsp; <span style='font-size:0.8em;opacity:0.7'>{badge}</span>", unsafe_allow_html=True)
    if panel.big5:
        prev = panel.prev_big5 or {}
        cur = panel.big5
        st.caption(
            "Current → "
            f"O {cur.get('openness', 0) * 100:.0f}{_delta_str(cur.get('openness', 0) * 100, (prev.get('openness') or 0) * 100 if 'openness' in prev else None)} · "
            f"C {cur.get('conscientiousness', 0) * 100:.0f}{_delta_str(cur.get('conscientiousness', 0) * 100, (prev.get('conscientiousness') or 0) * 100 if 'conscientiousness' in prev else None)} · "
            f"E {cur.get('extraversion', 0) * 100:.0f}{_delta_str(cur.get('extraversion', 0) * 100, (prev.get('extraversion') or 0) * 100 if 'extraversion' in prev else None)} · "
            f"A {cur.get('agreeableness', 0) * 100:.0f}{_delta_str(cur.get('agreeableness', 0) * 100, (prev.get('agreeableness') or 0) * 100 if 'agreeableness' in prev else None)} · "
            f"N {cur.get('neuroticism', 0) * 100:.0f}{_delta_str(cur.get('neuroticism', 0) * 100, (prev.get('neuroticism') or 0) * 100 if 'neuroticism' in prev else None)}"
        )
    else:
        st.caption("Current → (Big5 not extracted yet — give it a few turns)")

    preset_col, resume_col = st.columns([3, 1])
    with preset_col:
        st.selectbox(
            "Big5 preset",
            options=list(BIG5_PRESETS.keys()),
            index=0,
            key="big5_preset",
            label_visibility="collapsed",
            on_change=_on_big5_preset_pick,
        )
    with resume_col:
        if st.button("↺ Track", key="resume_big5", disabled=track, use_container_width=True, help="Resume auto-sync to live values"):
            st.session_state["track_big5"] = True

    cols = st.columns(2)
    with cols[0]:
        st.slider("Openness", 0.0, 100.0, step=1.0, key="big5_slider_openness", on_change=_disable_big5_tracking)
        st.slider("Extraversion", 0.0, 100.0, step=1.0, key="big5_slider_extraversion", on_change=_disable_big5_tracking)
        st.slider("Neuroticism", 0.0, 100.0, step=1.0, key="big5_slider_neuroticism", on_change=_disable_big5_tracking)
    with cols[1]:
        st.slider("Conscientiousness", 0.0, 100.0, step=1.0, key="big5_slider_conscientiousness", on_change=_disable_big5_tracking)
        st.slider("Agreeableness", 0.0, 100.0, step=1.0, key="big5_slider_agreeableness", on_change=_disable_big5_tracking)

    if st.button("Apply personality override", type="primary", use_container_width=True, key="apply_big5", disabled=track, help="Freeze a slider first (drag or pick a preset) to enable"):
        try:
            big5 = {k: float(st.session_state[f"big5_slider_{k}"]) for k in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism")}
            client.agents.personality.update(
                ss.agent_id,
                big5=big5,
                assessment_method="manual_override",
            )
            if panel.big5:
                panel.prev_big5 = dict(panel.big5)
            panel.big5 = {k: v / 100.0 for k, v in big5.items()}
            push_banner("success", "Big5 overridden. Resuming live tracking.")
            st.session_state["track_big5"] = True
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"personality.update failed: {err}")


def render_session_controls(client: Sonzai, ss: Any) -> None:
    """End the current Sonzai session and immediately open a new one,
    blocking on the server-side consolidation/extraction pipeline so the
    right-pane state reflects the post-session-end snapshot.

    Backend `session.end(wait=True)` runs the full CE pipeline synchronously:
    user-personality overlay updates, mood baseline consolidation (L3→L2
    EMA), atomic-fact extraction, diary entry generation, constellation
    extraction. We refresh the panel inline so the user sees newly-extracted
    facts / Big5 drift / etc. without waiting on the 3s heartbeat.

    Local `ss.messages` is preserved — the chat history scroll stays put.
    """
    st.markdown("**Session controls**")
    st.caption(
        "Run the server-side CE pipeline (extraction, diary, consolidation, "
        "personality drift) and open a fresh session in one click. The chat "
        "history above is preserved — play around freely."
    )
    cols = st.columns(2)
    with cols[0]:
        if st.button(
            "🔄 End & new session",
            type="primary",
            use_container_width=True,
            disabled=ss.session is None,
            key="end_and_new_session_btn",
            help="Calls session.end, polls until extracted facts appear, refreshes the panel, then reopens a fresh session.",
        ):
            old_sid = ss.session_id
            old_session = ss.session
            facts_before = len(ss.panel.facts or [])

            with st.spinner("Ending session — running extraction pipeline (5–30s)…"):
                try:
                    # Platform >=1.5.5: wait=True blocks until per-turn extraction
                    # workers drain (CountInflightForSession). Facts are queryable
                    # the moment this call returns — no more polling needed.
                    old_session.end(wait=True)
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"session.end failed (non-fatal): {err}")
                ss.session = None
                ss.session_id = ""

                # Single inline refresh — extraction already landed server-side.
                _do_refresh(
                    client, ss.panel, ss.agent_id, ss.user_id,
                    ss.project_id, ss.webhook_event_type,
                )
                # Reopen so the next message has a session to use.
                try:
                    start_chat_session(client, ss)
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"could not reopen session: {err}")

            new_count = len(ss.panel.facts or [])
            delta = new_count - facts_before
            push_banner(
                "success",
                f"Session `{old_sid[:12]}…` ended → "
                f"{('+' + str(delta)) if delta > 0 else 'no new'} facts extracted → "
                f"new session `{ss.session_id[:12] if ss.session_id else '?'}…` started.",
            )
    with cols[1]:
        if st.button(
            "Force consolidation (25h)",
            use_container_width=True,
            key="force_consolidation_btn",
            help="Advances simulated time to fire daily workers — diary, deeper consolidation.",
        ):
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
                schedule_background_refresh(client, ss)
            except Exception as err:  # noqa: BLE001
                push_banner("warning", f"advance-time failed: {err}")

    last = ss.panel.last_consolidation
    if last:
        with st.expander("Last consolidation result", expanded=False):
            st.json(last)


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


def _render_local_receiver_section(ss: Any) -> None:
    """Start/stop an in-process HTTP receiver for webhook deliveries.

    The receiver itself can't fix the 404s seen in `Recent webhook
    deliveries` — Sonzai's dispatcher POSTs from the cloud and can't
    reach 127.0.0.1 directly. The flow is:

      1. Start receiver here → get http://127.0.0.1:PORT
      2. Expose with `ngrok http PORT` (or cloudflared) → public URL
      3. Paste the public URL into the Webhook URL field below
      4. Register, then trigger an event

    Deliveries that land in the receiver appear under
    "Recently received POSTs" with signature + body preview, which is
    the side the SDK's `list_delivery_attempts_for_project` can't show
    (it only knows what the backend sent + the status code received).
    """
    receiver: LocalReceiver | None = ss.get("local_receiver")
    with st.expander(
        "Local receiver", expanded=bool(receiver and receiver.running)
    ):
        if receiver and receiver.running:
            cols = st.columns([3, 1])
            with cols[0]:
                st.code(receiver.local_url, language="text")
                st.caption(
                    "Expose this with a tunnel and paste the public URL into "
                    "*Webhook URL* below. Examples:\n"
                    f"`ngrok http {receiver.port}`  ·  "
                    f"`cloudflared tunnel --url http://localhost:{receiver.port}`"
                )
            with cols[1]:
                if st.button("Stop", use_container_width=True, key="local_recv_stop"):
                    stop_local_receiver(receiver)
                    ss.local_receiver = None
                    push_banner("success", "Local receiver stopped.")
                    st.rerun()
                if st.button(
                    "Refresh", use_container_width=True, key="local_recv_refresh"
                ):
                    st.rerun()

            st.markdown("_Recently received POSTs:_")
            items = list(receiver.deliveries)
            if not items:
                st.caption(
                    "_Nothing received yet. Sonzai will POST here once your "
                    "tunnel forwards traffic and the registered URL above "
                    "points at it._"
                )
            else:
                # Newest first.
                for d in reversed(items[-5:]):
                    ts = datetime.fromtimestamp(d["ts"], tz=timezone.utc).isoformat(
                        timespec="seconds"
                    )
                    sig_badge = "🔏" if d["signature"] else "—"
                    st.markdown(
                        f"`POST {d['path']}` · {sig_badge} · "
                        f"{d['body_len']}B · {ts}"
                    )
                    body_preview = d["body"]
                    try:
                        parsed = json.loads(body_preview.decode("utf-8"))
                        st.code(
                            json.dumps(parsed, indent=2, ensure_ascii=False)[:1500],
                            language="json",
                        )
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        st.code(repr(body_preview[:500]), language="text")
        else:
            st.caption(
                "Spawns an HTTP receiver on 127.0.0.1 inside this Streamlit "
                "process. You still need a public tunnel (ngrok / "
                "cloudflared) to make it reachable from Sonzai's backend — "
                "this just gives you the local target."
            )
            if st.button(
                "Start receiver",
                type="primary",
                use_container_width=True,
                key="local_recv_start",
            ):
                try:
                    ss.local_receiver = start_local_receiver()
                    push_banner(
                        "success",
                        f"Local receiver listening on {ss.local_receiver.local_url}",
                    )
                    st.rerun()
                except OSError as err:
                    push_banner("warning", f"Failed to start receiver: {err}")


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

    _render_local_receiver_section(ss)

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
    "Anxious":   {"valence": 30, "arousal": 75, "tension": 55, "affiliation": 45},
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

    render_mood_section(client, ss)
    st.divider()
    render_big5_section(client, ss)
    st.divider()
    render_facts(panel)
    st.divider()
    render_inventory(panel)
    st.divider()
    render_constellation(panel)
    st.divider()
    render_session_controls(client, ss)
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
                if turn.role == "assistant" and turn.mood_label:
                    st.caption(f"_mood: {turn.mood_label}_")

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

    # Snapshot the mood label that the prompt was built from, so we can
    # display it next to the reply. Lets the user verify which override
    # was in effect for which reply at a glance.
    turn_mood_label = (ctx.get("current_mood") or {}).get("label", "") if isinstance(ctx, dict) else ""

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
        if turn_mood_label:
            st.caption(f"_mood: {turn_mood_label}_")

    ss.messages.append(ChatTurn(role="assistant", content=reply, mood_label=turn_mood_label))

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
        # turn.mood is a per-turn DELTA (≈ -1..+1) — not what the gauges
        # want. Fetch the absolute 0-100 state via get_mood and use that.
        new_mood = fetch_current_mood(client, ss.agent_id, ss.user_id)
        if new_mood is not None:
            if ss.panel.mood:
                ss.panel.prev_mood = dict(ss.panel.mood)
            ss.panel.mood = new_mood
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
        render_state_panel_live()


if __name__ == "__main__":
    main()
