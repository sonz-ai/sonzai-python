from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_upload_document_output_body import KbUploadDocumentOutputBody
from ...types import File, FileTypes
from io import BytesIO
from typing import cast



def _get_kwargs(
    project_id: str,
    *,
    body: File,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{project_id}/knowledge/documents".format(project_id=quote(str(project_id), safe=""),),
    }

    _kwargs["content"] = body.payload

    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbUploadDocumentOutputBody:
    if response.status_code == 200:
        response_200 = KbUploadDocumentOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbUploadDocumentOutputBody]:
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
    body: File,

) -> Response[ErrorModel | KbUploadDocumentOutputBody]:
    """ Upload a document for knowledge extraction

     Accepts multipart/form-data with a 'file' field (max 50 MB). The document is uploaded to cloud
    storage and queued for extraction.

    Args:
        project_id (str): Project UUID
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbUploadDocumentOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> ErrorModel | KbUploadDocumentOutputBody | None:
    """ Upload a document for knowledge extraction

     Accepts multipart/form-data with a 'file' field (max 50 MB). The document is uploaded to cloud
    storage and queued for extraction.

    Args:
        project_id (str): Project UUID
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbUploadDocumentOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> Response[ErrorModel | KbUploadDocumentOutputBody]:
    """ Upload a document for knowledge extraction

     Accepts multipart/form-data with a 'file' field (max 50 MB). The document is uploaded to cloud
    storage and queued for extraction.

    Args:
        project_id (str): Project UUID
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbUploadDocumentOutputBody]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: File,

) -> ErrorModel | KbUploadDocumentOutputBody | None:
    """ Upload a document for knowledge extraction

     Accepts multipart/form-data with a 'file' field (max 50 MB). The document is uploaded to cloud
    storage and queued for extraction.

    Args:
        project_id (str): Project UUID
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbUploadDocumentOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,
body=body,

    )).parsed
