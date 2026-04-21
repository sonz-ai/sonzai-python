from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.eval_run_event import EvalRunEvent
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    run_id: str,
    *,
    from_: int | Unset = 0,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["from"] = from_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/eval-runs/{run_id}/events".format(run_id=quote(str(run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | EvalRunEvent:
    if response.status_code == 200:
        response_200 = EvalRunEvent.from_dict(response.text)



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | EvalRunEvent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient,
    from_: int | Unset = 0,

) -> Response[ErrorModel | EvalRunEvent]:
    """ Stream eval run events (SSE)

     Streams Server-Sent Events for an eval run. Clients can (re)connect at any time to receive buffered
    events and live updates. Each `data:` frame carries an `EvalRunEvent` JSON object (discriminated by
    the `type` field); the stream terminates with `data: [DONE]`. Use the `from` query parameter to
    resume from a specific event index.

    Args:
        run_id (str): Eval run UUID
        from_ (int | Unset): Event index to stream from (default 0) Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | EvalRunEvent]
     """


    kwargs = _get_kwargs(
        run_id=run_id,
from_=from_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_id: str,
    *,
    client: AuthenticatedClient,
    from_: int | Unset = 0,

) -> ErrorModel | EvalRunEvent | None:
    """ Stream eval run events (SSE)

     Streams Server-Sent Events for an eval run. Clients can (re)connect at any time to receive buffered
    events and live updates. Each `data:` frame carries an `EvalRunEvent` JSON object (discriminated by
    the `type` field); the stream terminates with `data: [DONE]`. Use the `from` query parameter to
    resume from a specific event index.

    Args:
        run_id (str): Eval run UUID
        from_ (int | Unset): Event index to stream from (default 0) Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | EvalRunEvent
     """


    return sync_detailed(
        run_id=run_id,
client=client,
from_=from_,

    ).parsed

async def asyncio_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient,
    from_: int | Unset = 0,

) -> Response[ErrorModel | EvalRunEvent]:
    """ Stream eval run events (SSE)

     Streams Server-Sent Events for an eval run. Clients can (re)connect at any time to receive buffered
    events and live updates. Each `data:` frame carries an `EvalRunEvent` JSON object (discriminated by
    the `type` field); the stream terminates with `data: [DONE]`. Use the `from` query parameter to
    resume from a specific event index.

    Args:
        run_id (str): Eval run UUID
        from_ (int | Unset): Event index to stream from (default 0) Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | EvalRunEvent]
     """


    kwargs = _get_kwargs(
        run_id=run_id,
from_=from_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_id: str,
    *,
    client: AuthenticatedClient,
    from_: int | Unset = 0,

) -> ErrorModel | EvalRunEvent | None:
    """ Stream eval run events (SSE)

     Streams Server-Sent Events for an eval run. Clients can (re)connect at any time to receive buffered
    events and live updates. Each `data:` frame carries an `EvalRunEvent` JSON object (discriminated by
    the `type` field); the stream terminates with `data: [DONE]`. Use the `from` query parameter to
    resume from a specific event index.

    Args:
        run_id (str): Eval run UUID
        from_ (int | Unset): Event index to stream from (default 0) Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | EvalRunEvent
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,
from_=from_,

    )).parsed
