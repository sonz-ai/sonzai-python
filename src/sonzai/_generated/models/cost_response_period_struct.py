from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostResponsePeriodStruct")



@_attrs_define
class CostResponsePeriodStruct:
    """ 
        Attributes:
            end (str):
            start (str):
     """

    end: str
    start: str





    def to_dict(self) -> dict[str, Any]:
        end = self.end

        start = self.start


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "end": end,
            "start": start,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        end = d.pop("end")

        start = d.pop("start")

        cost_response_period_struct = cls(
            end=end,
            start=start,
        )

        return cost_response_period_struct

