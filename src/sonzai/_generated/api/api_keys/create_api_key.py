from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_api_key_input_body import CreateAPIKeyInputBody
from ...models.create_api_key_output_body import CreateAPIKeyOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    body: CreateAPIKeyInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/keys".format(project_id=quote(str(project_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreateAPIKeyOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = CreateAPIKeyOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreateAPIKeyOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAPIKeyInputBody,

) -> Response[CreateAPIKeyOutputBody | ErrorModel]:
    """ Create an API key

     Creates a new API key for the given project. The plaintext key is returned exactly once in the `key`
    response field — store it securely on the client side; the server only persists a hash.

    Args:
        project_id (str): Project UUID
        body (CreateAPIKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateAPIKeyOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAPIKeyInputBody,

) -> CreateAPIKeyOutputBody | ErrorModel | None:
    """ Create an API key

     Creates a new API key for the given project. The plaintext key is returned exactly once in the `key`
    response field — store it securely on the client side; the server only persists a hash.

    Args:
        project_id (str): Project UUID
        body (CreateAPIKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateAPIKeyOutputBody | ErrorModel
     """


    return sync_detailed(
        project_id=project_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAPIKeyInputBody,

) -> Response[CreateAPIKeyOutputBody | ErrorModel]:
    """ Create an API key

     Creates a new API key for the given project. The plaintext key is returned exactly once in the `key`
    response field — store it securely on the client side; the server only persists a hash.

    Args:
        project_id (str): Project UUID
        body (CreateAPIKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateAPIKeyOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateAPIKeyInputBody,

) -> CreateAPIKeyOutputBody | ErrorModel | None:
    """ Create an API key

     Creates a new API key for the given project. The plaintext key is returned exactly once in the `key`
    response field — store it securely on the client side; the server only persists a hash.

    Args:
        project_id (str): Project UUID
        body (CreateAPIKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateAPIKeyOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
body=body,

    )).parsed
