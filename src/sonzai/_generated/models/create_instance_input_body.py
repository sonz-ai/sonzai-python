from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateInstanceInputBody")



@_attrs_define
class CreateInstanceInputBody:
    """ 
        Attributes:
            name (str): Instance display name
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Optional description
     """

    name: str
    schema: str | Unset = UNSET
    description: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        schema = self.schema

        description = self.description


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        create_instance_input_body = cls(
            name=name,
            schema=schema,
            description=description,
        )

        return create_instance_input_body

