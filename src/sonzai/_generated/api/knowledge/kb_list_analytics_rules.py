from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.kb_list_analytics_rules_output_body import KbListAnalyticsRulesOutputBody
from typing import cast



def _get_kwargs(
    project_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{project_id}/knowledge/analytics/rules".format(project_id=quote(str(project_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | KbListAnalyticsRulesOutputBody:
    if response.status_code == 200:
        response_200 = KbListAnalyticsRulesOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | KbListAnalyticsRulesOutputBody]:
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

) -> Response[ErrorModel | KbListAnalyticsRulesOutputBody]:
    """ List analytics rules

     Returns all analytics rules defined for the project's knowledge base.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListAnalyticsRulesOutputBody]
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

) -> ErrorModel | KbListAnalyticsRulesOutputBody | None:
    """ List analytics rules

     Returns all analytics rules defined for the project's knowledge base.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListAnalyticsRulesOutputBody
     """


    return sync_detailed(
        project_id=project_id,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,

) -> Response[ErrorModel | KbListAnalyticsRulesOutputBody]:
    """ List analytics rules

     Returns all analytics rules defined for the project's knowledge base.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | KbListAnalyticsRulesOutputBody]
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

) -> ErrorModel | KbListAnalyticsRulesOutputBody | None:
    """ List analytics rules

     Returns all analytics rules defined for the project's knowledge base.

    Args:
        project_id (str): Project UUID

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | KbListAnalyticsRulesOutputBody
     """


    return (await asyncio_detailed(
        project_id=project_id,
client=client,

    )).parsed
