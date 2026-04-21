from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.update_user_persona_input_body import UpdateUserPersonaInputBody
from ...models.user_persona_record import UserPersonaRecord
from typing import cast



def _get_kwargs(
    persona_id: str,
    *,
    body: UpdateUserPersonaInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/user-personas/{persona_id}".format(persona_id=quote(str(persona_id), safe=""),),
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
    persona_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateUserPersonaInputBody,

) -> Response[ErrorModel | UserPersonaRecord]:
    """ Update a user persona

     Updates name, description, and/or style. `is_default` is preserved from the existing row.

    Args:
        persona_id (str): Persona UUID
        body (UpdateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPersonaRecord]
     """


    kwargs = _get_kwargs(
        persona_id=persona_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    persona_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateUserPersonaInputBody,

) -> ErrorModel | UserPersonaRecord | None:
    """ Update a user persona

     Updates name, description, and/or style. `is_default` is preserved from the existing row.

    Args:
        persona_id (str): Persona UUID
        body (UpdateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPersonaRecord
     """


    return sync_detailed(
        persona_id=persona_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    persona_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateUserPersonaInputBody,

) -> Response[ErrorModel | UserPersonaRecord]:
    """ Update a user persona

     Updates name, description, and/or style. `is_default` is preserved from the existing row.

    Args:
        persona_id (str): Persona UUID
        body (UpdateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | UserPersonaRecord]
     """


    kwargs = _get_kwargs(
        persona_id=persona_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    persona_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateUserPersonaInputBody,

) -> ErrorModel | UserPersonaRecord | None:
    """ Update a user persona

     Updates name, description, and/or style. `is_default` is preserved from the existing row.

    Args:
        persona_id (str): Persona UUID
        body (UpdateUserPersonaInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | UserPersonaRecord
     """


    return (await asyncio_detailed(
        persona_id=persona_id,
client=client,
body=body,

    )).parsed
