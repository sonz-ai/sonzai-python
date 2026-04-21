"""Personality Shift Demo — Streamlit + sonzai-python.

Create an agent, chat with it, drag sliders in real time. The next turn
reflects the new Big5 because the platform re-derives Dimensions on every
PUT. Sessions auto-close every 10 messages, triggering CE consolidation
(advance-time).

Run:
    cd demos/personality_shift
    pip install -r requirements.txt
    streamlit run app.py

Env (optional — the sidebar also lets you enter these):
    SONZAI_API_KEY    your platform API key
"""

from __future__ import annotations

import os
import threading
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

from presets import PRESETS


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------


MESSAGES_PER_SESSION = 10  # assistant turns that trigger auto-consolidation
TRAIT_ORDER = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
BIG5_EPSILON = 0.02  # below this, slider wiggle is treated as "no change"


@dataclass
class ChatTurn:
    role: str  # "user" | "assistant" | "system_banner"
    content: str
    session_number: int = 1
    big5_at_turn: dict[str, float] | None = None


@dataclass
class SessionEntry:
    number: int
    session_id: str
    big5_at_start: dict[str, float]
    assistant_count: int = 0
    ended: bool = False
    consolidation_result: dict | None = None


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
    ss.setdefault("baseline_big5", None)    # captured on connect
    ss.setdefault("applied_big5", None)     # last-synced-to-backend values
    ss.setdefault("current_dimensions", None)
    ss.setdefault("primary_traits", [])
    # pending_big5 reflects the sliders' live value — may differ from applied
    # between an interaction and its PUT
    ss.setdefault("pending_big5", None)

    # Sessions
    ss.setdefault("messages", [])           # flat list of ChatTurn (all sessions)
    ss.setdefault("sessions", [])           # list[SessionEntry]
    ss.setdefault("current_session", None)  # active SessionEntry or None

    # Transient UI
    ss.setdefault("banners", [])            # [{kind,text,ts}]


def push_banner(kind: str, text: str) -> None:
    st.session_state.banners.append({"kind": kind, "text": text, "ts": time.time()})
    st.session_state.banners = st.session_state.banners[-5:]


def big5_diff(a: dict | None, b: dict | None) -> bool:
    """Return True iff a differs from b by more than BIG5_EPSILON on any trait."""
    if not a or not b:
        return a != b
    for trait in TRAIT_ORDER:
        if abs(float(a.get(trait, 0.0)) - float(b.get(trait, 0.0))) > BIG5_EPSILON:
            return True
    return False


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


def apply_big5(client: Sonzai, agent_id: str, big5: dict[str, float]) -> None:
    client.agents.personality.update(agent_id=agent_id, big5=big5)
    new_big5, new_dims, traits = fetch_personality(client, agent_id)
    st.session_state.applied_big5 = new_big5
    st.session_state.pending_big5 = dict(new_big5)
    st.session_state.current_dimensions = new_dims
    st.session_state.primary_traits = traits
    # Request that the next rerun reseed the slider widgets from applied_big5.
    # Streamlit forbids writing widget-keyed session_state after the widget
    # has rendered in the current run, so we can't do it here — we set a
    # flag instead and the top of render_personality_panel applies it before
    # the sliders instantiate.
    st.session_state.needs_slider_sync = True


def ensure_applied(client: Sonzai, agent_id: str) -> bool:
    """Flush any pending slider changes to the backend. Returns True if a PUT fired."""
    pending = st.session_state.pending_big5
    applied = st.session_state.applied_big5
    if not pending or not applied:
        return False
    if not big5_diff(pending, applied):
        return False
    delta = summarize_delta(applied, pending)
    apply_big5(client, agent_id, pending)
    push_banner("success", f"Personality updated {delta}. Next turn will reflect it.")
    return True


def summarize_delta(old: dict, new: dict) -> str:
    parts = []
    for trait in TRAIT_ORDER:
        d = new.get(trait, 0) - old.get(trait, 0)
        if abs(d) > BIG5_EPSILON:
            arrow = "↑" if d > 0 else "↓"
            parts.append(f"{trait[:3]} {arrow}{abs(d):.2f}")
    return "(" + ", ".join(parts) + ")" if parts else ""


