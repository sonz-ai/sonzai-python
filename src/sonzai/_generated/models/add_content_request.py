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





T = TypeVar("T", bound="AddContentRequest")



@_attrs_define
class AddContentRequest:
    """ 
        Attributes:
            content (list[PrimeContentBlock] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
            source (str | Unset):
     """

    content: list[PrimeContentBlock] | None
    schema: str | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.prime_content_block import PrimeContentBlock
        content: list[dict[str, Any]] | None
        if isinstance(self.content, list):
            content = []
            for content_type_0_item_data in self.content:
                content_type_0_item = content_type_0_item_data.to_dict()
                content.append(content_type_0_item)


        else:
            content = self.content

        schema = self.schema

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prime_content_block import PrimeContentBlock
        d = dict(src_dict)
        def _parse_content(data: object) -> list[PrimeContentBlock] | None:
            if data is None:
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
            return cast(list[PrimeContentBlock] | None, data)

        content = _parse_content(d.pop("content"))


        schema = d.pop("$schema", UNSET)

        source = d.pop("source", UNSET)

        add_content_request = cls(
            content=content,
            schema=schema,
            source=source,
        )

        return add_content_request

