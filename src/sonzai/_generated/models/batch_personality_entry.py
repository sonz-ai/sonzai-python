from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.personality_profile import PersonalityProfile





T = TypeVar("T", bound="BatchPersonalityEntry")



@_attrs_define
class BatchPersonalityEntry:
    """ 
        Attributes:
            evolution_count (int):
            profile (PersonalityProfile):
     """

    evolution_count: int
    profile: PersonalityProfile





    def to_dict(self) -> dict[str, Any]:
        from ..models.personality_profile import PersonalityProfile
        evolution_count = self.evolution_count

        profile = self.profile.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "evolution_count": evolution_count,
            "profile": profile,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.personality_profile import PersonalityProfile
        d = dict(src_dict)
        evolution_count = d.pop("evolution_count")

        profile = PersonalityProfile.from_dict(d.pop("profile"))




        batch_personality_entry = cls(
            evolution_count=evolution_count,
            profile=profile,
        )

        return batch_personality_entry

