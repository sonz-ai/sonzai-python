from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="Preferences")



@_attrs_define
class Preferences:
    """ 
        Attributes:
            conversation_pace (str | Unset):
            emotional_expression (str | Unset):
            formality (str | Unset):
            humor_style (str | Unset):
     """

    conversation_pace: str | Unset = UNSET
    emotional_expression: str | Unset = UNSET
    formality: str | Unset = UNSET
    humor_style: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        conversation_pace = self.conversation_pace

        emotional_expression = self.emotional_expression

        formality = self.formality

        humor_style = self.humor_style


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if conversation_pace is not UNSET:
            field_dict["conversation_pace"] = conversation_pace
        if emotional_expression is not UNSET:
            field_dict["emotional_expression"] = emotional_expression
        if formality is not UNSET:
            field_dict["formality"] = formality
        if humor_style is not UNSET:
            field_dict["humor_style"] = humor_style

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        conversation_pace = d.pop("conversation_pace", UNSET)

        emotional_expression = d.pop("emotional_expression", UNSET)

        formality = d.pop("formality", UNSET)

        humor_style = d.pop("humor_style", UNSET)

        preferences = cls(
            conversation_pace=conversation_pace,
            emotional_expression=emotional_expression,
            formality=formality,
            humor_style=humor_style,
        )

        return preferences

