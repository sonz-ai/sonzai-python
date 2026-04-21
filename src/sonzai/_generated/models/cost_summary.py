from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostSummary")



@_attrs_define
class CostSummary:
    """ 
        Attributes:
            billing_mode (str):
            credit_balance_usd (float):
            input_cost_usd (float):
            output_cost_usd (float):
            service_cost_usd (float):
            token_cost_usd (float):
            token_price_per_1k_usd (float):
            total_cost_usd (float):
            total_input_tokens (int):
            total_output_tokens (int):
            total_tokens (int):
     """

    billing_mode: str
    credit_balance_usd: float
    input_cost_usd: float
    output_cost_usd: float
    service_cost_usd: float
    token_cost_usd: float
    token_price_per_1k_usd: float
    total_cost_usd: float
    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int





    def to_dict(self) -> dict[str, Any]:
        billing_mode = self.billing_mode

        credit_balance_usd = self.credit_balance_usd

        input_cost_usd = self.input_cost_usd

        output_cost_usd = self.output_cost_usd

        service_cost_usd = self.service_cost_usd

        token_cost_usd = self.token_cost_usd

        token_price_per_1k_usd = self.token_price_per_1k_usd

        total_cost_usd = self.total_cost_usd

        total_input_tokens = self.total_input_tokens

        total_output_tokens = self.total_output_tokens

        total_tokens = self.total_tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "billingMode": billing_mode,
            "creditBalanceUsd": credit_balance_usd,
            "inputCostUsd": input_cost_usd,
            "outputCostUsd": output_cost_usd,
            "serviceCostUsd": service_cost_usd,
            "tokenCostUsd": token_cost_usd,
            "tokenPricePer1KUsd": token_price_per_1k_usd,
            "totalCostUsd": total_cost_usd,
            "totalInputTokens": total_input_tokens,
            "totalOutputTokens": total_output_tokens,
            "totalTokens": total_tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        billing_mode = d.pop("billingMode")

        credit_balance_usd = d.pop("creditBalanceUsd")

        input_cost_usd = d.pop("inputCostUsd")

        output_cost_usd = d.pop("outputCostUsd")

        service_cost_usd = d.pop("serviceCostUsd")

        token_cost_usd = d.pop("tokenCostUsd")

        token_price_per_1k_usd = d.pop("tokenPricePer1KUsd")

        total_cost_usd = d.pop("totalCostUsd")

        total_input_tokens = d.pop("totalInputTokens")

        total_output_tokens = d.pop("totalOutputTokens")

        total_tokens = d.pop("totalTokens")

        cost_summary = cls(
            billing_mode=billing_mode,
            credit_balance_usd=credit_balance_usd,
            input_cost_usd=input_cost_usd,
            output_cost_usd=output_cost_usd,
            service_cost_usd=service_cost_usd,
            token_cost_usd=token_cost_usd,
            token_price_per_1k_usd=token_price_per_1k_usd,
            total_cost_usd=total_cost_usd,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            total_tokens=total_tokens,
        )

        return cost_summary

