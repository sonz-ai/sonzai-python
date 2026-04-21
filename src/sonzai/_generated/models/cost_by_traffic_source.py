from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostByTrafficSource")



@_attrs_define
class CostByTrafficSource:
    """ 
        Attributes:
            cost_usd (float):
            entry_count (int):
            tokens (int):
            traffic_source (str):
     """

    cost_usd: float
    entry_count: int
    tokens: int
    traffic_source: str





    def to_dict(self) -> dict[str, Any]:
        cost_usd = self.cost_usd

        entry_count = self.entry_count

        tokens = self.tokens

        traffic_source = self.traffic_source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "costUsd": cost_usd,
            "entryCount": entry_count,
            "tokens": tokens,
            "trafficSource": traffic_source,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_usd = d.pop("costUsd")

        entry_count = d.pop("entryCount")

        tokens = d.pop("tokens")

        traffic_source = d.pop("trafficSource")

        cost_by_traffic_source = cls(
            cost_usd=cost_usd,
            entry_count=entry_count,
            tokens=tokens,
            traffic_source=traffic_source,
        )

        return cost_by_traffic_source

