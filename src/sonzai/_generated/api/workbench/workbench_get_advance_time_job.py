from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.workbench_advance_time_job_body import WorkbenchAdvanceTimeJobBody
from typing import cast



def _get_kwargs(
    job_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workbench/advance-time/jobs/{job_id}".format(job_id=quote(str(job_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | WorkbenchAdvanceTimeJobBody:
    if response.status_code == 200:
        response_200 = WorkbenchAdvanceTimeJobBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | WorkbenchAdvanceTimeJobBody]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | WorkbenchAdvanceTimeJobBody]:
    """ Get async advance-time job status

     Returns the current state of an async advance-time job started via POST /workbench/advance-time with
    async=true. Status is one of 'running', 'succeeded', or 'failed'. Job state lives in Redis with a
    30-minute TTL — poll within that window.

    Args:
        job_id (str): Async advance-time job UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | WorkbenchAdvanceTimeJobBody]
     """


    kwargs = _get_kwargs(
        job_id=job_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    job_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | WorkbenchAdvanceTimeJobBody | None:
    """ Get async advance-time job status

     Returns the current state of an async advance-time job started via POST /workbench/advance-time with
    async=true. Status is one of 'running', 'succeeded', or 'failed'. Job state lives in Redis with a
    30-minute TTL — poll within that window.

    Args:
        job_id (str): Async advance-time job UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | WorkbenchAdvanceTimeJobBody
     """


    return sync_detailed(
        job_id=job_id,
client=client,

    ).parsed

async def asyncio_detailed(
    job_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | WorkbenchAdvanceTimeJobBody]:
    """ Get async advance-time job status

     Returns the current state of an async advance-time job started via POST /workbench/advance-time with
    async=true. Status is one of 'running', 'succeeded', or 'failed'. Job state lives in Redis with a
    30-minute TTL — poll within that window.

    Args:
        job_id (str): Async advance-time job UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | WorkbenchAdvanceTimeJobBody]
     """


    kwargs = _get_kwargs(
        job_id=job_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    job_id: str,
    *,
    client: AuthenticatedClient,

) -> ErrorModel | WorkbenchAdvanceTimeJobBody | None:
    """ Get async advance-time job status

     Returns the current state of an async advance-time job started via POST /workbench/advance-time with
    async=true. Status is one of 'running', 'succeeded', or 'failed'. Job state lives in Redis with a
    30-minute TTL — poll within that window.

    Args:
        job_id (str): Async advance-time job UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | WorkbenchAdvanceTimeJobBody
     """


    return (await asyncio_detailed(
        job_id=job_id,
client=client,

    )).parsed
