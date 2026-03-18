# Sonzai Python SDK

[![PyPI version](https://img.shields.io/pypi/v/sonzai.svg)](https://pypi.org/project/sonzai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

The official Python SDK for the [Sonzai Character Engine API](https://sonz.ai). Build AI characters with persistent memory, evolving personality, and proactive behaviors.

## Installation

```bash
pip install sonzai
```

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
    print(f"{node.title} (importance: {node.importance})")

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
# Run a simulation (streaming)
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
