from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_document import KBDocument





T = TypeVar("T", bound="KbListDocumentsOutputBody")



@_attrs_define
class KbListDocumentsOutputBody:
    """ 
        Attributes:
            documents (list[KBDocument] | None): List of documents
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    documents: list[KBDocument] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_document import KBDocument
        documents: list[dict[str, Any]] | None
        if isinstance(self.documents, list):
            documents = []
            for documents_type_0_item_data in self.documents:
                documents_type_0_item = documents_type_0_item_data.to_dict()
                documents.append(documents_type_0_item)


        else:
            documents = self.documents

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "documents": documents,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_document import KBDocument
        d = dict(src_dict)
        def _parse_documents(data: object) -> list[KBDocument] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                documents_type_0 = []
                _documents_type_0 = data
                for documents_type_0_item_data in (_documents_type_0):
                    documents_type_0_item = KBDocument.from_dict(documents_type_0_item_data)



                    documents_type_0.append(documents_type_0_item)

                return documents_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBDocument] | None, data)

        documents = _parse_documents(d.pop("documents"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_list_documents_output_body = cls(
            documents=documents,
            total=total,
            schema=schema,
        )

        return kb_list_documents_output_body

