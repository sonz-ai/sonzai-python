from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_related_node_properties import KBRelatedNodeProperties





T = TypeVar("T", bound="KBRelatedNode")



@_attrs_define
class KBRelatedNode:
    """ 
        Attributes:
            edge (str):
            label (str):
            node_id (str):
            type_ (str):
            properties (KBRelatedNodeProperties | Unset):
     """

    edge: str
    label: str
    node_id: str
    type_: str
    properties: KBRelatedNodeProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_related_node_properties import KBRelatedNodeProperties
        edge = self.edge

        label = self.label

        node_id = self.node_id

        type_ = self.type_

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "edge": edge,
            "label": label,
            "node_id": node_id,
            "type": type_,
        })
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_related_node_properties import KBRelatedNodeProperties
        d = dict(src_dict)
        edge = d.pop("edge")

        label = d.pop("label")

        node_id = d.pop("node_id")

        type_ = d.pop("type")

        _properties = d.pop("properties", UNSET)
        properties: KBRelatedNodeProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = KBRelatedNodeProperties.from_dict(_properties)




        kb_related_node = cls(
            edge=edge,
            label=label,
            node_id=node_id,
            type_=type_,
            properties=properties,
        )

        return kb_related_node

