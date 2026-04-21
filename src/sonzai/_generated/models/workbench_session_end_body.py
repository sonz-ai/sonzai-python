from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="WorkbenchSessionEndBody")



@_attrs_define
class WorkbenchSessionEndBody:
    """ 
        Attributes:
            ok (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    ok: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ok": ok,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ok = d.pop("ok")

        schema = d.pop("$schema", UNSET)

        workbench_session_end_body = cls(
            ok=ok,
            schema=schema,
        )

        return workbench_session_end_body

