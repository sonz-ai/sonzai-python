from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.tool_schema_entry import ToolSchemaEntry





T = TypeVar("T", bound="GetToolSchemasOutputBody")



@_attrs_define
class GetToolSchemasOutputBody:
    """ 
        Attributes:
            tools (list[ToolSchemaEntry] | None): Available tools for this agent
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    tools: list[ToolSchemaEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.tool_schema_entry import ToolSchemaEntry
        tools: list[dict[str, Any]] | None
        if isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item = tools_type_0_item_data.to_dict()
                tools.append(tools_type_0_item)


        else:
            tools = self.tools

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "tools": tools,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_schema_entry import ToolSchemaEntry
        d = dict(src_dict)
        def _parse_tools(data: object) -> list[ToolSchemaEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in (_tools_type_0):
                    tools_type_0_item = ToolSchemaEntry.from_dict(tools_type_0_item_data)



                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ToolSchemaEntry] | None, data)

        tools = _parse_tools(d.pop("tools"))


        schema = d.pop("$schema", UNSET)

        get_tool_schemas_output_body = cls(
            tools=tools,
            schema=schema,
        )

        return get_tool_schemas_output_body

