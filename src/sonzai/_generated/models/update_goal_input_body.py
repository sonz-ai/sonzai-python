from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateGoalInputBody")



@_attrs_define
class UpdateGoalInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            description (str | Unset): Updated description
            priority (int | Unset): Updated priority
            related_traits (list[str] | None | Unset): Updated related traits
            status (str | Unset): Updated status (active, achieved, abandoned)
            title (str | Unset): Updated title
            user_id (str | Unset): User ID for per-user goals
     """

    schema: str | Unset = UNSET
    description: str | Unset = UNSET
    priority: int | Unset = UNSET
    related_traits: list[str] | None | Unset = UNSET
    status: str | Unset = UNSET
    title: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        description = self.description

        priority = self.priority

        related_traits: list[str] | None | Unset
        if isinstance(self.related_traits, Unset):
            related_traits = UNSET
        elif isinstance(self.related_traits, list):
            related_traits = self.related_traits


        else:
            related_traits = self.related_traits

        status = self.status

        title = self.title

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if description is not UNSET:
            field_dict["description"] = description
        if priority is not UNSET:
            field_dict["priority"] = priority
        if related_traits is not UNSET:
            field_dict["related_traits"] = related_traits
        if status is not UNSET:
            field_dict["status"] = status
        if title is not UNSET:
            field_dict["title"] = title
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        description = d.pop("description", UNSET)

        priority = d.pop("priority", UNSET)

        def _parse_related_traits(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                related_traits_type_0 = cast(list[str], data)

                return related_traits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        related_traits = _parse_related_traits(d.pop("related_traits", UNSET))


        status = d.pop("status", UNSET)

        title = d.pop("title", UNSET)

        user_id = d.pop("user_id", UNSET)

        update_goal_input_body = cls(
            schema=schema,
            description=description,
            priority=priority,
            related_traits=related_traits,
            status=status,
            title=title,
            user_id=user_id,
        )

        return update_goal_input_body

