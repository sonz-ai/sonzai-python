from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SetAgentStatusOutputBody")



@_attrs_define
class SetAgentStatusOutputBody:
    """ 
        Attributes:
            agent_id (str):
            is_active (bool):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    is_active: bool
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        is_active = self.is_active

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "is_active": is_active,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        is_active = d.pop("is_active")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        set_agent_status_output_body = cls(
            agent_id=agent_id,
            is_active=is_active,
            success=success,
            schema=schema,
        )

        return set_agent_status_output_body

