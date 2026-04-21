from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AddCommentRequest")



@_attrs_define
class AddCommentRequest:
    """ 
        Attributes:
            content (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            is_internal (bool | Unset):
     """

    content: str
    schema: str | Unset = UNSET
    is_internal: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        schema = self.schema

        is_internal = self.is_internal


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if is_internal is not UNSET:
            field_dict["is_internal"] = is_internal

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        schema = d.pop("$schema", UNSET)

        is_internal = d.pop("is_internal", UNSET)

        add_comment_request = cls(
            content=content,
            schema=schema,
            is_internal=is_internal,
        )

        return add_comment_request

