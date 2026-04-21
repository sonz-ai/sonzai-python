from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="Behaviors")



@_attrs_define
class Behaviors:
    """ 
        Attributes:
            conflict_approach (str | Unset):
            empathy_style (str | Unset):
            question_frequency (str | Unset):
            response_length (str | Unset):
     """

    conflict_approach: str | Unset = UNSET
    empathy_style: str | Unset = UNSET
    question_frequency: str | Unset = UNSET
    response_length: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        conflict_approach = self.conflict_approach

        empathy_style = self.empathy_style

        question_frequency = self.question_frequency

        response_length = self.response_length


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if conflict_approach is not UNSET:
            field_dict["conflict_approach"] = conflict_approach
        if empathy_style is not UNSET:
            field_dict["empathy_style"] = empathy_style
        if question_frequency is not UNSET:
            field_dict["question_frequency"] = question_frequency
        if response_length is not UNSET:
            field_dict["response_length"] = response_length

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conflict_approach = d.pop("conflict_approach", UNSET)

        empathy_style = d.pop("empathy_style", UNSET)

        question_frequency = d.pop("question_frequency", UNSET)

        response_length = d.pop("response_length", UNSET)

        behaviors = cls(
            conflict_approach=conflict_approach,
            empathy_style=empathy_style,
            question_frequency=question_frequency,
            response_length=response_length,
        )

        return behaviors

