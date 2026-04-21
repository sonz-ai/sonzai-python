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






T = TypeVar("T", bound="AgentInstance")



@_attrs_define
class AgentInstance:
    """ 
        Attributes:
            agent_id (str):
            created_at (datetime.datetime):
            instance_id (str):
            is_default (bool):
            name (str):
            status (str):
            updated_at (datetime.datetime):
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset):
     """

    agent_id: str
    created_at: datetime.datetime
    instance_id: str
    is_default: bool
    name: str
    status: str
    updated_at: datetime.datetime
    schema: str | Unset = UNSET
    description: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        instance_id = self.instance_id

        is_default = self.is_default

        name = self.name

        status = self.status

        updated_at = self.updated_at.isoformat()

        schema = self.schema

        description = self.description


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "instance_id": instance_id,
            "is_default": is_default,
            "name": name,
            "status": status,
            "updated_at": updated_at,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = isoparse(d.pop("created_at"))




        instance_id = d.pop("instance_id")

        is_default = d.pop("is_default")

        name = d.pop("name")

        status = d.pop("status")

        updated_at = isoparse(d.pop("updated_at"))




        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        agent_instance = cls(
            agent_id=agent_id,
            created_at=created_at,
            instance_id=instance_id,
            is_default=is_default,
            name=name,
            status=status,
            updated_at=updated_at,
            schema=schema,
            description=description,
        )

        return agent_instance

