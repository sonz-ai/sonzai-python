from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.tool_schema_entry_parameters import ToolSchemaEntryParameters





T = TypeVar("T", bound="ToolSchemaEntry")



@_attrs_define
class ToolSchemaEntry:
    """ 
        Attributes:
            description (str): What the tool does
            endpoint (str): API endpoint for calling this tool
            name (str): Tool name
            parameters (ToolSchemaEntryParameters): JSON Schema describing the tool parameters
     """

    description: str
    endpoint: str
    name: str
    parameters: ToolSchemaEntryParameters





    def to_dict(self) -> dict[str, Any]:
        from ..models.tool_schema_entry_parameters import ToolSchemaEntryParameters
        description = self.description

        endpoint = self.endpoint

        name = self.name

        parameters = self.parameters.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "endpoint": endpoint,
            "name": name,
            "parameters": parameters,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_schema_entry_parameters import ToolSchemaEntryParameters
        d = dict(src_dict)
        description = d.pop("description")

        endpoint = d.pop("endpoint")

        name = d.pop("name")

        parameters = ToolSchemaEntryParameters.from_dict(d.pop("parameters"))




        tool_schema_entry = cls(
            description=description,
            endpoint=endpoint,
            name=name,
            parameters=parameters,
        )

        return tool_schema_entry

