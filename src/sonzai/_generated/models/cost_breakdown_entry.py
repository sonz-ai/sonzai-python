from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostBreakdownEntry")



@_attrs_define
class CostBreakdownEntry:
    """ 
        Attributes:
            cost_usd (float):
            input_tokens (int):
            key (str):
            label (str):
            output_tokens (int):
            turns (int):
     """

    cost_usd: float
    input_tokens: int
    key: str
    label: str
    output_tokens: int
    turns: int





    def to_dict(self) -> dict[str, Any]:
        cost_usd = self.cost_usd

        input_tokens = self.input_tokens

        key = self.key

        label = self.label

        output_tokens = self.output_tokens

        turns = self.turns


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "costUsd": cost_usd,
            "inputTokens": input_tokens,
            "key": key,
            "label": label,
            "outputTokens": output_tokens,
            "turns": turns,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost_usd = d.pop("costUsd")

        input_tokens = d.pop("inputTokens")

        key = d.pop("key")

        label = d.pop("label")

        output_tokens = d.pop("outputTokens")

        turns = d.pop("turns")

        cost_breakdown_entry = cls(
            cost_usd=cost_usd,
            input_tokens=input_tokens,
            key=key,
            label=label,
            output_tokens=output_tokens,
            turns=turns,
        )

        return cost_breakdown_entry

