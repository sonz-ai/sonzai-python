from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="VoiceLiveWSTokenInputBody")



@_attrs_define
class VoiceLiveWSTokenInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            compiled_system_prompt (str | Unset): Pre-compiled system prompt for the voice session
            language (str | Unset): Language code (default: en-US)
            user_id (str | Unset): User ID (auto-detected from auth if omitted)
            voice_name (str | Unset): Gemini voice name (default: Kore)
     """

    schema: str | Unset = UNSET
    compiled_system_prompt: str | Unset = UNSET
    language: str | Unset = UNSET
    user_id: str | Unset = UNSET
    voice_name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        compiled_system_prompt = self.compiled_system_prompt

        language = self.language

        user_id = self.user_id

        voice_name = self.voice_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if compiled_system_prompt is not UNSET:
            field_dict["compiledSystemPrompt"] = compiled_system_prompt
        if language is not UNSET:
            field_dict["language"] = language
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if voice_name is not UNSET:
            field_dict["voiceName"] = voice_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        compiled_system_prompt = d.pop("compiledSystemPrompt", UNSET)

        language = d.pop("language", UNSET)

        user_id = d.pop("userId", UNSET)

        voice_name = d.pop("voiceName", UNSET)

        voice_live_ws_token_input_body = cls(
            schema=schema,
            compiled_system_prompt=compiled_system_prompt,
            language=language,
            user_id=user_id,
            voice_name=voice_name,
        )

        return voice_live_ws_token_input_body

