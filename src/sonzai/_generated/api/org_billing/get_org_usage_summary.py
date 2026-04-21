from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.org_usage_summary_body import OrgUsageSummaryBody
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
        "url": "/org/usage-summary",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | OrgUsageSummaryBody:
    if response.status_code == 200:
        response_200 = OrgUsageSummaryBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | OrgUsageSummaryBody]:
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

) -> Response[ErrorModel | OrgUsageSummaryBody]:
    """ Get org usage summary

     Returns consolidated usage (token totals, session counts, characters) for the tenant.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | OrgUsageSummaryBody]
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

) -> ErrorModel | OrgUsageSummaryBody | None:
    """ Get org usage summary

     Returns consolidated usage (token totals, session counts, characters) for the tenant.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | OrgUsageSummaryBody
     """


    return sync_detailed(
        client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[ErrorModel | OrgUsageSummaryBody]:
    """ Get org usage summary

     Returns consolidated usage (token totals, session counts, characters) for the tenant.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | OrgUsageSummaryBody]
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

) -> ErrorModel | OrgUsageSummaryBody | None:
    """ Get org usage summary

     Returns consolidated usage (token totals, session counts, characters) for the tenant.

    Args:
        days (int | Unset): Lookback window in days Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | OrgUsageSummaryBody
     """


    return (await asyncio_detailed(
        client=client,
days=days,

    )).parsed
