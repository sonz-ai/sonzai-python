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






T = TypeVar("T", bound="ImportJob")



@_attrs_define
class ImportJob:
    """ 
        Attributes:
            agent_id (str):
            constellation_nodes (int):
            created_at (datetime.datetime):
            error_details (Any):
            errors (int):
            facts_deduped (int):
            facts_extracted (int):
            facts_stored (int):
            job_id (str):
            job_type (str):
            processed_users (int):
            source_type (str):
            status (str):
            tenant_id (str):
            total_users (int):
            updated_at (datetime.datetime):
            warmth_score (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            completed_at (datetime.datetime | Unset):
            payload (Any | Unset):
            source_id (str | Unset):
            started_at (datetime.datetime | Unset):
            user_id (str | Unset):
     """

    agent_id: str
    constellation_nodes: int
    created_at: datetime.datetime
    error_details: Any
    errors: int
    facts_deduped: int
    facts_extracted: int
    facts_stored: int
    job_id: str
    job_type: str
    processed_users: int
    source_type: str
    status: str
    tenant_id: str
    total_users: int
    updated_at: datetime.datetime
    warmth_score: int
    schema: str | Unset = UNSET
    completed_at: datetime.datetime | Unset = UNSET
    payload: Any | Unset = UNSET
    source_id: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        constellation_nodes = self.constellation_nodes

        created_at = self.created_at.isoformat()

        error_details = self.error_details

        errors = self.errors

        facts_deduped = self.facts_deduped

        facts_extracted = self.facts_extracted

        facts_stored = self.facts_stored

        job_id = self.job_id

        job_type = self.job_type

        processed_users = self.processed_users

        source_type = self.source_type

        status = self.status

        tenant_id = self.tenant_id

        total_users = self.total_users

        updated_at = self.updated_at.isoformat()

        warmth_score = self.warmth_score

        schema = self.schema

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        payload = self.payload

        source_id = self.source_id

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "constellation_nodes": constellation_nodes,
            "created_at": created_at,
            "error_details": error_details,
            "errors": errors,
            "facts_deduped": facts_deduped,
            "facts_extracted": facts_extracted,
            "facts_stored": facts_stored,
            "job_id": job_id,
            "job_type": job_type,
            "processed_users": processed_users,
            "source_type": source_type,
            "status": status,
            "tenant_id": tenant_id,
            "total_users": total_users,
            "updated_at": updated_at,
            "warmth_score": warmth_score,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if payload is not UNSET:
            field_dict["payload"] = payload
        if source_id is not UNSET:
            field_dict["source_id"] = source_id
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        constellation_nodes = d.pop("constellation_nodes")

        created_at = isoparse(d.pop("created_at"))




        error_details = d.pop("error_details")

        errors = d.pop("errors")

        facts_deduped = d.pop("facts_deduped")

        facts_extracted = d.pop("facts_extracted")

        facts_stored = d.pop("facts_stored")

        job_id = d.pop("job_id")

        job_type = d.pop("job_type")

        processed_users = d.pop("processed_users")

        source_type = d.pop("source_type")

        status = d.pop("status")

        tenant_id = d.pop("tenant_id")

        total_users = d.pop("total_users")

        updated_at = isoparse(d.pop("updated_at"))




        warmth_score = d.pop("warmth_score")

        schema = d.pop("$schema", UNSET)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at,  Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)




        payload = d.pop("payload", UNSET)

        source_id = d.pop("source_id", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)




        user_id = d.pop("user_id", UNSET)

        import_job = cls(
            agent_id=agent_id,
            constellation_nodes=constellation_nodes,
            created_at=created_at,
            error_details=error_details,
            errors=errors,
            facts_deduped=facts_deduped,
            facts_extracted=facts_extracted,
            facts_stored=facts_stored,
            job_id=job_id,
            job_type=job_type,
            processed_users=processed_users,
            source_type=source_type,
            status=status,
            tenant_id=tenant_id,
            total_users=total_users,
            updated_at=updated_at,
            warmth_score=warmth_score,
            schema=schema,
            completed_at=completed_at,
            payload=payload,
            source_id=source_id,
            started_at=started_at,
            user_id=user_id,
        )

        return import_job

