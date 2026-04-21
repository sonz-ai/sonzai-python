from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.seed_lore_generation_context_entity_terminology import SeedLoreGenerationContextEntityTerminology





T = TypeVar("T", bound="SeedLoreGenerationContext")



@_attrs_define
class SeedLoreGenerationContext:
    """ 
        Attributes:
            world_description (str):
            creator_onboarding_context (str | Unset):
            entity_terminology (SeedLoreGenerationContextEntityTerminology | Unset):
            origin_prompt_instructions (str | Unset):
     """

    world_description: str
    creator_onboarding_context: str | Unset = UNSET
    entity_terminology: SeedLoreGenerationContextEntityTerminology | Unset = UNSET
    origin_prompt_instructions: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.seed_lore_generation_context_entity_terminology import SeedLoreGenerationContextEntityTerminology
        world_description = self.world_description

        creator_onboarding_context = self.creator_onboarding_context

        entity_terminology: dict[str, Any] | Unset = UNSET
        if not isinstance(self.entity_terminology, Unset):
            entity_terminology = self.entity_terminology.to_dict()

        origin_prompt_instructions = self.origin_prompt_instructions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "worldDescription": world_description,
        })
        if creator_onboarding_context is not UNSET:
            field_dict["creatorOnboardingContext"] = creator_onboarding_context
        if entity_terminology is not UNSET:
            field_dict["entityTerminology"] = entity_terminology
        if origin_prompt_instructions is not UNSET:
            field_dict["originPromptInstructions"] = origin_prompt_instructions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_lore_generation_context_entity_terminology import SeedLoreGenerationContextEntityTerminology
        d = dict(src_dict)
        world_description = d.pop("worldDescription")

        creator_onboarding_context = d.pop("creatorOnboardingContext", UNSET)

        _entity_terminology = d.pop("entityTerminology", UNSET)
        entity_terminology: SeedLoreGenerationContextEntityTerminology | Unset
        if isinstance(_entity_terminology,  Unset):
            entity_terminology = UNSET
        else:
            entity_terminology = SeedLoreGenerationContextEntityTerminology.from_dict(_entity_terminology)




        origin_prompt_instructions = d.pop("originPromptInstructions", UNSET)

        seed_lore_generation_context = cls(
            world_description=world_description,
            creator_onboarding_context=creator_onboarding_context,
            entity_terminology=entity_terminology,
            origin_prompt_instructions=origin_prompt_instructions,
        )

        return seed_lore_generation_context

