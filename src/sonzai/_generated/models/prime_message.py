from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="PrimeMessage")



@_attrs_define
class PrimeMessage:
    """ 
        Attributes:
            content (str):
            role (str): 'user' or 'assistant'
            occurred_at (datetime.datetime | Unset): Original message timestamp. Advisory — DialogueMessage has no timestamp
                field today, so this is preserved in the import job payload for future extensions.
     """

    content: str
    role: str
    occurred_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        role = self.role

        occurred_at: str | Unset = UNSET
        if not isinstance(self.occurred_at, Unset):
            occurred_at = self.occurred_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "role": role,
        })
        if occurred_at is not UNSET:
            field_dict["occurred_at"] = occurred_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        role = d.pop("role")

        _occurred_at = d.pop("occurred_at", UNSET)
        occurred_at: datetime.datetime | Unset
        if isinstance(_occurred_at,  Unset):
            occurred_at = UNSET
        else:
            occurred_at = isoparse(_occurred_at)




        prime_message = cls(
            content=content,
            role=role,
            occurred_at=occurred_at,
        )

        return prime_message

