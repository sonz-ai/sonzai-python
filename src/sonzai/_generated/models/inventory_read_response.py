from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.group_result import GroupResult
  from ..models.inventory_item import InventoryItem
  from ..models.inventory_read_response_totals import InventoryReadResponseTotals





T = TypeVar("T", bound="InventoryReadResponse")



@_attrs_define
class InventoryReadResponse:
    """ 
        Attributes:
            items (list[InventoryItem] | None):
            total_items (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            groups (list[GroupResult] | None | Unset):
            next_cursor (str | Unset):
            totals (InventoryReadResponseTotals | Unset):
     """

    items: list[InventoryItem] | None
    total_items: int
    schema: str | Unset = UNSET
    groups: list[GroupResult] | None | Unset = UNSET
    next_cursor: str | Unset = UNSET
    totals: InventoryReadResponseTotals | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.group_result import GroupResult
        from ..models.inventory_item import InventoryItem
        from ..models.inventory_read_response_totals import InventoryReadResponseTotals
        items: list[dict[str, Any]] | None
        if isinstance(self.items, list):
            items = []
            for items_type_0_item_data in self.items:
                items_type_0_item = items_type_0_item_data.to_dict()
                items.append(items_type_0_item)


        else:
            items = self.items

        total_items = self.total_items

        schema = self.schema

        groups: list[dict[str, Any]] | None | Unset
        if isinstance(self.groups, Unset):
            groups = UNSET
        elif isinstance(self.groups, list):
            groups = []
            for groups_type_0_item_data in self.groups:
                groups_type_0_item = groups_type_0_item_data.to_dict()
                groups.append(groups_type_0_item)


        else:
            groups = self.groups

        next_cursor = self.next_cursor

        totals: dict[str, Any] | Unset = UNSET
        if not isinstance(self.totals, Unset):
            totals = self.totals.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
            "total_items": total_items,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if groups is not UNSET:
            field_dict["groups"] = groups
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if totals is not UNSET:
            field_dict["totals"] = totals

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_result import GroupResult
        from ..models.inventory_item import InventoryItem
        from ..models.inventory_read_response_totals import InventoryReadResponseTotals
        d = dict(src_dict)
        def _parse_items(data: object) -> list[InventoryItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                items_type_0 = []
                _items_type_0 = data
                for items_type_0_item_data in (_items_type_0):
                    items_type_0_item = InventoryItem.from_dict(items_type_0_item_data)



                    items_type_0.append(items_type_0_item)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[InventoryItem] | None, data)

        items = _parse_items(d.pop("items"))


        total_items = d.pop("total_items")

        schema = d.pop("$schema", UNSET)

        def _parse_groups(data: object) -> list[GroupResult] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                groups_type_0 = []
                _groups_type_0 = data
                for groups_type_0_item_data in (_groups_type_0):
                    groups_type_0_item = GroupResult.from_dict(groups_type_0_item_data)



                    groups_type_0.append(groups_type_0_item)

                return groups_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[GroupResult] | None | Unset, data)

        groups = _parse_groups(d.pop("groups", UNSET))


        next_cursor = d.pop("next_cursor", UNSET)

        _totals = d.pop("totals", UNSET)
        totals: InventoryReadResponseTotals | Unset
        if isinstance(_totals,  Unset):
            totals = UNSET
        else:
            totals = InventoryReadResponseTotals.from_dict(_totals)




        inventory_read_response = cls(
            items=items,
            total_items=total_items,
            schema=schema,
            groups=groups,
            next_cursor=next_cursor,
            totals=totals,
        )

        return inventory_read_response

