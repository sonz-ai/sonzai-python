from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.wakeups_response import WakeupsResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["status"] = status

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/wakeups".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | WakeupsResponse:
    if response.status_code == 200:
        response_200 = WakeupsResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | WakeupsResponse]:
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
    status: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ErrorModel | WakeupsResponse]:
    """ List scheduled wakeups for an agent

     Returns scheduled wakeups for an agent, optionally filtered by status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        status (str | Unset): Filter by status (e.g. pending, executed)
        limit (int | Unset): Max results (1-500) Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | WakeupsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
status=status,
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
    status: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ErrorModel | WakeupsResponse | None:
    """ List scheduled wakeups for an agent

     Returns scheduled wakeups for an agent, optionally filtered by status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        status (str | Unset): Filter by status (e.g. pending, executed)
        limit (int | Unset): Max results (1-500) Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | WakeupsResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
status=status,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    status: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> Response[ErrorModel | WakeupsResponse]:
    """ List scheduled wakeups for an agent

     Returns scheduled wakeups for an agent, optionally filtered by status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        status (str | Unset): Filter by status (e.g. pending, executed)
        limit (int | Unset): Max results (1-500) Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | WakeupsResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
status=status,
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
    status: str | Unset = UNSET,
    limit: int | Unset = 50,

) -> ErrorModel | WakeupsResponse | None:
    """ List scheduled wakeups for an agent

     Returns scheduled wakeups for an agent, optionally filtered by status.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        status (str | Unset): Filter by status (e.g. pending, executed)
        limit (int | Unset): Max results (1-500) Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | WakeupsResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
status=status,
limit=limit,

    )).parsed
