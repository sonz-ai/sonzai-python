"""Personality Shift Demo — Streamlit + sonzai-python.

Create an agent, chat with it, then shift its personality between sessions
via sliders (or one-click presets). The next session reflects the new Big5
because the platform re-derives Dimensions on every PUT.

Run:
    cd demos/personality_shift
    pip install -r requirements.txt
    streamlit run app.py

Env (optional — the sidebar also lets you enter these):
    SONZAI_API_KEY    your platform API key
"""

from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass, field

import streamlit as st

try:
    from sonzai import Sonzai
except ImportError as err:  # pragma: no cover
    st.error(
        "The `sonzai` package is not installed. From the repo root: "
        "`pip install -e .` (to use the local SDK) or `pip install sonzai`."
    )
    raise SystemExit(1) from err

from presets import PRESETS, Big5, Preset


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------


@dataclass
class ChatTurn:
    role: str  # "user" | "assistant"
    content: str
    session_number: int = 1


@dataclass
class SessionEntry:
    number: int
    session_id: str
    big5_at_start: dict[str, float]
    messages: list[ChatTurn] = field(default_factory=list)
    ended: bool = False


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("client", None)
    ss.setdefault("api_key", os.environ.get("SONZAI_API_KEY", ""))
    ss.setdefault("connected", False)

    # Agent + identity
    ss.setdefault("agent_id", "")
    ss.setdefault("agent_name", "")
    ss.setdefault("user_id", f"demo-user-{uuid.uuid4().hex[:8]}")
    ss.setdefault("instance_id", f"demo-inst-{uuid.uuid4().hex[:8]}")

    # Personality state
    ss.setdefault("baseline_big5", None)  # dict: the Big5 we snapshotted at connect
    ss.setdefault("current_big5", None)  # dict: the actual Big5 in production right now
    ss.setdefault("current_dimensions", None)
    ss.setdefault("primary_traits", [])
    # Slider values — only applied on an explicit click
    ss.setdefault("pending_big5", None)

    # Sessions
    ss.setdefault("sessions", [])  # list[SessionEntry], oldest first
    ss.setdefault("active_session_index", -1)  # index into sessions
    ss.setdefault("between_sessions", False)  # True when the active session has ended and the next hasn't started

    # Toast-style messages
    ss.setdefault("banners", [])  # list[dict{kind, text}]


def active_session() -> SessionEntry | None:
    ss = st.session_state
    if ss.active_session_index < 0 or ss.active_session_index >= len(ss.sessions):
        return None
    return ss.sessions[ss.active_session_index]


def push_banner(kind: str, text: str) -> None:
    st.session_state.banners.append({"kind": kind, "text": text, "ts": time.time()})
    st.session_state.banners = st.session_state.banners[-4:]


# ---------------------------------------------------------------------------
# Backend helpers
# ---------------------------------------------------------------------------


def get_client(api_key: str) -> Sonzai:
    return Sonzai(api_key=api_key)


def fetch_personality(client: Sonzai, agent_id: str) -> tuple[dict, dict, list[str]]:
    resp = client.agents.personality.get(agent_id)
    p = resp.profile
    big5 = {
        "openness": p.big5.openness.score,
        "conscientiousness": p.big5.conscientiousness.score,
        "extraversion": p.big5.extraversion.score,
        "agreeableness": p.big5.agreeableness.score,
        "neuroticism": p.big5.neuroticism.score,
    }
    dims = p.dimensions.model_dump() if hasattr(p.dimensions, "model_dump") else dict(p.dimensions or {})
    return big5, dims, list(p.primary_traits or [])


def apply_big5(client: Sonzai, agent_id: str, big5: dict[str, float], label: str) -> None:
    client.agents.personality.update(agent_id=agent_id, big5=big5)
    new_big5, new_dims, traits = fetch_personality(client, agent_id)
    st.session_state.current_big5 = new_big5
    st.session_state.current_dimensions = new_dims
    st.session_state.primary_traits = traits
    st.session_state.pending_big5 = dict(new_big5)  # sliders snap to reality
    push_banner("success", f"Applied '{label}'. The next session will use this personality.")


def start_session(client: Sonzai, agent_id: str) -> None:  # noqa: ARG001
    ss = st.session_state
    next_number = len(ss.sessions) + 1
    session_id = f"demo-session-{ss.user_id}-s{next_number}-{uuid.uuid4().hex[:6]}"
    big5_snapshot = dict(ss.current_big5 or {})
    entry = SessionEntry(number=next_number, session_id=session_id, big5_at_start=big5_snapshot)
    ss.sessions.append(entry)
    ss.active_session_index = len(ss.sessions) - 1
    ss.between_sessions = False


