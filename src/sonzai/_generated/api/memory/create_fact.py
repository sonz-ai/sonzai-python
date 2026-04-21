from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.atomic_fact import AtomicFact
from ...models.create_fact_input_body import CreateFactInputBody
from ...models.error_model import ErrorModel
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: CreateFactInputBody,
    instance_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["instance_id"] = instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/memory/facts".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AtomicFact | ErrorModel:
    if response.status_code == 200:
        response_200 = AtomicFact.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AtomicFact | ErrorModel]:
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
    body: CreateFactInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[AtomicFact | ErrorModel]:
    """ Create a new fact for an agent

     Creates a new atomic fact. Requires either `user_id` in the body or `metadata.scope=agent_global`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateFactInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AtomicFact | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
instance_id=instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateFactInputBody,
    instance_id: str | Unset = UNSET,

) -> AtomicFact | ErrorModel | None:
    """ Create a new fact for an agent

     Creates a new atomic fact. Requires either `user_id` in the body or `metadata.scope=agent_global`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateFactInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AtomicFact | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
body=body,
instance_id=instance_id,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateFactInputBody,
    instance_id: str | Unset = UNSET,

) -> Response[AtomicFact | ErrorModel]:
    """ Create a new fact for an agent

     Creates a new atomic fact. Requires either `user_id` in the body or `metadata.scope=agent_global`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateFactInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AtomicFact | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
body=body,
instance_id=instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateFactInputBody,
    instance_id: str | Unset = UNSET,

) -> AtomicFact | ErrorModel | None:
    """ Create a new fact for an agent

     Creates a new atomic fact. Requires either `user_id` in the body or `metadata.scope=agent_global`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        instance_id (str | Unset): Optional instance ID for scoping
        body (CreateFactInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AtomicFact | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,
instance_id=instance_id,

    )).parsed
