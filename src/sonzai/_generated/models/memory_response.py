from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.memory_node import MemoryNode
  from ..models.memory_response_contents import MemoryResponseContents





T = TypeVar("T", bound="MemoryResponse")



@_attrs_define
class MemoryResponse:
    """ 
        Attributes:
            nodes (list[MemoryNode] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
            contents (MemoryResponseContents | Unset):
     """

    nodes: list[MemoryNode] | None
    schema: str | Unset = UNSET
    contents: MemoryResponseContents | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.memory_node import MemoryNode
        from ..models.memory_response_contents import MemoryResponseContents
        nodes: list[dict[str, Any]] | None
        if isinstance(self.nodes, list):
            nodes = []
            for nodes_type_0_item_data in self.nodes:
                nodes_type_0_item = nodes_type_0_item_data.to_dict()
                nodes.append(nodes_type_0_item)


        else:
            nodes = self.nodes

        schema = self.schema

        contents: dict[str, Any] | Unset = UNSET
        if not isinstance(self.contents, Unset):
            contents = self.contents.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "nodes": nodes,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if contents is not UNSET:
            field_dict["contents"] = contents

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.memory_node import MemoryNode
        from ..models.memory_response_contents import MemoryResponseContents
        d = dict(src_dict)
        def _parse_nodes(data: object) -> list[MemoryNode] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                nodes_type_0 = []
                _nodes_type_0 = data
                for nodes_type_0_item_data in (_nodes_type_0):
                    nodes_type_0_item = MemoryNode.from_dict(nodes_type_0_item_data)



                    nodes_type_0.append(nodes_type_0_item)

                return nodes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[MemoryNode] | None, data)

        nodes = _parse_nodes(d.pop("nodes"))


        schema = d.pop("$schema", UNSET)

        _contents = d.pop("contents", UNSET)
        contents: MemoryResponseContents | Unset
        if isinstance(_contents,  Unset):
            contents = UNSET
        else:
            contents = MemoryResponseContents.from_dict(_contents)




        memory_response = cls(
            nodes=nodes,
            schema=schema,
            contents=contents,
        )

        return memory_response

