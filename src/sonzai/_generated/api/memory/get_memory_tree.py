from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.memory_response import MemoryResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    parent_id: str | Unset = UNSET,
    include_contents: str | Unset = UNSET,
    scope: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["user_id"] = user_id

    params["instance_id"] = instance_id

    params["parent_id"] = parent_id

    params["include_contents"] = include_contents

    params["scope"] = scope

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/memory".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | MemoryResponse:
    if response.status_code == 200:
        response_200 = MemoryResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | MemoryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    parent_id: str | Unset = UNSET,
    include_contents: str | Unset = UNSET,
    scope: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | MemoryResponse]:
    """ Get memory tree nodes for an agent

     Returns the memory tree nodes. Supports filtering by user_id, parent_id, and scope. Optionally
    includes fact contents per node.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope memory
        instance_id (str | Unset): Optional instance ID for scoping
        parent_id (str | Unset): If set, return children of this node
        include_contents (str | Unset): Set to 'true' to include fact contents per node
        scope (str | Unset): Optional scope filter (e.g. 'wisdom')
        limit (str | Unset): Max nodes to return (default 50, max 200)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | MemoryResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
parent_id=parent_id,
include_contents=include_contents,
scope=scope,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    parent_id: str | Unset = UNSET,
    include_contents: str | Unset = UNSET,
    scope: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | MemoryResponse | None:
    """ Get memory tree nodes for an agent

     Returns the memory tree nodes. Supports filtering by user_id, parent_id, and scope. Optionally
    includes fact contents per node.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope memory
        instance_id (str | Unset): Optional instance ID for scoping
        parent_id (str | Unset): If set, return children of this node
        include_contents (str | Unset): Set to 'true' to include fact contents per node
        scope (str | Unset): Optional scope filter (e.g. 'wisdom')
        limit (str | Unset): Max nodes to return (default 50, max 200)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | MemoryResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,
parent_id=parent_id,
include_contents=include_contents,
scope=scope,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    parent_id: str | Unset = UNSET,
    include_contents: str | Unset = UNSET,
    scope: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> Response[ErrorModel | MemoryResponse]:
    """ Get memory tree nodes for an agent

     Returns the memory tree nodes. Supports filtering by user_id, parent_id, and scope. Optionally
    includes fact contents per node.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope memory
        instance_id (str | Unset): Optional instance ID for scoping
        parent_id (str | Unset): If set, return children of this node
        include_contents (str | Unset): Set to 'true' to include fact contents per node
        scope (str | Unset): Optional scope filter (e.g. 'wisdom')
        limit (str | Unset): Max nodes to return (default 50, max 200)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | MemoryResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
parent_id=parent_id,
include_contents=include_contents,
scope=scope,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    parent_id: str | Unset = UNSET,
    include_contents: str | Unset = UNSET,
    scope: str | Unset = UNSET,
    limit: str | Unset = UNSET,

) -> ErrorModel | MemoryResponse | None:
    """ Get memory tree nodes for an agent

     Returns the memory tree nodes. Supports filtering by user_id, parent_id, and scope. Optionally
    includes fact contents per node.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope memory
        instance_id (str | Unset): Optional instance ID for scoping
        parent_id (str | Unset): If set, return children of this node
        include_contents (str | Unset): Set to 'true' to include fact contents per node
        scope (str | Unset): Optional scope filter (e.g. 'wisdom')
        limit (str | Unset): Max nodes to return (default 50, max 200)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | MemoryResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,
parent_id=parent_id,
include_contents=include_contents,
scope=scope,
limit=limit,

    )).parsed
