from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SearchResult")



@_attrs_define
class SearchResult:
    """ 
        Attributes:
            content (str):
            fact_id (str):
            fact_type (str):
            score (float):
     """

    content: str
    fact_id: str
    fact_type: str
    score: float





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        fact_id = self.fact_id

        fact_type = self.fact_type

        score = self.score


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "fact_id": fact_id,
            "fact_type": fact_type,
            "score": score,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        fact_id = d.pop("fact_id")

        fact_type = d.pop("fact_type")

        score = d.pop("score")

        search_result = cls(
            content=content,
            fact_id=fact_id,
            fact_type=fact_type,
            score=score,
        )

        return search_result

