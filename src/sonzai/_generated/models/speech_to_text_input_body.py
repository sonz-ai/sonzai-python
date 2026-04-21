from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="SpeechToTextInputBody")



@_attrs_define
class SpeechToTextInputBody:
    """ 
        Attributes:
            audio (str): Base64-encoded audio data
            audio_format (str): Audio format (e.g. wav, mp3)
            schema (str | Unset): A URL to the JSON Schema for this object.
            language (str | Unset): Language code for transcription
     """

    audio: str
    audio_format: str
    schema: str | Unset = UNSET
    language: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        audio = self.audio

        audio_format = self.audio_format

        schema = self.schema

        language = self.language


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "audio": audio,
            "audioFormat": audio_format,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        audio = d.pop("audio")

        audio_format = d.pop("audioFormat")

        schema = d.pop("$schema", UNSET)

        language = d.pop("language", UNSET)

        speech_to_text_input_body = cls(
            audio=audio,
            audio_format=audio_format,
            schema=schema,
            language=language,
        )

        return speech_to_text_input_body

