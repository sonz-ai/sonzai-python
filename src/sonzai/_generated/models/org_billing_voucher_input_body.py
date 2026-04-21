from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="OrgBillingVoucherInputBody")



@_attrs_define
class OrgBillingVoucherInputBody:
    """ 
        Attributes:
            code (str): Voucher code to redeem
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    code: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        code = self.code

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "code": code,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        schema = d.pop("$schema", UNSET)

        org_billing_voucher_input_body = cls(
            code=code,
            schema=schema,
        )

        return org_billing_voucher_input_body

