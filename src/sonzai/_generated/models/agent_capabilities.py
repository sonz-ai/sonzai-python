from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.custom_tool_definition import CustomToolDefinition
  from ..models.pending_capability import PendingCapability





T = TypeVar("T", bound="AgentCapabilities")



@_attrs_define
class AgentCapabilities:
    """ 
        Attributes:
            image_generation (bool):
            music_generation (bool):
            video_generation (bool):
            voice_generation (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
            custom_tools (list[CustomToolDefinition] | None | Unset):
            image_unlocked_at (datetime.datetime | Unset):
            inventory (bool | Unset):
            knowledge_base (bool | Unset):
            knowledge_base_project_id (str | Unset):
            knowledge_base_scope_mode (str | Unset):
            music_unlocked_at (datetime.datetime | Unset):
            pending_capabilities (list[PendingCapability] | None | Unset):
            remember_name (bool | Unset):
            video_unlocked_at (datetime.datetime | Unset):
            voice_id (str | Unset):
            voice_tier (int | Unset):
            voice_unlocked_at (datetime.datetime | Unset):
            web_search (bool | Unset):
     """

    image_generation: bool
    music_generation: bool
    video_generation: bool
    voice_generation: bool
    schema: str | Unset = UNSET
    custom_tools: list[CustomToolDefinition] | None | Unset = UNSET
    image_unlocked_at: datetime.datetime | Unset = UNSET
    inventory: bool | Unset = UNSET
    knowledge_base: bool | Unset = UNSET
    knowledge_base_project_id: str | Unset = UNSET
    knowledge_base_scope_mode: str | Unset = UNSET
    music_unlocked_at: datetime.datetime | Unset = UNSET
    pending_capabilities: list[PendingCapability] | None | Unset = UNSET
    remember_name: bool | Unset = UNSET
    video_unlocked_at: datetime.datetime | Unset = UNSET
    voice_id: str | Unset = UNSET
    voice_tier: int | Unset = UNSET
    voice_unlocked_at: datetime.datetime | Unset = UNSET
    web_search: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_tool_definition import CustomToolDefinition
        from ..models.pending_capability import PendingCapability
        image_generation = self.image_generation

        music_generation = self.music_generation

        video_generation = self.video_generation

        voice_generation = self.voice_generation

        schema = self.schema

        custom_tools: list[dict[str, Any]] | None | Unset
        if isinstance(self.custom_tools, Unset):
            custom_tools = UNSET
        elif isinstance(self.custom_tools, list):
            custom_tools = []
            for custom_tools_type_0_item_data in self.custom_tools:
                custom_tools_type_0_item = custom_tools_type_0_item_data.to_dict()
                custom_tools.append(custom_tools_type_0_item)


        else:
            custom_tools = self.custom_tools

        image_unlocked_at: str | Unset = UNSET
        if not isinstance(self.image_unlocked_at, Unset):
            image_unlocked_at = self.image_unlocked_at.isoformat()

        inventory = self.inventory

        knowledge_base = self.knowledge_base

        knowledge_base_project_id = self.knowledge_base_project_id

        knowledge_base_scope_mode = self.knowledge_base_scope_mode

        music_unlocked_at: str | Unset = UNSET
        if not isinstance(self.music_unlocked_at, Unset):
            music_unlocked_at = self.music_unlocked_at.isoformat()

        pending_capabilities: list[dict[str, Any]] | None | Unset
        if isinstance(self.pending_capabilities, Unset):
            pending_capabilities = UNSET
        elif isinstance(self.pending_capabilities, list):
            pending_capabilities = []
            for pending_capabilities_type_0_item_data in self.pending_capabilities:
                pending_capabilities_type_0_item = pending_capabilities_type_0_item_data.to_dict()
                pending_capabilities.append(pending_capabilities_type_0_item)


        else:
            pending_capabilities = self.pending_capabilities

        remember_name = self.remember_name

        video_unlocked_at: str | Unset = UNSET
        if not isinstance(self.video_unlocked_at, Unset):
            video_unlocked_at = self.video_unlocked_at.isoformat()

        voice_id = self.voice_id

        voice_tier = self.voice_tier

        voice_unlocked_at: str | Unset = UNSET
        if not isinstance(self.voice_unlocked_at, Unset):
            voice_unlocked_at = self.voice_unlocked_at.isoformat()

        web_search = self.web_search


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "imageGeneration": image_generation,
            "musicGeneration": music_generation,
            "videoGeneration": video_generation,
            "voiceGeneration": voice_generation,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if custom_tools is not UNSET:
            field_dict["customTools"] = custom_tools
        if image_unlocked_at is not UNSET:
            field_dict["imageUnlockedAt"] = image_unlocked_at
        if inventory is not UNSET:
            field_dict["inventory"] = inventory
        if knowledge_base is not UNSET:
            field_dict["knowledgeBase"] = knowledge_base
        if knowledge_base_project_id is not UNSET:
            field_dict["knowledgeBaseProjectId"] = knowledge_base_project_id
        if knowledge_base_scope_mode is not UNSET:
            field_dict["knowledgeBaseScopeMode"] = knowledge_base_scope_mode
        if music_unlocked_at is not UNSET:
            field_dict["musicUnlockedAt"] = music_unlocked_at
        if pending_capabilities is not UNSET:
            field_dict["pendingCapabilities"] = pending_capabilities
        if remember_name is not UNSET:
            field_dict["rememberName"] = remember_name
        if video_unlocked_at is not UNSET:
            field_dict["videoUnlockedAt"] = video_unlocked_at
        if voice_id is not UNSET:
            field_dict["voiceId"] = voice_id
        if voice_tier is not UNSET:
            field_dict["voiceTier"] = voice_tier
        if voice_unlocked_at is not UNSET:
            field_dict["voiceUnlockedAt"] = voice_unlocked_at
        if web_search is not UNSET:
            field_dict["webSearch"] = web_search

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_tool_definition import CustomToolDefinition
        from ..models.pending_capability import PendingCapability
        d = dict(src_dict)
        image_generation = d.pop("imageGeneration")

        music_generation = d.pop("musicGeneration")

        video_generation = d.pop("videoGeneration")

        voice_generation = d.pop("voiceGeneration")

        schema = d.pop("$schema", UNSET)

        def _parse_custom_tools(data: object) -> list[CustomToolDefinition] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                custom_tools_type_0 = []
                _custom_tools_type_0 = data
                for custom_tools_type_0_item_data in (_custom_tools_type_0):
                    custom_tools_type_0_item = CustomToolDefinition.from_dict(custom_tools_type_0_item_data)



                    custom_tools_type_0.append(custom_tools_type_0_item)

                return custom_tools_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CustomToolDefinition] | None | Unset, data)

        custom_tools = _parse_custom_tools(d.pop("customTools", UNSET))


        _image_unlocked_at = d.pop("imageUnlockedAt", UNSET)
        image_unlocked_at: datetime.datetime | Unset
        if isinstance(_image_unlocked_at,  Unset):
            image_unlocked_at = UNSET
        else:
            image_unlocked_at = isoparse(_image_unlocked_at)




        inventory = d.pop("inventory", UNSET)

        knowledge_base = d.pop("knowledgeBase", UNSET)

        knowledge_base_project_id = d.pop("knowledgeBaseProjectId", UNSET)

        knowledge_base_scope_mode = d.pop("knowledgeBaseScopeMode", UNSET)

        _music_unlocked_at = d.pop("musicUnlockedAt", UNSET)
        music_unlocked_at: datetime.datetime | Unset
        if isinstance(_music_unlocked_at,  Unset):
            music_unlocked_at = UNSET
        else:
            music_unlocked_at = isoparse(_music_unlocked_at)




        def _parse_pending_capabilities(data: object) -> list[PendingCapability] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pending_capabilities_type_0 = []
                _pending_capabilities_type_0 = data
                for pending_capabilities_type_0_item_data in (_pending_capabilities_type_0):
                    pending_capabilities_type_0_item = PendingCapability.from_dict(pending_capabilities_type_0_item_data)



                    pending_capabilities_type_0.append(pending_capabilities_type_0_item)

                return pending_capabilities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PendingCapability] | None | Unset, data)

        pending_capabilities = _parse_pending_capabilities(d.pop("pendingCapabilities", UNSET))


        remember_name = d.pop("rememberName", UNSET)

        _video_unlocked_at = d.pop("videoUnlockedAt", UNSET)
        video_unlocked_at: datetime.datetime | Unset
        if isinstance(_video_unlocked_at,  Unset):
            video_unlocked_at = UNSET
        else:
            video_unlocked_at = isoparse(_video_unlocked_at)




        voice_id = d.pop("voiceId", UNSET)

        voice_tier = d.pop("voiceTier", UNSET)

        _voice_unlocked_at = d.pop("voiceUnlockedAt", UNSET)
        voice_unlocked_at: datetime.datetime | Unset
        if isinstance(_voice_unlocked_at,  Unset):
            voice_unlocked_at = UNSET
        else:
            voice_unlocked_at = isoparse(_voice_unlocked_at)




        web_search = d.pop("webSearch", UNSET)

        agent_capabilities = cls(
            image_generation=image_generation,
            music_generation=music_generation,
            video_generation=video_generation,
            voice_generation=voice_generation,
            schema=schema,
            custom_tools=custom_tools,
            image_unlocked_at=image_unlocked_at,
            inventory=inventory,
            knowledge_base=knowledge_base,
            knowledge_base_project_id=knowledge_base_project_id,
            knowledge_base_scope_mode=knowledge_base_scope_mode,
            music_unlocked_at=music_unlocked_at,
            pending_capabilities=pending_capabilities,
            remember_name=remember_name,
            video_unlocked_at=video_unlocked_at,
            voice_id=voice_id,
            voice_tier=voice_tier,
            voice_unlocked_at=voice_unlocked_at,
            web_search=web_search,
        )

        return agent_capabilities

