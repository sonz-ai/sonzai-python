from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_capabilities_input_body_memory_mode import UpdateCapabilitiesInputBodyMemoryMode
from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateCapabilitiesInputBody")



@_attrs_define
class UpdateCapabilitiesInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            image_generation (bool | Unset): Enable/disable image generation
            inventory (bool | Unset): Enable/disable inventory tracking
            knowledge_base (bool | Unset): Enable/disable knowledge base search
            memory_mode (UpdateCapabilitiesInputBodyMemoryMode | Unset): Supplementary memory recall timing. 'sync'
                (default) blocks context build until recall returns so facts land in the current turn. 'async' lets the recall
                race a deadline — slow hits spill to the next turn for lower first-response latency.
            remember_name (bool | Unset): Enable/disable remember name tool
            web_search (bool | Unset): Enable/disable web search tool
     """

    schema: str | Unset = UNSET
    image_generation: bool | Unset = UNSET
    inventory: bool | Unset = UNSET
    knowledge_base: bool | Unset = UNSET
    memory_mode: UpdateCapabilitiesInputBodyMemoryMode | Unset = UNSET
    remember_name: bool | Unset = UNSET
    web_search: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        image_generation = self.image_generation

        inventory = self.inventory

        knowledge_base = self.knowledge_base

        memory_mode: str | Unset = UNSET
        if not isinstance(self.memory_mode, Unset):
            memory_mode = self.memory_mode.value


        remember_name = self.remember_name

        web_search = self.web_search


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if image_generation is not UNSET:
            field_dict["imageGeneration"] = image_generation
        if inventory is not UNSET:
            field_dict["inventory"] = inventory
        if knowledge_base is not UNSET:
            field_dict["knowledgeBase"] = knowledge_base
        if memory_mode is not UNSET:
            field_dict["memoryMode"] = memory_mode
        if remember_name is not UNSET:
            field_dict["rememberName"] = remember_name
        if web_search is not UNSET:
            field_dict["webSearch"] = web_search

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        image_generation = d.pop("imageGeneration", UNSET)

        inventory = d.pop("inventory", UNSET)

        knowledge_base = d.pop("knowledgeBase", UNSET)

        _memory_mode = d.pop("memoryMode", UNSET)
        memory_mode: UpdateCapabilitiesInputBodyMemoryMode | Unset
        if isinstance(_memory_mode,  Unset):
            memory_mode = UNSET
        else:
            memory_mode = UpdateCapabilitiesInputBodyMemoryMode(_memory_mode)




        remember_name = d.pop("rememberName", UNSET)

        web_search = d.pop("webSearch", UNSET)

        update_capabilities_input_body = cls(
            schema=schema,
            image_generation=image_generation,
            inventory=inventory,
            knowledge_base=knowledge_base,
            memory_mode=memory_mode,
            remember_name=remember_name,
            web_search=web_search,
        )

        return update_capabilities_input_body

