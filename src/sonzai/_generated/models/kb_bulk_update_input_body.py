from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.bulk_update_entry import BulkUpdateEntry





T = TypeVar("T", bound="KbBulkUpdateInputBody")



@_attrs_define
class KbBulkUpdateInputBody:
    """ 
        Attributes:
            updates (list[BulkUpdateEntry] | None): Entries to upsert
            schema (str | Unset): A URL to the JSON Schema for this object.
            source (str | Unset): Source identifier (defaults to 'bulk_api')
     """

    updates: list[BulkUpdateEntry] | None
    schema: str | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_update_entry import BulkUpdateEntry
        updates: list[dict[str, Any]] | None
        if isinstance(self.updates, list):
            updates = []
            for updates_type_0_item_data in self.updates:
                updates_type_0_item = updates_type_0_item_data.to_dict()
                updates.append(updates_type_0_item)


        else:
            updates = self.updates

        schema = self.schema

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "updates": updates,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_update_entry import BulkUpdateEntry
        d = dict(src_dict)
        def _parse_updates(data: object) -> list[BulkUpdateEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                updates_type_0 = []
                _updates_type_0 = data
                for updates_type_0_item_data in (_updates_type_0):
                    updates_type_0_item = BulkUpdateEntry.from_dict(updates_type_0_item_data)



                    updates_type_0.append(updates_type_0_item)

                return updates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[BulkUpdateEntry] | None, data)

        updates = _parse_updates(d.pop("updates"))


        schema = d.pop("$schema", UNSET)

        source = d.pop("source", UNSET)

        kb_bulk_update_input_body = cls(
            updates=updates,
            schema=schema,
            source=source,
        )

        return kb_bulk_update_input_body

