from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WorkbenchStateHabit")



@_attrs_define
class WorkbenchStateHabit:
    """ 
        Attributes:
            category (str):
            formed (bool):
            name (str):
            strength (float):
     """

    category: str
    formed: bool
    name: str
    strength: float





    def to_dict(self) -> dict[str, Any]:
        category = self.category

        formed = self.formed

        name = self.name

        strength = self.strength


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "category": category,
            "formed": formed,
            "name": name,
            "strength": strength,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        category = d.pop("category")

        formed = d.pop("formed")

        name = d.pop("name")

        strength = d.pop("strength")

        workbench_state_habit = cls(
            category=category,
            formed=formed,
            name=name,
            strength=strength,
        )

        return workbench_state_habit

