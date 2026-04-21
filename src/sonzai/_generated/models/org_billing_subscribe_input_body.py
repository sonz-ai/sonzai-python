from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="OrgBillingSubscribeInputBody")



@_attrs_define
class OrgBillingSubscribeInputBody:
    """ 
        Attributes:
            contract_id (str): Enterprise contract UUID to subscribe to
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    contract_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        contract_id = self.contract_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "contractId": contract_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        contract_id = d.pop("contractId")

        schema = d.pop("$schema", UNSET)

        org_billing_subscribe_input_body = cls(
            contract_id=contract_id,
            schema=schema,
        )

        return org_billing_subscribe_input_body

