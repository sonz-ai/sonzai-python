from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_node import KBNode





T = TypeVar("T", bound="KbListOrgNodesOutputBody")



@_attrs_define
class KbListOrgNodesOutputBody:
    """ 
        Attributes:
            nodes (list[KBNode] | None):
            total (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    nodes: list[KBNode] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_node import KBNode
        nodes: list[dict[str, Any]] | None
        if isinstance(self.nodes, list):
            nodes = []
            for nodes_type_0_item_data in self.nodes:
                nodes_type_0_item = nodes_type_0_item_data.to_dict()
                nodes.append(nodes_type_0_item)


        else:
            nodes = self.nodes

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "nodes": nodes,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_node import KBNode
        d = dict(src_dict)
        def _parse_nodes(data: object) -> list[KBNode] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                nodes_type_0 = []
                _nodes_type_0 = data
                for nodes_type_0_item_data in (_nodes_type_0):
                    nodes_type_0_item = KBNode.from_dict(nodes_type_0_item_data)



                    nodes_type_0.append(nodes_type_0_item)

                return nodes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBNode] | None, data)

        nodes = _parse_nodes(d.pop("nodes"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_list_org_nodes_output_body = cls(
            nodes=nodes,
            total=total,
            schema=schema,
        )

        return kb_list_org_nodes_output_body

