"""Main Sonzai client classes."""

from __future__ import annotations

import os

from ._http import AsyncHTTPClient, HTTPClient
from .resources.agents import Agents, AsyncAgents
from .resources.custom_llm import AsyncCustomLLM, CustomLLM
from .resources.eval_runs import AsyncEvalRuns, EvalRuns
from .resources.eval_templates import AsyncEvalTemplates, EvalTemplates
from .resources.knowledge import AsyncKnowledge, Knowledge
from .resources.project_config import AsyncProjectConfig, ProjectConfig
from .resources.project_notifications import (
    AsyncProjectNotifications,
    ProjectNotifications,
)
from .resources.voice import AsyncVoices, Voices
from .resources.webhooks import AsyncWebhooks, Webhooks

DEFAULT_BASE_URL = "https://api.sonz.ai"


class Sonzai:
    """Synchronous client for the Sonzai Mind Layer API.

    Usage::

        from sonzai import Sonzai

        client = Sonzai(api_key="your-api-key")

        # Create an agent
        agent = client.agents.create(name="Luna")

        # Chat with an agent
        response = client.agents.chat(
            agent_id="agent-id",
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(response.content)

        # Stream chat
        for event in client.agents.chat(
            agent_id="agent-id",
            messages=[{"role": "user", "content": "Tell me a story"}],
            stream=True,
        ):
            print(event.content, end="", flush=True)

        client.close()
    """

    agents: Agents
    knowledge: Knowledge
    eval_templates: EvalTemplates
    eval_runs: EvalRuns
    voices: Voices
    webhooks: Webhooks
    project_config: ProjectConfig
    custom_llm: CustomLLM
    project_notifications: ProjectNotifications

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        """Initialize the Sonzai client.

        Args:
            api_key: Your project API key. Falls back to ``SONZAI_API_KEY`` env var.
            base_url: API base URL. Falls back to ``SONZAI_BASE_URL`` or the default.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
        """
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable"
            )

        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)

        self._http = HTTPClient(
            base_url=resolved_url,
            api_key=resolved_key,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.agents = Agents(self._http)
        self.knowledge = Knowledge(self._http)
        self.eval_templates = EvalTemplates(self._http)
        self.eval_runs = EvalRuns(self._http)
        self.voices = Voices(self._http)
        self.webhooks = Webhooks(self._http)
        self.project_config = ProjectConfig(self._http)
        self.custom_llm = CustomLLM(self._http)
        self.project_notifications = ProjectNotifications(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> Sonzai:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncSonzai:
    """Asynchronous client for the Sonzai Mind Layer API.

    Usage::

        import asyncio
        from sonzai import AsyncSonzai

        async def main():
            client = AsyncSonzai(api_key="your-api-key")

            response = await client.agents.chat(
                "agent-id",
                messages=[{"role": "user", "content": "Hello!"}],
            )
            print(response.content)

            await client.close()

        asyncio.run(main())
    """

    agents: AsyncAgents
    knowledge: AsyncKnowledge
    eval_templates: AsyncEvalTemplates
    eval_runs: AsyncEvalRuns
    voices: AsyncVoices
    webhooks: AsyncWebhooks
    project_config: AsyncProjectConfig
    custom_llm: AsyncCustomLLM
    project_notifications: AsyncProjectNotifications

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable"
            )

        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)

        self._http = AsyncHTTPClient(
            base_url=resolved_url,
            api_key=resolved_key,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.agents = AsyncAgents(self._http)
        self.knowledge = AsyncKnowledge(self._http)
        self.eval_templates = AsyncEvalTemplates(self._http)
        self.eval_runs = AsyncEvalRuns(self._http)
        self.voices = AsyncVoices(self._http)
        self.webhooks = AsyncWebhooks(self._http)
        self.project_config = AsyncProjectConfig(self._http)
        self.custom_llm = AsyncCustomLLM(self._http)
        self.project_notifications = AsyncProjectNotifications(self._http)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncSonzai:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
