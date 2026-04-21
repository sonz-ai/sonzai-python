from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.goal import Goal





T = TypeVar("T", bound="GoalsResponse")



@_attrs_define
class GoalsResponse:
    """ 
        Attributes:
            goals (list[Goal] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    goals: list[Goal] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.goal import Goal
        goals: list[dict[str, Any]] | None
        if isinstance(self.goals, list):
            goals = []
            for goals_type_0_item_data in self.goals:
                goals_type_0_item = goals_type_0_item_data.to_dict()
                goals.append(goals_type_0_item)


        else:
            goals = self.goals

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "goals": goals,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.goal import Goal
        d = dict(src_dict)
        def _parse_goals(data: object) -> list[Goal] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                goals_type_0 = []
                _goals_type_0 = data
                for goals_type_0_item_data in (_goals_type_0):
                    goals_type_0_item = Goal.from_dict(goals_type_0_item_data)



                    goals_type_0.append(goals_type_0_item)

                return goals_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Goal] | None, data)

        goals = _parse_goals(d.pop("goals"))


        schema = d.pop("$schema", UNSET)

        goals_response = cls(
            goals=goals,
            schema=schema,
        )

        return goals_response

