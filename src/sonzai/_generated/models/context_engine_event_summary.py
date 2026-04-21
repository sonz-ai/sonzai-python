from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.context_engine_event_by_type import ContextEngineEventByType





T = TypeVar("T", bound="ContextEngineEventSummary")



@_attrs_define
class ContextEngineEventSummary:
    """ 
        Attributes:
            by_type (list[ContextEngineEventByType] | None):
            month (str):
            total_charge_usd (float):
            total_events (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    by_type: list[ContextEngineEventByType] | None
    month: str
    total_charge_usd: float
    total_events: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.context_engine_event_by_type import ContextEngineEventByType
        by_type: list[dict[str, Any]] | None
        if isinstance(self.by_type, list):
            by_type = []
            for by_type_type_0_item_data in self.by_type:
                by_type_type_0_item = by_type_type_0_item_data.to_dict()
                by_type.append(by_type_type_0_item)


        else:
            by_type = self.by_type

        month = self.month

        total_charge_usd = self.total_charge_usd

        total_events = self.total_events

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "byType": by_type,
            "month": month,
            "totalChargeUsd": total_charge_usd,
            "totalEvents": total_events,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context_engine_event_by_type import ContextEngineEventByType
        d = dict(src_dict)
        def _parse_by_type(data: object) -> list[ContextEngineEventByType] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_type_type_0 = []
                _by_type_type_0 = data
                for by_type_type_0_item_data in (_by_type_type_0):
                    by_type_type_0_item = ContextEngineEventByType.from_dict(by_type_type_0_item_data)



                    by_type_type_0.append(by_type_type_0_item)

                return by_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ContextEngineEventByType] | None, data)

        by_type = _parse_by_type(d.pop("byType"))


        month = d.pop("month")

        total_charge_usd = d.pop("totalChargeUsd")

        total_events = d.pop("totalEvents")

        schema = d.pop("$schema", UNSET)

        context_engine_event_summary = cls(
            by_type=by_type,
            month=month,
            total_charge_usd=total_charge_usd,
            total_events=total_events,
            schema=schema,
        )

        return context_engine_event_summary

