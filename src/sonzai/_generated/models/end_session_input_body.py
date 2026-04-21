from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.session_message import SessionMessage





T = TypeVar("T", bound="EndSessionInputBody")



@_attrs_define
class EndSessionInputBody:
    """ 
        Attributes:
            duration_seconds (int): Session duration in seconds
            session_id (str): Session identifier to end
            total_messages (int): Total number of messages in the session
            user_id (str): ID of the user ending the session
            schema (str | Unset): A URL to the JSON Schema for this object.
            instance_id (str | Unset): Optional agent instance identifier
            messages (list[SessionMessage] | None | Unset): Full conversation for memory extraction
            user_display_name (str | Unset): Optional display name for the user; when supplied, skips the CE
                UserPrimingMetadata lookup
            user_timezone (str | Unset): Optional IANA timezone for the user (e.g., Asia/Singapore); when supplied, skips
                the CE UserPrimingMetadata lookup
     """

    duration_seconds: int
    session_id: str
    total_messages: int
    user_id: str
    schema: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    messages: list[SessionMessage] | None | Unset = UNSET
    user_display_name: str | Unset = UNSET
    user_timezone: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.session_message import SessionMessage
        duration_seconds = self.duration_seconds

        session_id = self.session_id

        total_messages = self.total_messages

        user_id = self.user_id

        schema = self.schema

        instance_id = self.instance_id

        messages: list[dict[str, Any]] | None | Unset
        if isinstance(self.messages, Unset):
            messages = UNSET
        elif isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)


        else:
            messages = self.messages

        user_display_name = self.user_display_name

        user_timezone = self.user_timezone


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "duration_seconds": duration_seconds,
            "session_id": session_id,
            "total_messages": total_messages,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if messages is not UNSET:
            field_dict["messages"] = messages
        if user_display_name is not UNSET:
            field_dict["user_display_name"] = user_display_name
        if user_timezone is not UNSET:
            field_dict["user_timezone"] = user_timezone

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_message import SessionMessage
        d = dict(src_dict)
        duration_seconds = d.pop("duration_seconds")

        session_id = d.pop("session_id")

        total_messages = d.pop("total_messages")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        def _parse_messages(data: object) -> list[SessionMessage] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in (_messages_type_0):
                    messages_type_0_item = SessionMessage.from_dict(messages_type_0_item_data)



                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SessionMessage] | None | Unset, data)

        messages = _parse_messages(d.pop("messages", UNSET))


        user_display_name = d.pop("user_display_name", UNSET)

        user_timezone = d.pop("user_timezone", UNSET)

        end_session_input_body = cls(
            duration_seconds=duration_seconds,
            session_id=session_id,
            total_messages=total_messages,
            user_id=user_id,
            schema=schema,
            instance_id=instance_id,
            messages=messages,
            user_display_name=user_display_name,
            user_timezone=user_timezone,
        )

        return end_session_input_body

