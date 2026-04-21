from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DeleteWisdomResponse")



@_attrs_define
class DeleteWisdomResponse:
    """ 
        Attributes:
            fact_id (str):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    fact_id: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        fact_id = self.fact_id

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fact_id": fact_id,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fact_id = d.pop("fact_id")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        delete_wisdom_response = cls(
            fact_id=fact_id,
            success=success,
            schema=schema,
        )

        return delete_wisdom_response

