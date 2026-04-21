from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ServiceUsageByOp")



@_attrs_define
class ServiceUsageByOp:
    """ 
        Attributes:
            charge_usd (float):
            count (int):
            operation (str):
            unit_price_usd (float):
     """

    charge_usd: float
    count: int
    operation: str
    unit_price_usd: float





    def to_dict(self) -> dict[str, Any]:
        charge_usd = self.charge_usd

        count = self.count

        operation = self.operation

        unit_price_usd = self.unit_price_usd


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "chargeUsd": charge_usd,
            "count": count,
            "operation": operation,
            "unitPriceUsd": unit_price_usd,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        charge_usd = d.pop("chargeUsd")

        count = d.pop("count")

        operation = d.pop("operation")

        unit_price_usd = d.pop("unitPriceUsd")

        service_usage_by_op = cls(
            charge_usd=charge_usd,
            count=count,
            operation=operation,
            unit_price_usd=unit_price_usd,
        )

        return service_usage_by_op

