from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.dialogue_msg_huma import DialogueMsgHuma





T = TypeVar("T", bound="AgentDialogueInputBody")



@_attrs_define
class AgentDialogueInputBody:
    """ 
        Attributes:
            messages (list[DialogueMsgHuma] | None): Conversation messages
            user_id (str): ID of the user
            schema (str | Unset): A URL to the JSON Schema for this object.
            enriched_context (Any | Unset): Pre-built enriched context JSON
            instance_id (str | Unset): Agent instance identifier
            request_type (str | Unset): Request type
            scene_guidance (str | Unset): Scene guidance prompt
            tool_config (Any | Unset): Tool configuration
     """

    messages: list[DialogueMsgHuma] | None
    user_id: str
    schema: str | Unset = UNSET
    enriched_context: Any | Unset = UNSET
    instance_id: str | Unset = UNSET
    request_type: str | Unset = UNSET
    scene_guidance: str | Unset = UNSET
    tool_config: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.dialogue_msg_huma import DialogueMsgHuma
        messages: list[dict[str, Any]] | None
        if isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)


        else:
            messages = self.messages

        user_id = self.user_id

        schema = self.schema

        enriched_context = self.enriched_context

        instance_id = self.instance_id

        request_type = self.request_type

        scene_guidance = self.scene_guidance

        tool_config = self.tool_config


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "messages": messages,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if enriched_context is not UNSET:
            field_dict["enriched_context"] = enriched_context
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if request_type is not UNSET:
            field_dict["request_type"] = request_type
        if scene_guidance is not UNSET:
            field_dict["scene_guidance"] = scene_guidance
        if tool_config is not UNSET:
            field_dict["tool_config"] = tool_config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dialogue_msg_huma import DialogueMsgHuma
        d = dict(src_dict)
        def _parse_messages(data: object) -> list[DialogueMsgHuma] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in (_messages_type_0):
                    messages_type_0_item = DialogueMsgHuma.from_dict(messages_type_0_item_data)



                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DialogueMsgHuma] | None, data)

        messages = _parse_messages(d.pop("messages"))


        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        enriched_context = d.pop("enriched_context", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        request_type = d.pop("request_type", UNSET)

        scene_guidance = d.pop("scene_guidance", UNSET)

        tool_config = d.pop("tool_config", UNSET)

        agent_dialogue_input_body = cls(
            messages=messages,
            user_id=user_id,
            schema=schema,
            enriched_context=enriched_context,
            instance_id=instance_id,
            request_type=request_type,
            scene_guidance=scene_guidance,
            tool_config=tool_config,
        )

        return agent_dialogue_input_body

