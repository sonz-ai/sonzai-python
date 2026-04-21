from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchGenerateCharacterBehaviors")



@_attrs_define
class WorkbenchGenerateCharacterBehaviors:
    """ 
        Attributes:
            conflict_approach (str):
            empathy_style (str):
            question_frequency (str):
            response_length (str):
     """

    conflict_approach: str
    empathy_style: str
    question_frequency: str
    response_length: str





    def to_dict(self) -> dict[str, Any]:
        conflict_approach = self.conflict_approach

        empathy_style = self.empathy_style

        question_frequency = self.question_frequency

        response_length = self.response_length


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "conflict_approach": conflict_approach,
            "empathy_style": empathy_style,
            "question_frequency": question_frequency,
            "response_length": response_length,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conflict_approach = d.pop("conflict_approach")

        empathy_style = d.pop("empathy_style")

        question_frequency = d.pop("question_frequency")

        response_length = d.pop("response_length")

        workbench_generate_character_behaviors = cls(
            conflict_approach=conflict_approach,
            empathy_style=empathy_style,
            question_frequency=question_frequency,
            response_length=response_length,
        )

        return workbench_generate_character_behaviors

