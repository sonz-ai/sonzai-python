from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ChatSSEDelta")



@_attrs_define
class ChatSSEDelta:
    """ 
        Attributes:
            content (str | Unset): Incremental content token
     """

    content: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        chat_sse_delta = cls(
            content=content,
        )

        return chat_sse_delta

