from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.batch_get_personalities_input_body import BatchGetPersonalitiesInputBody
from ...models.batch_personality_response import BatchPersonalityResponse
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    *,
    body: BatchGetPersonalitiesInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/personalities/batch",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BatchPersonalityResponse | ErrorModel:
    if response.status_code == 200:
        response_200 = BatchPersonalityResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BatchPersonalityResponse | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BatchGetPersonalitiesInputBody,

) -> Response[BatchPersonalityResponse | ErrorModel]:
    """ Batch-fetch agent personalities

     Returns personality profiles and evolution counts for up to 50 agents in a single request.

    Args:
        body (BatchGetPersonalitiesInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchPersonalityResponse | ErrorModel]
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
    body: BatchGetPersonalitiesInputBody,

) -> BatchPersonalityResponse | ErrorModel | None:
    """ Batch-fetch agent personalities

     Returns personality profiles and evolution counts for up to 50 agents in a single request.

    Args:
        body (BatchGetPersonalitiesInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchPersonalityResponse | ErrorModel
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BatchGetPersonalitiesInputBody,

) -> Response[BatchPersonalityResponse | ErrorModel]:
    """ Batch-fetch agent personalities

     Returns personality profiles and evolution counts for up to 50 agents in a single request.

    Args:
        body (BatchGetPersonalitiesInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchPersonalityResponse | ErrorModel]
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
    body: BatchGetPersonalitiesInputBody,

) -> BatchPersonalityResponse | ErrorModel | None:
    """ Batch-fetch agent personalities

     Returns personality profiles and evolution counts for up to 50 agents in a single request.

    Args:
        body (BatchGetPersonalitiesInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchPersonalityResponse | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
