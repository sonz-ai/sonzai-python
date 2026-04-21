from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.chat_sse_delta import ChatSSEDelta





T = TypeVar("T", bound="ChatSSEChoice")



@_attrs_define
class ChatSSEChoice:
    """ 
        Attributes:
            delta (ChatSSEDelta):
            index (int): Choice index, always 0 today
            finish_reason (str | Unset): Non-empty on the terminal chunk (e.g. "stop")
     """

    delta: ChatSSEDelta
    index: int
    finish_reason: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.chat_sse_delta import ChatSSEDelta
        delta = self.delta.to_dict()

        index = self.index

        finish_reason = self.finish_reason


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "delta": delta,
            "index": index,
        })
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_sse_delta import ChatSSEDelta
        d = dict(src_dict)
        delta = ChatSSEDelta.from_dict(d.pop("delta"))




        index = d.pop("index")

        finish_reason = d.pop("finish_reason", UNSET)

        chat_sse_choice = cls(
            delta=delta,
            index=index,
            finish_reason=finish_reason,
        )

        return chat_sse_choice

