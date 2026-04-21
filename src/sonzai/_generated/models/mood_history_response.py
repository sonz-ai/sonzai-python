from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.mood_history_entry import MoodHistoryEntry





T = TypeVar("T", bound="MoodHistoryResponse")



@_attrs_define
class MoodHistoryResponse:
    """ 
        Attributes:
            entries (list[MoodHistoryEntry] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    entries: list[MoodHistoryEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.mood_history_entry import MoodHistoryEntry
        entries: list[dict[str, Any]] | None
        if isinstance(self.entries, list):
            entries = []
            for entries_type_0_item_data in self.entries:
                entries_type_0_item = entries_type_0_item_data.to_dict()
                entries.append(entries_type_0_item)


        else:
            entries = self.entries

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "entries": entries,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mood_history_entry import MoodHistoryEntry
        d = dict(src_dict)
        def _parse_entries(data: object) -> list[MoodHistoryEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entries_type_0 = []
                _entries_type_0 = data
                for entries_type_0_item_data in (_entries_type_0):
                    entries_type_0_item = MoodHistoryEntry.from_dict(entries_type_0_item_data)



                    entries_type_0.append(entries_type_0_item)

                return entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[MoodHistoryEntry] | None, data)

        entries = _parse_entries(d.pop("entries"))


        schema = d.pop("$schema", UNSET)

        mood_history_response = cls(
            entries=entries,
            schema=schema,
        )

        return mood_history_response

