from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RegenerateAvatarInputBody")



@_attrs_define
class RegenerateAvatarInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            style (str | Unset): Avatar art style override
     """

    schema: str | Unset = UNSET
    style: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        style = self.style


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        style = d.pop("style", UNSET)

        regenerate_avatar_input_body = cls(
            schema=schema,
            style=style,
        )

        return regenerate_avatar_input_body

