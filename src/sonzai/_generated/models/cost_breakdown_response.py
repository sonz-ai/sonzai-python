from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.cost_breakdown_entry import CostBreakdownEntry
  from ..models.cost_breakdown_response_period_struct import CostBreakdownResponsePeriodStruct





T = TypeVar("T", bound="CostBreakdownResponse")



@_attrs_define
class CostBreakdownResponse:
    """ 
        Attributes:
            by_agent (list[CostBreakdownEntry] | None):
            by_model (list[CostBreakdownEntry] | None):
            by_operation (list[CostBreakdownEntry] | None):
            period (CostBreakdownResponsePeriodStruct):
            total_cost_usd (float):
            total_input_tokens (int):
            total_output_tokens (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    by_agent: list[CostBreakdownEntry] | None
    by_model: list[CostBreakdownEntry] | None
    by_operation: list[CostBreakdownEntry] | None
    period: CostBreakdownResponsePeriodStruct
    total_cost_usd: float
    total_input_tokens: int
    total_output_tokens: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.cost_breakdown_entry import CostBreakdownEntry
        from ..models.cost_breakdown_response_period_struct import CostBreakdownResponsePeriodStruct
        by_agent: list[dict[str, Any]] | None
        if isinstance(self.by_agent, list):
            by_agent = []
            for by_agent_type_0_item_data in self.by_agent:
                by_agent_type_0_item = by_agent_type_0_item_data.to_dict()
                by_agent.append(by_agent_type_0_item)


        else:
            by_agent = self.by_agent

        by_model: list[dict[str, Any]] | None
        if isinstance(self.by_model, list):
            by_model = []
            for by_model_type_0_item_data in self.by_model:
                by_model_type_0_item = by_model_type_0_item_data.to_dict()
                by_model.append(by_model_type_0_item)


        else:
            by_model = self.by_model

        by_operation: list[dict[str, Any]] | None
        if isinstance(self.by_operation, list):
            by_operation = []
            for by_operation_type_0_item_data in self.by_operation:
                by_operation_type_0_item = by_operation_type_0_item_data.to_dict()
                by_operation.append(by_operation_type_0_item)


        else:
            by_operation = self.by_operation

        period = self.period.to_dict()

        total_cost_usd = self.total_cost_usd

        total_input_tokens = self.total_input_tokens

        total_output_tokens = self.total_output_tokens

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "byAgent": by_agent,
            "byModel": by_model,
            "byOperation": by_operation,
            "period": period,
            "totalCostUsd": total_cost_usd,
            "totalInputTokens": total_input_tokens,
            "totalOutputTokens": total_output_tokens,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cost_breakdown_entry import CostBreakdownEntry
        from ..models.cost_breakdown_response_period_struct import CostBreakdownResponsePeriodStruct
        d = dict(src_dict)
        def _parse_by_agent(data: object) -> list[CostBreakdownEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_agent_type_0 = []
                _by_agent_type_0 = data
                for by_agent_type_0_item_data in (_by_agent_type_0):
                    by_agent_type_0_item = CostBreakdownEntry.from_dict(by_agent_type_0_item_data)



                    by_agent_type_0.append(by_agent_type_0_item)

                return by_agent_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostBreakdownEntry] | None, data)

        by_agent = _parse_by_agent(d.pop("byAgent"))


        def _parse_by_model(data: object) -> list[CostBreakdownEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_model_type_0 = []
                _by_model_type_0 = data
                for by_model_type_0_item_data in (_by_model_type_0):
                    by_model_type_0_item = CostBreakdownEntry.from_dict(by_model_type_0_item_data)



                    by_model_type_0.append(by_model_type_0_item)

                return by_model_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostBreakdownEntry] | None, data)

        by_model = _parse_by_model(d.pop("byModel"))


        def _parse_by_operation(data: object) -> list[CostBreakdownEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_operation_type_0 = []
                _by_operation_type_0 = data
                for by_operation_type_0_item_data in (_by_operation_type_0):
                    by_operation_type_0_item = CostBreakdownEntry.from_dict(by_operation_type_0_item_data)



                    by_operation_type_0.append(by_operation_type_0_item)

                return by_operation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CostBreakdownEntry] | None, data)

        by_operation = _parse_by_operation(d.pop("byOperation"))


        period = CostBreakdownResponsePeriodStruct.from_dict(d.pop("period"))




        total_cost_usd = d.pop("totalCostUsd")

        total_input_tokens = d.pop("totalInputTokens")

        total_output_tokens = d.pop("totalOutputTokens")

        schema = d.pop("$schema", UNSET)

        cost_breakdown_response = cls(
            by_agent=by_agent,
            by_model=by_model,
            by_operation=by_operation,
            period=period,
            total_cost_usd=total_cost_usd,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            schema=schema,
        )

        return cost_breakdown_response

