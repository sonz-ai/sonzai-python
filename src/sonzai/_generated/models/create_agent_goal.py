from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateAgentGoal")



@_attrs_define
class CreateAgentGoal:
    """ 
        Attributes:
            description (str):
            priority (int):
            title (str):
            type_ (str):
            related_traits (list[str] | None | Unset):
     """

    description: str
    priority: int
    title: str
    type_: str
    related_traits: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        priority = self.priority

        title = self.title

        type_ = self.type_

        related_traits: list[str] | None | Unset
        if isinstance(self.related_traits, Unset):
            related_traits = UNSET
        elif isinstance(self.related_traits, list):
            related_traits = self.related_traits


        else:
            related_traits = self.related_traits


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "priority": priority,
            "title": title,
            "type": type_,
        })
        if related_traits is not UNSET:
            field_dict["related_traits"] = related_traits

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        priority = d.pop("priority")

        title = d.pop("title")

        type_ = d.pop("type")

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


        create_agent_goal = cls(
            description=description,
            priority=priority,
            title=title,
            type_=type_,
            related_traits=related_traits,
        )

        return create_agent_goal