def start_new_session() -> SessionEntry:
    ss = st.session_state
    next_number = len(ss.sessions) + 1
    session_id = f"demo-session-{ss.user_id}-s{next_number}-{uuid.uuid4().hex[:6]}"
    entry = SessionEntry(
        number=next_number,
        session_id=session_id,
        big5_at_start=dict(ss.applied_big5 or {}),
    )
    ss.sessions.append(entry)
    ss.current_session = entry
    return entry


def close_session_and_consolidate(client: Sonzai, agent_id: str, session: SessionEntry) -> None:
    """End the session server-side and kick off advance-time (best-effort, timeout-bounded)."""
    ss = st.session_state
    session.ended = True

    # Build transcript from this session's messages for the sessions.end call.
    msgs_for_end = [
        {"role": m.role, "content": m.content}
        for m in ss.messages
        if m.role in ("user", "assistant") and m.session_number == session.number
    ]

    try:
        client.agents.sessions.end(
            agent_id,
            user_id=ss.user_id,
            session_id=session.session_id,
            instance_id=ss.instance_id,
            total_messages=len(msgs_for_end),
            duration_seconds=max(30, len(msgs_for_end) * 20),
            messages=msgs_for_end or None,
        )
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"sessions.end failed (non-fatal): {err}")

    # Advance-time runs CE daily jobs (consolidation, diary, decay, etc.)
    # Cloudflare's edge times out at ~100s so we cap the client side at 25s
    # and let the server finish asynchronously if it's still working.
    result_holder: dict = {}

    def _advance() -> None:
        try:
            resp = client.workbench.advance_time(
                agent_id,
                ss.user_id,
                25.0,  # one full simulated day triggers the daily gates
                instance_id=ss.instance_id,
            )
            result_holder["resp"] = resp
        except Exception as err:  # noqa: BLE001
            result_holder["err"] = err

    t = threading.Thread(target=_advance, daemon=True)
    t.start()
    t.join(timeout=25.0)
    if t.is_alive():
        push_banner(
            "info",
            f"Session {session.number} consolidation still running in background "
            "(advance-time exceeded 25s client cap). Moving on.",
        )
        session.consolidation_result = {"status": "pending_in_background"}
    elif "err" in result_holder:
        push_banner("warning", f"advance-time failed (non-fatal): {result_holder['err']}")
        session.consolidation_result = {"status": "failed", "error": str(result_holder["err"])}
    else:
        resp = result_holder.get("resp")
        diary_count = getattr(resp, "diary_entries_created", 0) or 0
        days = getattr(resp, "days_processed", 1) or 1
        session.consolidation_result = {
            "status": "ok",
            "days_processed": days,
            "diary_entries": diary_count,
        }
        push_banner(
            "success",
            f"Session {session.number} consolidated — {days} day processed, "
            f"{diary_count} diary entries generated.",
        )

    # Refresh derived Dimensions — CE jobs may have mutated them via decay etc.
    try:
        new_big5, new_dims, traits = fetch_personality(client, agent_id)
        ss.applied_big5 = new_big5
        ss.pending_big5 = dict(new_big5)
        ss.current_dimensions = new_dims
        ss.primary_traits = traits
    except Exception as err:  # noqa: BLE001
        push_banner("warning", f"Could not refresh personality post-consolidation: {err}")

    # Record a banner turn so the chat scrollback shows the boundary.
    ss.messages.append(
        ChatTurn(
            role="system_banner",
            content=f"Session {session.number} completed. Running consolidation…",
            session_number=session.number,
        )
    )


def restore_baseline(client: Sonzai, agent_id: str) -> None:
    baseline = st.session_state.baseline_big5
    if not baseline:
        push_banner("warning", "No baseline snapshot — nothing to restore.")
        return
    apply_big5(client, agent_id, dict(baseline))
    push_banner("success", "Personality restored to the baseline captured on connect.")


# ---------------------------------------------------------------------------
# Connect flow
# ---------------------------------------------------------------------------


def _extract_agent_id(result) -> str | None:
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


