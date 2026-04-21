from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.mood_aggregate_response import MoodAggregateResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    days: int | Unset = 5,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/mood/aggregate".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | MoodAggregateResponse:
    if response.status_code == 200:
        response_200 = MoodAggregateResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | MoodAggregateResponse]:
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
    days: int | Unset = 5,

) -> Response[ErrorModel | MoodAggregateResponse]:
    """ Get aggregated mood across users

     Computes an average mood across all users who interacted with the agent within the specified time
    window. Only the latest entry per user is considered.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        days (int | Unset): Number of days to aggregate over Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | MoodAggregateResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 5,

) -> ErrorModel | MoodAggregateResponse | None:
    """ Get aggregated mood across users

     Computes an average mood across all users who interacted with the agent within the specified time
    window. Only the latest entry per user is considered.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        days (int | Unset): Number of days to aggregate over Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | MoodAggregateResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 5,

) -> Response[ErrorModel | MoodAggregateResponse]:
    """ Get aggregated mood across users

     Computes an average mood across all users who interacted with the agent within the specified time
    window. Only the latest entry per user is considered.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        days (int | Unset): Number of days to aggregate over Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | MoodAggregateResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 5,

) -> ErrorModel | MoodAggregateResponse | None:
    """ Get aggregated mood across users

     Computes an average mood across all users who interacted with the agent within the specified time
    window. Only the latest entry per user is considered.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        days (int | Unset): Number of days to aggregate over Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | MoodAggregateResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
days=days,

    )).parsed
