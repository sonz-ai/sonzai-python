from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_list_documents_output_body import KbListDocumentsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    limit: int | Unset = 50,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/documents".format(project_id=quote(str(project_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbListDocumentsOutputBody:
    if response.status_code == 200:
        response_200 = KbListDocumentsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbListDocumentsOutputBody]:
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
    limit: int | Unset = 50,

) -> Response[ErrorModel | KbListDocumentsOutputBody]:
    """ List knowledge base documents

     Returns documents uploaded to the knowledge base for the given project.

    Args:
        project_id (str): Project UUID
        limit (int | Unset): Max documents to return Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListDocumentsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,

) -> ErrorModel | KbListDocumentsOutputBody | None:
    """ List knowledge base documents

     Returns documents uploaded to the knowledge base for the given project.

    Args:
        project_id (str): Project UUID
        limit (int | Unset): Max documents to return Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListDocumentsOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,

) -> Response[ErrorModel | KbListDocumentsOutputBody]:
    """ List knowledge base documents

     Returns documents uploaded to the knowledge base for the given project.

    Args:
        project_id (str): Project UUID
        limit (int | Unset): Max documents to return Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListDocumentsOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 50,

) -> ErrorModel | KbListDocumentsOutputBody | None:
    """ List knowledge base documents

     Returns documents uploaded to the knowledge base for the given project.

    Args:
        project_id (str): Project UUID
        limit (int | Unset): Max documents to return Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListDocumentsOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
limit=limit,

    )).parsed
