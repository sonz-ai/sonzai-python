# OpenAI Agents SDK + Sonzai — Companion Demo (Streamlit, Gemini-backed)

A two-pane Streamlit app that shows you can plug **your own agent harness**
(OpenAI Agents SDK) into **Sonzai** as the memory layer — and watch every
piece of Sonzai state update live as you chat.

The LLM runs through the **OpenAI Agents SDK pointed at Gemini's
OpenAI-compat endpoint**. **No OpenAI API key is needed or used.**

```
┌──────────────── LEFT (chat) ───────────────┬─────────── RIGHT (live state) ───────────┐
│  [chat history scrolling]                  │  Mood: valence/arousal/tension/affil      │
│                                            │   (real-time, from session.turn)          │
│  User: hey, my dog Mochi just turned 3     │                                           │
│  Assistant: happy birthday Mochi! …        │  Personality (Big5)                       │
│                                            │   openness, conscientiousness, …          │
│  [chat input]                              │   (polled, lags 5-15s)                    │
│                                            │                                           │
│                                            │  Recent facts (polled)                    │
│                                            │   - User has a dog named Mochi            │
│                                            │   - Mochi just turned 3                   │
│                                            │                                           │
│                                            │  Inventory (polled)                       │
│                                            │   - blue running shoes ×1                 │
│                                            │                                           │
│                                            │  Constellation (graph render)             │
│                                            │   [interactive node graph]                │
│                                            │                                           │
│                                            │  [Force consolidation]                    │
│                                            │   → POST /workbench/advance-time          │
└────────────────────────────────────────────┴───────────────────────────────────────────┘
```

## Why Gemini and not OpenAI?

The OpenAI Agents SDK only requires an `AsyncOpenAI` client — it does not
care whose servers that client talks to. We point it at Gemini's
OpenAI-compatible endpoint:

```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI

set_tracing_disabled(True)  # don't ship traces to OpenAI; we have no key

gemini_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ["GEMINI_API_KEY"],
)
model = OpenAIChatCompletionsModel(
    model="gemini-3.1-flash-lite-preview",
    openai_client=gemini_client,
)
agent = Agent(name="Companion", instructions=..., tools=[...], model=model)
result = Runner.run_sync(agent, user_msg)
```

If the primary model name is rejected by Gemini's compat layer, the sidebar
exposes a **fallback** (`gemini-2.0-flash-exp`). Both work today.

## Prerequisites

