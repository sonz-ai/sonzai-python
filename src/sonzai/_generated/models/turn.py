from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Turn")



@_attrs_define
class Turn:
    """ 
        Attributes:
            user_message (str):
     """

    user_message: str





    def to_dict(self) -> dict[str, Any]:
        user_message = self.user_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "user_message": user_message,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_message = d.pop("user_message")

        turn = cls(
            user_message=user_message,
        )

        return turn

