from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchGenerateCharacterGoal")



@_attrs_define
class WorkbenchGenerateCharacterGoal:
    """ 
        Attributes:
            description (str):
            title (str):
            priority (int | Unset):
            type_ (str | Unset):
     """

    description: str
    title: str
    priority: int | Unset = UNSET
    type_: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        title = self.title

        priority = self.priority

        type_ = self.type_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "title": title,
        })
        if priority is not UNSET:
            field_dict["priority"] = priority
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        title = d.pop("title")

        priority = d.pop("priority", UNSET)

        type_ = d.pop("type", UNSET)

        workbench_generate_character_goal = cls(
            description=description,
            title=title,
            priority=priority,
            type_=type_,
        )

        return workbench_generate_character_goal

