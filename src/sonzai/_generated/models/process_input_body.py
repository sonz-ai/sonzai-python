from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.process_message import ProcessMessage





T = TypeVar("T", bound="ProcessInputBody")



@_attrs_define
class ProcessInputBody:
    """ 
        Attributes:
            messages (list[ProcessMessage] | None): Conversation transcript (minimum 2 messages)
            user_id (str): ID of the user whose conversation is being processed
            schema (str | Unset): A URL to the JSON Schema for this object.
            instance_id (str | Unset): Agent instance scope
            model (str | Unset): LLM model (informational only)
            provider (str | Unset): LLM provider (informational only)
            session_id (str | Unset): Session identifier (auto-generated if empty)
     """

    messages: list[ProcessMessage] | None
    user_id: str
    schema: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    model: str | Unset = UNSET
    provider: str | Unset = UNSET
    session_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.process_message import ProcessMessage
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

        instance_id = self.instance_id

        model = self.model

        provider = self.provider

        session_id = self.session_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "messages": messages,
            "userId": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if instance_id is not UNSET:
            field_dict["instanceId"] = instance_id
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_message import ProcessMessage
        d = dict(src_dict)
        def _parse_messages(data: object) -> list[ProcessMessage] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in (_messages_type_0):
                    messages_type_0_item = ProcessMessage.from_dict(messages_type_0_item_data)



                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ProcessMessage] | None, data)

        messages = _parse_messages(d.pop("messages"))


        user_id = d.pop("userId")

        schema = d.pop("$schema", UNSET)

        instance_id = d.pop("instanceId", UNSET)

        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        session_id = d.pop("sessionId", UNSET)

        process_input_body = cls(
            messages=messages,
            user_id=user_id,
            schema=schema,
            instance_id=instance_id,
            model=model,
            provider=provider,
            session_id=session_id,
        )

        return process_input_body

