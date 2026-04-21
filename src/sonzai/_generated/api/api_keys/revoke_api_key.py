from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.revoke_api_key_output_body import RevokeAPIKeyOutputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    key_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{project_id}/keys/{key_id}".format(project_id=quote(str(project_id), safe=""),key_id=quote(str(key_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | RevokeAPIKeyOutputBody:
    if response.status_code == 200:
        response_200 = RevokeAPIKeyOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | RevokeAPIKeyOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    key_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RevokeAPIKeyOutputBody]:
    """ Revoke an API key

     Marks the API key inactive. Subsequent requests using the key are rejected by APIKeyAuthMiddleware.

    Args:
        project_id (str): Project UUID
        key_id (str): API key UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RevokeAPIKeyOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
key_id=key_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    key_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RevokeAPIKeyOutputBody | None:
    """ Revoke an API key

     Marks the API key inactive. Subsequent requests using the key are rejected by APIKeyAuthMiddleware.

    Args:
        project_id (str): Project UUID
        key_id (str): API key UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RevokeAPIKeyOutputBody
     """


    return sync_detailed(
        project_id=project_id,
key_id=key_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    key_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | RevokeAPIKeyOutputBody]:
    """ Revoke an API key

     Marks the API key inactive. Subsequent requests using the key are rejected by APIKeyAuthMiddleware.

    Args:
        project_id (str): Project UUID
        key_id (str): API key UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | RevokeAPIKeyOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
key_id=key_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    key_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | RevokeAPIKeyOutputBody | None:
    """ Revoke an API key

     Marks the API key inactive. Subsequent requests using the key are rejected by APIKeyAuthMiddleware.

    Args:
        project_id (str): Project UUID
        key_id (str): API key UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | RevokeAPIKeyOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
key_id=key_id,
client=client,

    )).parsed
