from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    project_id: str,
    rule_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{project_id}/knowledge/analytics/rules/{rule_id}".format(project_id=quote(str(project_id), safe=""),rule_id=quote(str(rule_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ErrorModel:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | ErrorModel]:
    """ Delete an analytics rule

     Removes an analytics rule from the knowledge base.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,

) -> Any | ErrorModel | None:
    """ Delete an analytics rule

     Removes an analytics rule from the knowledge base.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return sync_detailed(
        project_id=project_id,
rule_id=rule_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | ErrorModel]:
    """ Delete an analytics rule

     Removes an analytics rule from the knowledge base.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorModel]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
rule_id=rule_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: str,
    rule_id: str,
    *,
    client: AuthenticatedClient,

) -> Any | ErrorModel | None:
    """ Delete an analytics rule

     Removes an analytics rule from the knowledge base.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorModel
     """


    return (await asyncio_detailed(
        project_id=project_id,
rule_id=rule_id,
client=client,

    )).parsed
