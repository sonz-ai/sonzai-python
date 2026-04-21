from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.seed_identity_memory_template import SeedIdentityMemoryTemplate
  from ..models.seed_lore_generation_context import SeedLoreGenerationContext
  from ..models.seed_memory_big_5 import SeedMemoryBig5
  from ..models.seed_static_lore_memory import SeedStaticLoreMemory





T = TypeVar("T", bound="GenerateSeedMemoriesInputBody")



@_attrs_define
class GenerateSeedMemoriesInputBody:
    """ 
        Attributes:
            agent_name (str): Agent display name
            personality_prompt (str): Personality prompt text
            speech_patterns (list[str] | None): Agent's speech patterns
            true_interests (list[str] | None): Agent's true interests
            schema (str | Unset): A URL to the JSON Schema for this object.
            big5 (SeedMemoryBig5 | Unset):
            creator_display_name (str | Unset): Creator's display name
            generate_origin_story (bool | Unset): Whether to generate origin story
            generate_personalized_memories (bool | Unset): Whether to generate personalized memories
            identity_memory_templates (list[SeedIdentityMemoryTemplate] | None | Unset): Identity memory templates
            lore_generation_context (SeedLoreGenerationContext | Unset):
            primary_traits (list[str] | None | Unset): Primary personality traits
            static_lore_memories (list[SeedStaticLoreMemory] | None | Unset): Pre-defined lore memories
            true_dislikes (list[str] | None | Unset): Agent's true dislikes
     """

    agent_name: str
    personality_prompt: str
    speech_patterns: list[str] | None
    true_interests: list[str] | None
    schema: str | Unset = UNSET
    big5: SeedMemoryBig5 | Unset = UNSET
    creator_display_name: str | Unset = UNSET
    generate_origin_story: bool | Unset = UNSET
    generate_personalized_memories: bool | Unset = UNSET
    identity_memory_templates: list[SeedIdentityMemoryTemplate] | None | Unset = UNSET
    lore_generation_context: SeedLoreGenerationContext | Unset = UNSET
    primary_traits: list[str] | None | Unset = UNSET
    static_lore_memories: list[SeedStaticLoreMemory] | None | Unset = UNSET
    true_dislikes: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.seed_identity_memory_template import SeedIdentityMemoryTemplate
        from ..models.seed_lore_generation_context import SeedLoreGenerationContext
        from ..models.seed_memory_big_5 import SeedMemoryBig5
        from ..models.seed_static_lore_memory import SeedStaticLoreMemory
        agent_name = self.agent_name

        personality_prompt = self.personality_prompt

        speech_patterns: list[str] | None
        if isinstance(self.speech_patterns, list):
            speech_patterns = self.speech_patterns


        else:
            speech_patterns = self.speech_patterns

        true_interests: list[str] | None
        if isinstance(self.true_interests, list):
            true_interests = self.true_interests


        else:
            true_interests = self.true_interests

        schema = self.schema

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        creator_display_name = self.creator_display_name

        generate_origin_story = self.generate_origin_story

        generate_personalized_memories = self.generate_personalized_memories

        identity_memory_templates: list[dict[str, Any]] | None | Unset
        if isinstance(self.identity_memory_templates, Unset):
            identity_memory_templates = UNSET
        elif isinstance(self.identity_memory_templates, list):
            identity_memory_templates = []
            for identity_memory_templates_type_0_item_data in self.identity_memory_templates:
                identity_memory_templates_type_0_item = identity_memory_templates_type_0_item_data.to_dict()
                identity_memory_templates.append(identity_memory_templates_type_0_item)


        else:
            identity_memory_templates = self.identity_memory_templates

        lore_generation_context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.lore_generation_context, Unset):
            lore_generation_context = self.lore_generation_context.to_dict()

        primary_traits: list[str] | None | Unset
        if isinstance(self.primary_traits, Unset):
            primary_traits = UNSET
        elif isinstance(self.primary_traits, list):
            primary_traits = self.primary_traits


        else:
            primary_traits = self.primary_traits

        static_lore_memories: list[dict[str, Any]] | None | Unset
        if isinstance(self.static_lore_memories, Unset):
            static_lore_memories = UNSET
        elif isinstance(self.static_lore_memories, list):
            static_lore_memories = []
            for static_lore_memories_type_0_item_data in self.static_lore_memories:
                static_lore_memories_type_0_item = static_lore_memories_type_0_item_data.to_dict()
                static_lore_memories.append(static_lore_memories_type_0_item)


        else:
            static_lore_memories = self.static_lore_memories

        true_dislikes: list[str] | None | Unset
        if isinstance(self.true_dislikes, Unset):
            true_dislikes = UNSET
        elif isinstance(self.true_dislikes, list):
            true_dislikes = self.true_dislikes


        else:
            true_dislikes = self.true_dislikes


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentName": agent_name,
            "personalityPrompt": personality_prompt,
            "speechPatterns": speech_patterns,
            "trueInterests": true_interests,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if creator_display_name is not UNSET:
            field_dict["creatorDisplayName"] = creator_display_name
        if generate_origin_story is not UNSET:
            field_dict["generateOriginStory"] = generate_origin_story
        if generate_personalized_memories is not UNSET:
            field_dict["generatePersonalizedMemories"] = generate_personalized_memories
        if identity_memory_templates is not UNSET:
            field_dict["identityMemoryTemplates"] = identity_memory_templates
        if lore_generation_context is not UNSET:
            field_dict["loreGenerationContext"] = lore_generation_context
        if primary_traits is not UNSET:
            field_dict["primaryTraits"] = primary_traits
        if static_lore_memories is not UNSET:
            field_dict["staticLoreMemories"] = static_lore_memories
        if true_dislikes is not UNSET:
            field_dict["trueDislikes"] = true_dislikes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_identity_memory_template import SeedIdentityMemoryTemplate
        from ..models.seed_lore_generation_context import SeedLoreGenerationContext
        from ..models.seed_memory_big_5 import SeedMemoryBig5
        from ..models.seed_static_lore_memory import SeedStaticLoreMemory
        d = dict(src_dict)
        agent_name = d.pop("agentName")

        personality_prompt = d.pop("personalityPrompt")

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

        speech_patterns = _parse_speech_patterns(d.pop("speechPatterns"))


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

        true_interests = _parse_true_interests(d.pop("trueInterests"))


        schema = d.pop("$schema", UNSET)

        _big5 = d.pop("big5", UNSET)
        big5: SeedMemoryBig5 | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = SeedMemoryBig5.from_dict(_big5)




        creator_display_name = d.pop("creatorDisplayName", UNSET)

        generate_origin_story = d.pop("generateOriginStory", UNSET)

        generate_personalized_memories = d.pop("generatePersonalizedMemories", UNSET)

        def _parse_identity_memory_templates(data: object) -> list[SeedIdentityMemoryTemplate] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                identity_memory_templates_type_0 = []
                _identity_memory_templates_type_0 = data
                for identity_memory_templates_type_0_item_data in (_identity_memory_templates_type_0):
                    identity_memory_templates_type_0_item = SeedIdentityMemoryTemplate.from_dict(identity_memory_templates_type_0_item_data)



                    identity_memory_templates_type_0.append(identity_memory_templates_type_0_item)

                return identity_memory_templates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SeedIdentityMemoryTemplate] | None | Unset, data)

        identity_memory_templates = _parse_identity_memory_templates(d.pop("identityMemoryTemplates", UNSET))


        _lore_generation_context = d.pop("loreGenerationContext", UNSET)
        lore_generation_context: SeedLoreGenerationContext | Unset
        if isinstance(_lore_generation_context,  Unset):
            lore_generation_context = UNSET
        else:
            lore_generation_context = SeedLoreGenerationContext.from_dict(_lore_generation_context)




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

        primary_traits = _parse_primary_traits(d.pop("primaryTraits", UNSET))


        def _parse_static_lore_memories(data: object) -> list[SeedStaticLoreMemory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                static_lore_memories_type_0 = []
                _static_lore_memories_type_0 = data
                for static_lore_memories_type_0_item_data in (_static_lore_memories_type_0):
                    static_lore_memories_type_0_item = SeedStaticLoreMemory.from_dict(static_lore_memories_type_0_item_data)



                    static_lore_memories_type_0.append(static_lore_memories_type_0_item)

                return static_lore_memories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SeedStaticLoreMemory] | None | Unset, data)

        static_lore_memories = _parse_static_lore_memories(d.pop("staticLoreMemories", UNSET))


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

        true_dislikes = _parse_true_dislikes(d.pop("trueDislikes", UNSET))


        generate_seed_memories_input_body = cls(
            agent_name=agent_name,
            personality_prompt=personality_prompt,
            speech_patterns=speech_patterns,
            true_interests=true_interests,
            schema=schema,
            big5=big5,
            creator_display_name=creator_display_name,
            generate_origin_story=generate_origin_story,
            generate_personalized_memories=generate_personalized_memories,
            identity_memory_templates=identity_memory_templates,
            lore_generation_context=lore_generation_context,
            primary_traits=primary_traits,
            static_lore_memories=static_lore_memories,
            true_dislikes=true_dislikes,
        )

        return generate_seed_memories_input_body

