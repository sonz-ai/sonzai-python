from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostByService")



@_attrs_define
class CostByService:
    """ 
        Attributes:
            cost_usd (float):
            count (int):
            service (str):
     """

    cost_usd: float
    count: int
    service: str





    def to_dict(self) -> dict[str, Any]:
        cost_usd = self.cost_usd

        count = self.count

        service = self.service


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "costUsd": cost_usd,
            "count": count,
            "service": service,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_usd = d.pop("costUsd")

        count = d.pop("count")

        service = d.pop("service")

        cost_by_service = cls(
            cost_usd=cost_usd,
            count=count,
            service=service,
        )

        return cost_by_service

