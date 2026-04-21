from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.usage_response import UsageResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    month: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["month"] = month

    params["project_id"] = project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/analytics/usage",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UsageResponse:
    if response.status_code == 200:
        response_200 = UsageResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UsageResponse]:
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
    project_id: str | Unset = UNSET,

) -> Response[ErrorModel | UsageResponse]:
    """ Token and session usage analytics

     Returns daily token consumption and session counts over the requested window (default 30 days).

    Args:
        month (str | Unset): Month filter YYYY-MM (defaults to current month)
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UsageResponse]
     """


    kwargs = _get_kwargs(
        month=month,
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
    project_id: str | Unset = UNSET,

) -> ErrorModel | UsageResponse | None:
    """ Token and session usage analytics

     Returns daily token consumption and session counts over the requested window (default 30 days).

    Args:
        month (str | Unset): Month filter YYYY-MM (defaults to current month)
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UsageResponse
     """


    return sync_detailed(
        client=client,
month=month,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    month: str | Unset = UNSET,
    project_id: str | Unset = UNSET,

) -> Response[ErrorModel | UsageResponse]:
    """ Token and session usage analytics

     Returns daily token consumption and session counts over the requested window (default 30 days).

    Args:
        month (str | Unset): Month filter YYYY-MM (defaults to current month)
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UsageResponse]
     """


    kwargs = _get_kwargs(
        month=month,
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
    project_id: str | Unset = UNSET,

) -> ErrorModel | UsageResponse | None:
    """ Token and session usage analytics

     Returns daily token consumption and session counts over the requested window (default 30 days).

    Args:
        month (str | Unset): Month filter YYYY-MM (defaults to current month)
        project_id (str | Unset): Optional project UUID filter

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UsageResponse
     """


    return (await asyncio_detailed(
        client=client,
month=month,
project_id=project_id,

    )).parsed