def end_session(client: Sonzai, agent_id: str) -> None:
    ss = st.session_state
    s = active_session()
    if s is None or s.ended:
        return
    msgs_for_end = [{"role": m.role, "content": m.content} for m in s.messages]
    try:
        client.agents.sessions.end(
            agent_id,
            user_id=ss.user_id,
            session_id=s.session_id,
            instance_id=ss.instance_id,
            total_messages=len(msgs_for_end),
            duration_seconds=max(30, len(msgs_for_end) * 20),
            messages=msgs_for_end or None,
        )
    except Exception as err:  # noqa: BLE001
        # Session-end triggers server-side consolidation jobs; a failure
        # shouldn't block the demo UX. Surface it but let the user keep going.
        push_banner("warning", f"sessions.end failed (non-fatal): {err}")
    s.ended = True
    ss.between_sessions = True
    push_banner(
        "info",
        f"Session {s.number} closed. Adjust the sliders, then press 'Start next session'.",
    )


def restore_baseline(client: Sonzai, agent_id: str) -> None:
    baseline = st.session_state.baseline_big5
    if not baseline:
        push_banner("warning", "No baseline snapshot — nothing to restore.")
        return
    apply_big5(client, agent_id, dict(baseline), "Baseline")


# ---------------------------------------------------------------------------
# Sidebar — agent config + creation
# ---------------------------------------------------------------------------


def render_sidebar() -> None:
    ss = st.session_state
    with st.sidebar:
        st.header("Agent setup")
        api_key = st.text_input(
            "API key",
            value=ss.api_key,
            type="password",
            help="Get one at platform.sonz.ai. Defaults to $SONZAI_API_KEY.",
        )
        ss.api_key = api_key

        if ss.connected:
            st.success(f"Connected: {ss.agent_name or ss.agent_id[:8]}…")
            if st.button("Disconnect"):
                ss.connected = False
                ss.client = None
                ss.sessions = []
                ss.active_session_index = -1
                ss.between_sessions = False
                ss.agent_id = ""
                ss.agent_name = ""
                ss.baseline_big5 = None
                ss.current_big5 = None
                ss.pending_big5 = None
                st.rerun()
            return

        mode = st.radio("Agent source", ["Create new", "Use existing"], horizontal=True)

        if mode == "Create new":
            default_name = f"Demo Agent {uuid.uuid4().hex[:4]}"
            name = st.text_input("Agent name", value=default_name)
            description = st.text_area(
                "Personality prompt",
                value=(
                    "You are a curious, direct software engineer in your late 20s who "
                    "loves building things and speaks casually. You answer in 1-3 short "
                    "sentences unless asked to elaborate."
                ),
                height=130,
                help="Goes into the agent's system prompt. Keep it concrete and short.",
            )
            gender = st.selectbox("Gender", ["female", "male", "nonbinary"], index=0)
            can_create = bool(api_key and name and description)
            if st.button("Create agent", type="primary", disabled=not can_create):
                try:
                    client = get_client(api_key)
                    with st.spinner("Generating + creating agent (10-30s, LLM is picking the Big5)…"):
                        # LLM-generated personality — takes the description and
                        # expands it into Big5 scores, speech patterns, etc.
                        # Sliders start at whatever the LLM chose; user can
                        # still drag to any personality from there.
                        result = client.agents.generation.generate_and_create(
                            name=name,
                            description=description,
                            gender=gender,
                        )
                    agent_id = _extract_agent_id(result)
                    if not agent_id:
                        st.error(f"Agent creation returned no agent_id. Raw: {result}")
                        return
                    _connect(client, agent_id, agent_name=name)
                    st.rerun()
                except Exception as err:  # noqa: BLE001
                    st.error(
                        f"Create failed: {err}\n\n"
                        "Tip: if the platform's generate-character path is "
                        "unhealthy, switch to 'Use existing' and paste an "
                        "agent UUID instead."
                    )
        else:
            existing_id = st.text_input("Agent ID (UUID)", help="Paste an existing agent's UUID.")
            if st.button("Connect", type="primary", disabled=not (api_key and existing_id)):
                try:
                    client = get_client(api_key)
                    _connect(client, existing_id, agent_name="")
                    st.rerun()
                except Exception as err:  # noqa: BLE001
                    st.error(f"Connect failed: {err}")

        st.divider()
        st.caption(
            "The demo snapshots the agent's Big5 on connect and offers a one-click "
            "Restore from the right panel. Closing the browser without restoring "
            "leaves the agent in the last applied state."
        )


