from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.prime_content_block import PrimeContentBlock
  from ..models.prime_user_metadata import PrimeUserMetadata
  from ..models.structured_import_spec import StructuredImportSpec





T = TypeVar("T", bound="PrimeUserRequest")



@_attrs_define
class PrimeUserRequest:
    """ 
        Attributes:
            display_name (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            content (list[PrimeContentBlock] | None | Unset):
            metadata (PrimeUserMetadata | Unset):
            source (str | Unset):
            structured_import (StructuredImportSpec | Unset):
     """

    display_name: str
    schema: str | Unset = UNSET
    content: list[PrimeContentBlock] | None | Unset = UNSET
    metadata: PrimeUserMetadata | Unset = UNSET
    source: str | Unset = UNSET
    structured_import: StructuredImportSpec | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.prime_content_block import PrimeContentBlock
        from ..models.prime_user_metadata import PrimeUserMetadata
        from ..models.structured_import_spec import StructuredImportSpec
        display_name = self.display_name

        schema = self.schema

        content: list[dict[str, Any]] | None | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        elif isinstance(self.content, list):
            content = []
            for content_type_0_item_data in self.content:
                content_type_0_item = content_type_0_item_data.to_dict()
                content.append(content_type_0_item)


        else:
            content = self.content

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        source = self.source

        structured_import: dict[str, Any] | Unset = UNSET
        if not isinstance(self.structured_import, Unset):
            structured_import = self.structured_import.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "display_name": display_name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if content is not UNSET:
            field_dict["content"] = content
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if source is not UNSET:
            field_dict["source"] = source
        if structured_import is not UNSET:
            field_dict["structured_import"] = structured_import

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prime_content_block import PrimeContentBlock
        from ..models.prime_user_metadata import PrimeUserMetadata
        from ..models.structured_import_spec import StructuredImportSpec
        d = dict(src_dict)
        display_name = d.pop("display_name")

        schema = d.pop("$schema", UNSET)

        def _parse_content(data: object) -> list[PrimeContentBlock] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_0 = []
                _content_type_0 = data
                for content_type_0_item_data in (_content_type_0):
                    content_type_0_item = PrimeContentBlock.from_dict(content_type_0_item_data)



                    content_type_0.append(content_type_0_item)

                return content_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PrimeContentBlock] | None | Unset, data)

        content = _parse_content(d.pop("content", UNSET))


        _metadata = d.pop("metadata", UNSET)
        metadata: PrimeUserMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = PrimeUserMetadata.from_dict(_metadata)




        source = d.pop("source", UNSET)

        _structured_import = d.pop("structured_import", UNSET)
        structured_import: StructuredImportSpec | Unset
        if isinstance(_structured_import,  Unset):
            structured_import = UNSET
        else:
            structured_import = StructuredImportSpec.from_dict(_structured_import)




        prime_user_request = cls(
            display_name=display_name,
            schema=schema,
            content=content,
            metadata=metadata,
            source=source,
            structured_import=structured_import,
        )

        return prime_user_request

