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
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import streamlit as st

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
GEMINI_MODEL_PRIMARY = "gemini-3.1-flash-lite-preview"
GEMINI_MODEL_FALLBACK = "gemini-2.0-flash-exp"

GEMINI_OPENAI_COMPAT_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Hours to advance for "Force consolidation". 9h jumps past the 8h deferred
# consolidation gate; 25h triggers all daily workers. 25h is the safer choice.
FORCE_CONSOLIDATION_HOURS = 25.0

# Soft delay before polling personality / facts / inventory after a turn —
# Sonzai's deferred extraction usually lands within 5-15s.
POST_TURN_REFRESH_DELAY_S = 3.0


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
    big5: dict[str, float] | None = None  # 5 scores in 0..1
    facts: list[str] = field(default_factory=list)
    inventory: list[dict[str, Any]] = field(default_factory=list)
    constellation: dict[str, Any] | None = None  # raw {nodes, edges}
    last_extraction_id: str | None = None
    last_extraction_status: str | None = None
    last_consolidation: dict[str, Any] | None = None


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


def push_banner(kind: str, text: str) -> None:
    st.session_state.banners.append({"kind": kind, "text": text, "ts": time.time()})
    st.session_state.banners = st.session_state.banners[-4:]


# ---------------------------------------------------------------------------
# Sonzai context -> system instructions
# ---------------------------------------------------------------------------


def build_instructions(ctx: dict[str, Any], agent_name: str) -> str:
    """Render Sonzai's enriched context as an OpenAI-Agents system prompt."""
    parts: list[str] = []
    profile = ctx.get("profile") or {}
    name = profile.get("name") or agent_name or "Companion"
    parts.append(f"You are {name}, a helpful, curious companion.")

    big5 = profile.get("big5")
    if isinstance(big5, dict):
        traits = ", ".join(
            f"{k} {float(v.get('score', v) if isinstance(v, dict) else v):.2f}"
            for k, v in big5.items()
        )
        parts.append(f"Personality (Big5): {traits}.")

    speech = profile.get("speech_patterns")
    if isinstance(speech, list) and speech:
        parts.append("Speech patterns: " + "; ".join(str(s) for s in speech[:3]) + ".")

    behavioral = ctx.get("behavioral") or {}
    mood = behavioral.get("mood") or behavioral
    if isinstance(mood, dict) and any(k in mood for k in ("valence", "arousal", "tension")):
        parts.append(
            f"Current mood: valence={mood.get('valence', 0):+.2f}, "
            f"arousal={mood.get('arousal', 0):+.2f}, "
            f"tension={mood.get('tension', 0):+.2f}."
        )

    memory = ctx.get("memory") or {}
    facts = memory.get("facts") or memory.get("relevant_facts") or []
    if isinstance(facts, list) and facts:
        bullets = []
        for f in facts[:8]:
            text = f.get("text") if isinstance(f, dict) else str(f)
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


def fetch_personality_big5(client: Sonzai, agent_id: str) -> dict[str, float] | None:
    try:
        resp = client.agents.personality.get(agent_id)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"personality.get failed: {err}")
        return None
    p = resp.profile
    return {
        "openness": float(p.big5.openness.score),
        "conscientiousness": float(p.big5.conscientiousness.score),
        "extraversion": float(p.big5.extraversion.score),
        "agreeableness": float(p.big5.agreeableness.score),
        "neuroticism": float(p.big5.neuroticism.score),
    }


def fetch_recent_facts(client: Sonzai, agent_id: str, user_id: str, limit: int = 8) -> list[str]:
    """Pull recent facts via memory.list_all_facts (active facts for this pair)."""
    try:
        resp = client.agents.memory.list_all_facts(agent_id, user_id, limit=limit)
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"memory.list_all_facts failed: {err}")
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
        # Give the 5-15s deferred extraction a small head-start. The user
        # sees a spinner, and a re-poll on the next turn catches anything
        # that didn't land yet.
        time.sleep(POST_TURN_REFRESH_DELAY_S)

    panel: StatePanel = ss.panel
    panel.big5 = fetch_personality_big5(client, ss.agent_id)
    panel.facts = fetch_recent_facts(client, ss.agent_id, ss.user_id)
    panel.inventory = fetch_inventory(client, ss.agent_id, ss.user_id)
    panel.constellation = fetch_constellation(client, ss.agent_id, ss.user_id)


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
                ):
                    if k in ss:
                        del ss[k]
                st.rerun()
            return

        st.divider()
        st.subheader("Create new agent")
        default_name = f"Companion {uuid.uuid4().hex[:4]}"
        name = st.text_input("Agent name", value=default_name)
        description = st.text_area(
            "Description",
            value=(
                "A curious, warm, slightly nerdy companion who likes asking "
                "follow-up questions and remembers what the user shares."
            ),
            height=110,
        )
        gender = st.selectbox("Gender", ["nonbinary", "female", "male"], index=0)

        can_create = bool(ss.sonzai_key and ss.gemini_key and name and description)
        if st.button("Create agent + start session", type="primary", disabled=not can_create):
            try:
                client = Sonzai(api_key=ss.sonzai_key)
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
                start_chat_session(client, ss)
                # Initial right-panel snapshot (no extraction wait — nothing
                # has happened yet).
                refresh_right_panel(client, ss, wait_for_extraction=False)
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


def render_state_panel(client: Sonzai, ss: Any) -> None:
    panel: StatePanel = ss.panel
    st.subheader("Live state")
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


# ---------------------------------------------------------------------------
# Chat pane
# ---------------------------------------------------------------------------


def render_chat_pane(client: Sonzai, ss: Any) -> None:
    st.subheader("Chat")
    st.caption(
        "OpenAI Agents SDK runs the LLM via Gemini's OpenAI-compat endpoint. "
        "Sonzai supplies context and ingests the transcript."
    )

    # History
    for turn in ss.messages:
        with st.chat_message(turn.role):
            st.write(turn.content)

    # Optional image attachment — Gemini is multimodal, so we pass any URL the
    # user provides through to the Agents SDK as an `input_image` content
    # block. The text-bridging into Sonzai is documented in
    # `run_result_to_sonzai_messages`.
    image_url = st.text_input(
        "Attach image (URL)",
        value="",
        placeholder="https://… (jpg/png) — optional, sent to Gemini multimodally",
        key="attached_image_url",
        help=(
            "Paste a public image URL. Gemini will see the actual image; "
            "Sonzai gets a text marker `[User shared image: <url>]` so it can "
            "extract facts about what was shared."
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
        with st.chat_message("assistant"):
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

    with st.chat_message("assistant"):
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

    # 4) Re-poll the lagged state. We sleep ~3s first so deferred extraction
    #    has a chance to land — facts/Big5 are eventual, not immediate.
    with st.spinner("Refreshing personality / facts / inventory / constellation…"):
        refresh_right_panel(client, ss, wait_for_extraction=True)
    st.rerun()


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
        render_state_panel(st.session_state.client, st.session_state)


if __name__ == "__main__":
    main()
