from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.behavioral_traits import BehavioralTraits
  from ..models.big_5_assessment import Big5Assessment
  from ..models.interaction_preferences import InteractionPreferences
  from ..models.personality_dimensions import PersonalityDimensions





T = TypeVar("T", bound="UserOverlayResponse")



@_attrs_define
class UserOverlayResponse:
    """ 
        Attributes:
            agent_id (str):
            behaviors (BehavioralTraits):
            big5 (Big5Assessment):
            created_at (str):
            dimensions (PersonalityDimensions):
            preferences (InteractionPreferences):
            primary_traits (list[str] | None):
            updated_at (str):
            user_id (str):
     """

    agent_id: str
    behaviors: BehavioralTraits
    big5: Big5Assessment
    created_at: str
    dimensions: PersonalityDimensions
    preferences: InteractionPreferences
    primary_traits: list[str] | None
    updated_at: str
    user_id: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        agent_id = self.agent_id

        behaviors = self.behaviors.to_dict()

        big5 = self.big5.to_dict()

        created_at = self.created_at

        dimensions = self.dimensions.to_dict()

        preferences = self.preferences.to_dict()

        primary_traits: list[str] | None
        if isinstance(self.primary_traits, list):
            primary_traits = self.primary_traits


        else:
            primary_traits = self.primary_traits

        updated_at = self.updated_at

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "behaviors": behaviors,
            "big5": big5,
            "created_at": created_at,
            "dimensions": dimensions,
            "preferences": preferences,
            "primary_traits": primary_traits,
            "updated_at": updated_at,
            "user_id": user_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        behaviors = BehavioralTraits.from_dict(d.pop("behaviors"))




        big5 = Big5Assessment.from_dict(d.pop("big5"))




        created_at = d.pop("created_at")

        dimensions = PersonalityDimensions.from_dict(d.pop("dimensions"))




        preferences = InteractionPreferences.from_dict(d.pop("preferences"))




        def _parse_primary_traits(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                primary_traits_type_0 = cast(list[str], data)

                return primary_traits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        primary_traits = _parse_primary_traits(d.pop("primary_traits"))


        updated_at = d.pop("updated_at")

        user_id = d.pop("user_id")

        user_overlay_response = cls(
            agent_id=agent_id,
            behaviors=behaviors,
            big5=big5,
            created_at=created_at,
            dimensions=dimensions,
            preferences=preferences,
            primary_traits=primary_traits,
            updated_at=updated_at,
            user_id=user_id,
        )

        return user_overlay_response

