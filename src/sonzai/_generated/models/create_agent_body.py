from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_agent_body_behaviors_struct import CreateAgentBodyBehaviorsStruct
  from ..models.create_agent_body_big_5_struct import CreateAgentBodyBig5Struct
  from ..models.create_agent_body_capabilities_struct import CreateAgentBodyCapabilitiesStruct
  from ..models.create_agent_body_dimensions_struct import CreateAgentBodyDimensionsStruct
  from ..models.create_agent_body_preferences_struct import CreateAgentBodyPreferencesStruct
  from ..models.create_agent_body_tool_capabilities_struct import CreateAgentBodyToolCapabilitiesStruct
  from ..models.create_agent_goal import CreateAgentGoal
  from ..models.create_agent_lore_context import CreateAgentLoreContext
  from ..models.create_agent_seed_memory import CreateAgentSeedMemory





T = TypeVar("T", bound="CreateAgentBody")



@_attrs_define
class CreateAgentBody:
    """ 
        Attributes:
            name (str): Agent display name
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_id (str | Unset): Optional pre-set agent UUID
            avatar_url (str | Unset): Pre-existing avatar image URL
            behaviors (CreateAgentBodyBehaviorsStruct | Unset):
            big5 (CreateAgentBodyBig5Struct | Unset):
            bio (str | Unset): Agent biography
            capabilities (CreateAgentBodyCapabilitiesStruct | Unset):
            dimensions (CreateAgentBodyDimensionsStruct | Unset):
            gender (str | Unset): Agent gender
            generate_avatar (bool | Unset): Auto-generate avatar (default true)
            generate_origin_story (bool | Unset): Auto-generate origin story
            generate_personalized_memories (bool | Unset): Auto-generate personalized memories
            initial_goals (list[CreateAgentGoal] | None | Unset): Goals to set on creation
            language (str | Unset): Agent language
            lore_generation_context (CreateAgentLoreContext | Unset):
            personality_prompt (str | Unset): Core personality prompt
            preferences (CreateAgentBodyPreferencesStruct | Unset):
            primary_traits (list[str] | None | Unset): Primary personality traits
            project_id (str | Unset): Project UUID to assign
            seed_memories (list[CreateAgentSeedMemory] | None | Unset): Pre-generated lore entries
            speech_patterns (list[str] | None | Unset): Speech pattern descriptors
            tool_capabilities (CreateAgentBodyToolCapabilitiesStruct | Unset):
            true_dislikes (list[str] | None | Unset): Agent dislikes
            true_interests (list[str] | None | Unset): Agent interests
            user_display_name (str | Unset): Owner display name
            user_id (str | Unset): Owner user ID (for API-key auth)
     """

    name: str
    schema: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    avatar_url: str | Unset = UNSET
    behaviors: CreateAgentBodyBehaviorsStruct | Unset = UNSET
    big5: CreateAgentBodyBig5Struct | Unset = UNSET
    bio: str | Unset = UNSET
    capabilities: CreateAgentBodyCapabilitiesStruct | Unset = UNSET
    dimensions: CreateAgentBodyDimensionsStruct | Unset = UNSET
    gender: str | Unset = UNSET
    generate_avatar: bool | Unset = UNSET
    generate_origin_story: bool | Unset = UNSET
    generate_personalized_memories: bool | Unset = UNSET
    initial_goals: list[CreateAgentGoal] | None | Unset = UNSET
    language: str | Unset = UNSET
    lore_generation_context: CreateAgentLoreContext | Unset = UNSET
    personality_prompt: str | Unset = UNSET
    preferences: CreateAgentBodyPreferencesStruct | Unset = UNSET
    primary_traits: list[str] | None | Unset = UNSET
    project_id: str | Unset = UNSET
    seed_memories: list[CreateAgentSeedMemory] | None | Unset = UNSET
    speech_patterns: list[str] | None | Unset = UNSET
    tool_capabilities: CreateAgentBodyToolCapabilitiesStruct | Unset = UNSET
    true_dislikes: list[str] | None | Unset = UNSET
    true_interests: list[str] | None | Unset = UNSET
    user_display_name: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_agent_body_behaviors_struct import CreateAgentBodyBehaviorsStruct
        from ..models.create_agent_body_big_5_struct import CreateAgentBodyBig5Struct
        from ..models.create_agent_body_capabilities_struct import CreateAgentBodyCapabilitiesStruct
        from ..models.create_agent_body_dimensions_struct import CreateAgentBodyDimensionsStruct
        from ..models.create_agent_body_preferences_struct import CreateAgentBodyPreferencesStruct
        from ..models.create_agent_body_tool_capabilities_struct import CreateAgentBodyToolCapabilitiesStruct
        from ..models.create_agent_goal import CreateAgentGoal
        from ..models.create_agent_lore_context import CreateAgentLoreContext
        from ..models.create_agent_seed_memory import CreateAgentSeedMemory
        name = self.name

        schema = self.schema

        agent_id = self.agent_id

        avatar_url = self.avatar_url

        behaviors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.behaviors, Unset):
            behaviors = self.behaviors.to_dict()

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        bio = self.bio

        capabilities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()

        gender = self.gender

        generate_avatar = self.generate_avatar

        generate_origin_story = self.generate_origin_story

        generate_personalized_memories = self.generate_personalized_memories

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

        language = self.language

        lore_generation_context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.lore_generation_context, Unset):
            lore_generation_context = self.lore_generation_context.to_dict()

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

        project_id = self.project_id

        seed_memories: list[dict[str, Any]] | None | Unset
        if isinstance(self.seed_memories, Unset):
            seed_memories = UNSET
        elif isinstance(self.seed_memories, list):
            seed_memories = []
            for seed_memories_type_0_item_data in self.seed_memories:
                seed_memories_type_0_item = seed_memories_type_0_item_data.to_dict()
                seed_memories.append(seed_memories_type_0_item)


        else:
            seed_memories = self.seed_memories

        speech_patterns: list[str] | None | Unset
        if isinstance(self.speech_patterns, Unset):
            speech_patterns = UNSET
        elif isinstance(self.speech_patterns, list):
            speech_patterns = self.speech_patterns


        else:
            speech_patterns = self.speech_patterns

        tool_capabilities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tool_capabilities, Unset):
            tool_capabilities = self.tool_capabilities.to_dict()

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

        user_display_name = self.user_display_name

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if behaviors is not UNSET:
            field_dict["behaviors"] = behaviors
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if bio is not UNSET:
            field_dict["bio"] = bio
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if gender is not UNSET:
            field_dict["gender"] = gender
        if generate_avatar is not UNSET:
            field_dict["generate_avatar"] = generate_avatar
        if generate_origin_story is not UNSET:
            field_dict["generate_origin_story"] = generate_origin_story
        if generate_personalized_memories is not UNSET:
            field_dict["generate_personalized_memories"] = generate_personalized_memories
        if initial_goals is not UNSET:
            field_dict["initial_goals"] = initial_goals
        if language is not UNSET:
            field_dict["language"] = language
        if lore_generation_context is not UNSET:
            field_dict["lore_generation_context"] = lore_generation_context
        if personality_prompt is not UNSET:
            field_dict["personality_prompt"] = personality_prompt
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if primary_traits is not UNSET:
            field_dict["primary_traits"] = primary_traits
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if seed_memories is not UNSET:
            field_dict["seed_memories"] = seed_memories
        if speech_patterns is not UNSET:
            field_dict["speech_patterns"] = speech_patterns
        if tool_capabilities is not UNSET:
            field_dict["tool_capabilities"] = tool_capabilities
        if true_dislikes is not UNSET:
            field_dict["true_dislikes"] = true_dislikes
        if true_interests is not UNSET:
            field_dict["true_interests"] = true_interests
        if user_display_name is not UNSET:
            field_dict["user_display_name"] = user_display_name
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_agent_body_behaviors_struct import CreateAgentBodyBehaviorsStruct
        from ..models.create_agent_body_big_5_struct import CreateAgentBodyBig5Struct
        from ..models.create_agent_body_capabilities_struct import CreateAgentBodyCapabilitiesStruct
        from ..models.create_agent_body_dimensions_struct import CreateAgentBodyDimensionsStruct
        from ..models.create_agent_body_preferences_struct import CreateAgentBodyPreferencesStruct
        from ..models.create_agent_body_tool_capabilities_struct import CreateAgentBodyToolCapabilitiesStruct
        from ..models.create_agent_goal import CreateAgentGoal
        from ..models.create_agent_lore_context import CreateAgentLoreContext
        from ..models.create_agent_seed_memory import CreateAgentSeedMemory
        d = dict(src_dict)
        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        agent_id = d.pop("agent_id", UNSET)

        avatar_url = d.pop("avatar_url", UNSET)

        _behaviors = d.pop("behaviors", UNSET)
        behaviors: CreateAgentBodyBehaviorsStruct | Unset
        if isinstance(_behaviors,  Unset):
            behaviors = UNSET
        else:
            behaviors = CreateAgentBodyBehaviorsStruct.from_dict(_behaviors)




        _big5 = d.pop("big5", UNSET)
        big5: CreateAgentBodyBig5Struct | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = CreateAgentBodyBig5Struct.from_dict(_big5)




        bio = d.pop("bio", UNSET)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: CreateAgentBodyCapabilitiesStruct | Unset
        if isinstance(_capabilities,  Unset):
            capabilities = UNSET
        else:
            capabilities = CreateAgentBodyCapabilitiesStruct.from_dict(_capabilities)




        _dimensions = d.pop("dimensions", UNSET)
        dimensions: CreateAgentBodyDimensionsStruct | Unset
        if isinstance(_dimensions,  Unset):
            dimensions = UNSET
        else:
            dimensions = CreateAgentBodyDimensionsStruct.from_dict(_dimensions)




        gender = d.pop("gender", UNSET)

        generate_avatar = d.pop("generate_avatar", UNSET)

        generate_origin_story = d.pop("generate_origin_story", UNSET)

        generate_personalized_memories = d.pop("generate_personalized_memories", UNSET)

        def _parse_initial_goals(data: object) -> list[CreateAgentGoal] | None | Unset:
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
                    initial_goals_type_0_item = CreateAgentGoal.from_dict(initial_goals_type_0_item_data)



                    initial_goals_type_0.append(initial_goals_type_0_item)

                return initial_goals_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CreateAgentGoal] | None | Unset, data)

        initial_goals = _parse_initial_goals(d.pop("initial_goals", UNSET))


        language = d.pop("language", UNSET)

        _lore_generation_context = d.pop("lore_generation_context", UNSET)
        lore_generation_context: CreateAgentLoreContext | Unset
        if isinstance(_lore_generation_context,  Unset):
            lore_generation_context = UNSET
        else:
            lore_generation_context = CreateAgentLoreContext.from_dict(_lore_generation_context)




        personality_prompt = d.pop("personality_prompt", UNSET)

        _preferences = d.pop("preferences", UNSET)
        preferences: CreateAgentBodyPreferencesStruct | Unset
        if isinstance(_preferences,  Unset):
            preferences = UNSET
        else:
            preferences = CreateAgentBodyPreferencesStruct.from_dict(_preferences)




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


        project_id = d.pop("project_id", UNSET)

        def _parse_seed_memories(data: object) -> list[CreateAgentSeedMemory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                seed_memories_type_0 = []
                _seed_memories_type_0 = data
                for seed_memories_type_0_item_data in (_seed_memories_type_0):
                    seed_memories_type_0_item = CreateAgentSeedMemory.from_dict(seed_memories_type_0_item_data)



                    seed_memories_type_0.append(seed_memories_type_0_item)

                return seed_memories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CreateAgentSeedMemory] | None | Unset, data)

        seed_memories = _parse_seed_memories(d.pop("seed_memories", UNSET))


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


        _tool_capabilities = d.pop("tool_capabilities", UNSET)
        tool_capabilities: CreateAgentBodyToolCapabilitiesStruct | Unset
        if isinstance(_tool_capabilities,  Unset):
            tool_capabilities = UNSET
        else:
            tool_capabilities = CreateAgentBodyToolCapabilitiesStruct.from_dict(_tool_capabilities)




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


        user_display_name = d.pop("user_display_name", UNSET)

        user_id = d.pop("user_id", UNSET)

        create_agent_body = cls(
            name=name,
            schema=schema,
            agent_id=agent_id,
            avatar_url=avatar_url,
            behaviors=behaviors,
            big5=big5,
            bio=bio,
            capabilities=capabilities,
            dimensions=dimensions,
            gender=gender,
            generate_avatar=generate_avatar,
            generate_origin_story=generate_origin_story,
            generate_personalized_memories=generate_personalized_memories,
            initial_goals=initial_goals,
            language=language,
            lore_generation_context=lore_generation_context,
            personality_prompt=personality_prompt,
            preferences=preferences,
            primary_traits=primary_traits,
            project_id=project_id,
            seed_memories=seed_memories,
            speech_patterns=speech_patterns,
            tool_capabilities=tool_capabilities,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
            user_display_name=user_display_name,
            user_id=user_id,
        )

        return create_agent_body

