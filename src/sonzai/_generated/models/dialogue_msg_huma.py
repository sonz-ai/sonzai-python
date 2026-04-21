from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DialogueMsgHuma")



@_attrs_define
class DialogueMsgHuma:
    """ 
        Attributes:
            content (str): Message content
            role (str): Message role (user, assistant, system)
            time (str | Unset): Message timestamp (RFC3339)
     """

    content: str
    role: str
    time: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role = self.role

        time = self.time


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "role": role,
        })
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        role = d.pop("role")

        time = d.pop("time", UNSET)

        dialogue_msg_huma = cls(
            content=content,
            role=role,
            time=time,
        )

        return dialogue_msg_huma

