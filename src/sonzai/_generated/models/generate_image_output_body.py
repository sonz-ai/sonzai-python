from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="GenerateImageOutputBody")



@_attrs_define
class GenerateImageOutputBody:
    """ 
        Attributes:
            gcs_uri (str): GCS URI of the image
            generation_time_ms (int): Time spent generating in milliseconds
            image_id (str): Generated image ID
            mime_type (str): MIME type of the image
            public_url (str): Public URL of the image
            success (bool): Whether image was generated
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    gcs_uri: str
    generation_time_ms: int
    image_id: str
    mime_type: str
    public_url: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        gcs_uri = self.gcs_uri

        generation_time_ms = self.generation_time_ms

        image_id = self.image_id

        mime_type = self.mime_type

        public_url = self.public_url

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "gcs_uri": gcs_uri,
            "generation_time_ms": generation_time_ms,
            "image_id": image_id,
            "mime_type": mime_type,
            "public_url": public_url,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gcs_uri = d.pop("gcs_uri")

        generation_time_ms = d.pop("generation_time_ms")

        image_id = d.pop("image_id")

        mime_type = d.pop("mime_type")

        public_url = d.pop("public_url")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        generate_image_output_body = cls(
            gcs_uri=gcs_uri,
            generation_time_ms=generation_time_ms,
            image_id=image_id,
            mime_type=mime_type,
            public_url=public_url,
            success=success,
            schema=schema,
        )

        return generate_image_output_body

