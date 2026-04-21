from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_eval_templates_output_body import ListEvalTemplatesOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    type_: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["type"] = type_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/eval-templates",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListEvalTemplatesOutputBody:
    if response.status_code == 200:
        response_200 = ListEvalTemplatesOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListEvalTemplatesOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,

) -> Response[ErrorModel | ListEvalTemplatesOutputBody]:
    """ List eval templates

     Returns eval templates for the authenticated tenant. Optionally filter by type.

    Args:
        type_ (str | Unset): Filter by template type (e.g. quality, adaptation)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListEvalTemplatesOutputBody]
     """


    kwargs = _get_kwargs(
        type_=type_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,

) -> ErrorModel | ListEvalTemplatesOutputBody | None:
    """ List eval templates

     Returns eval templates for the authenticated tenant. Optionally filter by type.

    Args:
        type_ (str | Unset): Filter by template type (e.g. quality, adaptation)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListEvalTemplatesOutputBody
     """


    return sync_detailed(
        client=client,
type_=type_,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,

) -> Response[ErrorModel | ListEvalTemplatesOutputBody]:
    """ List eval templates

     Returns eval templates for the authenticated tenant. Optionally filter by type.

    Args:
        type_ (str | Unset): Filter by template type (e.g. quality, adaptation)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListEvalTemplatesOutputBody]
     """


    kwargs = _get_kwargs(
        type_=type_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    type_: str | Unset = UNSET,

) -> ErrorModel | ListEvalTemplatesOutputBody | None:
    """ List eval templates

     Returns eval templates for the authenticated tenant. Optionally filter by type.

    Args:
        type_ (str | Unset): Filter by template type (e.g. quality, adaptation)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListEvalTemplatesOutputBody
     """


    return (await asyncio_detailed(
        client=client,
type_=type_,

    )).parsed
