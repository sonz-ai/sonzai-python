from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="StorefrontUpsertAgentInputBody")



@_attrs_define
class StorefrontUpsertAgentInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            avatar_url (str | Unset): Avatar image URL
            description (str | Unset): Public description
            display_name (str | Unset): Public display name
            featured (bool | Unset): Pin to the storefront homepage
            max_turns_per_visit (int | Unset): Per-visitor turn limit
            slug (str | Unset): URL slug for the agent within the storefront
     """

    schema: str | Unset = UNSET
    avatar_url: str | Unset = UNSET
    description: str | Unset = UNSET
    display_name: str | Unset = UNSET
    featured: bool | Unset = UNSET
    max_turns_per_visit: int | Unset = UNSET
    slug: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        avatar_url = self.avatar_url

        description = self.description

        display_name = self.display_name

        featured = self.featured

        max_turns_per_visit = self.max_turns_per_visit

        slug = self.slug


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if featured is not UNSET:
            field_dict["featured"] = featured
        if max_turns_per_visit is not UNSET:
            field_dict["max_turns_per_visit"] = max_turns_per_visit
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        avatar_url = d.pop("avatar_url", UNSET)

        description = d.pop("description", UNSET)

        display_name = d.pop("display_name", UNSET)

        featured = d.pop("featured", UNSET)

        max_turns_per_visit = d.pop("max_turns_per_visit", UNSET)

        slug = d.pop("slug", UNSET)

        storefront_upsert_agent_input_body = cls(
            schema=schema,
            avatar_url=avatar_url,
            description=description,
            display_name=display_name,
            featured=featured,
            max_turns_per_visit=max_turns_per_visit,
            slug=slug,
        )

        return storefront_upsert_agent_input_body

