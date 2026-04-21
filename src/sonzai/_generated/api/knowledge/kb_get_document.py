from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_document import KBDocument
from typing import cast



def _get_kwargs(
    project_id: str,
    doc_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/documents/{doc_id}".format(project_id=quote(str(project_id), safe=""),doc_id=quote(str(doc_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBDocument:
    if response.status_code == 200:
        response_200 = KBDocument.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBDocument]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    doc_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | KBDocument]:
    """ Get a single document

     Returns metadata for a specific knowledge base document.

    Args:
        project_id (str): Project UUID
        doc_id (str): Document UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBDocument]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
doc_id=doc_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    doc_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | KBDocument | None:
    """ Get a single document

     Returns metadata for a specific knowledge base document.

    Args:
        project_id (str): Project UUID
        doc_id (str): Document UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBDocument
     """


    return sync_detailed(
        project_id=project_id,
doc_id=doc_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    doc_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | KBDocument]:
    """ Get a single document

     Returns metadata for a specific knowledge base document.

    Args:
        project_id (str): Project UUID
        doc_id (str): Document UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBDocument]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
doc_id=doc_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    doc_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | KBDocument | None:
    """ Get a single document

     Returns metadata for a specific knowledge base document.

    Args:
        project_id (str): Project UUID
        doc_id (str): Document UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBDocument
     """


    return (await asyncio_detailed(
        project_id=project_id,
doc_id=doc_id,
client=client,

    )).parsed
