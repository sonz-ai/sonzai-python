"""LLM provider identifiers and model ID constants.

Use these when specifying a ``provider`` or ``model`` in chat requests, or when
building a model picker UI.  At runtime you can also call
``client.list_models()`` to get the live list of providers and models enabled on
the current deployment.

Example::

    from sonzai import Sonzai
    from sonzai import providers

    client = Sonzai(api_key="...")

    # Use a constant directly
    response = client.agents.chat(
        agent_id="agent-id",
        messages=[{"role": "user", "content": "Hello!"}],
        provider=providers.GEMINI,
        model=providers.models.GEMINI_FLASH_LITE,
    )

    # Or fetch the live list
    result = client.list_models()
    print("Available providers:", [p.provider for p in result.providers])
"""

# ---------------------------------------------------------------------------
# Provider identifiers
# ---------------------------------------------------------------------------

GEMINI = "gemini"
"""Provider ID for Google Gemini."""

ZHIPU = "zhipu"
"""Provider ID for Zhipu AI (GLM-4 family)."""

VOLCENGINE = "volcengine"
"""Provider ID for VolcEngine (Doubao family)."""

OPENROUTER = "openrouter"
"""Provider ID for OpenRouter (multi-model gateway, used as fallback)."""

CUSTOM = "custom"
"""Provider ID for a project-configured custom LLM (BYOM)."""

# ---------------------------------------------------------------------------
# Model IDs
# ---------------------------------------------------------------------------

# Google Gemini
GEMINI_FLASH_LITE = "gemini-3.1-flash-lite-preview"
"""Fast, cost-efficient model — recommended default for most use cases."""

# Zhipu AI
ZHIPU_GLM4_FLASH = "glm-4-flash"
"""Lightweight, zero-cost flash model for high-throughput workloads."""

ZHIPU_GLM4_PLUS = "glm-4-plus"
"""Highest-capability GLM-4 model."""

# VolcEngine (Doubao)
VOLCENGINE_DOUBAO_CHARACTER = "doubao-1-5-pro-32k-character"
"""Long-context character model optimised for roleplay and dialogue."""

# OpenRouter (fallback)
OPENROUTER_CLAUDE_HAIKU = "anthropic/claude-3-haiku"
OPENROUTER_CLAUDE_SONNET = "anthropic/claude-3.5-sonnet"

# ---------------------------------------------------------------------------
# Default
# ---------------------------------------------------------------------------

DEFAULT_MODEL = GEMINI_FLASH_LITE
"""The platform's default model ID."""
