"""Main Sonzai client classes."""

from __future__ import annotations

import os

import httpx

from ._http import AsyncHTTPClient, HTTPClient
from ._retry import RetryPolicy
from .resources.account_config import AccountConfig, AsyncAccountConfig
from .resources.agents import Agents, AsyncAgents
from .resources.analytics import Analytics, AsyncAnalytics
from .types import PlatformModelsResponse
from .resources.custom_llm import AsyncCustomLLM, CustomLLM
from .resources.eval_runs import AsyncEvalRuns, EvalRuns
from .resources.eval_templates import AsyncEvalTemplates, EvalTemplates
from .resources.knowledge import AsyncKnowledge, Knowledge
from .resources.org import AsyncOrg, Org
from .resources.project_config import AsyncProjectConfig, ProjectConfig
from .resources.project_notifications import (
    AsyncProjectNotifications,
    ProjectNotifications,
)
from .resources.projects import AsyncProjects, Projects
from .resources.schedules import AsyncSchedules, Schedules
from .resources.skills import AsyncSkills, Skills
from .resources.storefront import AsyncStorefront, Storefront
from .resources.support import AsyncSupport, Support
from .resources.tenants import AsyncTenants, Tenants
from .resources.user_personas import AsyncUserPersonas, UserPersonas
from .resources.voice import AsyncVoices, Voices
from .resources.webhooks import AsyncWebhooks, Webhooks
from .resources.wisdom import AsyncWisdom, Wisdom
from .resources.workbench import AsyncWorkbench, Workbench

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
    analytics: Analytics
    knowledge: Knowledge
    eval_templates: EvalTemplates
    eval_runs: EvalRuns
    projects: Projects
    user_personas: UserPersonas
    voices: Voices
    webhooks: Webhooks
    project_config: ProjectConfig
    account_config: AccountConfig
    custom_llm: CustomLLM
    project_notifications: ProjectNotifications
    schedules: Schedules
    workbench: Workbench
    org: Org
    storefront: Storefront
    support: Support
    tenants: Tenants

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        max_retries: int | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        """Initialize the Sonzai client.

        Args:
            api_key: Your project API key. Falls back to ``SONZAI_API_KEY`` env var.
            base_url: API base URL. Falls back to ``SONZAI_BASE_URL`` or the default.
            timeout: Request timeout in seconds.
            retry: ``RetryPolicy`` instance controlling retry behaviour. When provided,
                takes precedence over ``max_retries``.
            max_retries: Maximum number of retry attempts. Backwards-compat shorthand;
                prefer ``retry=RetryPolicy(max_attempts=...)``.
            http_client: Custom ``httpx.Client`` instance. When provided, the SDK
                uses this client directly instead of creating a new one.
        """
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable"
            )

        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)

        # Build the effective RetryPolicy. retry= wins; max_retries= is compat shim.
        if retry is None and max_retries is not None:
            retry = RetryPolicy(max_attempts=max_retries)

        if http_client is not None:
            self._http = HTTPClient(
                base_url=resolved_url,
                api_key=resolved_key,
                timeout=timeout,
                retry=retry,
                httpx_client=http_client,
            )
        else:
            self._http = HTTPClient(
                base_url=resolved_url,
                api_key=resolved_key,
                timeout=timeout,
                retry=retry,
            )

        self.agents = Agents(self._http)
        self.analytics = Analytics(self._http)
        self.knowledge = Knowledge(self._http)
        self.eval_templates = EvalTemplates(self._http)
        self.eval_runs = EvalRuns(self._http)
        self.projects = Projects(self._http)
        self.user_personas = UserPersonas(self._http)
        self.voices = Voices(self._http)
        self.webhooks = Webhooks(self._http)
        self.project_config = ProjectConfig(self._http)
        self.account_config = AccountConfig(self._http)
        self.custom_llm = CustomLLM(self._http)
        self.project_notifications = ProjectNotifications(self._http)
        self.schedules = Schedules(self._http)
        self.skills = Skills(self._http)
        self.wisdom = Wisdom(self._http)
        self.workbench = Workbench(self._http)
        self.org = Org(self._http)
        self.storefront = Storefront(self._http)
        self.support = Support(self._http)
        self.tenants = Tenants(self._http)

    def list_models(self) -> PlatformModelsResponse:
        """Return all LLM providers and model variants enabled on this deployment.

        Platform-level call — does not require an agent ID. Use this to
        populate model picker UIs or validate model IDs before a chat request.

        Example::

            result = client.list_models()
            for p in result.providers:
                print(p.provider_name, [m.id for m in p.models])
        """
        data = self._http.get("/api/v1/models")
        return PlatformModelsResponse.model_validate(data)

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
    analytics: AsyncAnalytics
    knowledge: AsyncKnowledge
    eval_templates: AsyncEvalTemplates
    eval_runs: AsyncEvalRuns
    projects: AsyncProjects
    user_personas: AsyncUserPersonas
    voices: AsyncVoices
    webhooks: AsyncWebhooks
    project_config: AsyncProjectConfig
    account_config: AsyncAccountConfig
    custom_llm: AsyncCustomLLM
    project_notifications: AsyncProjectNotifications
    schedules: AsyncSchedules
    workbench: AsyncWorkbench
    org: AsyncOrg
    storefront: AsyncStorefront
    support: AsyncSupport
    tenants: AsyncTenants

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        max_retries: int | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable"
            )

        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)

        # Build the effective RetryPolicy. retry= wins; max_retries= is compat shim.
        if retry is None and max_retries is not None:
            retry = RetryPolicy(max_attempts=max_retries)

        if http_client is not None:
            self._http = AsyncHTTPClient(
                base_url=resolved_url,
                api_key=resolved_key,
                timeout=timeout,
                retry=retry,
                httpx_client=http_client,
            )
        else:
            self._http = AsyncHTTPClient(
                base_url=resolved_url,
                api_key=resolved_key,
                timeout=timeout,
                retry=retry,
            )

        self.agents = AsyncAgents(self._http)
        self.analytics = AsyncAnalytics(self._http)
        self.knowledge = AsyncKnowledge(self._http)
        self.eval_templates = AsyncEvalTemplates(self._http)
        self.eval_runs = AsyncEvalRuns(self._http)
        self.projects = AsyncProjects(self._http)
        self.user_personas = AsyncUserPersonas(self._http)
        self.voices = AsyncVoices(self._http)
        self.webhooks = AsyncWebhooks(self._http)
        self.project_config = AsyncProjectConfig(self._http)
        self.account_config = AsyncAccountConfig(self._http)
        self.custom_llm = AsyncCustomLLM(self._http)
        self.project_notifications = AsyncProjectNotifications(self._http)
        self.schedules = AsyncSchedules(self._http)
        self.skills = AsyncSkills(self._http)
        self.wisdom = AsyncWisdom(self._http)
        self.workbench = AsyncWorkbench(self._http)
        self.org = AsyncOrg(self._http)
        self.storefront = AsyncStorefront(self._http)
        self.support = AsyncSupport(self._http)
        self.tenants = AsyncTenants(self._http)

    async def list_models(self) -> PlatformModelsResponse:
        """Return all LLM providers and model variants enabled on this deployment.

        Platform-level call — does not require an agent ID. Use this to
        populate model picker UIs or validate model IDs before a chat request.

        Example::

            result = await client.list_models()
            for p in result.providers:
                print(p.provider_name, [m.id for m in p.models])
        """
        data = await self._http.get("/api/v1/models")
        return PlatformModelsResponse.model_validate(data)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncSonzai:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
