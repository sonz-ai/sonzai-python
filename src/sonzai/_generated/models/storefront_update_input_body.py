from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="StorefrontUpdateInputBody")



@_attrs_define
class StorefrontUpdateInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            access_type (str | Unset): open | code | invite
            contact_email (str | Unset): Contact email shown publicly
            description (str | Unset): Public-facing description
            display_name (str | Unset): Public-facing display name
            hero_image_url (str | Unset): Hero banner image URL
            invite_code (str | Unset): Access code (if access_type=code)
            max_visits_per_user (int | Unset): Per-visitor rate cap
            slug (str | Unset): Storefront URL slug (e.g. "/s/{slug}")
            theme (str | Unset): Theme identifier
     """

    schema: str | Unset = UNSET
    access_type: str | Unset = UNSET
    contact_email: str | Unset = UNSET
    description: str | Unset = UNSET
    display_name: str | Unset = UNSET
    hero_image_url: str | Unset = UNSET
    invite_code: str | Unset = UNSET
    max_visits_per_user: int | Unset = UNSET
    slug: str | Unset = UNSET
    theme: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        access_type = self.access_type

        contact_email = self.contact_email

        description = self.description

        display_name = self.display_name

        hero_image_url = self.hero_image_url

        invite_code = self.invite_code

        max_visits_per_user = self.max_visits_per_user

        slug = self.slug

        theme = self.theme


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if access_type is not UNSET:
            field_dict["access_type"] = access_type
        if contact_email is not UNSET:
            field_dict["contact_email"] = contact_email
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if hero_image_url is not UNSET:
            field_dict["hero_image_url"] = hero_image_url
        if invite_code is not UNSET:
            field_dict["invite_code"] = invite_code
        if max_visits_per_user is not UNSET:
            field_dict["max_visits_per_user"] = max_visits_per_user
        if slug is not UNSET:
            field_dict["slug"] = slug
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        access_type = d.pop("access_type", UNSET)

        contact_email = d.pop("contact_email", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("display_name", UNSET)

        hero_image_url = d.pop("hero_image_url", UNSET)

        invite_code = d.pop("invite_code", UNSET)

        max_visits_per_user = d.pop("max_visits_per_user", UNSET)

        slug = d.pop("slug", UNSET)

        theme = d.pop("theme", UNSET)

        storefront_update_input_body = cls(
            schema=schema,
            access_type=access_type,
            contact_email=contact_email,
            description=description,
            display_name=display_name,
            hero_image_url=hero_image_url,
            invite_code=invite_code,
            max_visits_per_user=max_visits_per_user,
            slug=slug,
            theme=theme,
        )

        return storefront_update_input_body

