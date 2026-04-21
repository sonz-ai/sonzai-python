from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.service_usage_by_op import ServiceUsageByOp





T = TypeVar("T", bound="ServiceUsageSummary")



@_attrs_define
class ServiceUsageSummary:
    """ 
        Attributes:
            by_operation (list[ServiceUsageByOp] | None):
            month (str):
            total_charge_usd (float):
            total_events (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    by_operation: list[ServiceUsageByOp] | None
    month: str
    total_charge_usd: float
    total_events: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.service_usage_by_op import ServiceUsageByOp
        by_operation: list[dict[str, Any]] | None
        if isinstance(self.by_operation, list):
            by_operation = []
            for by_operation_type_0_item_data in self.by_operation:
                by_operation_type_0_item = by_operation_type_0_item_data.to_dict()
                by_operation.append(by_operation_type_0_item)


        else:
            by_operation = self.by_operation

        month = self.month

        total_charge_usd = self.total_charge_usd

        total_events = self.total_events

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "byOperation": by_operation,
            "month": month,
            "totalChargeUsd": total_charge_usd,
            "totalEvents": total_events,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_usage_by_op import ServiceUsageByOp
        d = dict(src_dict)
        def _parse_by_operation(data: object) -> list[ServiceUsageByOp] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_operation_type_0 = []
                _by_operation_type_0 = data
                for by_operation_type_0_item_data in (_by_operation_type_0):
                    by_operation_type_0_item = ServiceUsageByOp.from_dict(by_operation_type_0_item_data)



                    by_operation_type_0.append(by_operation_type_0_item)

                return by_operation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ServiceUsageByOp] | None, data)

        by_operation = _parse_by_operation(d.pop("byOperation"))


        month = d.pop("month")

        total_charge_usd = d.pop("totalChargeUsd")

        total_events = d.pop("totalEvents")

        schema = d.pop("$schema", UNSET)

        service_usage_summary = cls(
            by_operation=by_operation,
            month=month,
            total_charge_usd=total_charge_usd,
            total_events=total_events,
            schema=schema,
        )

        return service_usage_summary

