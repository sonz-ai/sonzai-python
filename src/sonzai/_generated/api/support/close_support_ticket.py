from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.support_ticket import SupportTicket
from typing import cast



def _get_kwargs(
    ticket_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/support/tickets/{ticket_id}/close".format(ticket_id=quote(str(ticket_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SupportTicket:
    if response.status_code == 200:
        response_200 = SupportTicket.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SupportTicket]:
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

) -> Response[ErrorModel | SupportTicket]:
    """ Close a support ticket (user)

     Closes the ticket if the caller is its original creator. Returns 403 when the caller is in the
    tenant but did not create the ticket.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SupportTicket]
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

) -> ErrorModel | SupportTicket | None:
    """ Close a support ticket (user)

     Closes the ticket if the caller is its original creator. Returns 403 when the caller is in the
    tenant but did not create the ticket.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SupportTicket
     """


    return sync_detailed(
        ticket_id=ticket_id,
client=client,

    ).parsed

async def asyncio_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | SupportTicket]:
    """ Close a support ticket (user)

     Closes the ticket if the caller is its original creator. Returns 403 when the caller is in the
    tenant but did not create the ticket.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SupportTicket]
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

) -> ErrorModel | SupportTicket | None:
    """ Close a support ticket (user)

     Closes the ticket if the caller is its original creator. Returns 403 when the caller is in the
    tenant but did not create the ticket.

    Args:
        ticket_id (str): Ticket UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SupportTicket
     """


    return (await asyncio_detailed(
        ticket_id=ticket_id,
client=client,

    )).parsed
