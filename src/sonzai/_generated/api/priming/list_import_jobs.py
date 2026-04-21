from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.list_import_jobs_output_body import ListImportJobsOutputBody
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    limit: int | Unset = 20,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/users/imports".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | ListImportJobsOutputBody:
    if response.status_code == 200:
        response_200 = ListImportJobsOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | ListImportJobsOutputBody]:
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
    limit: int | Unset = 20,

) -> Response[ErrorModel | ListImportJobsOutputBody]:
    """ List import jobs for an agent

     Returns recent import jobs for the given agent, ordered by creation time.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max jobs to return Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListImportJobsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,

) -> ErrorModel | ListImportJobsOutputBody | None:
    """ List import jobs for an agent

     Returns recent import jobs for the given agent, ordered by creation time.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max jobs to return Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListImportJobsOutputBody
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,

) -> Response[ErrorModel | ListImportJobsOutputBody]:
    """ List import jobs for an agent

     Returns recent import jobs for the given agent, ordered by creation time.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max jobs to return Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | ListImportJobsOutputBody]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,

) -> ErrorModel | ListImportJobsOutputBody | None:
    """ List import jobs for an agent

     Returns recent import jobs for the given agent, ordered by creation time.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        limit (int | Unset): Max jobs to return Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | ListImportJobsOutputBody
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
limit=limit,

    )).parsed
