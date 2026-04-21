from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchResetAgentBody")



@_attrs_define
class WorkbenchResetAgentBody:
    """ 
        Attributes:
            agent_id (str):
            message (str):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    message: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        message = self.message

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "message": message,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        message = d.pop("message")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        workbench_reset_agent_body = cls(
            agent_id=agent_id,
            message=message,
            success=success,
            schema=schema,
        )

        return workbench_reset_agent_body

