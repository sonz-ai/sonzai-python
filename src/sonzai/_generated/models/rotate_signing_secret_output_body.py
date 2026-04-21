from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="RotateSigningSecretOutputBody")



@_attrs_define
class RotateSigningSecretOutputBody:
    """ 
        Attributes:
            signing_secret (str): The new HMAC signing secret
            success (bool): Whether the secret was rotated
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    signing_secret: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        signing_secret = self.signing_secret

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "signing_secret": signing_secret,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        signing_secret = d.pop("signing_secret")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        rotate_signing_secret_output_body = cls(
            signing_secret=signing_secret,
            success=success,
            schema=schema,
        )

        return rotate_signing_secret_output_body

