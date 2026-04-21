from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="ActiveCharacterSummary")



@_attrs_define
class ActiveCharacterSummary:
    """ 
        Attributes:
            char_charge_usd (float):
            high_water_mark (int):
            month (str):
            price_per_char_usd (float):
            schema (str | Unset): A URL to the JSON Schema for this object.
            billed_at (datetime.datetime | Unset):
     """

    char_charge_usd: float
    high_water_mark: int
    month: str
    price_per_char_usd: float
    schema: str | Unset = UNSET
    billed_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        char_charge_usd = self.char_charge_usd

        high_water_mark = self.high_water_mark

        month = self.month

        price_per_char_usd = self.price_per_char_usd

        schema = self.schema

        billed_at: str | Unset = UNSET
        if not isinstance(self.billed_at, Unset):
            billed_at = self.billed_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "charChargeUsd": char_charge_usd,
            "highWaterMark": high_water_mark,
            "month": month,
            "pricePerCharUsd": price_per_char_usd,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if billed_at is not UNSET:
            field_dict["billedAt"] = billed_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        char_charge_usd = d.pop("charChargeUsd")

        high_water_mark = d.pop("highWaterMark")

        month = d.pop("month")

        price_per_char_usd = d.pop("pricePerCharUsd")

        schema = d.pop("$schema", UNSET)

        _billed_at = d.pop("billedAt", UNSET)
        billed_at: datetime.datetime | Unset
        if isinstance(_billed_at,  Unset):
            billed_at = UNSET
        else:
            billed_at = isoparse(_billed_at)




        active_character_summary = cls(
            char_charge_usd=char_charge_usd,
            high_water_mark=high_water_mark,
            month=month,
            price_per_char_usd=price_per_char_usd,
            schema=schema,
            billed_at=billed_at,
        )

        return active_character_summary

