from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SignificantMoment")



@_attrs_define
class SignificantMoment:
    """ 
        Attributes:
            created_at (str):
            description (str):
            reasoning (str):
            trigger_type (str):
            emotional_impact (str | Unset):
            location (str | Unset):
            partner_name (str | Unset):
            traits_affected (list[str] | None | Unset):
     """

    created_at: str
    description: str
    reasoning: str
    trigger_type: str
    emotional_impact: str | Unset = UNSET
    location: str | Unset = UNSET
    partner_name: str | Unset = UNSET
    traits_affected: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        description = self.description

        reasoning = self.reasoning

        trigger_type = self.trigger_type

        emotional_impact = self.emotional_impact

        location = self.location

        partner_name = self.partner_name

        traits_affected: list[str] | None | Unset
        if isinstance(self.traits_affected, Unset):
            traits_affected = UNSET
        elif isinstance(self.traits_affected, list):
            traits_affected = self.traits_affected


        else:
            traits_affected = self.traits_affected


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "description": description,
            "reasoning": reasoning,
            "trigger_type": trigger_type,
        })
        if emotional_impact is not UNSET:
            field_dict["emotional_impact"] = emotional_impact
        if location is not UNSET:
            field_dict["location"] = location
        if partner_name is not UNSET:
            field_dict["partner_name"] = partner_name
        if traits_affected is not UNSET:
            field_dict["traits_affected"] = traits_affected

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at")

        description = d.pop("description")

        reasoning = d.pop("reasoning")

        trigger_type = d.pop("trigger_type")

        emotional_impact = d.pop("emotional_impact", UNSET)

        location = d.pop("location", UNSET)

        partner_name = d.pop("partner_name", UNSET)

        def _parse_traits_affected(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                traits_affected_type_0 = cast(list[str], data)

                return traits_affected_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        traits_affected = _parse_traits_affected(d.pop("traits_affected", UNSET))


        significant_moment = cls(
            created_at=created_at,
            description=description,
            reasoning=reasoning,
            trigger_type=trigger_type,
            emotional_impact=emotional_impact,
            location=location,
            partner_name=partner_name,
            traits_affected=traits_affected,
        )

        return significant_moment

