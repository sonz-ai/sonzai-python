from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="EndSessionOutputBody")



@_attrs_define
class EndSessionOutputBody:
    """ 
        Attributes:
            async_ (bool): Whether processing continues asynchronously
            success (bool): Whether the session end was accepted
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    async_: bool
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        async_ = self.async_

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "async": async_,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        async_ = d.pop("async")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        end_session_output_body = cls(
            async_=async_,
            success=success,
            schema=schema,
        )

        return end_session_output_body

