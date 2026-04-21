from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CustomToolDefinition")



@_attrs_define
class CustomToolDefinition:
    """ 
        Attributes:
            description (str):
            name (str):
            parameters (Any):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    description: str
    name: str
    parameters: Any
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        parameters = self.parameters

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "name": name,
            "parameters": parameters,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        parameters = d.pop("parameters")

        schema = d.pop("$schema", UNSET)

        custom_tool_definition = cls(
            description=description,
            name=name,
            parameters=parameters,
            schema=schema,
        )

        return custom_tool_definition

