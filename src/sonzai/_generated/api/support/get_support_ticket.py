from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.ticket_detail_response import TicketDetailResponse
from typing import cast



def _get_kwargs(
    ticket_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/support/tickets/{ticket_id}".format(ticket_id=quote(str(ticket_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | TicketDetailResponse:
    if response.status_code == 200:
        response_200 = TicketDetailResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | TicketDetailResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | TicketDetailResponse]:
    """ Get a support ticket with comments

     Returns the ticket and its comment thread. 404 when the ticket belongs to a different tenant.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TicketDetailResponse]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    ticket_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | TicketDetailResponse | None:
    """ Get a support ticket with comments

     Returns the ticket and its comment thread. 404 when the ticket belongs to a different tenant.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TicketDetailResponse
     """


    return sync_detailed(
        ticket_id=ticket_id,
client=client,

    ).parsed

async def asyncio_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | TicketDetailResponse]:
    """ Get a support ticket with comments

     Returns the ticket and its comment thread. 404 when the ticket belongs to a different tenant.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TicketDetailResponse]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    ticket_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | TicketDetailResponse | None:
    """ Get a support ticket with comments

     Returns the ticket and its comment thread. 404 when the ticket belongs to a different tenant.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TicketDetailResponse
     """


    return (await asyncio_detailed(
        ticket_id=ticket_id,
client=client,

    )).parsed
