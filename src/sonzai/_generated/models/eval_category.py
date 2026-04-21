from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="EvalCategory")



@_attrs_define
class EvalCategory:
    """ 
        Attributes:
            key (str):
            label (str):
            prompt_instructions (str):
     """

    key: str
    label: str
    prompt_instructions: str





    def to_dict(self) -> dict[str, Any]:
        key = self.key

        label = self.label

        prompt_instructions = self.prompt_instructions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "key": key,
            "label": label,
            "prompt_instructions": prompt_instructions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        label = d.pop("label")

        prompt_instructions = d.pop("prompt_instructions")

        eval_category = cls(
            key=key,
            label=label,
            prompt_instructions=prompt_instructions,
        )

        return eval_category

