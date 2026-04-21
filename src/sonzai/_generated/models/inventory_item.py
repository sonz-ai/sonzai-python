from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.inventory_item_market_properties import InventoryItemMarketProperties
  from ..models.inventory_item_user_properties import InventoryItemUserProperties





T = TypeVar("T", bound="InventoryItem")



@_attrs_define
class InventoryItem:
    """ 
        Attributes:
            fact_id (str):
            item_label (str):
            user_properties (InventoryItemUserProperties):
            gain_loss (float | Unset):
            kb_node_id (str | Unset):
            market_properties (InventoryItemMarketProperties | Unset):
     """

    fact_id: str
    item_label: str
    user_properties: InventoryItemUserProperties
    gain_loss: float | Unset = UNSET
    kb_node_id: str | Unset = UNSET
    market_properties: InventoryItemMarketProperties | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_item_market_properties import InventoryItemMarketProperties
        from ..models.inventory_item_user_properties import InventoryItemUserProperties
        fact_id = self.fact_id

        item_label = self.item_label

        user_properties = self.user_properties.to_dict()

        gain_loss = self.gain_loss

        kb_node_id = self.kb_node_id

        market_properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.market_properties, Unset):
            market_properties = self.market_properties.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fact_id": fact_id,
            "item_label": item_label,
            "user_properties": user_properties,
        })
        if gain_loss is not UNSET:
            field_dict["gain_loss"] = gain_loss
        if kb_node_id is not UNSET:
            field_dict["kb_node_id"] = kb_node_id
        if market_properties is not UNSET:
            field_dict["market_properties"] = market_properties

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_item_market_properties import InventoryItemMarketProperties
        from ..models.inventory_item_user_properties import InventoryItemUserProperties
        d = dict(src_dict)
        fact_id = d.pop("fact_id")

        item_label = d.pop("item_label")

        user_properties = InventoryItemUserProperties.from_dict(d.pop("user_properties"))




        gain_loss = d.pop("gain_loss", UNSET)

        kb_node_id = d.pop("kb_node_id", UNSET)

        _market_properties = d.pop("market_properties", UNSET)
        market_properties: InventoryItemMarketProperties | Unset
        if isinstance(_market_properties,  Unset):
            market_properties = UNSET
        else:
            market_properties = InventoryItemMarketProperties.from_dict(_market_properties)




        inventory_item = cls(
            fact_id=fact_id,
            item_label=item_label,
            user_properties=user_properties,
            gain_loss=gain_loss,
            kb_node_id=kb_node_id,
            market_properties=market_properties,
        )

        return inventory_item

