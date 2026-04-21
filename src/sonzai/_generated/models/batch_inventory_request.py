from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.batch_inventory_item import BatchInventoryItem





T = TypeVar("T", bound="BatchInventoryRequest")



@_attrs_define
class BatchInventoryRequest:
    """ 
        Attributes:
            items (list[BatchInventoryItem] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
            project_id (str | Unset):
     """

    items: list[BatchInventoryItem] | None
    schema: str | Unset = UNSET
    project_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.batch_inventory_item import BatchInventoryItem
        items: list[dict[str, Any]] | None
        if isinstance(self.items, list):
            items = []
            for items_type_0_item_data in self.items:
                items_type_0_item = items_type_0_item_data.to_dict()
                items.append(items_type_0_item)


        else:
            items = self.items

        schema = self.schema

        project_id = self.project_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_inventory_item import BatchInventoryItem
        d = dict(src_dict)
        def _parse_items(data: object) -> list[BatchInventoryItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                items_type_0 = []
                _items_type_0 = data
                for items_type_0_item_data in (_items_type_0):
                    items_type_0_item = BatchInventoryItem.from_dict(items_type_0_item_data)



                    items_type_0.append(items_type_0_item)

                return items_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[BatchInventoryItem] | None, data)

        items = _parse_items(d.pop("items"))


        schema = d.pop("$schema", UNSET)

        project_id = d.pop("project_id", UNSET)

        batch_inventory_request = cls(
            items=items,
            schema=schema,
            project_id=project_id,
        )

        return batch_inventory_request

