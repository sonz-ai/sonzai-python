from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_eval_template_output_body import DeleteEvalTemplateOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    template_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/eval-templates/{template_id}".format(template_id=quote(str(template_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteEvalTemplateOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteEvalTemplateOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteEvalTemplateOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteEvalTemplateOutputBody | ErrorModel]:
    """ Delete an eval template

     Deletes an eval template. System templates cannot be deleted.

    Args:
        template_id (str): Template UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEvalTemplateOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        template_id=template_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteEvalTemplateOutputBody | ErrorModel | None:
    """ Delete an eval template

     Deletes an eval template. System templates cannot be deleted.

    Args:
        template_id (str): Template UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEvalTemplateOutputBody | ErrorModel
     """


    return sync_detailed(
        template_id=template_id,
client=client,

    ).parsed

async def asyncio_detailed(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteEvalTemplateOutputBody | ErrorModel]:
    """ Delete an eval template

     Deletes an eval template. System templates cannot be deleted.

    Args:
        template_id (str): Template UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEvalTemplateOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        template_id=template_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    template_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteEvalTemplateOutputBody | ErrorModel | None:
    """ Delete an eval template

     Deletes an eval template. System templates cannot be deleted.

    Args:
        template_id (str): Template UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEvalTemplateOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        template_id=template_id,
client=client,

    )).parsed
