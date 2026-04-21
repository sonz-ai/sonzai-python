from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UsageDailyEntry")



@_attrs_define
class UsageDailyEntry:
    """ 
        Attributes:
            cache_tokens (int):
            cost_usd (float):
            date (str):
            input_tokens (int):
            output_tokens (int):
            turns (int):
     """

    cache_tokens: int
    cost_usd: float
    date: str
    input_tokens: int
    output_tokens: int
    turns: int





    def to_dict(self) -> dict[str, Any]:
        cache_tokens = self.cache_tokens

        cost_usd = self.cost_usd

        date = self.date

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        turns = self.turns


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cacheTokens": cache_tokens,
            "costUsd": cost_usd,
            "date": date,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "turns": turns,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_tokens = d.pop("cacheTokens")

        cost_usd = d.pop("costUsd")

        date = d.pop("date")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        turns = d.pop("turns")

        usage_daily_entry = cls(
            cache_tokens=cache_tokens,
            cost_usd=cost_usd,
            date=date,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            turns=turns,
        )

        return usage_daily_entry

