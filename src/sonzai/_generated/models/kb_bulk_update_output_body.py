from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbBulkUpdateOutputBody")



@_attrs_define
class KbBulkUpdateOutputBody:
    """ 
        Attributes:
            created (int): Nodes created
            not_found (int): Entries that could not be matched
            processed (int): Total entries processed
            updated (int): Nodes updated
            schema (str | Unset): A URL to the JSON Schema for this object.
            count (int | Unset): Total queued (async only)
            status (str | Unset): 'queued' for async processing
     """

    created: int
    not_found: int
    processed: int
    updated: int
    schema: str | Unset = UNSET
    count: int | Unset = UNSET
    status: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created = self.created

        not_found = self.not_found

        processed = self.processed

        updated = self.updated

        schema = self.schema

        count = self.count

        status = self.status


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created": created,
            "not_found": not_found,
            "processed": processed,
            "updated": updated,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if count is not UNSET:
            field_dict["count"] = count
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = d.pop("created")

        not_found = d.pop("not_found")

        processed = d.pop("processed")

        updated = d.pop("updated")

        schema = d.pop("$schema", UNSET)

        count = d.pop("count", UNSET)

        status = d.pop("status", UNSET)

        kb_bulk_update_output_body = cls(
            created=created,
            not_found=not_found,
            processed=processed,
            updated=updated,
            schema=schema,
            count=count,
            status=status,
        )

        return kb_bulk_update_output_body

