from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.direct_update_request_properties import DirectUpdateRequestProperties





T = TypeVar("T", bound="DirectUpdateRequest")



@_attrs_define
class DirectUpdateRequest:
    """ 
        Attributes:
            properties (DirectUpdateRequestProperties):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    properties: DirectUpdateRequestProperties
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.direct_update_request_properties import DirectUpdateRequestProperties
        properties = self.properties.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "properties": properties,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.direct_update_request_properties import DirectUpdateRequestProperties
        d = dict(src_dict)
        properties = DirectUpdateRequestProperties.from_dict(d.pop("properties"))




        schema = d.pop("$schema", UNSET)

        direct_update_request = cls(
            properties=properties,
            schema=schema,
        )

        return direct_update_request

