from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.cost_response import CostResponse
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["start"] = start

    params["end"] = end

    params["group_by"] = group_by

    params["project_id"] = project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/analytics/cost",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CostResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = CostResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CostResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> Response[CostResponse | ErrorModel]:
    """ Cost analytics with billing-aware pricing

     Returns USD cost summary + daily cost chart + project breakdown over the requested window (default
    30 days).

    Args:
        start (str | Unset): Start date YYYY-MM-DD (defaults to 30 days ago)
        end (str | Unset): End date YYYY-MM-DD (defaults to today)
        group_by (str | Unset): Group by 'project' (default) or 'character'
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CostResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        start=start,
end=end,
group_by=group_by,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> CostResponse | ErrorModel | None:
    """ Cost analytics with billing-aware pricing

     Returns USD cost summary + daily cost chart + project breakdown over the requested window (default
    30 days).

    Args:
        start (str | Unset): Start date YYYY-MM-DD (defaults to 30 days ago)
        end (str | Unset): End date YYYY-MM-DD (defaults to today)
        group_by (str | Unset): Group by 'project' (default) or 'character'
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CostResponse | ErrorModel
     """


    return sync_detailed(
        client=client,
start=start,
end=end,
group_by=group_by,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> Response[CostResponse | ErrorModel]:
    """ Cost analytics with billing-aware pricing

     Returns USD cost summary + daily cost chart + project breakdown over the requested window (default
    30 days).

    Args:
        start (str | Unset): Start date YYYY-MM-DD (defaults to 30 days ago)
        end (str | Unset): End date YYYY-MM-DD (defaults to today)
        group_by (str | Unset): Group by 'project' (default) or 'character'
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CostResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        start=start,
end=end,
group_by=group_by,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,
    group_by: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> CostResponse | ErrorModel | None:
    """ Cost analytics with billing-aware pricing

     Returns USD cost summary + daily cost chart + project breakdown over the requested window (default
    30 days).

    Args:
        start (str | Unset): Start date YYYY-MM-DD (defaults to 30 days ago)
        end (str | Unset): End date YYYY-MM-DD (defaults to today)
        group_by (str | Unset): Group by 'project' (default) or 'character'
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CostResponse | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
start=start,
end=end,
group_by=group_by,
project_id=project_id,

    )).parsed
