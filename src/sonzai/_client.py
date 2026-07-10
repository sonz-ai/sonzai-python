"""Main Sonzai client classes."""

from __future__ import annotations

import os
from typing import Any

import httpx

from ._http import AsyncHTTPClient, HTTPClient
from ._retry import RetryPolicy
from .resources.account_config import AccountConfig, AsyncAccountConfig
from .resources.agents import Agents, AsyncAgents
from .resources.analytics import Analytics, AsyncAnalytics
from .resources.builtin_agents import AsyncBuiltinAgents, BuiltinAgents
from .resources.byok import BYOK, AsyncBYOK
from .resources.channel_connections import AsyncChannelConnections, ChannelConnections
from .resources.channels import AsyncChannels, Channels
from .resources.composio import AsyncComposio, Composio
from .resources.conversations import AsyncConversations, Conversations
from .resources.crm import AsyncCrm, Crm
from .resources.custom_agents import AsyncCustomAgents, CustomAgents
from .resources.custom_llm import AsyncCustomLLM, CustomLLM
from .resources.eval_runs import AsyncEvalRuns, EvalRuns
from .resources.eval_templates import AsyncEvalTemplates, EvalTemplates
from .resources.ingest import AsyncIngest, Ingest
from .resources.knowledge import AsyncKnowledge, Knowledge
from .resources.lead_assignments import AsyncLeadAssignments, LeadAssignments
from .resources.mcp_catalog import AsyncMCPCatalog, MCPCatalog
from .resources.ml import ML, AsyncML
from .resources.org import AsyncOrg, Org
from .resources.pipelines import AsyncPipelines, Pipelines
from .resources.project_config import AsyncProjectConfig, ProjectConfig
from .resources.project_notifications import (
    AsyncProjectNotifications,
    ProjectNotifications,
)
from .resources.projects import AsyncProjects, Projects
from .resources.routing import AsyncRouting, Routing
from .resources.runtime import AsyncRuntime, Runtime
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
from .types import PlatformModelsResponse

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
    builtin_agents: BuiltinAgents
    ml: ML
    lead_assignments: LeadAssignments
    ingest: Ingest
    knowledge: Knowledge
    mcp_catalog: MCPCatalog
    eval_templates: EvalTemplates
    eval_runs: EvalRuns
    projects: Projects
    user_personas: UserPersonas
    voices: Voices
    webhooks: Webhooks
    channels: Channels
    channel_connections: ChannelConnections
    conversations: Conversations
    crm: Crm
    custom_agents: CustomAgents
    pipelines: Pipelines
    project_config: ProjectConfig
    account_config: AccountConfig
    byok: BYOK
    custom_llm: CustomLLM
    project_notifications: ProjectNotifications
    schedules: Schedules
    workbench: Workbench
    org: Org
    storefront: Storefront
    support: Support
    tenants: Tenants
    runtime: Runtime
    routing: Routing

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        runtime_base_url: str | None = None,
        runtime_api_key: str | None = None,
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        max_retries: int | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        """Initialize the Sonzai client.

        Args:
            api_key: Your project API key. Falls back to ``SONZAI_API_KEY`` env var.
                Required for platform API resources; CRM-only clients may omit it
                when both runtime credentials are configured.
            base_url: API base URL. Falls back to ``SONZAI_BASE_URL`` or the default.
            runtime_base_url: Deployed app-runtime base URL for runtime-local resources
                such as CRM. Falls back to ``SONZAI_RUNTIME_BASE_URL``.
            runtime_api_key: Runtime adapter token for ``Authorization: Bearer`` on
                app-runtime routes. Falls back to ``SONZAI_RUNTIME_API_KEY``. Required
                whenever ``runtime_base_url`` is configured; it is distinct from
                ``api_key`` and is never inferred from it.
            timeout: Request timeout in seconds.
            retry: ``RetryPolicy`` instance controlling retry behaviour. When provided,
                takes precedence over ``max_retries``.
            max_retries: Maximum number of retry attempts. Backwards-compat shorthand;
                prefer ``retry=RetryPolicy(max_attempts=...)``.
            http_client: Custom ``httpx.Client`` instance. When provided, the SDK
                uses this client directly instead of creating a new one.
        """
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)
        resolved_runtime_url = runtime_base_url or os.environ.get("SONZAI_RUNTIME_BASE_URL")
        resolved_runtime_key = runtime_api_key or os.environ.get("SONZAI_RUNTIME_API_KEY", "")
        if resolved_runtime_url and not resolved_runtime_key:
            raise ValueError(
                "runtime_api_key must be provided or set via the SONZAI_RUNTIME_API_KEY "
                "environment variable when runtime_base_url is configured"
            )
        if not resolved_key and not (resolved_runtime_url and resolved_runtime_key):
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable "
                "unless both runtime_base_url and runtime_api_key are configured"
            )

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
        self._runtime_http = (
            HTTPClient(
                base_url=resolved_runtime_url,
                api_key=resolved_runtime_key,
                timeout=timeout,
                retry=retry,
            )
            if resolved_runtime_url
            else None
        )

        self.agents = Agents(self._http)
        self.analytics = Analytics(self._http)
        self.builtin_agents = BuiltinAgents(self._http)
        self.ml = ML(self._http)
        self.lead_assignments = LeadAssignments(self._http)
        self.ingest = Ingest(self._http)
        self.knowledge = Knowledge(self._http)
        self.mcp_catalog = MCPCatalog(self._http)
        self.eval_templates = EvalTemplates(self._http)
        self.eval_runs = EvalRuns(self._http)
        self.projects = Projects(self._http)
        self.user_personas = UserPersonas(self._http)
        self.voices = Voices(self._http)
        self.webhooks = Webhooks(self._http)
        self.channels = Channels(self._http)
        self.channel_connections = ChannelConnections(self._http)
        self.conversations = Conversations(self._http)
        self.crm = Crm(self._runtime_http)
        self.custom_agents = CustomAgents(self._http)
        self.pipelines = Pipelines(self._http)
        self.project_config = ProjectConfig(self._http)
        self.account_config = AccountConfig(self._http)
        self.byok = BYOK(self._http)
        self.custom_llm = CustomLLM(self._http)
        self.project_notifications = ProjectNotifications(self._http)
        self.schedules = Schedules(self._http)
        self.composio = Composio(self._http)
        self.skills = Skills(self._http)
        self.wisdom = Wisdom(self._http)
        self.workbench = Workbench(self._http)
        self.org = Org(self._http)
        self.storefront = Storefront(self._http)
        self.support = Support(self._http)
        self.tenants = Tenants(self._http)
        self.runtime = Runtime(self._http)
        self.routing = Routing(self._http)

    def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Call any platform operation through the SDK transport.

        Prefer a named resource when available. This escape hatch keeps a
        custom runtime compatible with newly added OpenAPI operations before
        the next convenience-resource release.
        """
        return self._http.request(
            method,
            path,
            json_data=json_data,
            params=params,
            headers=headers,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

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
        if self._runtime_http is not None:
            self._runtime_http.close()

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
    builtin_agents: AsyncBuiltinAgents
    ml: AsyncML
    lead_assignments: AsyncLeadAssignments
    ingest: AsyncIngest
    knowledge: AsyncKnowledge
    mcp_catalog: AsyncMCPCatalog
    eval_templates: AsyncEvalTemplates
    eval_runs: AsyncEvalRuns
    projects: AsyncProjects
    user_personas: AsyncUserPersonas
    voices: AsyncVoices
    webhooks: AsyncWebhooks
    channels: AsyncChannels
    channel_connections: AsyncChannelConnections
    conversations: AsyncConversations
    crm: AsyncCrm
    custom_agents: AsyncCustomAgents
    pipelines: AsyncPipelines
    project_config: AsyncProjectConfig
    account_config: AsyncAccountConfig
    byok: AsyncBYOK
    custom_llm: AsyncCustomLLM
    project_notifications: AsyncProjectNotifications
    schedules: AsyncSchedules
    composio: AsyncComposio
    skills: AsyncSkills
    wisdom: AsyncWisdom
    workbench: AsyncWorkbench
    org: AsyncOrg
    storefront: AsyncStorefront
    support: AsyncSupport
    tenants: AsyncTenants
    runtime: AsyncRuntime
    routing: AsyncRouting

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        runtime_base_url: str | None = None,
        runtime_api_key: str | None = None,
        timeout: float = 30.0,
        retry: RetryPolicy | None = None,
        max_retries: int | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("SONZAI_API_KEY", "")
        resolved_url = base_url or os.environ.get("SONZAI_BASE_URL", DEFAULT_BASE_URL)
        resolved_runtime_url = runtime_base_url or os.environ.get("SONZAI_RUNTIME_BASE_URL")
        resolved_runtime_key = runtime_api_key or os.environ.get("SONZAI_RUNTIME_API_KEY", "")
        if resolved_runtime_url and not resolved_runtime_key:
            raise ValueError(
                "runtime_api_key must be provided or set via the SONZAI_RUNTIME_API_KEY "
                "environment variable when runtime_base_url is configured"
            )
        if not resolved_key and not (resolved_runtime_url and resolved_runtime_key):
            raise ValueError(
                "api_key must be provided or set via the SONZAI_API_KEY environment variable "
                "unless both runtime_base_url and runtime_api_key are configured"
            )

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
        self._runtime_http = (
            AsyncHTTPClient(
                base_url=resolved_runtime_url,
                api_key=resolved_runtime_key,
                timeout=timeout,
                retry=retry,
            )
            if resolved_runtime_url
            else None
        )

        self.agents = AsyncAgents(self._http)
        self.analytics = AsyncAnalytics(self._http)
        self.builtin_agents = AsyncBuiltinAgents(self._http)
        self.ml = AsyncML(self._http)
        self.lead_assignments = AsyncLeadAssignments(self._http)
        self.ingest = AsyncIngest(self._http)
        self.knowledge = AsyncKnowledge(self._http)
        self.mcp_catalog = AsyncMCPCatalog(self._http)
        self.eval_templates = AsyncEvalTemplates(self._http)
        self.eval_runs = AsyncEvalRuns(self._http)
        self.projects = AsyncProjects(self._http)
        self.user_personas = AsyncUserPersonas(self._http)
        self.voices = AsyncVoices(self._http)
        self.webhooks = AsyncWebhooks(self._http)
        self.channels = AsyncChannels(self._http)
        self.channel_connections = AsyncChannelConnections(self._http)
        self.conversations = AsyncConversations(self._http)
        self.crm = AsyncCrm(self._runtime_http)
        self.custom_agents = AsyncCustomAgents(self._http)
        self.pipelines = AsyncPipelines(self._http)
        self.project_config = AsyncProjectConfig(self._http)
        self.account_config = AsyncAccountConfig(self._http)
        self.byok = AsyncBYOK(self._http)
        self.custom_llm = AsyncCustomLLM(self._http)
        self.project_notifications = AsyncProjectNotifications(self._http)
        self.schedules = AsyncSchedules(self._http)
        self.composio = AsyncComposio(self._http)
        self.skills = AsyncSkills(self._http)
        self.wisdom = AsyncWisdom(self._http)
        self.workbench = AsyncWorkbench(self._http)
        self.org = AsyncOrg(self._http)
        self.storefront = AsyncStorefront(self._http)
        self.support = AsyncSupport(self._http)
        self.tenants = AsyncTenants(self._http)
        self.runtime = AsyncRuntime(self._http)
        self.routing = AsyncRouting(self._http)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json_data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Async form of :meth:`Sonzai.request`."""
        return await self._http.request(
            method,
            path,
            json_data=json_data,
            params=params,
            headers=headers,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

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
        if self._runtime_http is not None:
            await self._runtime_http.close()

    async def __aenter__(self) -> AsyncSonzai:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
