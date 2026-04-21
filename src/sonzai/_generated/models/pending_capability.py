from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="PendingCapability")



@_attrs_define
class PendingCapability:
    """ 
        Attributes:
            capability (str):
            context (str | Unset):
     """

    capability: str
    context: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        capability = self.capability

        context = self.context


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "capability": capability,
        })
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        capability = d.pop("capability")

        context = d.pop("context", UNSET)

        pending_capability = cls(
            capability=capability,
            context=context,
        )

        return pending_capability

