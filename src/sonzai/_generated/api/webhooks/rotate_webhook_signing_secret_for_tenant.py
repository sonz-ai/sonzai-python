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
    event_type: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/webhooks/{event_type}/rotate-secret".format(event_type=quote(str(event_type), safe=""),),
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
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RotateSigningSecretOutputBody]:
    """ Rotate webhook signing secret (tenant-scoped)

     Generates a new HMAC signing secret for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RotateSigningSecretOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RotateSigningSecretOutputBody | None:
    """ Rotate webhook signing secret (tenant-scoped)

     Generates a new HMAC signing secret for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RotateSigningSecretOutputBody
     """


    return sync_detailed(
        event_type=event_type,
client=client,

    ).parsed

async def asyncio_detailed(
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RotateSigningSecretOutputBody]:
    """ Rotate webhook signing secret (tenant-scoped)

     Generates a new HMAC signing secret for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RotateSigningSecretOutputBody]
     """


    kwargs = _get_kwargs(
        event_type=event_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    event_type: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RotateSigningSecretOutputBody | None:
    """ Rotate webhook signing secret (tenant-scoped)

     Generates a new HMAC signing secret for the project resolved from the API key's tenant context.

    Args:
        event_type (str): Webhook event type whose secret to rotate

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RotateSigningSecretOutputBody
     """


    return (await asyncio_detailed(
        event_type=event_type,
client=client,

    )).parsed
