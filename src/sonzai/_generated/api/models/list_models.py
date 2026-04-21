from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.cached_models_payload import CachedModelsPayload
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/models",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CachedModelsPayload | ErrorModel:
    if response.status_code == 200:
        response_200 = CachedModelsPayload.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CachedModelsPayload | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[CachedModelsPayload | ErrorModel]:
    """ List LLM providers and model variants

     Returns the LLM providers and model variants enabled on this deployment. Response is cached in
    memory for the lifetime of the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CachedModelsPayload | ErrorModel]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> CachedModelsPayload | ErrorModel | None:
    """ List LLM providers and model variants

     Returns the LLM providers and model variants enabled on this deployment. Response is cached in
    memory for the lifetime of the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CachedModelsPayload | ErrorModel
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[CachedModelsPayload | ErrorModel]:
    """ List LLM providers and model variants

     Returns the LLM providers and model variants enabled on this deployment. Response is cached in
    memory for the lifetime of the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CachedModelsPayload | ErrorModel]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> CachedModelsPayload | ErrorModel | None:
    """ List LLM providers and model variants

     Returns the LLM providers and model variants enabled on this deployment. Response is cached in
    memory for the lifetime of the server.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CachedModelsPayload | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
