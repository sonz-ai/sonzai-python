from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    *,
    body: Any,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workbench/advance-time",
    }

    _kwargs["json"] = body


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorModel:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,

) -> Response[Any | ErrorModel]:
    """ Advance simulated time in the workbench

     Runs the same background CE workers (diary, consolidation, constellation) the production scheduler
    would run, for a chosen number of simulated days. Used by the workbench time-machine UI and long-
    horizon benchmarks.

    Args:
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
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
    body: Any,

) -> Any | ErrorModel | None:
    """ Advance simulated time in the workbench

     Runs the same background CE workers (diary, consolidation, constellation) the production scheduler
    would run, for a chosen number of simulated days. Used by the workbench time-machine UI and long-
    horizon benchmarks.

    Args:
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,

) -> Response[Any | ErrorModel]:
    """ Advance simulated time in the workbench

     Runs the same background CE workers (diary, consolidation, constellation) the production scheduler
    would run, for a chosen number of simulated days. Used by the workbench time-machine UI and long-
    horizon benchmarks.

    Args:
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
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
    body: Any,

) -> Any | ErrorModel | None:
    """ Advance simulated time in the workbench

     Runs the same background CE workers (diary, consolidation, constellation) the production scheduler
    would run, for a chosen number of simulated days. Used by the workbench time-machine UI and long-
    horizon benchmarks.

    Args:
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
