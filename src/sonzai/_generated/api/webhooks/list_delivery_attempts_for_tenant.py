from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_delivery_attempts_output_body import ListDeliveryAttemptsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    event_type: str,
    *,
    limit: int | Unset = 50,
    offset: int | Unset = 0,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/webhooks/{event_type}/attempts".format(event_type=quote(str(event_type), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListDeliveryAttemptsOutputBody:
    if response.status_code == 200:
        response_200 = ListDeliveryAttemptsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListDeliveryAttemptsOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_type: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,

) -> Response[ErrorModel | ListDeliveryAttemptsOutputBody]:
    """ List webhook delivery attempts (tenant-scoped)

     Returns recent delivery attempts for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type
        limit (int | Unset): Max results Default: 50.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListDeliveryAttemptsOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,
limit=limit,
offset=offset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    event_type: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,

) -> ErrorModel | ListDeliveryAttemptsOutputBody | None:
    """ List webhook delivery attempts (tenant-scoped)

     Returns recent delivery attempts for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type
        limit (int | Unset): Max results Default: 50.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListDeliveryAttemptsOutputBody
     """


    return sync_detailed(
        event_type=event_type,
client=client,
limit=limit,
offset=offset,

    ).parsed

async def asyncio_detailed(
    event_type: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,

) -> Response[ErrorModel | ListDeliveryAttemptsOutputBody]:
    """ List webhook delivery attempts (tenant-scoped)

     Returns recent delivery attempts for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type
        limit (int | Unset): Max results Default: 50.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListDeliveryAttemptsOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,
limit=limit,
offset=offset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    event_type: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,
    offset: int | Unset = 0,

) -> ErrorModel | ListDeliveryAttemptsOutputBody | None:
    """ List webhook delivery attempts (tenant-scoped)

     Returns recent delivery attempts for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type
        limit (int | Unset): Max results Default: 50.
        offset (int | Unset): Pagination offset Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListDeliveryAttemptsOutputBody
     """


    return (await asyncio_detailed(
        event_type=event_type,
client=client,
limit=limit,
offset=offset,

    )).parsed
