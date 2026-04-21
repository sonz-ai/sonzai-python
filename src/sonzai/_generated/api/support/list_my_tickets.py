from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.ticket_list_response import TicketListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    status: str | Unset = UNSET,
    type_: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["status"] = status

    params["type"] = type_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/support/tickets",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | TicketListResponse:
    if response.status_code == 200:
        response_200 = TicketListResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | TicketListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    status: str | Unset = UNSET,
    type_: str | Unset = UNSET,

) -> Response[ErrorModel | TicketListResponse]:
    """ List my support tickets

     Returns tickets created by the authenticated user within their active tenant. Filter by `status` or
    `type`; paginate with `limit`/`offset`.

    Args:
        limit (int | Unset): Items per page Default: 20.
        offset (int | Unset): Pagination offset Default: 0.
        status (str | Unset): Filter by status (open, in_progress, resolved, closed)
        type_ (str | Unset): Filter by type (support, bug, feature_request, billing, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TicketListResponse]
     """


    kwargs = _get_kwargs(
        limit=limit,
offset=offset,
status=status,
type_=type_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    status: str | Unset = UNSET,
    type_: str | Unset = UNSET,

) -> ErrorModel | TicketListResponse | None:
    """ List my support tickets

     Returns tickets created by the authenticated user within their active tenant. Filter by `status` or
    `type`; paginate with `limit`/`offset`.

    Args:
        limit (int | Unset): Items per page Default: 20.
        offset (int | Unset): Pagination offset Default: 0.
        status (str | Unset): Filter by status (open, in_progress, resolved, closed)
        type_ (str | Unset): Filter by type (support, bug, feature_request, billing, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TicketListResponse
     """


    return sync_detailed(
        client=client,
limit=limit,
offset=offset,
status=status,
type_=type_,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    status: str | Unset = UNSET,
    type_: str | Unset = UNSET,

) -> Response[ErrorModel | TicketListResponse]:
    """ List my support tickets

     Returns tickets created by the authenticated user within their active tenant. Filter by `status` or
    `type`; paginate with `limit`/`offset`.

    Args:
        limit (int | Unset): Items per page Default: 20.
        offset (int | Unset): Pagination offset Default: 0.
        status (str | Unset): Filter by status (open, in_progress, resolved, closed)
        type_ (str | Unset): Filter by type (support, bug, feature_request, billing, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TicketListResponse]
     """


    kwargs = _get_kwargs(
        limit=limit,
offset=offset,
status=status,
type_=type_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    status: str | Unset = UNSET,
    type_: str | Unset = UNSET,

) -> ErrorModel | TicketListResponse | None:
    """ List my support tickets

     Returns tickets created by the authenticated user within their active tenant. Filter by `status` or
    `type`; paginate with `limit`/`offset`.

    Args:
        limit (int | Unset): Items per page Default: 20.
        offset (int | Unset): Pagination offset Default: 0.
        status (str | Unset): Filter by status (open, in_progress, resolved, closed)
        type_ (str | Unset): Filter by type (support, bug, feature_request, billing, ...)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TicketListResponse
     """


    return (await asyncio_detailed(
        client=client,
limit=limit,
offset=offset,
status=status,
type_=type_,

    )).parsed
