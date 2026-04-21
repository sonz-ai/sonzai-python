from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.workbench_advance_time_response import WorkbenchAdvanceTimeResponse





T = TypeVar("T", bound="WorkbenchAdvanceTimeJobBody")



@_attrs_define
class WorkbenchAdvanceTimeJobBody:
    """ 
        Attributes:
            job_id (str):
            status (str): running | succeeded | failed
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_id (str | Unset):
            error (str | Unset):
            result (WorkbenchAdvanceTimeResponse | Unset):
            started_at (str | Unset):
            updated_at (str | Unset):
            user_id (str | Unset):
     """

    job_id: str
    status: str
    schema: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    error: str | Unset = UNSET
    result: WorkbenchAdvanceTimeResponse | Unset = UNSET
    started_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.workbench_advance_time_response import WorkbenchAdvanceTimeResponse
        job_id = self.job_id

        status = self.status

        schema = self.schema

        agent_id = self.agent_id

        error = self.error

        result: dict[str, Any] | Unset = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        started_at = self.started_at

        updated_at = self.updated_at

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "job_id": job_id,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if error is not UNSET:
            field_dict["error"] = error
        if result is not UNSET:
            field_dict["result"] = result
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workbench_advance_time_response import WorkbenchAdvanceTimeResponse
        d = dict(src_dict)
        job_id = d.pop("job_id")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        agent_id = d.pop("agent_id", UNSET)

        error = d.pop("error", UNSET)

        _result = d.pop("result", UNSET)
        result: WorkbenchAdvanceTimeResponse | Unset
        if isinstance(_result,  Unset):
            result = UNSET
        else:
            result = WorkbenchAdvanceTimeResponse.from_dict(_result)




        started_at = d.pop("started_at", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        user_id = d.pop("user_id", UNSET)

        workbench_advance_time_job_body = cls(
            job_id=job_id,
            status=status,
            schema=schema,
            agent_id=agent_id,
            error=error,
            result=result,
            started_at=started_at,
            updated_at=updated_at,
            user_id=user_id,
        )

        return workbench_advance_time_job_body

