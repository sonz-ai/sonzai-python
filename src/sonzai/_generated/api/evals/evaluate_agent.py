from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.evaluate_accepted_body import EvaluateAcceptedBody
from ...models.evaluate_request import EvaluateRequest
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: EvaluateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/evaluate".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | EvaluateAcceptedBody:
    if response.status_code == 200:
        response_200 = EvaluateAcceptedBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | EvaluateAcceptedBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: EvaluateRequest,

) -> Response[ErrorModel | EvaluateAcceptedBody]:
    """ Evaluate an agent conversation

     Accepts a transcript and evaluation template, creates a pending eval run, and dispatches it to the
    NATS job queue for async processing. Returns 202 Accepted with the run_id and a `Location` header
    pointing at GET /eval-runs/{runId}. Poll that endpoint (or subscribe to /eval-runs/{runId}/events
    for SSE) for the result.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (EvaluateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | EvaluateAcceptedBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: EvaluateRequest,

) -> ErrorModel | EvaluateAcceptedBody | None:
    """ Evaluate an agent conversation

     Accepts a transcript and evaluation template, creates a pending eval run, and dispatches it to the
    NATS job queue for async processing. Returns 202 Accepted with the run_id and a `Location` header
    pointing at GET /eval-runs/{runId}. Poll that endpoint (or subscribe to /eval-runs/{runId}/events
    for SSE) for the result.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (EvaluateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | EvaluateAcceptedBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: EvaluateRequest,

) -> Response[ErrorModel | EvaluateAcceptedBody]:
    """ Evaluate an agent conversation

     Accepts a transcript and evaluation template, creates a pending eval run, and dispatches it to the
    NATS job queue for async processing. Returns 202 Accepted with the run_id and a `Location` header
    pointing at GET /eval-runs/{runId}. Poll that endpoint (or subscribe to /eval-runs/{runId}/events
    for SSE) for the result.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (EvaluateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | EvaluateAcceptedBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: EvaluateRequest,

) -> ErrorModel | EvaluateAcceptedBody | None:
    """ Evaluate an agent conversation

     Accepts a transcript and evaluation template, creates a pending eval run, and dispatches it to the
    NATS job queue for async processing. Returns 202 Accepted with the run_id and a `Location` header
    pointing at GET /eval-runs/{runId}. Poll that endpoint (or subscribe to /eval-runs/{runId}/events
    for SSE) for the result.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (EvaluateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | EvaluateAcceptedBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
