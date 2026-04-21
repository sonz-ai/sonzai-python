from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="OrgModelPriceItem")



@_attrs_define
class OrgModelPriceItem:
    """ 
        Attributes:
            input_price_per_1k (float):
            model (str):
            output_price_per_1k (float):
     """

    input_price_per_1k: float
    model: str
    output_price_per_1k: float





    def to_dict(self) -> dict[str, Any]:
        input_price_per_1k = self.input_price_per_1k

        model = self.model

        output_price_per_1k = self.output_price_per_1k


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "inputPricePer1K": input_price_per_1k,
            "model": model,
            "outputPricePer1K": output_price_per_1k,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_price_per_1k = d.pop("inputPricePer1K")

        model = d.pop("model")

        output_price_per_1k = d.pop("outputPricePer1K")

        org_model_price_item = cls(
            input_price_per_1k=input_price_per_1k,
            model=model,
            output_price_per_1k=output_price_per_1k,
        )

        return org_model_price_item

