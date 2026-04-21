from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_get_trends_output_body import KbGetTrendsOutputBody
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    node_id: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["node_id"] = node_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/trends".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbGetTrendsOutputBody:
    if response.status_code == 200:
        response_200 = KbGetTrendsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbGetTrendsOutputBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    node_id: str,

) -> Response[ErrorModel | KbGetTrendsOutputBody]:
    """ Get knowledge base trends

     Returns trend aggregations for a specific node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node ID to get trends for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetTrendsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    node_id: str,

) -> ErrorModel | KbGetTrendsOutputBody | None:
    """ Get knowledge base trends

     Returns trend aggregations for a specific node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node ID to get trends for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetTrendsOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
node_id=node_id,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    node_id: str,

) -> Response[ErrorModel | KbGetTrendsOutputBody]:
    """ Get knowledge base trends

     Returns trend aggregations for a specific node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node ID to get trends for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbGetTrendsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
node_id=node_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    node_id: str,

) -> ErrorModel | KbGetTrendsOutputBody | None:
    """ Get knowledge base trends

     Returns trend aggregations for a specific node.

    Args:
        project_id (str): Project UUID
        node_id (str): Node ID to get trends for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbGetTrendsOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
node_id=node_id,

    )).parsed
