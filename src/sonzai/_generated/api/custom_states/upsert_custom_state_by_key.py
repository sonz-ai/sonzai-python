from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.custom_state import CustomState
from ...models.error_model import ErrorModel
from ...models.upsert_custom_state_by_key_input_body import UpsertCustomStateByKeyInputBody
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    body: UpsertCustomStateByKeyInputBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/agents/{agent_id}/custom-states/by-key".format(agent_id=quote(str(agent_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CustomState | ErrorModel:
    if response.status_code == 200:
        response_200 = CustomState.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CustomState | ErrorModel]:
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
    body: UpsertCustomStateByKeyInputBody,

) -> Response[CustomState | ErrorModel]:
    """ Upsert a custom state by key

     Creates or updates a custom state by its composite key (agent_id, instance_id, scope, user_id, key).
    Scope defaults to `global` and content_type defaults to `text`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (UpsertCustomStateByKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomState | ErrorModel]
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
    body: UpsertCustomStateByKeyInputBody,

) -> CustomState | ErrorModel | None:
    """ Upsert a custom state by key

     Creates or updates a custom state by its composite key (agent_id, instance_id, scope, user_id, key).
    Scope defaults to `global` and content_type defaults to `text`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (UpsertCustomStateByKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomState | ErrorModel
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
    body: UpsertCustomStateByKeyInputBody,

) -> Response[CustomState | ErrorModel]:
    """ Upsert a custom state by key

     Creates or updates a custom state by its composite key (agent_id, instance_id, scope, user_id, key).
    Scope defaults to `global` and content_type defaults to `text`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (UpsertCustomStateByKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CustomState | ErrorModel]
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
    body: UpsertCustomStateByKeyInputBody,

) -> CustomState | ErrorModel | None:
    """ Upsert a custom state by key

     Creates or updates a custom state by its composite key (agent_id, instance_id, scope, user_id, key).
    Scope defaults to `global` and content_type defaults to `text`.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        body (UpsertCustomStateByKeyInputBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CustomState | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
body=body,

    )).parsed
