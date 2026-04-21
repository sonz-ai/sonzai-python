from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DirectUpdateResponse")



@_attrs_define
class DirectUpdateResponse:
    """ 
        Attributes:
            status (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            error (str | Unset):
            fact_id (str | Unset):
     """

    status: str
    schema: str | Unset = UNSET
    error: str | Unset = UNSET
    fact_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        status = self.status

        schema = self.schema

        error = self.error

        fact_id = self.fact_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if error is not UNSET:
            field_dict["error"] = error
        if fact_id is not UNSET:
            field_dict["fact_id"] = fact_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        error = d.pop("error", UNSET)

        fact_id = d.pop("fact_id", UNSET)

        direct_update_response = cls(
            status=status,
            schema=schema,
            error=error,
            fact_id=fact_id,
        )

        return direct_update_response

