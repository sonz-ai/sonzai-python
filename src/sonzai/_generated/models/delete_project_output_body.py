from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="DeleteProjectOutputBody")



@_attrs_define
class DeleteProjectOutputBody:
    """ 
        Attributes:
            status (str): Deletion status — "deleted" on success
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        delete_project_output_body = cls(
            status=status,
            schema=schema,
        )

        return delete_project_output_body

