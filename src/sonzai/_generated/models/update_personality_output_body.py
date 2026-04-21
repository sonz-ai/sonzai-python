from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdatePersonalityOutputBody")



@_attrs_define
class UpdatePersonalityOutputBody:
    """ 
        Attributes:
            success (bool): Whether the update was applied
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        update_personality_output_body = cls(
            success=success,
            schema=schema,
        )

        return update_personality_output_body

