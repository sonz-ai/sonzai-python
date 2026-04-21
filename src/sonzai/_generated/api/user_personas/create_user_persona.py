from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_user_persona_input_body import CreateUserPersonaInputBody
from ...models.error_model import ErrorModel
from ...models.user_persona_record import UserPersonaRecord
from typing import cast



def _get_kwargs(
    *,
    body: CreateUserPersonaInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user-personas",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | UserPersonaRecord:
    if response.status_code == 200:
        response_200 = UserPersonaRecord.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | UserPersonaRecord]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateUserPersonaInputBody,

) -> Response[ErrorModel | UserPersonaRecord]:
    """ Create a user persona

     Creates a new persona in the caller's tenant. Name is required.

    Args:
        body (CreateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPersonaRecord]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: CreateUserPersonaInputBody,

) -> ErrorModel | UserPersonaRecord | None:
    """ Create a user persona

     Creates a new persona in the caller's tenant. Name is required.

    Args:
        body (CreateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPersonaRecord
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateUserPersonaInputBody,

) -> Response[ErrorModel | UserPersonaRecord]:
    """ Create a user persona

     Creates a new persona in the caller's tenant. Name is required.

    Args:
        body (CreateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPersonaRecord]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateUserPersonaInputBody,

) -> ErrorModel | UserPersonaRecord | None:
    """ Create a user persona

     Creates a new persona in the caller's tenant. Name is required.

    Args:
        body (CreateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPersonaRecord
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