def _connect(client: Sonzai, agent_id: str, agent_name: str) -> None:
    big5, dims, traits = fetch_personality(client, agent_id)
    ss = st.session_state
    ss.client = client
    ss.agent_id = agent_id
    ss.agent_name = agent_name or ""
    ss.baseline_big5 = dict(big5)
    ss.current_big5 = dict(big5)
    ss.current_dimensions = dims
    ss.primary_traits = traits
    ss.pending_big5 = dict(big5)
    ss.connected = True
    ss.sessions = []
    ss.active_session_index = -1
    ss.between_sessions = True  # start between-sessions so user sees controls first
    push_banner(
        "success",
        "Baseline captured. Optionally shift personality via the sliders, then 'Start session 1'.",
    )


# ---------------------------------------------------------------------------
# Chat panel
# ---------------------------------------------------------------------------


def render_chat_panel() -> None:
    ss = st.session_state
    client: Sonzai = ss.client
    agent_id: str = ss.agent_id

    st.subheader("Chat")

    # Top bar: session state + end/start controls
    s = active_session()
    if ss.between_sessions:
        cols = st.columns([3, 2])
        with cols[0]:
            next_num = len(ss.sessions) + 1
            st.caption(
                f"No active session. Adjust personality on the right, then start session {next_num}."
            )
        with cols[1]:
            if st.button(
                f"Start session {next_num}",
                type="primary",
                use_container_width=True,
                key="start-session-btn",
            ):
                start_session(client, agent_id)
                st.rerun()
    else:
        assert s is not None
        cols = st.columns([3, 2])
        with cols[0]:
            st.caption(
                f"**Session {s.number}** active · `{s.session_id[-16:]}` · "
                f"A={s.big5_at_start.get('agreeableness', 0):.2f} "
                f"E={s.big5_at_start.get('extraversion', 0):.2f} "
                f"N={s.big5_at_start.get('neuroticism', 0):.2f}"
            )
        with cols[1]:
            if st.button(
                f"End session {s.number}",
                use_container_width=True,
                key="end-session-btn",
                help="Commits the session to the agent's memory. Personality sliders unlock after this.",
            ):
                end_session(client, agent_id)
                st.rerun()

    # History — all sessions, oldest first, with a separator between
    for sess in ss.sessions:
        st.markdown(
            f"<div style='margin:8px 0 4px 0;font-size:12px;color:#888;border-bottom:1px solid #333;'>"
            f"Session {sess.number} "
            f"(A={sess.big5_at_start.get('agreeableness', 0):.2f}, "
            f"E={sess.big5_at_start.get('extraversion', 0):.2f}, "
            f"N={sess.big5_at_start.get('neuroticism', 0):.2f})"
            f"</div>",
            unsafe_allow_html=True,
        )
        for turn in sess.messages:
            with st.chat_message(turn.role):
                st.write(turn.content)

    # Input
    if ss.between_sessions or s is None:
        st.chat_input("Start a session to begin chatting…", disabled=True)
        return

    prompt = st.chat_input(f"Message {ss.agent_name or 'the agent'}…")
    if not prompt:
        return

    s.messages.append(ChatTurn(role="user", content=prompt, session_number=s.number))
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        buf = ""
        try:
            stream = client.agents.chat(
                agent_id=agent_id,
                messages=[{"role": "user", "content": prompt}],
                user_id=ss.user_id,
                session_id=s.session_id,
                instance_id=ss.instance_id,
                stream=True,
            )
            for event in stream:
                delta = _extract_delta(event)
                if delta:
                    buf += delta
                    placeholder.markdown(buf)
        except Exception as err:  # noqa: BLE001
            placeholder.error(f"Chat failed: {err}")
            return

    s.messages.append(ChatTurn(role="assistant", content=buf, session_number=s.number))


def _extract_agent_id(result) -> str | None:
    """Pull an agent_id out of generate_and_create's forgiving return shape."""
    if result is None:
        return None
    # Object with attribute
    for attr in ("agent_id", "agentId", "id"):
        val = getattr(result, attr, None)
        if val:
            return str(val)
    # Dict
    if isinstance(result, dict):
        for key in ("agent_id", "agentId", "id"):
            if result.get(key):
                return str(result[key])
        # Some endpoints nest the agent under "agent" or "data"
        for wrapper in ("agent", "data", "created_agent"):
            nested = result.get(wrapper)
            if isinstance(nested, dict):
                for key in ("agent_id", "agentId", "id"):
                    if nested.get(key):
                        return str(nested[key])
    return None


