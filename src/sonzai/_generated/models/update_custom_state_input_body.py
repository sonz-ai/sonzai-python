from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateCustomStateInputBody")



@_attrs_define
class UpdateCustomStateInputBody:
    """ 
        Attributes:
            value (Any): Updated value
            schema (str | Unset): A URL to the JSON Schema for this object.
            content_type (str | Unset): Updated content type
     """

    value: Any
    schema: str | Unset = UNSET
    content_type: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        value = self.value

        schema = self.schema

        content_type = self.content_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "value": value,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if content_type is not UNSET:
            field_dict["content_type"] = content_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        schema = d.pop("$schema", UNSET)

        content_type = d.pop("content_type", UNSET)

        update_custom_state_input_body = cls(
            value=value,
            schema=schema,
            content_type=content_type,
        )

        return update_custom_state_input_body

