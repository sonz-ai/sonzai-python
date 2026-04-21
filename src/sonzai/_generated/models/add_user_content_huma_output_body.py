from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AddUserContentHumaOutputBody")



@_attrs_define
class AddUserContentHumaOutputBody:
    """ 
        Attributes:
            job_id (str): Import job UUID for tracking
            status (str): Job status (queued)
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    job_id: str
    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "job_id": job_id,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        add_user_content_huma_output_body = cls(
            job_id=job_id,
            status=status,
            schema=schema,
        )

        return add_user_content_huma_output_body

