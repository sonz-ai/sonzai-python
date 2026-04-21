from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.set_account_config_output_body import SetAccountConfigOutputBody
from ...types import File, FileTypes
from io import BytesIO
from typing import cast



def _get_kwargs(
    key: str,
    *,
    body: File,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/account/config/{key}".format(key=quote(str(key), safe=""),),
    }

    _kwargs["json"] = body.to_tuple()



    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | SetAccountConfigOutputBody:
    if response.status_code == 200:
        response_200 = SetAccountConfigOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | SetAccountConfigOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> Response[ErrorModel | SetAccountConfigOutputBody]:
    """ Set an account config value

     Stores a raw JSON value under the given key for the authenticated tenant. Body must be valid JSON (≤
    1 MB).

    Args:
        key (str): Config key
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SetAccountConfigOutputBody]
     """


    kwargs = _get_kwargs(
        key=key,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    key: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> ErrorModel | SetAccountConfigOutputBody | None:
    """ Set an account config value

     Stores a raw JSON value under the given key for the authenticated tenant. Body must be valid JSON (≤
    1 MB).

    Args:
        key (str): Config key
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SetAccountConfigOutputBody
     """


    return sync_detailed(
        key=key,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> Response[ErrorModel | SetAccountConfigOutputBody]:
    """ Set an account config value

     Stores a raw JSON value under the given key for the authenticated tenant. Body must be valid JSON (≤
    1 MB).

    Args:
        key (str): Config key
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | SetAccountConfigOutputBody]
     """


    kwargs = _get_kwargs(
        key=key,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    key: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> ErrorModel | SetAccountConfigOutputBody | None:
    """ Set an account config value

     Stores a raw JSON value under the given key for the authenticated tenant. Body must be valid JSON (≤
    1 MB).

    Args:
        key (str): Config key
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | SetAccountConfigOutputBody
     """


    return (await asyncio_detailed(
        key=key,
client=client,
body=body,

    )).parsed
