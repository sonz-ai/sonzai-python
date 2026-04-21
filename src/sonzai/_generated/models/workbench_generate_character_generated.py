from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.workbench_generate_character_behaviors import WorkbenchGenerateCharacterBehaviors
  from ..models.workbench_generate_character_big_5 import WorkbenchGenerateCharacterBig5
  from ..models.workbench_generate_character_goal import WorkbenchGenerateCharacterGoal
  from ..models.workbench_generate_character_preferences import WorkbenchGenerateCharacterPreferences





T = TypeVar("T", bound="WorkbenchGenerateCharacterGenerated")



@_attrs_define
class WorkbenchGenerateCharacterGenerated:
    """ 
        Attributes:
            bio (str):
            personality_prompt (str):
            behaviors (WorkbenchGenerateCharacterBehaviors | Unset):
            big5 (WorkbenchGenerateCharacterBig5 | Unset):
            dimensions (Any | Unset):
            initial_goals (list[WorkbenchGenerateCharacterGoal] | None | Unset):
            origin_prompt_instructions (str | Unset):
            preferences (WorkbenchGenerateCharacterPreferences | Unset):
            primary_traits (list[str] | None | Unset):
            speech_patterns (list[str] | None | Unset):
            true_dislikes (list[str] | None | Unset):
            true_interests (list[str] | None | Unset):
            world_description (str | Unset):
     """

    bio: str
    personality_prompt: str
    behaviors: WorkbenchGenerateCharacterBehaviors | Unset = UNSET
    big5: WorkbenchGenerateCharacterBig5 | Unset = UNSET
    dimensions: Any | Unset = UNSET
    initial_goals: list[WorkbenchGenerateCharacterGoal] | None | Unset = UNSET
    origin_prompt_instructions: str | Unset = UNSET
    preferences: WorkbenchGenerateCharacterPreferences | Unset = UNSET
    primary_traits: list[str] | None | Unset = UNSET
    speech_patterns: list[str] | None | Unset = UNSET
    true_dislikes: list[str] | None | Unset = UNSET
    true_interests: list[str] | None | Unset = UNSET
    world_description: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.workbench_generate_character_behaviors import WorkbenchGenerateCharacterBehaviors
        from ..models.workbench_generate_character_big_5 import WorkbenchGenerateCharacterBig5
        from ..models.workbench_generate_character_goal import WorkbenchGenerateCharacterGoal
        from ..models.workbench_generate_character_preferences import WorkbenchGenerateCharacterPreferences
        bio = self.bio

        personality_prompt = self.personality_prompt

        behaviors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.behaviors, Unset):
            behaviors = self.behaviors.to_dict()

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        dimensions = self.dimensions

        initial_goals: list[dict[str, Any]] | None | Unset
        if isinstance(self.initial_goals, Unset):
            initial_goals = UNSET
        elif isinstance(self.initial_goals, list):
            initial_goals = []
            for initial_goals_type_0_item_data in self.initial_goals:
                initial_goals_type_0_item = initial_goals_type_0_item_data.to_dict()
                initial_goals.append(initial_goals_type_0_item)


        else:
            initial_goals = self.initial_goals

        origin_prompt_instructions = self.origin_prompt_instructions

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

        world_description = self.world_description


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "bio": bio,
            "personality_prompt": personality_prompt,
        })
        if behaviors is not UNSET:
            field_dict["behaviors"] = behaviors
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if initial_goals is not UNSET:
            field_dict["initial_goals"] = initial_goals
        if origin_prompt_instructions is not UNSET:
            field_dict["origin_prompt_instructions"] = origin_prompt_instructions
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
        if world_description is not UNSET:
            field_dict["world_description"] = world_description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workbench_generate_character_behaviors import WorkbenchGenerateCharacterBehaviors
        from ..models.workbench_generate_character_big_5 import WorkbenchGenerateCharacterBig5
        from ..models.workbench_generate_character_goal import WorkbenchGenerateCharacterGoal
        from ..models.workbench_generate_character_preferences import WorkbenchGenerateCharacterPreferences
        d = dict(src_dict)
        bio = d.pop("bio")

        personality_prompt = d.pop("personality_prompt")

        _behaviors = d.pop("behaviors", UNSET)
        behaviors: WorkbenchGenerateCharacterBehaviors | Unset
        if isinstance(_behaviors,  Unset):
            behaviors = UNSET
        else:
            behaviors = WorkbenchGenerateCharacterBehaviors.from_dict(_behaviors)




        _big5 = d.pop("big5", UNSET)
        big5: WorkbenchGenerateCharacterBig5 | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = WorkbenchGenerateCharacterBig5.from_dict(_big5)




        dimensions = d.pop("dimensions", UNSET)

        def _parse_initial_goals(data: object) -> list[WorkbenchGenerateCharacterGoal] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                initial_goals_type_0 = []
                _initial_goals_type_0 = data
                for initial_goals_type_0_item_data in (_initial_goals_type_0):
                    initial_goals_type_0_item = WorkbenchGenerateCharacterGoal.from_dict(initial_goals_type_0_item_data)



                    initial_goals_type_0.append(initial_goals_type_0_item)

                return initial_goals_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchGenerateCharacterGoal] | None | Unset, data)

        initial_goals = _parse_initial_goals(d.pop("initial_goals", UNSET))


        origin_prompt_instructions = d.pop("origin_prompt_instructions", UNSET)

        _preferences = d.pop("preferences", UNSET)
        preferences: WorkbenchGenerateCharacterPreferences | Unset
        if isinstance(_preferences,  Unset):
            preferences = UNSET
        else:
            preferences = WorkbenchGenerateCharacterPreferences.from_dict(_preferences)




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


        world_description = d.pop("world_description", UNSET)

        workbench_generate_character_generated = cls(
            bio=bio,
            personality_prompt=personality_prompt,
            behaviors=behaviors,
            big5=big5,
            dimensions=dimensions,
            initial_goals=initial_goals,
            origin_prompt_instructions=origin_prompt_instructions,
            preferences=preferences,
            primary_traits=primary_traits,
            speech_patterns=speech_patterns,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
            world_description=world_description,
        )

        return workbench_generate_character_generated

