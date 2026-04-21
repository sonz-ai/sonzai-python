from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_voices_response import ListVoicesResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    gender: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["gender"] = gender


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/voices",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListVoicesResponse:
    if response.status_code == 200:
        response_200 = ListVoicesResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListVoicesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    gender: str | Unset = UNSET,

) -> Response[ErrorModel | ListVoicesResponse]:
    """ List available voices

     Returns the list of available Gemini voices for text-to-speech. Optionally filter by gender.

    Args:
        gender (str | Unset): Filter by gender (e.g. male, female)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListVoicesResponse]
     """


    kwargs = _get_kwargs(
        gender=gender,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    gender: str | Unset = UNSET,

) -> ErrorModel | ListVoicesResponse | None:
    """ List available voices

     Returns the list of available Gemini voices for text-to-speech. Optionally filter by gender.

    Args:
        gender (str | Unset): Filter by gender (e.g. male, female)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListVoicesResponse
     """


    return sync_detailed(
        client=client,
gender=gender,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    gender: str | Unset = UNSET,

) -> Response[ErrorModel | ListVoicesResponse]:
    """ List available voices

     Returns the list of available Gemini voices for text-to-speech. Optionally filter by gender.

    Args:
        gender (str | Unset): Filter by gender (e.g. male, female)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListVoicesResponse]
     """


    kwargs = _get_kwargs(
        gender=gender,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    gender: str | Unset = UNSET,

) -> ErrorModel | ListVoicesResponse | None:
    """ List available voices

     Returns the list of available Gemini voices for text-to-speech. Optionally filter by gender.

    Args:
        gender (str | Unset): Filter by gender (e.g. male, female)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListVoicesResponse
     """


    return (await asyncio_detailed(
        client=client,
gender=gender,

    )).parsed
