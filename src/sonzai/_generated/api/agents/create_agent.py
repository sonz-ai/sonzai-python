from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.agent_detail_response import AgentDetailResponse
from ...models.create_agent_body import CreateAgentBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    *,
    body: CreateAgentBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AgentDetailResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = AgentDetailResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AgentDetailResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateAgentBody,

) -> Response[AgentDetailResponse | ErrorModel]:
    """ Create or update an agent

     Creates a new agent (or updates if agent_id/name already exists). Handles profile creation in
    ScyllaDB and index upsert in CockroachDB. Optional lore generation, avatar generation, and initial
    goals are fired in background goroutines.

    Args:
        body (CreateAgentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentDetailResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: CreateAgentBody,

) -> AgentDetailResponse | ErrorModel | None:
    """ Create or update an agent

     Creates a new agent (or updates if agent_id/name already exists). Handles profile creation in
    ScyllaDB and index upsert in CockroachDB. Optional lore generation, avatar generation, and initial
    goals are fired in background goroutines.

    Args:
        body (CreateAgentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentDetailResponse | ErrorModel
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateAgentBody,

) -> Response[AgentDetailResponse | ErrorModel]:
    """ Create or update an agent

     Creates a new agent (or updates if agent_id/name already exists). Handles profile creation in
    ScyllaDB and index upsert in CockroachDB. Optional lore generation, avatar generation, and initial
    goals are fired in background goroutines.

    Args:
        body (CreateAgentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AgentDetailResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateAgentBody,

) -> AgentDetailResponse | ErrorModel | None:
    """ Create or update an agent

     Creates a new agent (or updates if agent_id/name already exists). Handles profile creation in
    ScyllaDB and index upsert in CockroachDB. Optional lore generation, avatar generation, and initial
    goals are fired in background goroutines.

    Args:
        body (CreateAgentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AgentDetailResponse | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
