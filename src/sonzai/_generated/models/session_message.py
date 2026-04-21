from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SessionMessage")



@_attrs_define
class SessionMessage:
    """ 
        Attributes:
            content (str): Message content
            role (str): Message role (user or assistant)
     """

    content: str
    role: str





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role = self.role


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "role": role,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        role = d.pop("role")

        session_message = cls(
            content=content,
            role=role,
        )

        return session_message

