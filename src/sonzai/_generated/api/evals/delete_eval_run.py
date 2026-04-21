from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_eval_run_output_body import DeleteEvalRunOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    run_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/eval-runs/{run_id}".format(run_id=quote(str(run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteEvalRunOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteEvalRunOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteEvalRunOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteEvalRunOutputBody | ErrorModel]:
    """ Delete an eval run

     Permanently deletes an eval run and its associated data.

    Args:
        run_id (str): Eval run UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEvalRunOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        run_id=run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteEvalRunOutputBody | ErrorModel | None:
    """ Delete an eval run

     Permanently deletes an eval run and its associated data.

    Args:
        run_id (str): Eval run UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEvalRunOutputBody | ErrorModel
     """


    return sync_detailed(
        run_id=run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    run_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteEvalRunOutputBody | ErrorModel]:
    """ Delete an eval run

     Permanently deletes an eval run and its associated data.

    Args:
        run_id (str): Eval run UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteEvalRunOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        run_id=run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteEvalRunOutputBody | ErrorModel | None:
    """ Delete an eval run

     Permanently deletes an eval run and its associated data.

    Args:
        run_id (str): Eval run UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteEvalRunOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,

    )).parsed
