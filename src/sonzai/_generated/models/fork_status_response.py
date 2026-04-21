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






T = TypeVar("T", bound="ForkStatusResponse")



@_attrs_define
class ForkStatusResponse:
    """ 
        Attributes:
            source_agent_id (str):
            status (str):
            tables_copied (int):
            tables_total (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            completed_at (datetime.datetime | Unset):
            error_message (str | Unset):
            started_at (datetime.datetime | Unset):
     """

    source_agent_id: str
    status: str
    tables_copied: int
    tables_total: int
    schema: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    error_message: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        source_agent_id = self.source_agent_id

        status = self.status

        tables_copied = self.tables_copied

        tables_total = self.tables_total

        schema = self.schema

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error_message = self.error_message

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "source_agent_id": source_agent_id,
            "status": status,
            "tables_copied": tables_copied,
            "tables_total": tables_total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_agent_id = d.pop("source_agent_id")

        status = d.pop("status")

        tables_copied = d.pop("tables_copied")

        tables_total = d.pop("tables_total")

        schema = d.pop("$schema", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)




        error_message = d.pop("error_message", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)




        fork_status_response = cls(
            source_agent_id=source_agent_id,
            status=status,
            tables_copied=tables_copied,
            tables_total=tables_total,
            schema=schema,
            completed_at=completed_at,
            error_message=error_message,
            started_at=started_at,
        )

        return fork_status_response

