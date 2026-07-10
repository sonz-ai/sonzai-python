"""Project routing configuration and permanent-route resource."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from .._generated.models import Config as RoutingConfig
from .._generated.models import ListPermanentRoutesResponse, PermanentRouteBody
from .._http import AsyncHTTPClient, HTTPClient


def _config_body(config: RoutingConfig | dict[str, Any]) -> dict[str, Any]:
    if isinstance(config, RoutingConfig):
        return config.model_dump(by_alias=True, exclude_none=True)
    return RoutingConfig.model_validate(config).model_dump(by_alias=True, exclude_none=True)


def _config_path(project_id: str) -> str:
    return f"/api/v1/projects/{quote(project_id, safe='')}/routing-config"


def _routes_path(project_id: str) -> str:
    return f"/api/v1/projects/{quote(project_id, safe='')}/permanent-routes"


class Routing:
    """Synchronous routing and permanent contact-to-agent operations."""

    def __init__(self, http: HTTPClient) -> None:
        self._http = http

    def get_config(self, project_id: str) -> RoutingConfig:
        return RoutingConfig.model_validate(self._http.get(_config_path(project_id)))

    def put_config(self, project_id: str, config: RoutingConfig | dict[str, Any]) -> RoutingConfig:
        data = self._http.put(_config_path(project_id), json_data=_config_body(config))
        return RoutingConfig.model_validate(data)

    def list_permanent_routes(self, project_id: str) -> ListPermanentRoutesResponse:
        return ListPermanentRoutesResponse.model_validate(self._http.get(_routes_path(project_id)))

    def classify_contact(
        self,
        project_id: str,
        *,
        user_id: str,
        contact_name: str,
        tier: str,
        agent_id: str,
    ) -> PermanentRouteBody:
        data = self._http.post(
            _routes_path(project_id),
            json_data={
                "user_id": user_id,
                "contact_name": contact_name,
                "tier": tier,
                "agent_id": agent_id,
            },
        )
        return PermanentRouteBody.model_validate(data)

    def override_permanent_route(
        self, project_id: str, user_id: str, *, agent_id: str
    ) -> PermanentRouteBody:
        path = f"{_routes_path(project_id)}/{quote(user_id, safe='')}/override"
        return PermanentRouteBody.model_validate(
            self._http.post(path, json_data={"agent_id": agent_id})
        )


class AsyncRouting:
    """Asynchronous routing and permanent contact-to-agent operations."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http

    async def get_config(self, project_id: str) -> RoutingConfig:
        return RoutingConfig.model_validate(await self._http.get(_config_path(project_id)))

    async def put_config(
        self, project_id: str, config: RoutingConfig | dict[str, Any]
    ) -> RoutingConfig:
        data = await self._http.put(_config_path(project_id), json_data=_config_body(config))
        return RoutingConfig.model_validate(data)

    async def list_permanent_routes(self, project_id: str) -> ListPermanentRoutesResponse:
        return ListPermanentRoutesResponse.model_validate(
            await self._http.get(_routes_path(project_id))
        )

    async def classify_contact(
        self,
        project_id: str,
        *,
        user_id: str,
        contact_name: str,
        tier: str,
        agent_id: str,
    ) -> PermanentRouteBody:
        data = await self._http.post(
            _routes_path(project_id),
            json_data={
                "user_id": user_id,
                "contact_name": contact_name,
                "tier": tier,
                "agent_id": agent_id,
            },
        )
        return PermanentRouteBody.model_validate(data)

    async def override_permanent_route(
        self, project_id: str, user_id: str, *, agent_id: str
    ) -> PermanentRouteBody:
        path = f"{_routes_path(project_id)}/{quote(user_id, safe='')}/override"
        return PermanentRouteBody.model_validate(
            await self._http.post(path, json_data={"agent_id": agent_id})
        )
