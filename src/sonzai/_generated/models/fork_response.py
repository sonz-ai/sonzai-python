from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ForkResponse")



@_attrs_define
class ForkResponse:
    """ 
        Attributes:
            agent_id (str):
            name (str):
            source_agent_id (str):
            status (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    agent_id: str
    name: str
    source_agent_id: str
    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        name = self.name

        source_agent_id = self.source_agent_id

        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "name": name,
            "source_agent_id": source_agent_id,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        name = d.pop("name")

        source_agent_id = d.pop("source_agent_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        fork_response = cls(
            agent_id=agent_id,
            name=name,
            source_agent_id=source_agent_id,
            status=status,
            schema=schema,
        )

        return fork_response

