from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.trigger_event_input_body_metadata import TriggerEventInputBodyMetadata





T = TypeVar("T", bound="TriggerEventInputBody")



@_attrs_define
class TriggerEventInputBody:
    """ 
        Attributes:
            event_type (str): Type of game event (e.g. session_end, achievement, milestone)
            user_id (str): ID of the user triggering the event
            schema (str | Unset): A URL to the JSON Schema for this object.
            event_description (str | Unset): Human-readable event description
            instance_id (str | Unset): Agent instance scope
            language (str | Unset): Language code for diary generation (default: en)
            messages (Any | Unset): Raw recent chat messages for diary context
            metadata (TriggerEventInputBodyMetadata | Unset): Event metadata (achievement_id, milestone_type, etc.)
     """

    event_type: str
    user_id: str
    schema: str | Unset = UNSET
    event_description: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    language: str | Unset = UNSET
    messages: Any | Unset = UNSET
    metadata: TriggerEventInputBodyMetadata | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.trigger_event_input_body_metadata import TriggerEventInputBodyMetadata
        event_type = self.event_type

        user_id = self.user_id

        schema = self.schema

        event_description = self.event_description

        instance_id = self.instance_id

        language = self.language

        messages = self.messages

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "event_type": event_type,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if event_description is not UNSET:
            field_dict["event_description"] = event_description
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if language is not UNSET:
            field_dict["language"] = language
        if messages is not UNSET:
            field_dict["messages"] = messages
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trigger_event_input_body_metadata import TriggerEventInputBodyMetadata
        d = dict(src_dict)
        event_type = d.pop("event_type")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        event_description = d.pop("event_description", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        language = d.pop("language", UNSET)

        messages = d.pop("messages", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: TriggerEventInputBodyMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = TriggerEventInputBodyMetadata.from_dict(_metadata)




        trigger_event_input_body = cls(
            event_type=event_type,
            user_id=user_id,
            schema=schema,
            event_description=event_description,
            instance_id=instance_id,
            language=language,
            messages=messages,
            metadata=metadata,
        )

        return trigger_event_input_body

