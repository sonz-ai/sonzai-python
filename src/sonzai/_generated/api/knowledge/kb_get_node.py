from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_node_output_body import KbGetNodeOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    node_id: str,
    *,
    history: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["history"] = history


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/nodes/{node_id}".format(project_id=quote(str(project_id), safe=""),node_id=quote(str(node_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetNodeOutputBody:
    if response.status_code == 200:
        response_200 = KbGetNodeOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetNodeOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient,
    history: str | Unset = UNSET,

) -> Response[ErrorModel | KbGetNodeOutputBody]:
    """ Get a knowledge base node with edges

     Returns the node with its connected outgoing and incoming edges. Optionally includes version
    history.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        history (str | Unset): Set to 'true' to include version history

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetNodeOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
history=history,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient,
    history: str | Unset = UNSET,

) -> ErrorModel | KbGetNodeOutputBody | None:
    """ Get a knowledge base node with edges

     Returns the node with its connected outgoing and incoming edges. Optionally includes version
    history.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        history (str | Unset): Set to 'true' to include version history

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetNodeOutputBody
     """


    return sync_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
history=history,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient,
    history: str | Unset = UNSET,

) -> Response[ErrorModel | KbGetNodeOutputBody]:
    """ Get a knowledge base node with edges

     Returns the node with its connected outgoing and incoming edges. Optionally includes version
    history.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        history (str | Unset): Set to 'true' to include version history

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetNodeOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
history=history,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient,
    history: str | Unset = UNSET,

) -> ErrorModel | KbGetNodeOutputBody | None:
    """ Get a knowledge base node with edges

     Returns the node with its connected outgoing and incoming edges. Optionally includes version
    history.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        history (str | Unset): Set to 'true' to include version history

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetNodeOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
history=history,

    )).parsed
