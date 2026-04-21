from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.trigger_consolidation_input_body import TriggerConsolidationInputBody
from ...models.trigger_consolidation_output_body import TriggerConsolidationOutputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: TriggerConsolidationInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/memory/consolidate".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | TriggerConsolidationOutputBody:
    if response.status_code == 200:
        response_200 = TriggerConsolidationOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | TriggerConsolidationOutputBody]:
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
    body: TriggerConsolidationInputBody,

) -> Response[ErrorModel | TriggerConsolidationOutputBody]:
    """ Trigger memory consolidation

     Triggers daily or weekly memory consolidation for the agent, optionally scoped to a specific user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (TriggerConsolidationInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TriggerConsolidationOutputBody]
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
    body: TriggerConsolidationInputBody,

) -> ErrorModel | TriggerConsolidationOutputBody | None:
    """ Trigger memory consolidation

     Triggers daily or weekly memory consolidation for the agent, optionally scoped to a specific user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (TriggerConsolidationInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TriggerConsolidationOutputBody
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
    body: TriggerConsolidationInputBody,

) -> Response[ErrorModel | TriggerConsolidationOutputBody]:
    """ Trigger memory consolidation

     Triggers daily or weekly memory consolidation for the agent, optionally scoped to a specific user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (TriggerConsolidationInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TriggerConsolidationOutputBody]
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
    body: TriggerConsolidationInputBody,

) -> ErrorModel | TriggerConsolidationOutputBody | None:
    """ Trigger memory consolidation

     Triggers daily or weekly memory consolidation for the agent, optionally scoped to a specific user.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (TriggerConsolidationInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TriggerConsolidationOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
