from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="BatchInventoryResponse")



@_attrs_define
class BatchInventoryResponse:
    """ 
        Attributes:
            added (int):
            failed (int):
            status (str):
            total (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            error (str | Unset):
     """

    added: int
    failed: int
    status: str
    total: int
    schema: str | Unset = UNSET
    error: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        added = self.added

        failed = self.failed

        status = self.status

        total = self.total

        schema = self.schema

        error = self.error


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "added": added,
            "failed": failed,
            "status": status,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        added = d.pop("added")

        failed = d.pop("failed")

        status = d.pop("status")

        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        error = d.pop("error", UNSET)

        batch_inventory_response = cls(
            added=added,
            failed=failed,
            status=status,
            total=total,
            schema=schema,
            error=error,
        )

        return batch_inventory_response

