from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchGenerateCharacterPreferences")



@_attrs_define
class WorkbenchGenerateCharacterPreferences:
    """ 
        Attributes:
            conversation_pace (str):
            emotional_expression (str):
            formality (str):
            humor_style (str):
     """

    conversation_pace: str
    emotional_expression: str
    formality: str
    humor_style: str





    def to_dict(self) -> dict[str, Any]:
        conversation_pace = self.conversation_pace

        emotional_expression = self.emotional_expression

        formality = self.formality

        humor_style = self.humor_style


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "conversation_pace": conversation_pace,
            "emotional_expression": emotional_expression,
            "formality": formality,
            "humor_style": humor_style,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conversation_pace = d.pop("conversation_pace")

        emotional_expression = d.pop("emotional_expression")

        formality = d.pop("formality")

        humor_style = d.pop("humor_style")

        workbench_generate_character_preferences = cls(
            conversation_pace=conversation_pace,
            emotional_expression=emotional_expression,
            formality=formality,
            humor_style=humor_style,
        )

        return workbench_generate_character_preferences

