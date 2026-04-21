from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.user_priming_metadata import UserPrimingMetadata





T = TypeVar("T", bound="UpdateUserMetadataHumaOutputBody")



@_attrs_define
class UpdateUserMetadataHumaOutputBody:
    """ 
        Attributes:
            facts_created (int): Number of new facts generated from metadata
            metadata (UserPrimingMetadata):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    facts_created: int
    metadata: UserPrimingMetadata
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_priming_metadata import UserPrimingMetadata
        facts_created = self.facts_created

        metadata = self.metadata.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_created": facts_created,
            "metadata": metadata,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_priming_metadata import UserPrimingMetadata
        d = dict(src_dict)
        facts_created = d.pop("facts_created")

        metadata = UserPrimingMetadata.from_dict(d.pop("metadata"))




        schema = d.pop("$schema", UNSET)

        update_user_metadata_huma_output_body = cls(
            facts_created=facts_created,
            metadata=metadata,
            schema=schema,
        )

        return update_user_metadata_huma_output_body

