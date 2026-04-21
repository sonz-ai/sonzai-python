from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateAgentProfileInputBody")



@_attrs_define
class UpdateAgentProfileInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            bio (str | Unset): Updated bio
            name (str | Unset): Updated display name
            personality_prompt (str | Unset): Updated personality prompt
            speech_patterns (list[str] | Unset): Updated speech patterns
            true_dislikes (list[str] | Unset): Updated dislikes
            true_interests (list[str] | Unset): Updated interests
     """

    schema: str | Unset = UNSET
    bio: str | Unset = UNSET
    name: str | Unset = UNSET
    personality_prompt: str | Unset = UNSET
    speech_patterns: list[str] | Unset = UNSET
    true_dislikes: list[str] | Unset = UNSET
    true_interests: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        bio = self.bio

        name = self.name

        personality_prompt = self.personality_prompt

        speech_patterns: list[str] | Unset = UNSET
        if not isinstance(self.speech_patterns, Unset):
            speech_patterns = self.speech_patterns



        true_dislikes: list[str] | Unset = UNSET
        if not isinstance(self.true_dislikes, Unset):
            true_dislikes = self.true_dislikes



        true_interests: list[str] | Unset = UNSET
        if not isinstance(self.true_interests, Unset):
            true_interests = self.true_interests




        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if bio is not UNSET:
            field_dict["bio"] = bio
        if name is not UNSET:
            field_dict["name"] = name
        if personality_prompt is not UNSET:
            field_dict["personality_prompt"] = personality_prompt
        if speech_patterns is not UNSET:
            field_dict["speech_patterns"] = speech_patterns
        if true_dislikes is not UNSET:
            field_dict["true_dislikes"] = true_dislikes
        if true_interests is not UNSET:
            field_dict["true_interests"] = true_interests

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        bio = d.pop("bio", UNSET)

        name = d.pop("name", UNSET)

        personality_prompt = d.pop("personality_prompt", UNSET)

        speech_patterns = cast(list[str], d.pop("speech_patterns", UNSET))


        true_dislikes = cast(list[str], d.pop("true_dislikes", UNSET))


        true_interests = cast(list[str], d.pop("true_interests", UNSET))


        update_agent_profile_input_body = cls(
            schema=schema,
            bio=bio,
            name=name,
            personality_prompt=personality_prompt,
            speech_patterns=speech_patterns,
            true_dislikes=true_dislikes,
            true_interests=true_interests,
        )

        return update_agent_profile_input_body

