from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.reset_memory_response import ResetMemoryResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    user_id: str,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["user_id"] = user_id

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/agents/{agent_id}/memory".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ResetMemoryResponse:
    if response.status_code == 200:
        response_200 = ResetMemoryResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ResetMemoryResponse]:
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
    user_id: str,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | ResetMemoryResponse]:
    """ Reset memory for an agent-user pair

     Deletes all facts and tree nodes for the specified agent and user. Requires `user_id` query
    parameter.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID whose memory to reset
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ResetMemoryResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | ResetMemoryResponse | None:
    """ Reset memory for an agent-user pair

     Deletes all facts and tree nodes for the specified agent and user. Requires `user_id` query
    parameter.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID whose memory to reset
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ResetMemoryResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    instance_id: str | Unset = UNSET,

) -> Response[ErrorModel | ResetMemoryResponse]:
    """ Reset memory for an agent-user pair

     Deletes all facts and tree nodes for the specified agent and user. Requires `user_id` query
    parameter.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID whose memory to reset
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ResetMemoryResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str,
    instance_id: str | Unset = UNSET,

) -> ErrorModel | ResetMemoryResponse | None:
    """ Reset memory for an agent-user pair

     Deletes all facts and tree nodes for the specified agent and user. Requires `user_id` query
    parameter.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID whose memory to reset
        instance_id (str | Unset): Optional instance ID for scoping

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ResetMemoryResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,

    )).parsed
