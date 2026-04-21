from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchGenerateBioBody")



@_attrs_define
class WorkbenchGenerateBioBody:
    """ 
        Attributes:
            bio (str):
            tone (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            confidence (float | Unset):
     """

    bio: str
    tone: str
    schema: str | Unset = UNSET
    confidence: float | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        bio = self.bio

        tone = self.tone

        schema = self.schema

        confidence = self.confidence


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "bio": bio,
            "tone": tone,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bio = d.pop("bio")

        tone = d.pop("tone")

        schema = d.pop("$schema", UNSET)

        confidence = d.pop("confidence", UNSET)

        workbench_generate_bio_body = cls(
            bio=bio,
            tone=tone,
            schema=schema,
            confidence=confidence,
        )

        return workbench_generate_bio_body

