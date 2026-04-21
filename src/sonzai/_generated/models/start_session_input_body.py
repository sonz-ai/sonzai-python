from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="StartSessionInputBody")



@_attrs_define
class StartSessionInputBody:
    """ 
        Attributes:
            session_id (str): Unique session identifier
            user_id (str): ID of the user starting the session
            schema (str | Unset): A URL to the JSON Schema for this object.
            instance_id (str | Unset): Optional agent instance identifier
            tool_definitions (Any | Unset): OpenAI-compatible tool definitions for this session
            user_display_name (str | Unset): Optional display name for the user
     """

    session_id: str
    user_id: str
    schema: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    tool_definitions: Any | Unset = UNSET
    user_display_name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        user_id = self.user_id

        schema = self.schema

        instance_id = self.instance_id

        tool_definitions = self.tool_definitions

        user_display_name = self.user_display_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "session_id": session_id,
            "user_id": user_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if tool_definitions is not UNSET:
            field_dict["tool_definitions"] = tool_definitions
        if user_display_name is not UNSET:
            field_dict["user_display_name"] = user_display_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id")

        user_id = d.pop("user_id")

        schema = d.pop("$schema", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        tool_definitions = d.pop("tool_definitions", UNSET)

        user_display_name = d.pop("user_display_name", UNSET)

        start_session_input_body = cls(
            session_id=session_id,
            user_id=user_id,
            schema=schema,
            instance_id=instance_id,
            tool_definitions=tool_definitions,
            user_display_name=user_display_name,
        )

        return start_session_input_body

