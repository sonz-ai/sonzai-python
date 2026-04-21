from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.storefront import Storefront
from ...models.storefront_update_input_body import StorefrontUpdateInputBody
from typing import cast



def _get_kwargs(
    *,
    body: StorefrontUpdateInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/storefront",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | Storefront:
    if response.status_code == 200:
        response_200 = Storefront.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | Storefront]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: StorefrontUpdateInputBody,

) -> Response[ErrorModel | Storefront]:
    """ Update storefront config

     Updates storefront metadata (slug, display name, access mode, rate caps). Does not publish; see
    publishStorefront.

    Args:
        body (StorefrontUpdateInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Storefront]
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
    body: StorefrontUpdateInputBody,

) -> ErrorModel | Storefront | None:
    """ Update storefront config

     Updates storefront metadata (slug, display name, access mode, rate caps). Does not publish; see
    publishStorefront.

    Args:
        body (StorefrontUpdateInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Storefront
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: StorefrontUpdateInputBody,

) -> Response[ErrorModel | Storefront]:
    """ Update storefront config

     Updates storefront metadata (slug, display name, access mode, rate caps). Does not publish; see
    publishStorefront.

    Args:
        body (StorefrontUpdateInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | Storefront]
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
    body: StorefrontUpdateInputBody,

) -> ErrorModel | Storefront | None:
    """ Update storefront config

     Updates storefront metadata (slug, display name, access mode, rate caps). Does not publish; see
    publishStorefront.

    Args:
        body (StorefrontUpdateInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | Storefront
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
