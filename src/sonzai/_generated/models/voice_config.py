from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="VoiceConfig")



@_attrs_define
class VoiceConfig:
    """ 
        Attributes:
            language (str | Unset):
            voice_name (str | Unset):
     """

    language: str | Unset = UNSET
    voice_name: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        language = self.language

        voice_name = self.voice_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if language is not UNSET:
            field_dict["language"] = language
        if voice_name is not UNSET:
            field_dict["voice_name"] = voice_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        language = d.pop("language", UNSET)

        voice_name = d.pop("voice_name", UNSET)

        voice_config = cls(
            language=language,
            voice_name=voice_name,
        )

        return voice_config

