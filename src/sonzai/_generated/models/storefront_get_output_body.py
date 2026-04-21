from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.storefront import Storefront





T = TypeVar("T", bound="StorefrontGetOutputBody")



@_attrs_define
class StorefrontGetOutputBody:
    """ 
        Attributes:
            slug (str):
            storefront (Storefront):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    slug: str
    storefront: Storefront
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.storefront import Storefront
        slug = self.slug

        storefront = self.storefront.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "slug": slug,
            "storefront": storefront,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storefront import Storefront
        d = dict(src_dict)
        slug = d.pop("slug")

        storefront = Storefront.from_dict(d.pop("storefront"))




        schema = d.pop("$schema", UNSET)

        storefront_get_output_body = cls(
            slug=slug,
            storefront=storefront,
            schema=schema,
        )

        return storefront_get_output_body

