from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.rotate_signing_secret_output_body import RotateSigningSecretOutputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    event_type: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/webhooks/{event_type}/rotate-secret".format(project_id=quote(str(project_id), safe=""),event_type=quote(str(event_type), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | RotateSigningSecretOutputBody:
    if response.status_code == 200:
        response_200 = RotateSigningSecretOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | RotateSigningSecretOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RotateSigningSecretOutputBody]:
    """ Rotate webhook signing secret

     Generates a new HMAC signing secret for the given webhook. The old secret is immediately
    invalidated.

    Args:
        project_id (str): Project UUID
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RotateSigningSecretOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
event_type=event_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RotateSigningSecretOutputBody | None:
    """ Rotate webhook signing secret

     Generates a new HMAC signing secret for the given webhook. The old secret is immediately
    invalidated.

    Args:
        project_id (str): Project UUID
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RotateSigningSecretOutputBody
     """


    return sync_detailed(
        project_id=project_id,
event_type=event_type,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RotateSigningSecretOutputBody]:
    """ Rotate webhook signing secret

     Generates a new HMAC signing secret for the given webhook. The old secret is immediately
    invalidated.

    Args:
        project_id (str): Project UUID
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RotateSigningSecretOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
event_type=event_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RotateSigningSecretOutputBody | None:
    """ Rotate webhook signing secret

     Generates a new HMAC signing secret for the given webhook. The old secret is immediately
    invalidated.

    Args:
        project_id (str): Project UUID
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RotateSigningSecretOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
event_type=event_type,
client=client,

    )).parsed
