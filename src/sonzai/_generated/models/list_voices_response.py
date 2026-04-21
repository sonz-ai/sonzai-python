from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.voice_info import VoiceInfo





T = TypeVar("T", bound="ListVoicesResponse")



@_attrs_define
class ListVoicesResponse:
    """ 
        Attributes:
            voices (list[VoiceInfo] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    voices: list[VoiceInfo] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.voice_info import VoiceInfo
        voices: list[dict[str, Any]] | None
        if isinstance(self.voices, list):
            voices = []
            for voices_type_0_item_data in self.voices:
                voices_type_0_item = voices_type_0_item_data.to_dict()
                voices.append(voices_type_0_item)


        else:
            voices = self.voices

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "voices": voices,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.voice_info import VoiceInfo
        d = dict(src_dict)
        def _parse_voices(data: object) -> list[VoiceInfo] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                voices_type_0 = []
                _voices_type_0 = data
                for voices_type_0_item_data in (_voices_type_0):
                    voices_type_0_item = VoiceInfo.from_dict(voices_type_0_item_data)



                    voices_type_0.append(voices_type_0_item)

                return voices_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[VoiceInfo] | None, data)

        voices = _parse_voices(d.pop("voices"))


        schema = d.pop("$schema", UNSET)

        list_voices_response = cls(
            voices=voices,
            schema=schema,
        )

        return list_voices_response

