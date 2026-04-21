from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.batch_inventory_item_properties import BatchInventoryItemProperties





T = TypeVar("T", bound="BatchInventoryItem")



@_attrs_define
class BatchInventoryItem:
    """ 
        Attributes:
            item_type (str):
            description (str | Unset):
            kb_node_id (str | Unset):
            properties (BatchInventoryItemProperties | Unset):
     """

    item_type: str
    description: str | Unset = UNSET
    kb_node_id: str | Unset = UNSET
    properties: BatchInventoryItemProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_inventory_item_properties import BatchInventoryItemProperties
        item_type = self.item_type

        description = self.description

        kb_node_id = self.kb_node_id

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "item_type": item_type,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if kb_node_id is not UNSET:
            field_dict["kb_node_id"] = kb_node_id
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_inventory_item_properties import BatchInventoryItemProperties
        d = dict(src_dict)
        item_type = d.pop("item_type")

        description = d.pop("description", UNSET)

        kb_node_id = d.pop("kb_node_id", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: BatchInventoryItemProperties | Unset
        if isinstance(_properties,  Unset):
            properties = UNSET
        else:
            properties = BatchInventoryItemProperties.from_dict(_properties)




        batch_inventory_item = cls(
            item_type=item_type,
            description=description,
            kb_node_id=kb_node_id,
            properties=properties,
        )

        return batch_inventory_item

