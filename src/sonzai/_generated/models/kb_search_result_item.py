from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbSearchResultItem")



@_attrs_define
class KbSearchResultItem:
    """ 
        Attributes:
            content (str):
            label (str):
            score (float):
            type_ (str):
            scope (str | Unset):
            source (str | Unset):
     """

    content: str
    label: str
    score: float
    type_: str
    scope: str | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        label = self.label

        score = self.score

        type_ = self.type_

        scope = self.scope

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "label": label,
            "score": score,
            "type": type_,
        })
        if scope is not UNSET:
            field_dict["scope"] = scope
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        label = d.pop("label")

        score = d.pop("score")

        type_ = d.pop("type")

        scope = d.pop("scope", UNSET)

        source = d.pop("source", UNSET)

        kb_search_result_item = cls(
            content=content,
            label=label,
            score=score,
            type_=type_,
            scope=scope,
            source=source,
        )

        return kb_search_result_item

