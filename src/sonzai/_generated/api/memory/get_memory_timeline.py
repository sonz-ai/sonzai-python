from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_model import ErrorModel
from ...models.timeline_response import TimelineResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    agent_id: str,
    *,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["user_id"] = user_id

    params["instance_id"] = instance_id

    params["start"] = start

    params["end"] = end


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/agents/{agent_id}/memory/timeline".format(agent_id=quote(str(agent_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ErrorModel | TimelineResponse:
    if response.status_code == 200:
        response_200 = TimelineResponse.from_dict(response.json())



        return response_200

    response_default = ErrorModel.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ErrorModel | TimelineResponse]:
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
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,

) -> Response[ErrorModel | TimelineResponse]:
    """ Get memory timeline grouped by session

     Returns facts grouped by session within a date range, ordered by time. Defaults to the last 30 days.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope timeline
        instance_id (str | Unset): Optional instance ID for scoping
        start (str | Unset): Start date in YYYY-MM-DD format (default: 30 days ago)
        end (str | Unset): End date in YYYY-MM-DD format (default: today)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TimelineResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
start=start,
end=end,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,

) -> ErrorModel | TimelineResponse | None:
    """ Get memory timeline grouped by session

     Returns facts grouped by session within a date range, ordered by time. Defaults to the last 30 days.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope timeline
        instance_id (str | Unset): Optional instance ID for scoping
        start (str | Unset): Start date in YYYY-MM-DD format (default: 30 days ago)
        end (str | Unset): End date in YYYY-MM-DD format (default: today)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TimelineResponse
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,
start=start,
end=end,

    ).parsed

async def asyncio_detailed(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,

) -> Response[ErrorModel | TimelineResponse]:
    """ Get memory timeline grouped by session

     Returns facts grouped by session within a date range, ordered by time. Defaults to the last 30 days.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope timeline
        instance_id (str | Unset): Optional instance ID for scoping
        start (str | Unset): Start date in YYYY-MM-DD format (default: 30 days ago)
        end (str | Unset): End date in YYYY-MM-DD format (default: today)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorModel | TimelineResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
user_id=user_id,
instance_id=instance_id,
start=start,
end=end,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: str,
    *,
    client: AuthenticatedClient,
    user_id: str | Unset = UNSET,
    instance_id: str | Unset = UNSET,
    start: str | Unset = UNSET,
    end: str | Unset = UNSET,

) -> ErrorModel | TimelineResponse | None:
    """ Get memory timeline grouped by session

     Returns facts grouped by session within a date range, ordered by time. Defaults to the last 30 days.

    Args:
        agent_id (str): Agent UUID or URL-encoded agent name
        user_id (str | Unset): Optional user ID to scope timeline
        instance_id (str | Unset): Optional instance ID for scoping
        start (str | Unset): Start date in YYYY-MM-DD format (default: 30 days ago)
        end (str | Unset): End date in YYYY-MM-DD format (default: today)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorModel | TimelineResponse
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,
user_id=user_id,
instance_id=instance_id,
start=start,
end=end,

    )).parsed
