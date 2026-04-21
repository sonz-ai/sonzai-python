from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbUploadDocumentOutputBody")



@_attrs_define
class KbUploadDocumentOutputBody:
    """ 
        Attributes:
            checksum (str): SHA-256 hex digest
            document_id (str): Newly created document UUID
            file_name (str): Original file name
            file_size (int): File size in bytes
            gcs_path (str): Cloud storage path
            status (str): Processing status
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    checksum: str
    document_id: str
    file_name: str
    file_size: int
    gcs_path: str
    status: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        checksum = self.checksum

        document_id = self.document_id

        file_name = self.file_name

        file_size = self.file_size

        gcs_path = self.gcs_path

        status = self.status

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "checksum": checksum,
            "document_id": document_id,
            "file_name": file_name,
            "file_size": file_size,
            "gcs_path": gcs_path,
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        checksum = d.pop("checksum")

        document_id = d.pop("document_id")

        file_name = d.pop("file_name")

        file_size = d.pop("file_size")

        gcs_path = d.pop("gcs_path")

        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        kb_upload_document_output_body = cls(
            checksum=checksum,
            document_id=document_id,
            file_name=file_name,
            file_size=file_size,
            gcs_path=gcs_path,
            status=status,
            schema=schema,
        )

        return kb_upload_document_output_body

