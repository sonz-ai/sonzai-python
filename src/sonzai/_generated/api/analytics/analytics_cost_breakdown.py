from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/analytics/cost/breakdown",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorModel:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Any | ErrorModel]:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Any | ErrorModel | None:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return sync_detailed(
        client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Any | ErrorModel]:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Any | ErrorModel | None:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
days=days,

    )).parsed
