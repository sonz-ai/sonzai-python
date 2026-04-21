from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_user_persona_output_body import DeleteUserPersonaOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    persona_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/user-personas/{persona_id}".format(persona_id=quote(str(persona_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteUserPersonaOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteUserPersonaOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteUserPersonaOutputBody | ErrorModel]:
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

) -> Response[DeleteUserPersonaOutputBody | ErrorModel]:
    """ Delete a user persona

     Deletes a persona after verifying tenant ownership.

    Args:
        persona_id (str): Persona UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteUserPersonaOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        persona_id=persona_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    persona_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteUserPersonaOutputBody | ErrorModel | None:
    """ Delete a user persona

     Deletes a persona after verifying tenant ownership.

    Args:
        persona_id (str): Persona UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteUserPersonaOutputBody | ErrorModel
     """


    return sync_detailed(
        persona_id=persona_id,
client=client,

    ).parsed

async def asyncio_detailed(
    persona_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteUserPersonaOutputBody | ErrorModel]:
    """ Delete a user persona

     Deletes a persona after verifying tenant ownership.

    Args:
        persona_id (str): Persona UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteUserPersonaOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        persona_id=persona_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    persona_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteUserPersonaOutputBody | ErrorModel | None:
    """ Delete a user persona

     Deletes a persona after verifying tenant ownership.

    Args:
        persona_id (str): Persona UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteUserPersonaOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        persona_id=persona_id,
client=client,

    )).parsed
