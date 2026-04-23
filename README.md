# Sonzai Python SDK

[![PyPI version](https://img.shields.io/pypi/v/sonzai.svg)](https://pypi.org/project/sonzai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

The official Python SDK for the [Sonzai Mind Layer API](https://sonz.ai). Build AI agents with persistent memory, evolving personality, and proactive behaviors.

## Installation

```bash
pip install sonzai
```

## Staying in sync with the production API

This SDK tracks `https://api.sonz.ai/docs/openapi.json`. A git pre-push hook
checks for drift; run `just install-hooks` once after cloning. To refresh the
committed spec snapshot, run `just sync-spec` and commit the diff.

## Benchmarks

Sonzai beats MemPalace on **two** benchmarks, running on the cheap end of the
LLM stack — chat, judge, and partner agent all run on **Gemini 3.1 Flash
Lite**. No frontier-model arms race propping up the numbers; the lift is
from the memory architecture. Drop in a heavier model and the ceiling goes
up from there.

### LongMemEval — retrieval (MemPalace's home turf)

| Metric | Sonzai | MemPalace (hybrid_v4) |
|---|---:|---:|
| R@G (overall recall) | **0.773** | 0.741 |
| R@1 (top-hit accuracy) | **0.800** | 0.770 |
| Recall@10, multi-session | **1.000** | 1.000 |

### SOTOPIA longitudinal — compounding across sessions

**Sonzai's USP: agents that compound.** Same agent, same partner, N sessions,
`advance_time` between each. Canonical SOTOPIA scores session 1 only — we
also run it at s10, s20, s30 and add an 8th judge-scored dim
`memory_continuity` (0..10) grading whether the agent treats the
relationship as continuous with prior sessions.

**Head-to-head at session 1** (no accumulated memory, standard SOTOPIA):

| Dimension (session 1) | Sonzai | MemPalace | Δ |
|---|---:|---:|---:|
| Believability (0..10) | **9.00** | 9.00 | tie |
| Relationship (−5..5) | **4.25** | 4.00 | **+0.25** |
| Knowledge (0..10) | **7.75** | 6.50 | **+1.25** |
| Goal (0..10) | **9.00** | 8.75 | **+0.25** |
| **Overall** | **8.44** | 8.03 | **+0.41** ✅ |

**Sonzai improves across sessions** (same agent, rolling history):

| Dim | s1 | s10 | s20 | s30 | Δ s1→s30 |
|---|---:|---:|---:|---:|---:|
| Believability (0..10) | 9.00 | 9.75 | 9.62 | **10.00** (ceiling) | **+1.00 ↑** |
| Relationship (−5..5) | 4.25 | 5.00 | 4.75 | **5.00** (ceiling) | **+0.75 ↑** |
| Knowledge (0..10) | 7.75 | 8.50 | 7.75 | **8.50** | **+0.75 ↑** |
| Goal (0..10) | 9.00 | 9.75 | 9.50 | **9.75** | **+0.75 ↑** |
| `memory_continuity` (0..10) | 5.00 | **10.00** (ceiling) | 9.75 | **10.00** (ceiling) | **+5.00 ↑** |
| **Overall** | 8.44 | 9.45 | 9.38 | **9.56** | **+1.13 ↑** |

Every non-floor dim climbs. Believability and relationship hit the rubric
ceiling by s30; `memory_continuity` hits the ceiling by s10 — Sonzai's
identity model is producing accurate unprompted callbacks before a
verbatim-retrieval baseline has history to compete.

Full scores, methodology, per-question-type breakdown, and reproduction
steps (including comparison against MemPalace's canonical
`longmemeval_bench.py`):

→ [benchmarks/README.md](benchmarks/README.md)

## Quick Start

```python
from sonzai import Sonzai

client = Sonzai(api_key="your-api-key")

# Chat with an agent
response = client.agents.chat(
    "your-agent-id",
    messages=[{"role": "user", "content": "Hello! What's your favorite hobby?"}],
    user_id="user-123",
)
print(response.content)

client.close()
```

## Authentication

Get your API key from the [Sonzai Dashboard](https://platform.sonz.ai) under **Projects > API Keys**.

```python
# Pass directly
client = Sonzai(api_key="sk-...")

# Or set the environment variable
# export SONZAI_API_KEY=sk-...
client = Sonzai()
```

## Usage

### Chat (Streaming)

```python
for event in client.agents.chat(
    "agent-id",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
):
    print(event.content, end="", flush=True)
```

### Chat (Non-streaming)

```python
response = client.agents.chat(
    "agent-id",
    messages=[{"role": "user", "content": "Hello!"}],
    user_id="user-123",
    session_id="session-456",  # optional, auto-created if omitted
)
print(response.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Chat (Advanced Options)

```python
response = client.agents.chat(
    "agent-id",
    messages=[{"role": "user", "content": "Hello!"}],
    user_id="user-123",
    user_display_name="Alex",
    provider="openai",
    model="gpt-4o",
    language="en",
    timezone="America/New_York",
    compiled_system_prompt="You are a helpful assistant.",
    tool_capabilities={"web_search": True, "remember_name": True, "image_generation": False},
    tool_definitions=[
        {"name": "get_weather", "description": "Get current weather", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}},
    ],
)
```

### Memory

```python
# Get memory tree
memory = client.agents.memory.list("agent-id", user_id="user-123")
for node in memory.nodes:
    print(f"{node.name} (importance: {node.importance})")

# Search memories
results = client.agents.memory.search("agent-id", query="favorite food")
for fact in results.results:
    print(f"{fact.content} (score: {fact.score})")

# Get memory timeline
timeline = client.agents.memory.timeline(
    "agent-id",
    user_id="user-123",
    start="2026-01-01",
    end="2026-03-01",
)

# Bulk create up to 1000 pre-formed facts in one request.
# source_type="manual" — no LLM extraction.
client.agents.memory.bulk_create_facts(
    "agent-id",
    user_id="user-123",
    facts=[
        {"content": "prefers espresso"},
        {"content": "based in Singapore", "fact_type": "location"},
    ],
)

# Single-call enriched context — fact retrieval runs query-conditioned
# (two-pass: entity-filtered + raw-text vector). recent_turns surfaces this
# session's raw messages before consolidation has run, so mid-session
# "remember what I just said" works immediately.
ctx = client.agents.get_context(
    "agent-id",
    user_id="user-123",
    query="what did we discuss earlier about espresso?",
)
for turn in ctx.recent_turns or []:
    print(f"[{turn.timestamp}] {turn.role}: {turn.content}")
```

### Personality

```python
personality = client.agents.personality.get("agent-id")
print(f"Name: {personality.profile.name}")
print(f"Openness: {personality.profile.big5.openness.score}")
print(f"Warmth: {personality.profile.dimensions.warmth}/10")
```

### Sessions

```python
# Start a session
client.agents.sessions.start(
    "agent-id",
    user_id="user-123",
    session_id="session-456",
)

# ... chat messages ...

# End a session
client.agents.sessions.end(
    "agent-id",
    user_id="user-123",
    session_id="session-456",
    total_messages=10,
    duration_seconds=300,
)
```

### Agent Instances

```python
# List instances
instances = client.agents.instances.list("agent-id")

# Create a new instance
instance = client.agents.instances.create("agent-id", name="Test Instance")
print(f"Created: {instance.instance_id}")

# Reset an instance
client.agents.instances.reset("agent-id", instance.instance_id)

# Delete an instance
client.agents.instances.delete("agent-id", instance.instance_id)
```

### Notifications

```python
# Get pending notifications
notifications = client.agents.notifications.list("agent-id", status="pending")
for n in notifications.notifications:
    print(f"[{n.check_type}] {n.generated_message}")

# Consume a notification
client.agents.notifications.consume("agent-id", n.message_id)

# Get notification history
history = client.agents.notifications.history("agent-id")
```

### Capabilities (sync/async memory recall)

Supplementary memory recall can run **synchronously** (blocks context build until recall returns — every fact lands in the current turn) or **asynchronously** (races a deadline — slow hits spill to the next turn for lower first-token latency). Default is `sync`.

`memory_mode` is an agent-wide capability — set it once, every subsequent chat uses that mode until you change it.

```python
# Read the current capabilities
caps = client.agents.get_capabilities("agent-id")
print(caps.memory_mode)  # "sync" or "async"

# Switch to async for lower first-token latency
client.agents.update_capabilities("agent-id", memory_mode="async")

# Switch back to sync
client.agents.update_capabilities("agent-id", memory_mode="sync")

# Other capabilities (all optional, PATCH-style — omitted fields are left unchanged)
client.agents.update_capabilities(
    "agent-id",
    memory_mode="async",
    knowledge_base=True,
    web_search=True,
    remember_name=True,
    image_generation=False,
    inventory=False,
)
```

You can also set `memory_mode` (and `knowledge_base`) at creation time via the `tool_capabilities` dict:

```python
agent = client.agents.create(
    name="Luna",
    tool_capabilities={
        "web_search": True,
        "remember_name": True,
        "image_generation": False,
        "inventory": False,
        "knowledge_base": True,     # enable project-scoped KB search
        "memory_mode": "async",      # "sync" (default) or "async"
    },
)
```

### Context Engine Data

```python
# Mood
mood = client.agents.get_mood("agent-id", user_id="user-123")

# Relationships
relationships = client.agents.get_relationships("agent-id", user_id="user-123")

# Habits, Goals, Interests
habits = client.agents.get_habits("agent-id")
goals = client.agents.get_goals("agent-id")
interests = client.agents.get_interests("agent-id")

# Diary
diary = client.agents.get_diary("agent-id")

# Users
users = client.agents.get_users("agent-id")
```

### Evaluation

```python
# Evaluate an agent
result = client.agents.evaluate(
    "agent-id",
    messages=[
        {"role": "user", "content": "I'm feeling sad today"},
        {"role": "assistant", "content": "I'm sorry to hear that..."},
    ],
    template_id="template-uuid",
)
print(f"Score: {result.score}")
print(f"Feedback: {result.feedback}")
```

### Simulation

```python
# Run a simulation (streaming — launches run, then streams events)
for event in client.agents.simulate(
    "agent-id",
    user_persona={
        "name": "Alex",
        "background": "College student",
        "personality_traits": ["curious", "friendly"],
        "communication_style": "casual",
    },
    config={
        "max_sessions": 3,
        "max_turns_per_session": 10,
    },
):
    print(f"[{event.type}] {event.message}")

# Fire-and-forget (returns RunRef immediately)
ref = client.agents.simulate_async(
    "agent-id",
    user_persona={"name": "Alex", "background": "Student"},
    config={"max_sessions": 2},
)
print(f"Run started: {ref.run_id}")

# Reconnect to stream later (supports resuming via from_index)
for event in client.eval_runs.stream_events(ref.run_id, from_index=0):
    print(f"[{event.type}] {event.message}")
```

### Run Eval (Simulation + Evaluation)

```python
# Combined simulation + evaluation
for event in client.agents.run_eval(
    "agent-id",
    template_id="template-uuid",
    user_persona={"name": "Alex", "background": "Student"},
    simulation_config={"max_sessions": 2, "max_turns_per_session": 5},
):
    print(f"[{event.type}] {event.message}")

# Fire-and-forget
ref = client.agents.run_eval_async(
    "agent-id",
    template_id="template-uuid",
    simulation_config={"max_sessions": 2},
)
print(f"Run started: {ref.run_id}")
```

### Re-evaluate (Eval Only)

```python
# Re-evaluate an existing run with a different template
for event in client.agents.eval_only(
    "agent-id",
    template_id="new-template-uuid",
    source_run_id="existing-run-uuid",
):
    print(f"[{event.type}] {event.message}")
```

### Custom States

```python
# Create a custom state
state = client.agents.custom_states.create(
    "agent-id",
    key="player_level",
    value={"level": 15, "xp": 2400},
    scope="user",
    content_type="json",
    user_id="user-123",
)

# List states
states = client.agents.custom_states.list("agent-id", scope="global")

# Upsert by composite key (create or update)
state = client.agents.custom_states.upsert(
    "agent-id",
    key="player_level",
    value={"level": 16, "xp": 3000},
    scope="user",
    user_id="user-123",
)

# Get by composite key
state = client.agents.custom_states.get_by_key(
    "agent-id",
    key="player_level",
    scope="user",
    user_id="user-123",
)

# Delete by composite key
client.agents.custom_states.delete_by_key(
    "agent-id",
    key="player_level",
    scope="user",
    user_id="user-123",
)
```

### Eval Templates

```python
# List templates
templates = client.eval_templates.list()

# Create a template
template = client.eval_templates.create(
    name="Empathy Check",
    scoring_rubric="Evaluate emotional awareness and response quality",
    categories=[
        {"name": "Emotional Awareness", "weight": 0.5, "criteria": "..."},
        {"name": "Response Quality", "weight": 0.5, "criteria": "..."},
    ],
)

# Update a template
client.eval_templates.update(template.id, name="Updated Name")

# Delete a template
client.eval_templates.delete(template.id)
```

### Eval Runs

```python
# List eval runs
runs = client.eval_runs.list(agent_id="agent-id")

# Get a specific run
run = client.eval_runs.get("run-id")
print(f"Status: {run.status}, Turns: {run.total_turns}")

# Stream events from a running eval (reconnectable)
for event in client.eval_runs.stream_events("run-id"):
    print(f"[{event.type}] {event.message}")

# Delete a run
client.eval_runs.delete("run-id")
```

## Async Support

Every method is also available as an async variant:

```python
import asyncio
from sonzai import AsyncSonzai

async def main():
    async with AsyncSonzai(api_key="your-api-key") as client:
        # Non-streaming
        response = await client.agents.chat(
            "agent-id",
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(response.content)

        # Streaming
        async for event in await client.agents.chat(
            "agent-id",
            messages=[{"role": "user", "content": "Tell me a story"}],
            stream=True,
        ):
            print(event.content, end="", flush=True)

asyncio.run(main())
```

## Configuration

```python
client = Sonzai(
    api_key="sk-...",            # or SONZAI_API_KEY env var
    base_url="https://api.sonz.ai",  # or SONZAI_BASE_URL env var
    timeout=30.0,                # request timeout in seconds
    max_retries=2,               # retry count for failed requests
)
```

## Error Handling

```python
from sonzai import (
    Sonzai,
    AuthenticationError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
    InternalServerError,
    SonzaiError,
)

try:
    response = client.agents.chat("agent-id", messages=[...])
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Agent not found")
except RateLimitError:
    print("Rate limit exceeded, try again later")
except SonzaiError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Clone the repo
git clone https://github.com/sonz-ai/sonzai-python.git
cd sonzai-python

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/

# Type check
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.