def _connect(client: Sonzai, agent_id: str, agent_name: str) -> None:
    big5, dims, traits = fetch_personality(client, agent_id)
    ss = st.session_state
    ss.client = client
    ss.agent_id = agent_id
    ss.agent_name = agent_name or ""
    ss.baseline_big5 = dict(big5)
    ss.applied_big5 = dict(big5)
    ss.pending_big5 = dict(big5)
    ss.current_dimensions = dims
    ss.primary_traits = traits
    ss.connected = True
    ss.sessions = []
    ss.current_session = None
    ss.messages = []
    push_banner("success", "Connected. Baseline captured. Start chatting.")


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
                for k in (
                    "connected", "client", "agent_id", "agent_name",
                    "baseline_big5", "applied_big5", "pending_big5",
                    "current_dimensions", "primary_traits",
                    "sessions", "current_session", "messages",
                ):
                    if k in ss:
                        del ss[k]
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
            )
            gender = st.selectbox("Gender", ["female", "male", "nonbinary"], index=0)
            can_create = bool(api_key and name and description)
            if st.button("Create agent", type="primary", disabled=not can_create):
                try:
                    client = get_client(api_key)
                    with st.spinner("Generating + creating agent (5-15s)…"):
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
                    st.error(f"Create failed: {err}")
        else:
            existing_id = st.text_input("Agent ID (UUID)")
            if st.button("Connect", type="primary", disabled=not (api_key and existing_id)):
                try:
                    client = get_client(api_key)
                    _connect(client, existing_id, agent_name="")
                    st.rerun()
                except Exception as err:  # noqa: BLE001
                    st.error(f"Connect failed: {err}")

        st.divider()
        st.caption(
            "Slide traits in real time during a chat — the next turn reflects the shift. "
            "Every " f"{MESSAGES_PER_SESSION}" " messages triggers an automatic session close "
            "with CE consolidation (advance-time). Click Restore to revert."
        )


# ---------------------------------------------------------------------------
# Chat panel
# ---------------------------------------------------------------------------


