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






T = TypeVar("T", bound="JobUser")



@_attrs_define
class JobUser:
    """ 
        Attributes:
            facts_deduped (int):
            facts_stored (int):
            job_id (str):
            status (str):
            updated_at (datetime.datetime):
            user_id (str):
            warmth_score (int):
            completed_at (datetime.datetime | Unset):
            error_message (str | Unset):
            started_at (datetime.datetime | Unset):
     """

    facts_deduped: int
    facts_stored: int
    job_id: str
    status: str
    updated_at: datetime.datetime
    user_id: str
    warmth_score: int
    completed_at: datetime.datetime | Unset = UNSET
    error_message: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        facts_deduped = self.facts_deduped

        facts_stored = self.facts_stored

        job_id = self.job_id

        status = self.status

        updated_at = self.updated_at.isoformat()

        user_id = self.user_id

        warmth_score = self.warmth_score

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        error_message = self.error_message

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_deduped": facts_deduped,
            "facts_stored": facts_stored,
            "job_id": job_id,
            "status": status,
            "updated_at": updated_at,
            "user_id": user_id,
            "warmth_score": warmth_score,
        })
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
        facts_deduped = d.pop("facts_deduped")

        facts_stored = d.pop("facts_stored")

        job_id = d.pop("job_id")

        status = d.pop("status")

        updated_at = isoparse(d.pop("updated_at"))




        user_id = d.pop("user_id")

        warmth_score = d.pop("warmth_score")

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




        job_user = cls(
            facts_deduped=facts_deduped,
            facts_stored=facts_stored,
            job_id=job_id,
            status=status,
            updated_at=updated_at,
            user_id=user_id,
            warmth_score=warmth_score,
            completed_at=completed_at,
            error_message=error_message,
            started_at=started_at,
        )

        return job_user

