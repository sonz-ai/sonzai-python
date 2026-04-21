from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateCustomToolInputBody")



@_attrs_define
class CreateCustomToolInputBody:
    """ 
        Attributes:
            description (str): Tool description
            name (str): Tool name (must not start with sonzai_)
            schema (str | Unset): A URL to the JSON Schema for this object.
            parameters (Any | Unset): JSON Schema for tool parameters
     """

    description: str
    name: str
    schema: str | Unset = UNSET
    parameters: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        schema = self.schema

        parameters = self.parameters


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        parameters = d.pop("parameters", UNSET)

        create_custom_tool_input_body = cls(
            description=description,
            name=name,
            schema=schema,
            parameters=parameters,
        )

        return create_custom_tool_input_body

