from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchGenerateCharacterUsage")



@_attrs_define
class WorkbenchGenerateCharacterUsage:
    """ 
        Attributes:
            completion_tokens (int):
            prompt_tokens (int):
            total_tokens (int):
            model (str | Unset):
     """

    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    model: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        completion_tokens = self.completion_tokens

        prompt_tokens = self.prompt_tokens

        total_tokens = self.total_tokens

        model = self.model


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "completionTokens": completion_tokens,
            "promptTokens": prompt_tokens,
            "totalTokens": total_tokens,
        })
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        completion_tokens = d.pop("completionTokens")

        prompt_tokens = d.pop("promptTokens")

        total_tokens = d.pop("totalTokens")

        model = d.pop("model", UNSET)

        workbench_generate_character_usage = cls(
            completion_tokens=completion_tokens,
            prompt_tokens=prompt_tokens,
            total_tokens=total_tokens,
            model=model,
        )

        return workbench_generate_character_usage

