from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="BatchImportUsersHumaOutputBody")



@_attrs_define
class BatchImportUsersHumaOutputBody:
    """ 
        Attributes:
            facts_created (int): Number of facts generated synchronously from metadata
            job_id (str): Import job UUID for tracking
            status (str): Job status (queued)
            total_users (int): Number of users in the batch
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    facts_created: int
    job_id: str
    status: str
    total_users: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        facts_created = self.facts_created

        job_id = self.job_id

        status = self.status

        total_users = self.total_users

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_created": facts_created,
            "job_id": job_id,
            "status": status,
            "total_users": total_users,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        facts_created = d.pop("facts_created")

        job_id = d.pop("job_id")

        status = d.pop("status")

        total_users = d.pop("total_users")

        schema = d.pop("$schema", UNSET)

        batch_import_users_huma_output_body = cls(
            facts_created=facts_created,
            job_id=job_id,
            status=status,
            total_users=total_users,
            schema=schema,
        )

        return batch_import_users_huma_output_body

