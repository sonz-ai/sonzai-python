from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateInstanceInputBody")



@_attrs_define
class UpdateInstanceInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Updated description
            name (str | Unset): Updated instance name
            status (str | Unset): Updated status (active, archived)
     """

    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    status: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        description = self.description

        name = self.name

        status = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        update_instance_input_body = cls(
            schema=schema,
            description=description,
            name=name,
            status=status,
        )

        return update_instance_input_body