def _extract_delta(event) -> str:
    choices = getattr(event, "choices", None)
    if not choices and isinstance(event, dict):
        choices = event.get("choices")
    if not choices:
        return ""
    first = choices[0]
    delta = getattr(first, "delta", None) if not isinstance(first, dict) else first.get("delta")
    if delta is None:
        return ""
    content = getattr(delta, "content", None) if not isinstance(delta, dict) else delta.get("content")
    return content or ""


# ---------------------------------------------------------------------------
# Personality panel — sliders + presets (only editable between sessions)
# ---------------------------------------------------------------------------

TRAIT_ORDER = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]


def render_personality_panel() -> None:
    ss = st.session_state
    client: Sonzai = ss.client
    agent_id: str = ss.agent_id

    st.subheader("Personality")

    # Banners
    for b in ss.banners[-4:]:
        if b["kind"] == "success":
            st.success(b["text"])
        elif b["kind"] == "warning":
            st.warning(b["text"])
        else:
            st.info(b["text"])

    editable = ss.between_sessions
    current = ss.current_big5 or {}
    baseline = ss.baseline_big5 or {}

    if not editable:
        st.caption("Personality is locked mid-session. End the session to shift between turns.")
    else:
        st.caption("Adjust Big5 with the sliders or pick a preset, then click **Apply**.")

    # Sliders / readonly bars
    with st.form("big5_form", clear_on_submit=False):
        values: dict[str, float] = {}
        for trait in TRAIT_ORDER:
            cur = float((ss.pending_big5 or current).get(trait, 0.5))
            if editable:
                values[trait] = st.slider(
                    trait,
                    min_value=0.0,
                    max_value=1.0,
                    value=cur,
                    step=0.05,
                    key=f"slider-{trait}",
                )
            else:
                st.progress(min(max(cur, 0.0), 1.0), text=f"{trait}: {cur:.2f}")
                values[trait] = cur
        submitted = st.form_submit_button(
            "Apply personality", type="primary", disabled=not editable, use_container_width=True
        )
        if submitted:
            try:
                apply_big5(client, agent_id, values, "Custom sliders")
                st.rerun()
            except Exception as err:  # noqa: BLE001
                push_banner("warning", f"Apply failed: {err}")
                st.rerun()

    # Baseline + current delta readout
    with st.expander("Current vs baseline", expanded=False):
        if baseline:
            for trait in TRAIT_ORDER:
                b = baseline.get(trait, 0.0)
                c = current.get(trait, b)
                delta = c - b
                sign = "▲" if delta > 0.005 else ("▼" if delta < -0.005 else "·")
                st.caption(f"{trait}: baseline {b:.2f} · current {c:.2f} · {sign} {delta:+.2f}")
        else:
            st.caption("No baseline yet.")

    # Derived Dimensions
    with st.expander("Derived Dimensions (from Big5)", expanded=False):
        dims = ss.current_dimensions or {}
        for k in sorted(dims.keys()):
            v = float(dims[k])
            st.progress(min(max(v, 0.0), 1.0), text=f"{k}: {v:.2f}")
        if ss.primary_traits:
            st.caption("Primary traits: " + ", ".join(ss.primary_traits))

    st.divider()
    st.markdown("**Presets** — one-click personality swap (applies immediately).")
    cols = st.columns(2)
    for i, preset in enumerate(PRESETS):
        col = cols[i % 2]
        with col:
            if st.button(
                preset.name,
                key=f"preset-{preset.name}",
                use_container_width=True,
                disabled=not editable,
                help=preset.description,
            ):
                try:
                    apply_big5(client, agent_id, preset.big5.as_dict(), preset.name)
                    st.rerun()
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"Apply failed: {err}")
                    st.rerun()

    st.divider()
    if st.button(
        "Restore to baseline",
        use_container_width=True,
        disabled=not editable,
        help="Revert Big5 to the values captured when you connected.",
    ):
        try:
            restore_baseline(client, agent_id)
            st.rerun()
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"Restore failed: {err}")
            st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="Personality Shift Demo", layout="wide")
    init_state()

    st.title("Personality Shift Demo")
    st.caption(
        "Create an agent, chat with it, then shift its personality between sessions "
        "using the sliders. The platform re-derives the agent's personality dimensions "
        "on every PUT, so the next session picks up the change automatically."
    )

    render_sidebar()

    if not st.session_state.connected:
        st.info("Pick an agent in the sidebar (create new or enter an existing ID) to begin.")
        return

    chat_col, personality_col = st.columns([3, 2], gap="large")
    with chat_col:
        render_chat_panel()
    with personality_col:
        render_personality_panel()


if __name__ == "__main__":
    main()
