from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.wakeup_entry import WakeupEntry





T = TypeVar("T", bound="WakeupsResponse")



@_attrs_define
class WakeupsResponse:
    """ 
        Attributes:
            wakeups (list[WakeupEntry] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    wakeups: list[WakeupEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.wakeup_entry import WakeupEntry
        wakeups: list[dict[str, Any]] | None
        if isinstance(self.wakeups, list):
            wakeups = []
            for wakeups_type_0_item_data in self.wakeups:
                wakeups_type_0_item = wakeups_type_0_item_data.to_dict()
                wakeups.append(wakeups_type_0_item)


        else:
            wakeups = self.wakeups

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "wakeups": wakeups,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.wakeup_entry import WakeupEntry
        d = dict(src_dict)
        def _parse_wakeups(data: object) -> list[WakeupEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                wakeups_type_0 = []
                _wakeups_type_0 = data
                for wakeups_type_0_item_data in (_wakeups_type_0):
                    wakeups_type_0_item = WakeupEntry.from_dict(wakeups_type_0_item_data)



                    wakeups_type_0.append(wakeups_type_0_item)

                return wakeups_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WakeupEntry] | None, data)

        wakeups = _parse_wakeups(d.pop("wakeups"))


        schema = d.pop("$schema", UNSET)

        wakeups_response = cls(
            wakeups=wakeups,
            schema=schema,
        )

        return wakeups_response

