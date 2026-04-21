from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="TextToSpeechInputBody")



@_attrs_define
class TextToSpeechInputBody:
    """ 
        Attributes:
            text (str): Text to convert to speech
            schema (str | Unset): A URL to the JSON Schema for this object.
            language (str | Unset): Language code (e.g. en-US)
            output_format (str | Unset): Audio output format
            voice_name (str | Unset): Voice name to use
     """

    text: str
    schema: str | Unset = UNSET
    language: str | Unset = UNSET
    output_format: str | Unset = UNSET
    voice_name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        text = self.text

        schema = self.schema

        language = self.language

        output_format = self.output_format

        voice_name = self.voice_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "text": text,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if language is not UNSET:
            field_dict["language"] = language
        if output_format is not UNSET:
            field_dict["outputFormat"] = output_format
        if voice_name is not UNSET:
            field_dict["voiceName"] = voice_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        schema = d.pop("$schema", UNSET)

        language = d.pop("language", UNSET)

        output_format = d.pop("outputFormat", UNSET)

        voice_name = d.pop("voiceName", UNSET)

        text_to_speech_input_body = cls(
            text=text,
            schema=schema,
            language=language,
            output_format=output_format,
            voice_name=voice_name,
        )

        return text_to_speech_input_body

