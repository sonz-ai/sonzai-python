from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="OrgBillingCheckoutInputBody")



@_attrs_define
class OrgBillingCheckoutInputBody:
    """ 
        Attributes:
            amount (int): Amount in smallest currency unit (e.g. cents for USD)
            schema (str | Unset): A URL to the JSON Schema for this object.
            currency (str | Unset): ISO 4217 currency code (default USD)
     """

    amount: int
    schema: str | Unset = UNSET
    currency: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        schema = self.schema

        currency = self.currency


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "amount": amount,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        schema = d.pop("$schema", UNSET)

        currency = d.pop("currency", UNSET)

        org_billing_checkout_input_body = cls(
            amount=amount,
            schema=schema,
            currency=currency,
        )

        return org_billing_checkout_input_body

