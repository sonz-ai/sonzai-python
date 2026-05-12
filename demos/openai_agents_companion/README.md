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
    model="gemini-3.1-flash-lite",
    openai_client=gemini_client,
)
agent = Agent(name="Companion", instructions=..., tools=[...], model=model)
result = Runner.run_sync(agent, user_msg)
```

If the primary model name is rejected by Gemini's compat layer, the sidebar
exposes a **fallback** (`gemini-2.0-flash-exp`). Both work today.

## Prerequisites

- Python 3.11+
- A Sonzai project + API key (see below)
- A Gemini API key from
  [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Set up your own project

You need a Sonzai project to scope your agents and webhooks against, and an
API key tied to that project. The demo never talks to anything outside that
project, so it's safe to spin up a fresh one just for kicking the tyres.

1. **Sign in.** Open [platform.sonz.ai](https://platform.sonz.ai) and sign
   in with your work email. Clerk handles auth; first-time sign-ups create a
   personal organization.
2. **Create a project.** From the dashboard, click **New project** and give
   it a recognizable name (e.g. `companion-demo`). Production environment is
   fine — projects are cheap; isolation is the win.
3. **Generate an API key.** Inside the project, open **Keys → Create key**.
   Copy the `sk_…` value immediately — the platform stores only a hash, so
   the plaintext is shown **once**. Treat it like a password.
4. **Get a Gemini key.** Visit
   [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   create a key, and copy it.
5. **Save both into `.env`** (the demo dir's `.gitignore` already excludes
   it):

   ```bash
   cat > .env <<'EOF'
   SONZAI_API_KEY=sk_...your_demo_project_key...
   GEMINI_API_KEY=AIza...
   EOF
   ```

That's it. Every agent the demo creates lives inside that project, and the
proactive webhook you'll register later is project-scoped to it as well.
Other tenants/projects on the platform never see your traffic.

> If you only have an organization-admin Clerk session and no project yet,
> the platform auto-creates a Default project for you on first agent create.
> But explicitly creating one keeps the boundary obvious during the demo.

## Run

```bash
cd demos/openai_agents_companion
pip install -r requirements.txt

# Option A — use the local SDK (recommended when hacking on the SDK itself):
pip install -e ../..

# Option B — use PyPI sonzai
pip install sonzai

# Load the .env you just created
export $(grep -v '^#' .env | xargs)

streamlit run app.py
```

The app opens at <http://localhost:8501>.

1. **Sidebar**: paste your Sonzai + Gemini keys (or rely on the env vars).
2. Pick a Gemini model. The default is `gemini-3.1-flash-lite`; the
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
| Proactive webhook | `client.webhooks.register_for_project(...)` + `list_delivery_attempts_for_project(...)` | Project-scoped subscription. Backend POSTs `on_wakeup_ready` to your URL with HMAC-signed body |
| Proactive notifications | `client.agents.notifications.list(agent_id, user_id=...)` | Stored copy of every proactive message — works even without a public webhook URL |

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

## Proactive-message webhooks

Sonzai can push to **your** URL whenever the agent generates a message on
its own initiative — daily diaries, mood-shift notices, scheduled
"wakeups," personality breakthroughs, and so on. The right pane has a
**Proactive webhook** section that wires the whole flow up against
whichever URL you give it (use [webhook.site](https://webhook.site) or an
`ngrok http <port>` tunnel — the URL has to be reachable from Sonzai's
backend).

### Register

Subscriptions are project-scoped. The demo resolves the agent's
`project_id` automatically right after `generate_and_create` by paging
`client.agents.list()` and matching on `agent_id`.

```python
resp = client.webhooks.register_for_project(
    project_id,
    "on_wakeup_ready",                    # event_type
    webhook_url="https://webhook.site/<your-uuid>",
    auth_header="Bearer my-shared-token", # optional, sent verbatim as Authorization
)
print(resp.signing_secret)  # only returned on the FIRST register — save it.
```

`signing_secret` is shown once. The demo surfaces it inline (and won't
show it again) — copy it to `client.webhooks.rotate_secret_for_project(...)`
later if you ever lose it.

### Event types

The platform fires several proactive event types; the demo's selector
picks any of:

| Event type | When it fires |
|---|---|
| `on_wakeup_ready` | A scheduled wakeup ran and produced a proactive message. Primary "send this to the user now" event. |
| `on_recurring_event_due` | A recurring event (e.g. daily check-in) hit its trigger time. |
| `on_diary_generated` | The agent finished a diary entry during consolidation. |
| `on_personality_updated` | Big5 / speech-pattern drift was applied. |
| `on_mood_updated` | Mood shifted enough to be worth notifying about. |
| `on_breakthrough_detected` | An "aha" moment — the agent's relationship-narrative changed materially. |

### Trigger one end-to-end

```python
client.agents.schedule_wakeup(
    agent_id,
    user_id=user_id,
    check_type="interest_followup",
    intent="demo_proactive_webhook",
    delay_hours=1,                        # tiny so advance_time can skip it
)
client.workbench.advance_time(agent_id, user_id, 25.0)  # jumps past the delay
```

`advance_time` runs the wakeup synchronously inside the simulated window —
no waiting for real time to pass. The dispatcher then POSTs
`on_wakeup_ready` to your URL.

The demo exposes both calls as buttons under **Proactive webhook**:
*Schedule a test wakeup*, then *Force consolidation now*.

### Payload + signing

Body fields (JSON):

```json
{
  "wakeup": { ... },
  "memory_context": { ... },
  "has_energy": true,
  "generated_message": "happy birthday Mochi! …"
}
```

Headers:

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `Authorization` | The `auth_header` you passed at registration (if any) |
| `Sonzai-Signature` | `t=<unix_ts>,v1=<hex_hmac_sha256>` over `f"{ts}.{raw_body}"` |

Verify with stdlib only — no extra dependency:

```python
import hmac, hashlib, time

def verify_sonzai_signature(raw_body: bytes, signature_header: str,
                            signing_secret: str, *, max_skew_seconds: int = 300) -> bool:
    # The server HMAC-keys the secret with the "whsec_" prefix stripped.
    raw_key = signing_secret[len("whsec_"):] if signing_secret.startswith("whsec_") else signing_secret
    parts = dict(p.split("=", 1) for p in signature_header.split(","))
    ts, sig = parts.get("t", ""), parts.get("v1", "")
    if not ts.isdigit() or abs(int(ts) - int(time.time())) > max_skew_seconds:
        return False
    signed = f"{ts}.".encode() + raw_body
    expected = hmac.new(raw_key.encode(), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)
```

The same snippet is one click away inside the right pane (under
**Verify the `Sonzai-Signature` header**).

### Inspecting deliveries

`client.webhooks.list_delivery_attempts_for_project(project_id, event_type, page_size=10)`
returns the backend's view of recent POSTs — `status`, `response_code`,
`duration_ms`, `error_message`, `attempt_number`, `created_at`. The demo
re-polls these after every chat turn so a 5xx on your end shows up
immediately.

### Polling fallback

Every dispatched proactive message is also persisted to the agent's
notifications table. If you don't (yet) have a public webhook URL, you
can poll `client.agents.notifications.list(agent_id, user_id=...)` and
mark messages consumed via `client.agents.notifications.consume(agent_id, message_id)`.
The demo shows both lanes side-by-side so you can see they reflect the
same flow.

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
