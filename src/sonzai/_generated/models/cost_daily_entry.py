from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostDailyEntry")



@_attrs_define
class CostDailyEntry:
    """ 
        Attributes:
            cost_usd (float):
            date (str):
            input_tokens (int):
            output_tokens (int):
            service_cost_usd (float):
            total_cost_usd (float):
            total_tokens (int):
     """

    cost_usd: float
    date: str
    input_tokens: int
    output_tokens: int
    service_cost_usd: float
    total_cost_usd: float
    total_tokens: int





    def to_dict(self) -> dict[str, Any]:
        cost_usd = self.cost_usd

        date = self.date

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        service_cost_usd = self.service_cost_usd

        total_cost_usd = self.total_cost_usd

        total_tokens = self.total_tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "costUsd": cost_usd,
            "date": date,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "serviceCostUsd": service_cost_usd,
            "totalCostUsd": total_cost_usd,
            "totalTokens": total_tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_usd = d.pop("costUsd")

        date = d.pop("date")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        service_cost_usd = d.pop("serviceCostUsd")

        total_cost_usd = d.pop("totalCostUsd")

        total_tokens = d.pop("totalTokens")

        cost_daily_entry = cls(
            cost_usd=cost_usd,
            date=date,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            service_cost_usd=service_cost_usd,
            total_cost_usd=total_cost_usd,
            total_tokens=total_tokens,
        )

        return cost_daily_entry

