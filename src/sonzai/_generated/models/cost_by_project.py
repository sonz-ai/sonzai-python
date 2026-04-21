from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostByProject")



@_attrs_define
class CostByProject:
    """ 
        Attributes:
            agent_count (int):
            cost_usd (float):
            input_tokens (int):
            output_tokens (int):
            project_id (str):
            project_name (str):
            service_cost_usd (float):
            total_tokens (int):
     """

    agent_count: int
    cost_usd: float
    input_tokens: int
    output_tokens: int
    project_id: str
    project_name: str
    service_cost_usd: float
    total_tokens: int





    def to_dict(self) -> dict[str, Any]:
        agent_count = self.agent_count

        cost_usd = self.cost_usd

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        project_id = self.project_id

        project_name = self.project_name

        service_cost_usd = self.service_cost_usd

        total_tokens = self.total_tokens


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentCount": agent_count,
            "costUsd": cost_usd,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "projectId": project_id,
            "projectName": project_name,
            "serviceCostUsd": service_cost_usd,
            "totalTokens": total_tokens,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_count = d.pop("agentCount")

        cost_usd = d.pop("costUsd")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        project_id = d.pop("projectId")

        project_name = d.pop("projectName")

        service_cost_usd = d.pop("serviceCostUsd")

        total_tokens = d.pop("totalTokens")

        cost_by_project = cls(
            agent_count=agent_count,
            cost_usd=cost_usd,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            project_id=project_id,
            project_name=project_name,
            service_cost_usd=service_cost_usd,
            total_tokens=total_tokens,
        )

        return cost_by_project

