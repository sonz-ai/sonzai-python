from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_analytics_rule import KBAnalyticsRule
from typing import cast



def _get_kwargs(
    project_id: str,
    rule_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/rules/{rule_id}".format(project_id=quote(str(project_id), safe=""),rule_id=quote(str(rule_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KBAnalyticsRule:
    if response.status_code == 200:
        response_200 = KBAnalyticsRule.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KBAnalyticsRule]:
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

) -> Response[ErrorModel | KBAnalyticsRule]:
    """ Get an analytics rule

     Returns a specific analytics rule by ID.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBAnalyticsRule]
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

) -> ErrorModel | KBAnalyticsRule | None:
    """ Get an analytics rule

     Returns a specific analytics rule by ID.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBAnalyticsRule
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

) -> Response[ErrorModel | KBAnalyticsRule]:
    """ Get an analytics rule

     Returns a specific analytics rule by ID.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KBAnalyticsRule]
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

) -> ErrorModel | KBAnalyticsRule | None:
    """ Get an analytics rule

     Returns a specific analytics rule by ID.

    Args:
        project_id (str): Project UUID
        rule_id (str): Rule UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KBAnalyticsRule
     """


    return (await asyncio_detailed(
        project_id=project_id,
rule_id=rule_id,
client=client,

    )).parsed
