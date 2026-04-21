from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.import_job import ImportJob





T = TypeVar("T", bound="ListImportJobsOutputBody")



@_attrs_define
class ListImportJobsOutputBody:
    """ 
        Attributes:
            count (int): Number of jobs returned
            jobs (list[ImportJob] | None): List of import jobs
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    count: int
    jobs: list[ImportJob] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.import_job import ImportJob
        count = self.count

        jobs: list[dict[str, Any]] | None
        if isinstance(self.jobs, list):
            jobs = []
            for jobs_type_0_item_data in self.jobs:
                jobs_type_0_item = jobs_type_0_item_data.to_dict()
                jobs.append(jobs_type_0_item)


        else:
            jobs = self.jobs

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "count": count,
            "jobs": jobs,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_job import ImportJob
        d = dict(src_dict)
        count = d.pop("count")

        def _parse_jobs(data: object) -> list[ImportJob] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                jobs_type_0 = []
                _jobs_type_0 = data
                for jobs_type_0_item_data in (_jobs_type_0):
                    jobs_type_0_item = ImportJob.from_dict(jobs_type_0_item_data)



                    jobs_type_0.append(jobs_type_0_item)

                return jobs_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ImportJob] | None, data)

        jobs = _parse_jobs(d.pop("jobs"))


        schema = d.pop("$schema", UNSET)

        list_import_jobs_output_body = cls(
            count=count,
            jobs=jobs,
            schema=schema,
        )

        return list_import_jobs_output_body