def render_chat_panel() -> None:
    ss = st.session_state
    client: Sonzai = ss.client
    agent_id: str = ss.agent_id

    st.subheader("Chat")

    session_number = ss.current_session.number if ss.current_session else len(ss.sessions) + 1
    assistant_count = ss.current_session.assistant_count if ss.current_session else 0
    st.caption(
        f"**Session {session_number}** · "
        f"{assistant_count}/{MESSAGES_PER_SESSION} messages this session · "
        f"{len(ss.sessions)} session(s) completed total"
    )

    # Render history
    for turn in ss.messages:
        if turn.role == "system_banner":
            st.info(turn.content, icon=None)
            continue
        with st.chat_message(turn.role):
            st.write(turn.content)

    prompt = st.chat_input(f"Message {ss.agent_name or 'the agent'}…")
    if not prompt:
        return

    # Flush any pending slider changes BEFORE the turn so the LLM sees the
    # new personality.
    ensure_applied(client, agent_id)

    # Open a new session if there isn't one active.
    if ss.current_session is None or ss.current_session.ended:
        start_new_session()

    session = ss.current_session
    assert session is not None

    # Record user turn
    ss.messages.append(
        ChatTurn(
            role="user",
            content=prompt,
            session_number=session.number,
            big5_at_turn=dict(ss.applied_big5 or {}),
        )
    )
    with st.chat_message("user"):
        st.write(prompt)

    # Stream assistant reply
    with st.chat_message("assistant"):
        placeholder = st.empty()
        buf = ""
        try:
            stream = client.agents.chat(
                agent_id=agent_id,
                messages=[{"role": "user", "content": prompt}],
                user_id=ss.user_id,
                session_id=session.session_id,
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

    ss.messages.append(
        ChatTurn(
            role="assistant",
            content=buf,
            session_number=session.number,
            big5_at_turn=dict(ss.applied_big5 or {}),
        )
    )
    session.assistant_count += 1

    # Auto-consolidate when the session hits its message cap.
    if session.assistant_count >= MESSAGES_PER_SESSION:
        placeholder_consol = st.empty()
        placeholder_consol.info(
            f"Session {session.number} completed. Running consolidation…", icon=None
        )
        close_session_and_consolidate(client, agent_id, session)
        placeholder_consol.empty()
        ss.current_session = None  # next chat opens a fresh session
        st.rerun()
    else:
        # Refresh the session counter + any post-turn state.
        st.rerun()


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
# Personality panel — always live
# ---------------------------------------------------------------------------


def render_personality_panel() -> None:
    ss = st.session_state
    client: Sonzai = ss.client
    agent_id: str = ss.agent_id

    st.subheader("Personality")
    st.caption(
        "Slide to shift the agent's Big5. Changes apply immediately — the next "
        "chat turn will reflect the new personality."
    )

    # Apply any pending programmatic slider sync BEFORE the sliders render.
    # Streamlit disallows writing a widget's session_state key after the
    # widget has been instantiated in the current run.
    if ss.get("needs_slider_sync") and ss.applied_big5:
        for trait in TRAIT_ORDER:
            ss[f"slider-{trait}"] = float(ss.applied_big5.get(trait, 0.5))
        ss.needs_slider_sync = False

    for b in ss.banners[-4:]:
        if b["kind"] == "success":
            st.success(b["text"])
        elif b["kind"] == "warning":
            st.warning(b["text"])
        else:
            st.info(b["text"])

    applied = ss.applied_big5 or {}
    baseline = ss.baseline_big5 or {}

    # Sliders are the source of truth for "what the user wants"; pending_big5
    # mirrors them so non-slider rerun paths can compare.
    new_slider_values: dict[str, float] = {}
    for trait in TRAIT_ORDER:
        default = float((ss.pending_big5 or applied).get(trait, 0.5))
        new_slider_values[trait] = st.slider(
            trait,
            min_value=0.0,
            max_value=1.0,
            value=default,
            step=0.05,
            key=f"slider-{trait}",
        )

    ss.pending_big5 = new_slider_values

    # If sliders have moved past epsilon since last applied, PUT immediately.
    if big5_diff(new_slider_values, applied):
        try:
            delta = summarize_delta(applied, new_slider_values)
            apply_big5(client, agent_id, new_slider_values)
            push_banner("success", f"Applied Big5 {delta}. The next turn reflects this.")
            st.rerun()
        except Exception as err:  # noqa: BLE001
            push_banner("warning", f"Apply failed: {err}")

    with st.expander("Current vs baseline", expanded=False):
        if baseline:
            for trait in TRAIT_ORDER:
                b = baseline.get(trait, 0.0)
                c = applied.get(trait, b)
                delta = c - b
                sign = "↑" if delta > 0.01 else ("↓" if delta < -0.01 else "·")
                st.caption(f"{trait}: baseline {b:.2f} · current {c:.2f} · {sign} {delta:+.2f}")

    with st.expander("Derived Dimensions (from Big5)", expanded=False):
        dims = ss.current_dimensions or {}
        for k in sorted(dims.keys()):
            v = float(dims[k])
            st.progress(min(max(v, 0.0), 1.0), text=f"{k}: {v:.2f}")
        if ss.primary_traits:
            st.caption("Primary traits: " + ", ".join(ss.primary_traits))

    st.divider()
    st.markdown("**Presets** — one-click personality swap.")
    cols = st.columns(2)
    for i, preset in enumerate(PRESETS):
        col = cols[i % 2]
        with col:
            if st.button(
                preset.name,
                key=f"preset-{preset.name}",
                use_container_width=True,
                help=preset.description,
            ):
                try:
                    apply_big5(client, agent_id, preset.big5.as_dict())
                    push_banner("success", f"Applied preset '{preset.name}'.")
                    st.rerun()
                except Exception as err:  # noqa: BLE001
                    push_banner("warning", f"Apply failed: {err}")
                    st.rerun()

    st.divider()
    if st.button("Restore to baseline", use_container_width=True):
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
        "Chat with an agent while dragging its Big5 in real time. Every "
        f"{MESSAGES_PER_SESSION} messages the demo auto-closes the session "
        "and runs CE consolidation (advance-time)."
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
