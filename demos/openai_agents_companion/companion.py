"""OpenAI Agents SDK + Sonzai memory companion — CLI demo.

Architecture:

    sonzai            — memory layer (personality, mood, facts, sessions)
    openai-agents     — your LLM + tool-calling harness (you own this loop)

Per turn:
    1. session.context(query=...)                  -> personality + mood + facts
    2. build instructions from that context
    3. Runner.run_sync(Agent(...), user_msg)       -> LLM + tool calls (your code)
    4. session.turn(messages=[...])                -> Sonzai extracts facts (sync mood ~300ms,
                                                       deferred extraction 5-15s)

Sonzai never sees the LLM. The LLM never sees Sonzai's storage. The contract
between them is just the messages list you submit each turn.

Run:
    cd demos/openai_agents_companion
    pip install -r requirements.txt        # or `pip install -e .`
    export SONZAI_API_KEY=sk-...
    export OPENAI_API_KEY=sk-...
    python companion.py
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any

try:
    from agents import Agent, ItemHelpers, Runner, function_tool
except ImportError as err:  # pragma: no cover
    print(
        "ERROR: openai-agents not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from err

try:
    from sonzai import Sonzai
except ImportError as err:  # pragma: no cover
    print(
        "ERROR: sonzai not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from err


# ---------------------------------------------------------------------------
# Demo tool — proves tool calls flow through to Sonzai
# ---------------------------------------------------------------------------


@function_tool
def get_current_time() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Sonzai context -> system instructions
# ---------------------------------------------------------------------------


def build_instructions(ctx: dict[str, Any]) -> str:
    """Render Sonzai's enriched context as an OpenAI system prompt.

    The context shape is open-ended JSON; we read defensively. Tenants
    typically use ``profile`` (personality) and ``behavioral`` (mood) plus
    a list of relevant ``memory.facts`` for retrieval-grounded replies.
    """
    parts: list[str] = []
    profile = ctx.get("profile") or {}
    name = profile.get("name") or "Companion"
    parts.append(f"You are {name}, a helpful and curious companion.")

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
# Agents-SDK RunResult -> Sonzai turn messages
# ---------------------------------------------------------------------------


def run_result_to_sonzai_messages(user_msg: str, result: Any) -> list[dict[str, Any]]:
    """Convert a Runner.run_sync result into Sonzai's tool-aware message format.

    Sonzai accepts OpenAI-style messages with optional tool_calls / tool_call_id.
    We walk RunItems and emit:
      MessageOutputItem  -> {role: assistant, content}
      ToolCallItem       -> {role: assistant, tool_calls: [{id, type, function}]}
      ToolCallOutputItem -> {role: tool, tool_call_id, content}
    """
    msgs: list[dict[str, Any]] = [{"role": "user", "content": user_msg}]

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
# Main loop
# ---------------------------------------------------------------------------


def main() -> int:
    sonzai_key = os.environ.get("SONZAI_API_KEY")
    if not sonzai_key:
        print("ERROR: SONZAI_API_KEY not set.", file=sys.stderr)
        return 1
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set.", file=sys.stderr)
        return 1

    sonzai = Sonzai(api_key=sonzai_key)

    print("Creating Sonzai agent…", flush=True)
    created = sonzai.agents.generation.generate_and_create(
        name=f"Companion {uuid.uuid4().hex[:4]}",
        description=(
            "A curious, warm, slightly nerdy companion who likes asking follow-up "
            "questions and remembers what the user shares."
        ),
        gender="nonbinary",
    )
    agent_id = (
        (created.get("agent_id") if isinstance(created, dict) else None)
        or (created.get("agent", {}).get("agent_id") if isinstance(created, dict) else None)
    )
    if not agent_id:
        print(f"ERROR: agent creation returned no agent_id. Raw: {created}", file=sys.stderr)
        return 1

    user_id = f"demo-user-{uuid.uuid4().hex[:8]}"
    session_id = f"demo-session-{uuid.uuid4().hex[:8]}"

    session = sonzai.agents.sessions.start(
        agent_id,
        user_id=user_id,
        session_id=session_id,
        provider="gemini",
        model="gemini-3.1-flash-lite-preview",
    )

    print(f"\nCompanion ready (agent={agent_id[:8]}…). Type your message.")
    print("Empty line or Ctrl+D to end.\n")

    while True:
        try:
            user_msg = input("You: ").strip()
        except EOFError:
            print()
            break
        if not user_msg:
            break

        # 1. Pull personality + mood + memories from Sonzai for THIS user.
        try:
            ctx = session.context(query=user_msg) or {}
        except Exception as err:
            print(f"  [sonzai context failed: {err}]")
            ctx = {}

        # 2. Run YOUR LLM agent with those instructions. Sonzai is not in this loop.
        agent = Agent(
            name="Companion",
            instructions=build_instructions(ctx),
            tools=[get_current_time],
            model="gpt-4o-mini",
        )
        try:
            result = Runner.run_sync(agent, user_msg)
        except Exception as err:
            print(f"  [openai-agents run failed: {err}]")
            continue

        reply = (result.final_output or "").strip()
        print(f"Assistant: {reply}\n")

        # 3. Hand the full transcript (incl. tool calls/results) back to Sonzai.
        sonzai_messages = run_result_to_sonzai_messages(user_msg, result)
        try:
            t0 = time.time()
            turn = session.turn(messages=sonzai_messages)
            elapsed_ms = (time.time() - t0) * 1000
            mood_str = ""
            if turn.mood is not None:
                mood_str = (
                    f" mood Δ valence={turn.mood.valence:+.2f} "
                    f"arousal={turn.mood.arousal:+.2f}"
                )
            print(
                f"  [sonzai: {elapsed_ms:.0f}ms · extraction={turn.extraction_id[:8]}…"
                f" status={turn.extraction_status}{mood_str}]\n"
            )
        except Exception as err:
            print(f"  [sonzai turn failed: {err}]\n")

    try:
        session.end()
    except Exception as err:
        print(f"  [sonzai session.end failed: {err}]")

    print("Session ended. Final extraction in progress — check sonz.ai/dashboard for details.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
