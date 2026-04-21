from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RedeemVoucherResponse")



@_attrs_define
class RedeemVoucherResponse:
    """ 
        Attributes:
            credit_amount_usd (float):
            message (str):
            new_balance (float):
            voucher_code (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    credit_amount_usd: float
    message: str
    new_balance: float
    voucher_code: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        credit_amount_usd = self.credit_amount_usd

        message = self.message

        new_balance = self.new_balance

        voucher_code = self.voucher_code

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "creditAmountUsd": credit_amount_usd,
            "message": message,
            "newBalance": new_balance,
            "voucherCode": voucher_code,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credit_amount_usd = d.pop("creditAmountUsd")

        message = d.pop("message")

        new_balance = d.pop("newBalance")

        voucher_code = d.pop("voucherCode")

        schema = d.pop("$schema", UNSET)

        redeem_voucher_response = cls(
            credit_amount_usd=credit_amount_usd,
            message=message,
            new_balance=new_balance,
            voucher_code=voucher_code,
            schema=schema,
        )

        return redeem_voucher_response

