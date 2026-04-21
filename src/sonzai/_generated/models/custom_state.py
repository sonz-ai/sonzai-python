from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="CustomState")



@_attrs_define
class CustomState:
    """ 
        Attributes:
            agent_id (str):
            content_type (str):
            created_at (datetime.datetime):
            instance_id (None | str):
            key (str):
            scope (str):
            state_id (str):
            updated_at (datetime.datetime):
            user_id (None | str):
            value (Any):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    content_type: str
    created_at: datetime.datetime
    instance_id: None | str
    key: str
    scope: str
    state_id: str
    updated_at: datetime.datetime
    user_id: None | str
    value: Any
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        content_type = self.content_type

        created_at = self.created_at.isoformat()

        instance_id: None | str
        instance_id = self.instance_id

        key = self.key

        scope = self.scope

        state_id = self.state_id

        updated_at = self.updated_at.isoformat()

        user_id: None | str
        user_id = self.user_id

        value = self.value

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "content_type": content_type,
            "created_at": created_at,
            "instance_id": instance_id,
            "key": key,
            "scope": scope,
            "state_id": state_id,
            "updated_at": updated_at,
            "user_id": user_id,
            "value": value,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        content_type = d.pop("content_type")

        created_at = isoparse(d.pop("created_at"))




        def _parse_instance_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        instance_id = _parse_instance_id(d.pop("instance_id"))


        key = d.pop("key")

        scope = d.pop("scope")

        state_id = d.pop("state_id")

        updated_at = isoparse(d.pop("updated_at"))




        def _parse_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_id = _parse_user_id(d.pop("user_id"))


        value = d.pop("value")

        schema = d.pop("$schema", UNSET)

        custom_state = cls(
            agent_id=agent_id,
            content_type=content_type,
            created_at=created_at,
            instance_id=instance_id,
            key=key,
            scope=scope,
            state_id=state_id,
            updated_at=updated_at,
            user_id=user_id,
            value=value,
            schema=schema,
        )

        return custom_state

