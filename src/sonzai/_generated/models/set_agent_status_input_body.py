from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SetAgentStatusInputBody")



@_attrs_define
class SetAgentStatusInputBody:
    """ 
        Attributes:
            is_active (bool): Whether the agent should be active
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    is_active: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        is_active = self.is_active

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "is_active": is_active,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_active = d.pop("is_active")

        schema = d.pop("$schema", UNSET)

        set_agent_status_input_body = cls(
            is_active=is_active,
            schema=schema,
        )

        return set_agent_status_input_body

