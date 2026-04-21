from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PrimeContentBlock")



@_attrs_define
class PrimeContentBlock:
    """ 
        Attributes:
            body (str):
            type_ (str):
     """

    body: str
    type_: str





    def to_dict(self) -> dict[str, Any]:
        body = self.body

        type_ = self.type_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "body": body,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        type_ = d.pop("type")

        prime_content_block = cls(
            body=body,
            type_=type_,
        )

        return prime_content_block

