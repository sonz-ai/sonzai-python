from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_eval_runs_output_body import ListEvalRunsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    agent_id: str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    params["limit"] = limit

    params["offset"] = offset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/eval-runs",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListEvalRunsOutputBody:
    if response.status_code == 200:
        response_200 = ListEvalRunsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListEvalRunsOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,

) -> Response[ErrorModel | ListEvalRunsOutputBody]:
    """ List eval runs

     Returns eval runs for the authenticated tenant, optionally filtered by agent.

    Args:
        agent_id (str | Unset): Filter by agent ID
        limit (int | Unset): Items per page (default 20) Default: 20.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListEvalRunsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,
offset=offset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,

) -> ErrorModel | ListEvalRunsOutputBody | None:
    """ List eval runs

     Returns eval runs for the authenticated tenant, optionally filtered by agent.

    Args:
        agent_id (str | Unset): Filter by agent ID
        limit (int | Unset): Items per page (default 20) Default: 20.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListEvalRunsOutputBody
     """


    return sync_detailed(
        client=client,
agent_id=agent_id,
limit=limit,
offset=offset,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,

) -> Response[ErrorModel | ListEvalRunsOutputBody]:
    """ List eval runs

     Returns eval runs for the authenticated tenant, optionally filtered by agent.

    Args:
        agent_id (str | Unset): Filter by agent ID
        limit (int | Unset): Items per page (default 20) Default: 20.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListEvalRunsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,
offset=offset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    agent_id: str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,

) -> ErrorModel | ListEvalRunsOutputBody | None:
    """ List eval runs

     Returns eval runs for the authenticated tenant, optionally filtered by agent.

    Args:
        agent_id (str | Unset): Filter by agent ID
        limit (int | Unset): Items per page (default 20) Default: 20.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListEvalRunsOutputBody
     """


    return (await asyncio_detailed(
        client=client,
agent_id=agent_id,
limit=limit,
offset=offset,

    )).parsed
