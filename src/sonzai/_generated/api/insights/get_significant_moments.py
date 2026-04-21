from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.significant_moments_response import SignificantMomentsResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    limit: int | Unset = 20,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/personality/significant-moments".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SignificantMomentsResponse:
    if response.status_code == 200:
        response_200 = SignificantMomentsResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SignificantMomentsResponse]:
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
    limit: int | Unset = 20,

) -> Response[ErrorModel | SignificantMomentsResponse]:
    """ Get significant personality moments

     Returns pivotal experiences that shaped the agent's personality evolution.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max moments to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SignificantMomentsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
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
    limit: int | Unset = 20,

) -> ErrorModel | SignificantMomentsResponse | None:
    """ Get significant personality moments

     Returns pivotal experiences that shaped the agent's personality evolution.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max moments to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SignificantMomentsResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,

) -> Response[ErrorModel | SignificantMomentsResponse]:
    """ Get significant personality moments

     Returns pivotal experiences that shaped the agent's personality evolution.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max moments to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SignificantMomentsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
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
    limit: int | Unset = 20,

) -> ErrorModel | SignificantMomentsResponse | None:
    """ Get significant personality moments

     Returns pivotal experiences that shaped the agent's personality evolution.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max moments to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SignificantMomentsResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
limit=limit,

    )).parsed
