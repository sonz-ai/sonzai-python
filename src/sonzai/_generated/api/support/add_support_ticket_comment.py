from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.add_comment_request import AddCommentRequest
from ...models.error_model import ErrorModel
from ...models.support_ticket_comment import SupportTicketComment
from typing import cast



def _get_kwargs(
    ticket_id: str,
    *,
    body: AddCommentRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/support/tickets/{ticket_id}/comments".format(ticket_id=quote(str(ticket_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SupportTicketComment:
    if response.status_code == 200:
        response_200 = SupportTicketComment.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SupportTicketComment]:
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
    body: AddCommentRequest,

) -> Response[ErrorModel | SupportTicketComment]:
    """ Add a comment to a support ticket

     Appends a user comment to the ticket thread. User comments are always external
    (`is_internal=false`); only staff can create internal comments via the admin portal.

    Args:
        ticket_id (str): Ticket UUID
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SupportTicketComment]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    ticket_id: str,
    *,
    client: AuthenticatedClient,
    body: AddCommentRequest,

) -> ErrorModel | SupportTicketComment | None:
    """ Add a comment to a support ticket

     Appends a user comment to the ticket thread. User comments are always external
    (`is_internal=false`); only staff can create internal comments via the admin portal.

    Args:
        ticket_id (str): Ticket UUID
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SupportTicketComment
     """


    return sync_detailed(
        ticket_id=ticket_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    ticket_id: str,
    *,
    client: AuthenticatedClient,
    body: AddCommentRequest,

) -> Response[ErrorModel | SupportTicketComment]:
    """ Add a comment to a support ticket

     Appends a user comment to the ticket thread. User comments are always external
    (`is_internal=false`); only staff can create internal comments via the admin portal.

    Args:
        ticket_id (str): Ticket UUID
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SupportTicketComment]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    ticket_id: str,
    *,
    client: AuthenticatedClient,
    body: AddCommentRequest,

) -> ErrorModel | SupportTicketComment | None:
    """ Add a comment to a support ticket

     Appends a user comment to the ticket thread. User comments are always external
    (`is_internal=false`); only staff can create internal comments via the admin portal.

    Args:
        ticket_id (str): Ticket UUID
        body (AddCommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SupportTicketComment
     """


    return (await asyncio_detailed(
        ticket_id=ticket_id,
client=client,
body=body,

    )).parsed
