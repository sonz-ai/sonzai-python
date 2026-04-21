from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_summaries_period import ListSummariesPeriod
from ...models.summaries_response import SummariesResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    period: ListSummariesPeriod | Unset = UNSET,
    limit: int | Unset = 20,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_period: str | Unset = UNSET
    if not isinstance(period, Unset):
        json_period = period.value

    params["period"] = json_period

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/memory/summaries".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SummariesResponse:
    if response.status_code == 200:
        response_200 = SummariesResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SummariesResponse]:
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
    period: ListSummariesPeriod | Unset = UNSET,
    limit: int | Unset = 20,

) -> Response[ErrorModel | SummariesResponse]:
    """ List memory consolidation summaries

     Returns recent memory consolidation summaries for the agent, optionally filtered by period
    (daily/weekly).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        period (ListSummariesPeriod | Unset): Filter by consolidation stage: 'daily' or 'weekly'
        limit (int | Unset): Max summaries to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SummariesResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
period=period,
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
    period: ListSummariesPeriod | Unset = UNSET,
    limit: int | Unset = 20,

) -> ErrorModel | SummariesResponse | None:
    """ List memory consolidation summaries

     Returns recent memory consolidation summaries for the agent, optionally filtered by period
    (daily/weekly).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        period (ListSummariesPeriod | Unset): Filter by consolidation stage: 'daily' or 'weekly'
        limit (int | Unset): Max summaries to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SummariesResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
period=period,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    period: ListSummariesPeriod | Unset = UNSET,
    limit: int | Unset = 20,

) -> Response[ErrorModel | SummariesResponse]:
    """ List memory consolidation summaries

     Returns recent memory consolidation summaries for the agent, optionally filtered by period
    (daily/weekly).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        period (ListSummariesPeriod | Unset): Filter by consolidation stage: 'daily' or 'weekly'
        limit (int | Unset): Max summaries to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SummariesResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
period=period,
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
    period: ListSummariesPeriod | Unset = UNSET,
    limit: int | Unset = 20,

) -> ErrorModel | SummariesResponse | None:
    """ List memory consolidation summaries

     Returns recent memory consolidation summaries for the agent, optionally filtered by period
    (daily/weekly).

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        period (ListSummariesPeriod | Unset): Filter by consolidation stage: 'daily' or 'weekly'
        limit (int | Unset): Max summaries to return (1-100) Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SummariesResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
period=period,
limit=limit,

    )).parsed
