from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.add_content_request import AddContentRequest
from ...models.add_user_content_huma_output_body import AddUserContentHumaOutputBody
from ...models.error_model import ErrorModel
from typing import cast



def _get_kwargs(
    agent_id: str,
    user_id: str,
    *,
    body: AddContentRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/agents/{agent_id}/users/{user_id}/content".format(agent_id=quote(str(agent_id), safe=""),user_id=quote(str(user_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AddUserContentHumaOutputBody | ErrorModel:
    if response.status_code == 200:
        response_200 = AddUserContentHumaOutputBody.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AddUserContentHumaOutputBody | ErrorModel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: AddContentRequest,

) -> Response[AddUserContentHumaOutputBody | ErrorModel]:
    """ Add content for a user

     Queues raw content blocks (text, chat transcripts) for async LLM extraction. Returns a job ID for
    tracking.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to add content for
        body (AddContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddUserContentHumaOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: AddContentRequest,

) -> AddUserContentHumaOutputBody | ErrorModel | None:
    """ Add content for a user

     Queues raw content blocks (text, chat transcripts) for async LLM extraction. Returns a job ID for
    tracking.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to add content for
        body (AddContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddUserContentHumaOutputBody | ErrorModel
     """


    return sync_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: AddContentRequest,

) -> Response[AddUserContentHumaOutputBody | ErrorModel]:
    """ Add content for a user

     Queues raw content blocks (text, chat transcripts) for async LLM extraction. Returns a job ID for
    tracking.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to add content for
        body (AddContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddUserContentHumaOutputBody | ErrorModel]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    user_id: str,
    *,
    client: AuthenticatedClient,
    body: AddContentRequest,

) -> AddUserContentHumaOutputBody | ErrorModel | None:
    """ Add content for a user

     Queues raw content blocks (text, chat transcripts) for async LLM extraction. Returns a job ID for
    tracking.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str): User ID to add content for
        body (AddContentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddUserContentHumaOutputBody | ErrorModel
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
user_id=user_id,
client=client,
body=body,

    )).parsed
