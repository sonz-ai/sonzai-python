from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_project_output_body import DeleteProjectOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    project_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{project_id}".format(project_id=quote(str(project_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteProjectOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = DeleteProjectOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteProjectOutputBody | ErrorModel]:
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

) -> Response[DeleteProjectOutputBody | ErrorModel]:
    """ Delete a project

     Deactivates all agents under the project, then deletes it. Org-admin only.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteProjectOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteProjectOutputBody | ErrorModel | None:
    """ Delete a project

     Deactivates all agents under the project, then deletes it. Org-admin only.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteProjectOutputBody | ErrorModel
     """


    return sync_detailed(
        project_id=project_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteProjectOutputBody | ErrorModel]:
    """ Delete a project

     Deactivates all agents under the project, then deletes it. Org-admin only.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteProjectOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,

) -> DeleteProjectOutputBody | ErrorModel | None:
    """ Delete a project

     Deactivates all agents under the project, then deletes it. Org-admin only.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteProjectOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,

    )).parsed
