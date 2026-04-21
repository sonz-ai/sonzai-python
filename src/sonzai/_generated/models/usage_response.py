from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.usage_by_project import UsageByProject
  from ..models.usage_daily_entry import UsageDailyEntry
  from ..models.usage_response_period_struct import UsageResponsePeriodStruct





T = TypeVar("T", bound="UsageResponse")



@_attrs_define
class UsageResponse:
    """ 
        Attributes:
            by_project (list[UsageByProject] | None):
            daily (list[UsageDailyEntry] | None):
            period (UsageResponsePeriodStruct):
            total_cache_tokens (int):
            total_cost_usd (float):
            total_input_tokens (int):
            total_output_tokens (int):
            total_turns (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    by_project: list[UsageByProject] | None
    daily: list[UsageDailyEntry] | None
    period: UsageResponsePeriodStruct
    total_cache_tokens: int
    total_cost_usd: float
    total_input_tokens: int
    total_output_tokens: int
    total_turns: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_by_project import UsageByProject
        from ..models.usage_daily_entry import UsageDailyEntry
        from ..models.usage_response_period_struct import UsageResponsePeriodStruct
        by_project: list[dict[str, Any]] | None
        if isinstance(self.by_project, list):
            by_project = []
            for by_project_type_0_item_data in self.by_project:
                by_project_type_0_item = by_project_type_0_item_data.to_dict()
                by_project.append(by_project_type_0_item)


        else:
            by_project = self.by_project

        daily: list[dict[str, Any]] | None
        if isinstance(self.daily, list):
            daily = []
            for daily_type_0_item_data in self.daily:
                daily_type_0_item = daily_type_0_item_data.to_dict()
                daily.append(daily_type_0_item)


        else:
            daily = self.daily

        period = self.period.to_dict()

        total_cache_tokens = self.total_cache_tokens

        total_cost_usd = self.total_cost_usd

        total_input_tokens = self.total_input_tokens

        total_output_tokens = self.total_output_tokens

        total_turns = self.total_turns

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "byProject": by_project,
            "daily": daily,
            "period": period,
            "totalCacheTokens": total_cache_tokens,
            "totalCostUsd": total_cost_usd,
            "totalInputTokens": total_input_tokens,
            "totalOutputTokens": total_output_tokens,
            "totalTurns": total_turns,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_by_project import UsageByProject
        from ..models.usage_daily_entry import UsageDailyEntry
        from ..models.usage_response_period_struct import UsageResponsePeriodStruct
        d = dict(src_dict)
        def _parse_by_project(data: object) -> list[UsageByProject] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_project_type_0 = []
                _by_project_type_0 = data
                for by_project_type_0_item_data in (_by_project_type_0):
                    by_project_type_0_item = UsageByProject.from_dict(by_project_type_0_item_data)



                    by_project_type_0.append(by_project_type_0_item)

                return by_project_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageByProject] | None, data)

        by_project = _parse_by_project(d.pop("byProject"))


        def _parse_daily(data: object) -> list[UsageDailyEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                daily_type_0 = []
                _daily_type_0 = data
                for daily_type_0_item_data in (_daily_type_0):
                    daily_type_0_item = UsageDailyEntry.from_dict(daily_type_0_item_data)



                    daily_type_0.append(daily_type_0_item)

                return daily_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UsageDailyEntry] | None, data)

        daily = _parse_daily(d.pop("daily"))


        period = UsageResponsePeriodStruct.from_dict(d.pop("period"))




        total_cache_tokens = d.pop("totalCacheTokens")

        total_cost_usd = d.pop("totalCostUsd")

        total_input_tokens = d.pop("totalInputTokens")

        total_output_tokens = d.pop("totalOutputTokens")

        total_turns = d.pop("totalTurns")

        schema = d.pop("$schema", UNSET)

        usage_response = cls(
            by_project=by_project,
            daily=daily,
            period=period,
            total_cache_tokens=total_cache_tokens,
            total_cost_usd=total_cost_usd,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            total_turns=total_turns,
            schema=schema,
        )

        return usage_response