- Python 3.11+
- `SONZAI_API_KEY` — get one at [platform.sonz.ai](https://platform.sonz.ai)
- `GEMINI_API_KEY` — get one at
  [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Run

```bash
cd demos/openai_agents_companion
pip install -r requirements.txt

# Option A — use the local SDK (recommended when hacking on the SDK itself):
pip install -e ../..

# Option B — use PyPI sonzai
pip install sonzai

export SONZAI_API_KEY=sk-...
export GEMINI_API_KEY=AI...

streamlit run app.py
```

The app opens at <http://localhost:8501>.

1. **Sidebar**: paste your Sonzai + Gemini keys (or rely on the env vars).
2. Pick a Gemini model. The default is `gemini-3.1-flash-lite-preview`; the
   fallback (`gemini-2.0-flash-exp`) is one click away if the compat layer
   ever rejects the primary name.
3. Fill in a name + description and click **Create agent + start session**.
   The SDK call (`client.agents.generation.generate_and_create`) seeds the
   agent's Big5, speech patterns, and interests in 5-15s.
4. Chat in the left pane.

## What you'll see in the right pane

| Section | Source | Cadence |
|---|---|---|
| Mood (4 dims) | `session.turn().mood` | **Real-time** — included in every turn response |
| Personality (Big5) | `client.agents.personality.get(agent_id)` | Polled after each turn — **lags 5-15s** while extraction runs |
| Recent facts | `client.agents.memory.list_all_facts(...)` | Polled after each turn — lagged for the same reason |
| Inventory | `client.agents.inventory.query_inventory(...)` | Polled after each turn (real-time once the backend inventory work lands) |
| Constellation | `client.agents.get_constellation(agent_id, user_id=...)` | Polled after each turn; mostly populated after consolidation |
| Force consolidation | `client.workbench.advance_time(..., 25.0)` | Synchronous — fires diary, consolidation, constellation extraction |

After every turn the right panel waits ~3s, then re-polls so the deferred
extraction has time to land. Anything that hasn't shown up yet will appear
on the next turn or after you click **Force consolidation**.

## What this demonstrates

1. **You own the LLM.** Sonzai has zero opinion on which model serves the
   reply. Here the OpenAI Agents SDK does the work, but routed entirely
   through Gemini.
2. **`session.context(query=...)`** returns personality + mood + relevant
   facts. The demo renders that into the system prompt for OpenAI Agents.
3. **`session.turn(messages=...)`** receives the full transcript — user
   message, assistant reply, **plus tool calls and tool results** — so
   Sonzai can extract facts from tool outputs too.
4. **Mood updates inline (~300ms)** in the response and is shown in the
   right pane immediately. Deeper extraction (facts, personality drift)
   runs async (5-15s) under the returned `extraction_id` and surfaces on
   the next poll.
5. **Force consolidation** uses `/workbench/advance-time` to short-circuit
   the 8h deferred-consolidation gate so you can see diary entries and
   constellation nodes appear in seconds rather than waiting for real time.

## Calling Sonzai's built-in tools from your harness

Sonzai exposes a small set of agent-bound tool endpoints (knowledge-base
search, time-machine reads, …) under `/api/v1/agents/{agent_id}/tools/…`.
When your harness is the OpenAI Agents SDK, the cleanest pattern is to
wrap each Sonzai endpoint as an `@function_tool` and add it to the agent's
`tools=[…]` list. The LLM then decides when to call it — same as any
developer-defined tool.

The demo includes a wrapper around `client.agents.knowledge_search` (which
posts to `/api/v1/agents/{agent_id}/tools/kb-search`):

```python
from agents import function_tool

def make_kb_search_tool(client, agent_id):
    @function_tool
    def kb_search(query: str) -> str:
        """Search the agent's knowledge base for relevant facts."""
        resp = client.agents.knowledge_search(agent_id, query=query, limit=5)
        if not resp.results:
            return "No relevant knowledge found."
        return "\n".join(
            f"- {r.label}: {r.content}" for r in resp.results
        )
    return kb_search

agent = Agent(
    name="Companion",
    instructions=...,
    tools=[get_current_time, make_kb_search_tool(client, agent_id)],
    model=model,
)
```

Two notes:

1. **The wrapper is bound to a specific `agent_id`.** That's why we use a
   factory function — `@function_tool` only sees the closed-over client +
   id, so the LLM doesn't need to (and can't) supply them as arguments.
2. **The same pattern works for any other Sonzai tool.** Examples:
   `client.agents.timemachine.get(...)` for past-state reads, or
   `client.agents.inventory.query_inventory(...)` if you want the LLM to
   self-check inventory before answering. Just wrap, add to `tools=[…]`.

## Handling images / multimodal

Gemini is multimodal end-to-end. Sonzai's `/turn` schema is currently
text-only — `messages: [{role, content: str}]`. The demo bridges these two
truths with a simple convention:

1. **Gemini sees the actual image.** When the user provides an image URL,
   the demo passes the run input as a Responses-API list with an
   `input_image` content block:

    ```python
    run_input = [{
        "role": "user",
        "type": "message",
        "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": image_url, "detail": "auto"},
        ],
    }]
    result = Runner.run_sync(agent, run_input)
    ```

2. **Sonzai gets a text marker.** When forwarding the transcript to
   `session.turn(...)`, the demo embeds the URL into the user-message
   text:

    ```text
    "look at this   [User shared image: https://example.com/mochi.jpg]"
    ```

   The fact-extraction pipeline then sees the URL inline and records it
   as a normal fact ("user shared an image of …"). On the next turn,
   `session.context(query=…)` will surface that fact in the system prompt
   if relevant.

This is intentionally minimal — no Sonzai schema extension, no
vision-describe pre-step. If you want richer image grounding, you can add
a tiny "describe this image" Gemini call first and put the description
plus the URL into the bridge text. The demo leaves that as an exercise.

## File map

| File | What it does |
|---|---|
| `app.py` | The whole demo (~600 LOC). Read top-to-bottom. |
| `requirements.txt` | `streamlit`, `openai-agents`, `sonzai`, `pyvis`. |
| `README.md` | This file. |

## Notes / caveats

- **The agent is created fresh on every Streamlit session.** For
  production, persist `agent_id` and `user_id` so the user's memory
  accumulates across runs. (You can paste an existing UUID by editing the
  sidebar — or extend the demo with a "Use existing" mode like
  `demos/personality_shift`.)
- **Tool-call shape conversion is best-effort.** The OpenAI Agents SDK
  produces RunItems whose `raw_item` follows the OpenAI Responses API. We
  translate to Sonzai's tool-aware Chat-Completions-style schema
  (`role: assistant | tool`, `tool_calls[]`, `tool_call_id`).
- **Constellation rendering uses [`pyvis`](https://pyvis.readthedocs.io/).**
  If `pyvis` isn't installed the panel falls back to a node/edge count
  summary instead of crashing.
- **Tracing is disabled.** The Agents SDK ships traces to OpenAI by
  default; we call `set_tracing_disabled(True)` so it doesn't try to use
  an OpenAI key we don't have.
- **Inventory may be lagged.** Real-time inventory is in flight on the
  backend; the demo simply re-polls per turn, which is good enough either
  way.
