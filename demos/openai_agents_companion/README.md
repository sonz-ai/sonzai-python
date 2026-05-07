# OpenAI Agents SDK + Sonzai Memory — Companion Demo

A minimal CLI showing that you can bring **your own agent framework**
(OpenAI Agents SDK in this case) and use **Sonzai as the memory layer**.

## Architecture

```
┌─────────────────────────┐         ┌───────────────────────────┐
│  openai-agents (yours)  │         │  sonzai (memory layer)    │
│  - Agent + tools        │         │  - personality            │
│  - Runner.run_sync      │         │  - mood (valence/arousal) │
│  - LLM of your choice   │         │  - facts / memories       │
└──────────┬──────────────┘         └────────────┬──────────────┘
           │                                     │
           │  build_instructions(ctx)            │
           │ ◀──────── session.context(query) ───┤  (per turn)
           │                                     │
           │  Runner.run_sync(agent, user_msg)   │  (LLM + tool calls
           │     => final_output + new_items     │   happen ENTIRELY
           │                                     │   inside your harness)
           │                                     │
           │  session.turn(messages=transcript) ▶│  (Sonzai extracts
           │                                     │   facts; sync mood
           │                                     │   ~300ms, deferred
           │                                     │   extraction 5–15s)
           ▼                                     ▼
       (reply printed)                   (memory updated)
```

Sonzai never sees the LLM. Your harness never sees Sonzai's storage.
The contract between them is just the messages list you submit each turn.

## What this demonstrates

1. **`session.context(query=...)`** returns personality + mood + relevant
   facts. The demo renders that into a system prompt for OpenAI Agents.
2. **The LLM and tools are entirely yours.** This demo uses
   `gpt-4o-mini` with one toy `get_current_time` tool. Swap in any model,
   any tools, any guardrails.
3. **`session.turn(messages=...)`** receives the full transcript —
   user message, assistant reply, **plus tool calls and tool results** —
   so Sonzai can extract facts from tool outputs too.
4. **Mood updates inline (~300ms)** in the response; deeper extraction
   runs async (5–15s) under the returned `extraction_id`.

## Prerequisites

- Python 3.11+
- `SONZAI_API_KEY` — get one at [sonz.ai](https://sonz.ai)
- `OPENAI_API_KEY` — your own OpenAI key (Sonzai does not proxy this)

## Run

```bash
cd demos/openai_agents_companion
pip install -r requirements.txt

# Option A: use the local SDK while hacking on it
pip install -e ../..

# Option B: install the released SDK from PyPI
pip install sonzai

export SONZAI_API_KEY=sk-...
export OPENAI_API_KEY=sk-...

python companion.py
```

You'll see something like:

```
Creating Sonzai agent…

Companion ready (agent=8a3f4c1e…). Type your message.
Empty line or Ctrl+D to end.

You: hey, my name is sam and i'm into rock climbing
Assistant: Nice to meet you, Sam! Rock climbing — bouldering or roped routes?
  [sonzai: 312ms · extraction=b71e9c2a… status=queued mood Δ valence=+0.18 arousal=+0.05]

You: what time is it?
Assistant: It's 2026-05-06T14:22:11+00:00 UTC.
  [sonzai: 287ms · extraction=4a82d5fb… status=queued]

You:
Session ended. Final extraction in progress — check sonz.ai/dashboard for details.
```

The second turn used the `get_current_time` tool — both the call and the
tool's output get sent to Sonzai's `/turn` so future sessions know the
companion answered a "time" question (and any user-grounding facts the
LLM produced are extracted from the assistant text).

## Why this matters

If you already have an agent framework you like — OpenAI Agents SDK,
LangGraph, Pydantic AI, Mastra, your homegrown loop — Sonzai slots in as
the **stateful memory layer** without forcing you to migrate. You keep
ownership of:

- the LLM and how you call it
- the tool catalogue and the tool execution path
- guardrails, output parsing, structured outputs
- streaming, retries, caching

Sonzai owns: personality evolution, mood dynamics, fact extraction,
cross-session consolidation, and the per-turn enriched context that
makes those things show up automatically in your system prompt.

## File map

| File | What it does |
|---|---|
| `companion.py` | The whole demo (~150 lines). Read top-to-bottom. |
| `requirements.txt` | `openai-agents` + `sonzai`. |
| `README.md` | This file. |

## Notes / caveats

- **Defaults to Gemini for Sonzai's extraction model** (`provider="gemini"`,
  `model="gemini-3.1-flash-lite-preview"`). This is the model Sonzai uses
  to derive facts/mood from the transcript — it has nothing to do with
  the LLM your agent uses for replies.
- **The agent is created fresh on every run.** For production, persist
  `agent_id` and `user_id` so the user's memory accumulates across runs.
- **Tool-call shape conversion is best-effort.** OpenAI Agents SDK
  produces RunItems whose `raw_item` follows the OpenAI Responses API.
  We translate to Sonzai's tool-aware Chat-Completions-style schema
  (`role: assistant | tool`, `tool_calls[]`, `tool_call_id`). If you use
  hosted tools (computer use, file search, web search), you may want to
  filter or summarize those before sending — facts extracted from
  arbitrary tool outputs are only useful if they're in human-readable
  text.
