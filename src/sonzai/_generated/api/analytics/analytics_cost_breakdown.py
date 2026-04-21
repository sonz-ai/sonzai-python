from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.cost_breakdown_response import CostBreakdownResponse
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    month: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["month"] = month

    params["start"] = start

    params["end"] = end

    params["project_id"] = project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/analytics/cost/breakdown",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CostBreakdownResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = CostBreakdownResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CostBreakdownResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    month: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> Response[CostBreakdownResponse | ErrorModel]:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        month (str | Unset): Month shortcut YYYY-MM (takes priority over start/end)
        start (str | Unset): Start date YYYY-MM-DD
        end (str | Unset): End date YYYY-MM-DD
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CostBreakdownResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        month=month,
start=start,
end=end,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    month: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> CostBreakdownResponse | ErrorModel | None:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        month (str | Unset): Month shortcut YYYY-MM (takes priority over start/end)
        start (str | Unset): Start date YYYY-MM-DD
        end (str | Unset): End date YYYY-MM-DD
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CostBreakdownResponse | ErrorModel
     """


    return sync_detailed(
        client=client,
month=month,
start=start,
end=end,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    month: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> Response[CostBreakdownResponse | ErrorModel]:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        month (str | Unset): Month shortcut YYYY-MM (takes priority over start/end)
        start (str | Unset): Start date YYYY-MM-DD
        end (str | Unset): End date YYYY-MM-DD
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CostBreakdownResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        month=month,
start=start,
end=end,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    month: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> CostBreakdownResponse | ErrorModel | None:
    """ Cost breakdown by operation / model / agent

     Returns tokens + USD grouped three ways (operation, model, agent) over the requested window. Query
    params: `month=YYYY-MM` (shortcut) OR `start`/`end` (YYYY-MM-DD). Optional `project_id` filter.
    Backed by platform.token_usage_daily_by_op which is populated for every priced LLM + embedding call.

    Args:
        month (str | Unset): Month shortcut YYYY-MM (takes priority over start/end)
        start (str | Unset): Start date YYYY-MM-DD
        end (str | Unset): End date YYYY-MM-DD
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CostBreakdownResponse | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
month=month,
start=start,
end=end,
project_id=project_id,

    )).parsed
