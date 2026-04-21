from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="InsertEdgeDetail")



@_attrs_define
class InsertEdgeDetail:
    """ 
        Attributes:
            edge_id (str):
            from_node (str):
            relation (str):
            to_node (str):
     """

    edge_id: str
    from_node: str
    relation: str
    to_node: str





    def to_dict(self) -> dict[str, Any]:
        edge_id = self.edge_id

        from_node = self.from_node

        relation = self.relation

        to_node = self.to_node


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "edge_id": edge_id,
            "from_node": from_node,
            "relation": relation,
            "to_node": to_node,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        edge_id = d.pop("edge_id")

        from_node = d.pop("from_node")

        relation = d.pop("relation")

        to_node = d.pop("to_node")

        insert_edge_detail = cls(
            edge_id=edge_id,
            from_node=from_node,
            relation=relation,
            to_node=to_node,
        )

        return insert_edge_detail

