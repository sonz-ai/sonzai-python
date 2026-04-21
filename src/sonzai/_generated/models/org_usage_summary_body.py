from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="OrgUsageSummaryBody")



@_attrs_define
class OrgUsageSummaryBody:
    """ 
        Attributes:
            char_price_per_month_usd (float):
            credit_balance_usd (float):
            estimated_cost_usd (float):
            input_token_price_per_1k_usd (float):
            output_token_price_per_1k_usd (float):
            token_price_per_1k_usd (float):
            total_characters (int):
            total_input_tokens (int):
            total_messages (int):
            total_output_tokens (int):
            total_projects (int):
            total_sessions (int):
            total_tokens (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    char_price_per_month_usd: float
    credit_balance_usd: float
    estimated_cost_usd: float
    input_token_price_per_1k_usd: float
    output_token_price_per_1k_usd: float
    token_price_per_1k_usd: float
    total_characters: int
    total_input_tokens: int
    total_messages: int
    total_output_tokens: int
    total_projects: int
    total_sessions: int
    total_tokens: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        char_price_per_month_usd = self.char_price_per_month_usd

        credit_balance_usd = self.credit_balance_usd

        estimated_cost_usd = self.estimated_cost_usd

        input_token_price_per_1k_usd = self.input_token_price_per_1k_usd

        output_token_price_per_1k_usd = self.output_token_price_per_1k_usd

        token_price_per_1k_usd = self.token_price_per_1k_usd

        total_characters = self.total_characters

        total_input_tokens = self.total_input_tokens

        total_messages = self.total_messages

        total_output_tokens = self.total_output_tokens

        total_projects = self.total_projects

        total_sessions = self.total_sessions

        total_tokens = self.total_tokens

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "charPricePerMonthUsd": char_price_per_month_usd,
            "creditBalanceUsd": credit_balance_usd,
            "estimatedCostUsd": estimated_cost_usd,
            "inputTokenPricePer1KUsd": input_token_price_per_1k_usd,
            "outputTokenPricePer1KUsd": output_token_price_per_1k_usd,
            "tokenPricePer1KUsd": token_price_per_1k_usd,
            "totalCharacters": total_characters,
            "totalInputTokens": total_input_tokens,
            "totalMessages": total_messages,
            "totalOutputTokens": total_output_tokens,
            "totalProjects": total_projects,
            "totalSessions": total_sessions,
            "totalTokens": total_tokens,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        char_price_per_month_usd = d.pop("charPricePerMonthUsd")

        credit_balance_usd = d.pop("creditBalanceUsd")

        estimated_cost_usd = d.pop("estimatedCostUsd")

        input_token_price_per_1k_usd = d.pop("inputTokenPricePer1KUsd")

        output_token_price_per_1k_usd = d.pop("outputTokenPricePer1KUsd")

        token_price_per_1k_usd = d.pop("tokenPricePer1KUsd")

        total_characters = d.pop("totalCharacters")

        total_input_tokens = d.pop("totalInputTokens")

        total_messages = d.pop("totalMessages")

        total_output_tokens = d.pop("totalOutputTokens")

        total_projects = d.pop("totalProjects")

        total_sessions = d.pop("totalSessions")

        total_tokens = d.pop("totalTokens")

        schema = d.pop("$schema", UNSET)

        org_usage_summary_body = cls(
            char_price_per_month_usd=char_price_per_month_usd,
            credit_balance_usd=credit_balance_usd,
            estimated_cost_usd=estimated_cost_usd,
            input_token_price_per_1k_usd=input_token_price_per_1k_usd,
            output_token_price_per_1k_usd=output_token_price_per_1k_usd,
            token_price_per_1k_usd=token_price_per_1k_usd,
            total_characters=total_characters,
            total_input_tokens=total_input_tokens,
            total_messages=total_messages,
            total_output_tokens=total_output_tokens,
            total_projects=total_projects,
            total_sessions=total_sessions,
            total_tokens=total_tokens,
            schema=schema,
        )

        return org_usage_summary_body

