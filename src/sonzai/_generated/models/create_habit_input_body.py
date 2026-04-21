from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateHabitInputBody")



@_attrs_define
class CreateHabitInputBody:
    """ 
        Attributes:
            name (str): Habit name (unique per agent or per user)
            schema (str | Unset): A URL to the JSON Schema for this object.
            category (str | Unset): Habit category (defaults to behavioral)
            description (str | Unset): Habit description
            display_name (str | Unset): Human-readable display name
            strength (float | Unset): Initial strength value (0.0 to 1.0)
            user_id (str | Unset): Optional user ID for per-user habits
     """

    name: str
    schema: str | Unset = UNSET
    category: str | Unset = UNSET
    description: str | Unset = UNSET
    display_name: str | Unset = UNSET
    strength: float | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        schema = self.schema

        category = self.category

        description = self.description

        display_name = self.display_name

        strength = self.strength

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if category is not UNSET:
            field_dict["category"] = category
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if strength is not UNSET:
            field_dict["strength"] = strength
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        category = d.pop("category", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("display_name", UNSET)

        strength = d.pop("strength", UNSET)

        user_id = d.pop("user_id", UNSET)

        create_habit_input_body = cls(
            name=name,
            schema=schema,
            category=category,
            description=description,
            display_name=display_name,
            strength=strength,
            user_id=user_id,
        )

        return create_habit_input_body

