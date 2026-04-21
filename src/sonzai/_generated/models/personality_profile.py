from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.behavioral_traits import BehavioralTraits
  from ..models.big_5_assessment import Big5Assessment
  from ..models.interaction_preferences import InteractionPreferences
  from ..models.personality_dimensions import PersonalityDimensions
  from ..models.personality_profile_emotional_tendencies import PersonalityProfileEmotionalTendencies
  from ..models.personality_profile_trait_precisions import PersonalityProfileTraitPrecisions





T = TypeVar("T", bound="PersonalityProfile")



@_attrs_define
class PersonalityProfile:
    """ 
        Attributes:
            agent_id (str):
            behaviors (BehavioralTraits):
            big5 (Big5Assessment):
            created_at (str):
            dimensions (PersonalityDimensions):
            gender (str):
            name (str):
            preferences (InteractionPreferences):
            primary_traits (list[str] | None):
            speech_patterns (list[str] | None):
            temperature (float):
            true_dislikes (list[str] | None):
            true_interests (list[str] | None):
            avatar_url (str | Unset):
            bio (str | Unset):
            emotional_tendencies (PersonalityProfileEmotionalTendencies | Unset):
            personality_prompt (str | Unset):
            trait_precisions (PersonalityProfileTraitPrecisions | Unset):
     """

    agent_id: str
    behaviors: BehavioralTraits
    big5: Big5Assessment
    created_at: str
    dimensions: PersonalityDimensions
    gender: str
    name: str
    preferences: InteractionPreferences
    primary_traits: list[str] | None
    speech_patterns: list[str] | None
    temperature: float
    true_dislikes: list[str] | None
    true_interests: list[str] | None
    avatar_url: str | Unset = UNSET
    bio: str | Unset = UNSET
    emotional_tendencies: PersonalityProfileEmotionalTendencies | Unset = UNSET
    personality_prompt: str | Unset = UNSET
    trait_precisions: PersonalityProfileTraitPrecisions | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        from ..models.personality_profile_emotional_tendencies import PersonalityProfileEmotionalTendencies
        from ..models.personality_profile_trait_precisions import PersonalityProfileTraitPrecisions
        agent_id = self.agent_id

        behaviors = self.behaviors.to_dict()

        big5 = self.big5.to_dict()

        created_at = self.created_at

        dimensions = self.dimensions.to_dict()

        gender = self.gender

        name = self.name

        preferences = self.preferences.to_dict()

        primary_traits: list[str] | None
        if isinstance(self.primary_traits, list):
            primary_traits = self.primary_traits


        else:
            primary_traits = self.primary_traits

        speech_patterns: list[str] | None
        if isinstance(self.speech_patterns, list):
            speech_patterns = self.speech_patterns


        else:
            speech_patterns = self.speech_patterns

        temperature = self.temperature

        true_dislikes: list[str] | None
        if isinstance(self.true_dislikes, list):
            true_dislikes = self.true_dislikes


        else:
            true_dislikes = self.true_dislikes

        true_interests: list[str] | None
        if isinstance(self.true_interests, list):
            true_interests = self.true_interests


        else:
            true_interests = self.true_interests

        avatar_url = self.avatar_url

        bio = self.bio

        emotional_tendencies: dict[str, Any] | Unset = UNSET
        if not isinstance(self.emotional_tendencies, Unset):
            emotional_tendencies = self.emotional_tendencies.to_dict()

        personality_prompt = self.personality_prompt

        trait_precisions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.trait_precisions, Unset):
            trait_precisions = self.trait_precisions.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "behaviors": behaviors,
            "big5": big5,
            "created_at": created_at,
            "dimensions": dimensions,
            "gender": gender,
            "name": name,
            "preferences": preferences,
            "primary_traits": primary_traits,
            "speech_patterns": speech_patterns,
            "temperature": temperature,
            "true_dislikes": true_dislikes,
            "true_interests": true_interests,
        })
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if bio is not UNSET:
            field_dict["bio"] = bio
        if emotional_tendencies is not UNSET:
            field_dict["emotional_tendencies"] = emotional_tendencies
        if personality_prompt is not UNSET:
            field_dict["personality_prompt"] = personality_prompt
        if trait_precisions is not UNSET:
            field_dict["trait_precisions"] = trait_precisions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.behavioral_traits import BehavioralTraits
        from ..models.big_5_assessment import Big5Assessment
        from ..models.interaction_preferences import InteractionPreferences
        from ..models.personality_dimensions import PersonalityDimensions
        from ..models.personality_profile_emotional_tendencies import PersonalityProfileEmotionalTendencies
        from ..models.personality_profile_trait_precisions import PersonalityProfileTraitPrecisions
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        behaviors = BehavioralTraits.from_dict(d.pop("behaviors"))




        big5 = Big5Assessment.from_dict(d.pop("big5"))




        created_at = d.pop("created_at")

        dimensions = PersonalityDimensions.from_dict(d.pop("dimensions"))




        gender = d.pop("gender")

        name = d.pop("name")

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


        def _parse_speech_patterns(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                speech_patterns_type_0 = cast(list[str], data)

                return speech_patterns_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        speech_patterns = _parse_speech_patterns(d.pop("speech_patterns"))


        temperature = d.pop("temperature")

        def _parse_true_dislikes(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_dislikes_type_0 = cast(list[str], data)

                return true_dislikes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        true_dislikes = _parse_true_dislikes(d.pop("true_dislikes"))


        def _parse_true_interests(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_interests_type_0 = cast(list[str], data)

                return true_interests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        true_interests = _parse_true_interests(d.pop("true_interests"))


        avatar_url = d.pop("avatar_url", UNSET)

        bio = d.pop("bio", UNSET)

        _emotional_tendencies = d.pop("emotional_tendencies", UNSET)
        emotional_tendencies: PersonalityProfileEmotionalTendencies | Unset
        if isinstance(_emotional_tendencies,  Unset):
            emotional_tendencies = UNSET
        else:
            emotional_tendencies = PersonalityProfileEmotionalTendencies.from_dict(_emotional_tendencies)




        personality_prompt = d.pop("personality_prompt", UNSET)

        _trait_precisions = d.pop("trait_precisions", UNSET)
        trait_precisions: PersonalityProfileTraitPrecisions | Unset
        if isinstance(_trait_precisions,  Unset):
            trait_precisions = UNSET
        else:
            trait_precisions = PersonalityProfileTraitPrecisions.from_dict(_trait_precisions)




        personality_profile = cls(
            agent_id=agent_id,
            behaviors=behaviors,
            big5=big5,
            created_at=created_at,
            dimensions=dimensions,
            gender=gender,
            name=name,
            preferences=preferences,
            primary_traits=primary_traits,
            speech_patterns=speech_patterns,
            temperature=temperature,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
            avatar_url=avatar_url,
            bio=bio,
            emotional_tendencies=emotional_tendencies,
            personality_prompt=personality_prompt,
            trait_precisions=trait_precisions,
        )

        return personality_profile

