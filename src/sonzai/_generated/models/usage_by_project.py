from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UsageByProject")



@_attrs_define
class UsageByProject:
    """ 
        Attributes:
            cache_tokens (int):
            cost_usd (float):
            input_tokens (int):
            output_tokens (int):
            project_id (str):
            project_name (str):
            turns (int):
     """

    cache_tokens: int
    cost_usd: float
    input_tokens: int
    output_tokens: int
    project_id: str
    project_name: str
    turns: int





    def to_dict(self) -> dict[str, Any]:
        cache_tokens = self.cache_tokens

        cost_usd = self.cost_usd

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        project_id = self.project_id

        project_name = self.project_name

        turns = self.turns


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cacheTokens": cache_tokens,
            "costUsd": cost_usd,
            "inputTokens": input_tokens,
            "outputTokens": output_tokens,
            "projectId": project_id,
            "projectName": project_name,
            "turns": turns,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_tokens = d.pop("cacheTokens")

        cost_usd = d.pop("costUsd")

        input_tokens = d.pop("inputTokens")

        output_tokens = d.pop("outputTokens")

        project_id = d.pop("projectId")

        project_name = d.pop("projectName")

        turns = d.pop("turns")

        usage_by_project = cls(
            cache_tokens=cache_tokens,
            cost_usd=cost_usd,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            project_id=project_id,
            project_name=project_name,
            turns=turns,
        )

        return usage_by_project

