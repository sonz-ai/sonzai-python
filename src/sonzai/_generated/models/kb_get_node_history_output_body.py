from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_node_history import KBNodeHistory





T = TypeVar("T", bound="KbGetNodeHistoryOutputBody")



@_attrs_define
class KbGetNodeHistoryOutputBody:
    """ 
        Attributes:
            history (list[KBNodeHistory] | None): Version history entries
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    history: list[KBNodeHistory] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_node_history import KBNodeHistory
        history: list[dict[str, Any]] | None
        if isinstance(self.history, list):
            history = []
            for history_type_0_item_data in self.history:
                history_type_0_item = history_type_0_item_data.to_dict()
                history.append(history_type_0_item)


        else:
            history = self.history

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "history": history,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_node_history import KBNodeHistory
        d = dict(src_dict)
        def _parse_history(data: object) -> list[KBNodeHistory] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                history_type_0 = []
                _history_type_0 = data
                for history_type_0_item_data in (_history_type_0):
                    history_type_0_item = KBNodeHistory.from_dict(history_type_0_item_data)



                    history_type_0.append(history_type_0_item)

                return history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBNodeHistory] | None, data)

        history = _parse_history(d.pop("history"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_get_node_history_output_body = cls(
            history=history,
            total=total,
            schema=schema,
        )

        return kb_get_node_history_output_body

