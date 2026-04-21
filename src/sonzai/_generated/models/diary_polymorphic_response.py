from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.diary_entry import DiaryEntry





T = TypeVar("T", bound="DiaryPolymorphicResponse")



@_attrs_define
class DiaryPolymorphicResponse:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            entries (list[DiaryEntry] | None | Unset):
            entry (DiaryEntry | Unset):
     """

    schema: str | Unset = UNSET
    entries: list[DiaryEntry] | None | Unset = UNSET
    entry: DiaryEntry | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.diary_entry import DiaryEntry
        schema = self.schema

        entries: list[dict[str, Any]] | None | Unset
        if isinstance(self.entries, Unset):
            entries = UNSET
        elif isinstance(self.entries, list):
            entries = []
            for entries_type_0_item_data in self.entries:
                entries_type_0_item = entries_type_0_item_data.to_dict()
                entries.append(entries_type_0_item)


        else:
            entries = self.entries

        entry: dict[str, Any] | Unset = UNSET
        if not isinstance(self.entry, Unset):
            entry = self.entry.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if entries is not UNSET:
            field_dict["entries"] = entries
        if entry is not UNSET:
            field_dict["entry"] = entry

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.diary_entry import DiaryEntry
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        def _parse_entries(data: object) -> list[DiaryEntry] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entries_type_0 = []
                _entries_type_0 = data
                for entries_type_0_item_data in (_entries_type_0):
                    entries_type_0_item = DiaryEntry.from_dict(entries_type_0_item_data)



                    entries_type_0.append(entries_type_0_item)

                return entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DiaryEntry] | None | Unset, data)

        entries = _parse_entries(d.pop("entries", UNSET))


        _entry = d.pop("entry", UNSET)
        entry: DiaryEntry | Unset
        if isinstance(_entry,  Unset):
            entry = UNSET
        else:
            entry = DiaryEntry.from_dict(_entry)




        diary_polymorphic_response = cls(
            schema=schema,
            entries=entries,
            entry=entry,
        )

        return diary_polymorphic_response

