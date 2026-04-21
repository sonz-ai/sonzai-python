from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.analytics_realtime_response import AnalyticsRealtimeResponse
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/analytics/realtime",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AnalyticsRealtimeResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = AnalyticsRealtimeResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AnalyticsRealtimeResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AnalyticsRealtimeResponse | ErrorModel]:
    """ Dashboard analytics realtime

     Returns overview stats plus daily-trend chart data. Drives the dashboard home charts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnalyticsRealtimeResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> AnalyticsRealtimeResponse | ErrorModel | None:
    """ Dashboard analytics realtime

     Returns overview stats plus daily-trend chart data. Drives the dashboard home charts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnalyticsRealtimeResponse | ErrorModel
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AnalyticsRealtimeResponse | ErrorModel]:
    """ Dashboard analytics realtime

     Returns overview stats plus daily-trend chart data. Drives the dashboard home charts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnalyticsRealtimeResponse | ErrorModel]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> AnalyticsRealtimeResponse | ErrorModel | None:
    """ Dashboard analytics realtime

     Returns overview stats plus daily-trend chart data. Drives the dashboard home charts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnalyticsRealtimeResponse | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
