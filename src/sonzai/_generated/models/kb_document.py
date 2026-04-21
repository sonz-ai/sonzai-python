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






T = TypeVar("T", bound="KBDocument")



@_attrs_define
class KBDocument:
    """ 
        Attributes:
            checksum (str):
            content_type (str):
            created_at (datetime.datetime):
            document_id (str):
            edge_count (int):
            extraction_tokens (int):
            file_name (str):
            file_size (int):
            gcs_path (str):
            node_count (int):
            project_id (str):
            status (str):
            updated_at (datetime.datetime):
            uploaded_by (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            effective_date (datetime.datetime | Unset):
            error_msg (str | Unset):
     """

    checksum: str
    content_type: str
    created_at: datetime.datetime
    document_id: str
    edge_count: int
    extraction_tokens: int
    file_name: str
    file_size: int
    gcs_path: str
    node_count: int
    project_id: str
    status: str
    updated_at: datetime.datetime
    uploaded_by: str
    schema: str | Unset = UNSET
    effective_date: datetime.datetime | Unset = UNSET
    error_msg: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        checksum = self.checksum

        content_type = self.content_type

        created_at = self.created_at.isoformat()

        document_id = self.document_id

        edge_count = self.edge_count

        extraction_tokens = self.extraction_tokens

        file_name = self.file_name

        file_size = self.file_size

        gcs_path = self.gcs_path

        node_count = self.node_count

        project_id = self.project_id

        status = self.status

        updated_at = self.updated_at.isoformat()

        uploaded_by = self.uploaded_by

        schema = self.schema

        effective_date: str | Unset = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        error_msg = self.error_msg


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "checksum": checksum,
            "content_type": content_type,
            "created_at": created_at,
            "document_id": document_id,
            "edge_count": edge_count,
            "extraction_tokens": extraction_tokens,
            "file_name": file_name,
            "file_size": file_size,
            "gcs_path": gcs_path,
            "node_count": node_count,
            "project_id": project_id,
            "status": status,
            "updated_at": updated_at,
            "uploaded_by": uploaded_by,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if effective_date is not UNSET:
            field_dict["effective_date"] = effective_date
        if error_msg is not UNSET:
            field_dict["error_msg"] = error_msg

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checksum = d.pop("checksum")

        content_type = d.pop("content_type")

        created_at = isoparse(d.pop("created_at"))




        document_id = d.pop("document_id")

        edge_count = d.pop("edge_count")

        extraction_tokens = d.pop("extraction_tokens")

        file_name = d.pop("file_name")

        file_size = d.pop("file_size")

        gcs_path = d.pop("gcs_path")

        node_count = d.pop("node_count")

        project_id = d.pop("project_id")

        status = d.pop("status")

        updated_at = isoparse(d.pop("updated_at"))




        uploaded_by = d.pop("uploaded_by")

        schema = d.pop("$schema", UNSET)

        _effective_date = d.pop("effective_date", UNSET)
        effective_date: datetime.datetime | Unset
        if isinstance(_effective_date,  Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date)




        error_msg = d.pop("error_msg", UNSET)

        kb_document = cls(
            checksum=checksum,
            content_type=content_type,
            created_at=created_at,
            document_id=document_id,
            edge_count=edge_count,
            extraction_tokens=extraction_tokens,
            file_name=file_name,
            file_size=file_size,
            gcs_path=gcs_path,
            node_count=node_count,
            project_id=project_id,
            status=status,
            updated_at=updated_at,
            uploaded_by=uploaded_by,
            schema=schema,
            effective_date=effective_date,
            error_msg=error_msg,
        )

        return kb_document

