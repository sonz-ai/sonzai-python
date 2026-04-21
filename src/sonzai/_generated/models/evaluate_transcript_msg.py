from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="EvaluateTranscriptMsg")



@_attrs_define
class EvaluateTranscriptMsg:
    """ 
        Attributes:
            content (str): Message content
            role (str): Message role (user, assistant, system)
            session_index (int | Unset): Session index when the transcript spans multiple sessions
     """

    content: str
    role: str
    session_index: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role = self.role

        session_index = self.session_index


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "role": role,
        })
        if session_index is not UNSET:
            field_dict["session_index"] = session_index

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        role = d.pop("role")

        session_index = d.pop("session_index", UNSET)

        evaluate_transcript_msg = cls(
            content=content,
            role=role,
            session_index=session_index,
        )

        return evaluate_transcript_msg

