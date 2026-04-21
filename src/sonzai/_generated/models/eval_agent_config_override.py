from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.behaviors import Behaviors
  from ..models.big_5 import Big5
  from ..models.dimensions import Dimensions
  from ..models.preferences import Preferences
  from ..models.voice_config import VoiceConfig





T = TypeVar("T", bound="EvalAgentConfigOverride")



@_attrs_define
class EvalAgentConfigOverride:
    """ 
        Attributes:
            behaviors (Behaviors | Unset):
            big5 (Big5 | Unset):
            bio (str | Unset): Short bio/backstory
            dimensions (Dimensions | Unset):
            gender (str | Unset): Character gender (free-form)
            model (str | Unset): Override LLM model for this run (matches top-level RunEvalRequest.model semantics)
            name (str | Unset): Character display name
            personality_prompt (str | Unset): Personality prompt baseline
            preferences (Preferences | Unset):
            primary_traits (list[str] | None | Unset): Primary personality traits
            speech_patterns (list[str] | None | Unset): Recurring speech patterns
            true_dislikes (list[str] | None | Unset): Authentic dislikes
            true_interests (list[str] | None | Unset): Authentic interests
            voice (VoiceConfig | Unset):
     """

    behaviors: Behaviors | Unset = UNSET
    big5: Big5 | Unset = UNSET
    bio: str | Unset = UNSET
    dimensions: Dimensions | Unset = UNSET
    gender: str | Unset = UNSET
    model: str | Unset = UNSET
    name: str | Unset = UNSET
    personality_prompt: str | Unset = UNSET
    preferences: Preferences | Unset = UNSET
    primary_traits: list[str] | None | Unset = UNSET
    speech_patterns: list[str] | None | Unset = UNSET
    true_dislikes: list[str] | None | Unset = UNSET
    true_interests: list[str] | None | Unset = UNSET
    voice: VoiceConfig | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.behaviors import Behaviors
        from ..models.big_5 import Big5
        from ..models.dimensions import Dimensions
        from ..models.preferences import Preferences
        from ..models.voice_config import VoiceConfig
        behaviors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.behaviors, Unset):
            behaviors = self.behaviors.to_dict()

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        bio = self.bio

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()

        gender = self.gender

        model = self.model

        name = self.name

        personality_prompt = self.personality_prompt

        preferences: dict[str, Any] | Unset = UNSET
        if not isinstance(self.preferences, Unset):
            preferences = self.preferences.to_dict()

        primary_traits: list[str] | None | Unset
        if isinstance(self.primary_traits, Unset):
            primary_traits = UNSET
        elif isinstance(self.primary_traits, list):
            primary_traits = self.primary_traits


        else:
            primary_traits = self.primary_traits

        speech_patterns: list[str] | None | Unset
        if isinstance(self.speech_patterns, Unset):
            speech_patterns = UNSET
        elif isinstance(self.speech_patterns, list):
            speech_patterns = self.speech_patterns


        else:
            speech_patterns = self.speech_patterns

        true_dislikes: list[str] | None | Unset
        if isinstance(self.true_dislikes, Unset):
            true_dislikes = UNSET
        elif isinstance(self.true_dislikes, list):
            true_dislikes = self.true_dislikes


        else:
            true_dislikes = self.true_dislikes

        true_interests: list[str] | None | Unset
        if isinstance(self.true_interests, Unset):
            true_interests = UNSET
        elif isinstance(self.true_interests, list):
            true_interests = self.true_interests


        else:
            true_interests = self.true_interests

        voice: dict[str, Any] | Unset = UNSET
        if not isinstance(self.voice, Unset):
            voice = self.voice.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if behaviors is not UNSET:
            field_dict["behaviors"] = behaviors
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if bio is not UNSET:
            field_dict["bio"] = bio
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if gender is not UNSET:
            field_dict["gender"] = gender
        if model is not UNSET:
            field_dict["model"] = model
        if name is not UNSET:
            field_dict["name"] = name
        if personality_prompt is not UNSET:
            field_dict["personality_prompt"] = personality_prompt
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if primary_traits is not UNSET:
            field_dict["primary_traits"] = primary_traits
        if speech_patterns is not UNSET:
            field_dict["speech_patterns"] = speech_patterns
        if true_dislikes is not UNSET:
            field_dict["true_dislikes"] = true_dislikes
        if true_interests is not UNSET:
            field_dict["true_interests"] = true_interests
        if voice is not UNSET:
            field_dict["voice"] = voice

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.behaviors import Behaviors
        from ..models.big_5 import Big5
        from ..models.dimensions import Dimensions
        from ..models.preferences import Preferences
        from ..models.voice_config import VoiceConfig
        d = dict(src_dict)
        _behaviors = d.pop("behaviors", UNSET)
        behaviors: Behaviors | Unset
        if isinstance(_behaviors,  Unset):
            behaviors = UNSET
        else:
            behaviors = Behaviors.from_dict(_behaviors)




        _big5 = d.pop("big5", UNSET)
        big5: Big5 | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = Big5.from_dict(_big5)




        bio = d.pop("bio", UNSET)

        _dimensions = d.pop("dimensions", UNSET)
        dimensions: Dimensions | Unset
        if isinstance(_dimensions,  Unset):
            dimensions = UNSET
        else:
            dimensions = Dimensions.from_dict(_dimensions)




        gender = d.pop("gender", UNSET)

        model = d.pop("model", UNSET)

        name = d.pop("name", UNSET)

        personality_prompt = d.pop("personality_prompt", UNSET)

        _preferences = d.pop("preferences", UNSET)
        preferences: Preferences | Unset
        if isinstance(_preferences,  Unset):
            preferences = UNSET
        else:
            preferences = Preferences.from_dict(_preferences)




        def _parse_primary_traits(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                primary_traits_type_0 = cast(list[str], data)

                return primary_traits_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        primary_traits = _parse_primary_traits(d.pop("primary_traits", UNSET))


        def _parse_speech_patterns(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                speech_patterns_type_0 = cast(list[str], data)

                return speech_patterns_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        speech_patterns = _parse_speech_patterns(d.pop("speech_patterns", UNSET))


        def _parse_true_dislikes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_dislikes_type_0 = cast(list[str], data)

                return true_dislikes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        true_dislikes = _parse_true_dislikes(d.pop("true_dislikes", UNSET))


        def _parse_true_interests(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                true_interests_type_0 = cast(list[str], data)

                return true_interests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        true_interests = _parse_true_interests(d.pop("true_interests", UNSET))


        _voice = d.pop("voice", UNSET)
        voice: VoiceConfig | Unset
        if isinstance(_voice,  Unset):
            voice = UNSET
        else:
            voice = VoiceConfig.from_dict(_voice)




        eval_agent_config_override = cls(
            behaviors=behaviors,
            big5=big5,
            bio=bio,
            dimensions=dimensions,
            gender=gender,
            model=model,
            name=name,
            personality_prompt=personality_prompt,
            preferences=preferences,
            primary_traits=primary_traits,
            speech_patterns=speech_patterns,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
            voice=voice,
        )

        return eval_agent_config_override

