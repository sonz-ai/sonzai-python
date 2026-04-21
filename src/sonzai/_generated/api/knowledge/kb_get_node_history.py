from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_node_history_output_body import KbGetNodeHistoryOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    node_id: str,
    *,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/nodes/{node_id}/history".format(project_id=quote(str(project_id), safe=""),node_id=quote(str(node_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetNodeHistoryOutputBody:
    if response.status_code == 200:
        response_200 = KbGetNodeHistoryOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetNodeHistoryOutputBody]:
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
    limit: int | Unset = 50,

) -> Response[ErrorModel | KbGetNodeHistoryOutputBody]:
    """ Get node version history

     Returns the version history for a specific knowledge base node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        limit (int | Unset): Max history entries Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetNodeHistoryOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
limit=limit,

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
    limit: int | Unset = 50,

) -> ErrorModel | KbGetNodeHistoryOutputBody | None:
    """ Get node version history

     Returns the version history for a specific knowledge base node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        limit (int | Unset): Max history entries Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetNodeHistoryOutputBody
     """


    return sync_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    node_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,

) -> Response[ErrorModel | KbGetNodeHistoryOutputBody]:
    """ Get node version history

     Returns the version history for a specific knowledge base node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        limit (int | Unset): Max history entries Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetNodeHistoryOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,
limit=limit,

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
    limit: int | Unset = 50,

) -> ErrorModel | KbGetNodeHistoryOutputBody | None:
    """ Get node version history

     Returns the version history for a specific knowledge base node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node UUID
        limit (int | Unset): Max history entries Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetNodeHistoryOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
node_id=node_id,
client=client,
limit=limit,

    )).parsed
