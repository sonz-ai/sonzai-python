from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RelationshipEntry")



@_attrs_define
class RelationshipEntry:
    """ 
        Attributes:
            love_score (int):
            user_id (str):
            chemistry_score (int | Unset):
            narrative (str | Unset):
            updated_at (str | Unset):
     """

    love_score: int
    user_id: str
    chemistry_score: int | Unset = UNSET
    narrative: str | Unset = UNSET
    updated_at: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        love_score = self.love_score

        user_id = self.user_id

        chemistry_score = self.chemistry_score

        narrative = self.narrative

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "love_score": love_score,
            "user_id": user_id,
        })
        if chemistry_score is not UNSET:
            field_dict["chemistry_score"] = chemistry_score
        if narrative is not UNSET:
            field_dict["narrative"] = narrative
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        love_score = d.pop("love_score")

        user_id = d.pop("user_id")

        chemistry_score = d.pop("chemistry_score", UNSET)

        narrative = d.pop("narrative", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        relationship_entry = cls(
            love_score=love_score,
            user_id=user_id,
            chemistry_score=chemistry_score,
            narrative=narrative,
            updated_at=updated_at,
        )

        return relationship_entry

