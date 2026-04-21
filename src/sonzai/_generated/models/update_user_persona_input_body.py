from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateUserPersonaInputBody")



@_attrs_define
class UpdateUserPersonaInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Free-text description
            name (str | Unset): Persona display name
            style (str | Unset): Conversational style
     """

    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    style: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        description = self.description

        name = self.name

        style = self.style


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        style = d.pop("style", UNSET)

        update_user_persona_input_body = cls(
            schema=schema,
            description=description,
            name=name,
            style=style,
        )

        return update_user_persona_input_body

