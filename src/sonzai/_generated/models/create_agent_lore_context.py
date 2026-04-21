from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_agent_lore_context_entity_terminology import CreateAgentLoreContextEntityTerminology





T = TypeVar("T", bound="CreateAgentLoreContext")



@_attrs_define
class CreateAgentLoreContext:
    """ 
        Attributes:
            world_description (str):
            entity_terminology (CreateAgentLoreContextEntityTerminology | Unset):
            origin_prompt_instructions (str | Unset):
     """

    world_description: str
    entity_terminology: CreateAgentLoreContextEntityTerminology | Unset = UNSET
    origin_prompt_instructions: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_agent_lore_context_entity_terminology import CreateAgentLoreContextEntityTerminology
        world_description = self.world_description

        entity_terminology: dict[str, Any] | Unset = UNSET
        if not isinstance(self.entity_terminology, Unset):
            entity_terminology = self.entity_terminology.to_dict()

        origin_prompt_instructions = self.origin_prompt_instructions


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "world_description": world_description,
        })
        if entity_terminology is not UNSET:
            field_dict["entity_terminology"] = entity_terminology
        if origin_prompt_instructions is not UNSET:
            field_dict["origin_prompt_instructions"] = origin_prompt_instructions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_agent_lore_context_entity_terminology import CreateAgentLoreContextEntityTerminology
        d = dict(src_dict)
        world_description = d.pop("world_description")

        _entity_terminology = d.pop("entity_terminology", UNSET)
        entity_terminology: CreateAgentLoreContextEntityTerminology | Unset
        if isinstance(_entity_terminology,  Unset):
            entity_terminology = UNSET
        else:
            entity_terminology = CreateAgentLoreContextEntityTerminology.from_dict(_entity_terminology)




        origin_prompt_instructions = d.pop("origin_prompt_instructions", UNSET)

        create_agent_lore_context = cls(
            world_description=world_description,
            entity_terminology=entity_terminology,
            origin_prompt_instructions=origin_prompt_instructions,
        )

        return create_agent_lore_context

