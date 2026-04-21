from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="Storefront")



@_attrs_define
class Storefront:
    """ 
        Attributes:
            accent_color (str):
            access_mode (str):
            anon_msg_limit_per_session (int):
            anon_rate_limit_per_min (int):
            anon_session_ttl_minutes (int):
            background_color (str):
            created_at (datetime.datetime):
            custom_css (str):
            display_name (str):
            is_published (bool):
            layout (str):
            logo_url (str):
            primary_color (str):
            show_agent_avatars (bool):
            storefront_id (str):
            tagline (str):
            tenant_id (str):
            updated_at (datetime.datetime):
            welcome_message (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    accent_color: str
    access_mode: str
    anon_msg_limit_per_session: int
    anon_rate_limit_per_min: int
    anon_session_ttl_minutes: int
    background_color: str
    created_at: datetime.datetime
    custom_css: str
    display_name: str
    is_published: bool
    layout: str
    logo_url: str
    primary_color: str
    show_agent_avatars: bool
    storefront_id: str
    tagline: str
    tenant_id: str
    updated_at: datetime.datetime
    welcome_message: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        accent_color = self.accent_color

        access_mode = self.access_mode

        anon_msg_limit_per_session = self.anon_msg_limit_per_session

        anon_rate_limit_per_min = self.anon_rate_limit_per_min

        anon_session_ttl_minutes = self.anon_session_ttl_minutes

        background_color = self.background_color

        created_at = self.created_at.isoformat()

        custom_css = self.custom_css

        display_name = self.display_name

        is_published = self.is_published

        layout = self.layout

        logo_url = self.logo_url

        primary_color = self.primary_color

        show_agent_avatars = self.show_agent_avatars

        storefront_id = self.storefront_id

        tagline = self.tagline

        tenant_id = self.tenant_id

        updated_at = self.updated_at.isoformat()

        welcome_message = self.welcome_message

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "accent_color": accent_color,
            "access_mode": access_mode,
            "anon_msg_limit_per_session": anon_msg_limit_per_session,
            "anon_rate_limit_per_min": anon_rate_limit_per_min,
            "anon_session_ttl_minutes": anon_session_ttl_minutes,
            "background_color": background_color,
            "created_at": created_at,
            "custom_css": custom_css,
            "display_name": display_name,
            "is_published": is_published,
            "layout": layout,
            "logo_url": logo_url,
            "primary_color": primary_color,
            "show_agent_avatars": show_agent_avatars,
            "storefront_id": storefront_id,
            "tagline": tagline,
            "tenant_id": tenant_id,
            "updated_at": updated_at,
            "welcome_message": welcome_message,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        accent_color = d.pop("accent_color")

        access_mode = d.pop("access_mode")

        anon_msg_limit_per_session = d.pop("anon_msg_limit_per_session")

        anon_rate_limit_per_min = d.pop("anon_rate_limit_per_min")

        anon_session_ttl_minutes = d.pop("anon_session_ttl_minutes")

        background_color = d.pop("background_color")

        created_at = isoparse(d.pop("created_at"))




        custom_css = d.pop("custom_css")

        display_name = d.pop("display_name")

        is_published = d.pop("is_published")

        layout = d.pop("layout")

        logo_url = d.pop("logo_url")

        primary_color = d.pop("primary_color")

        show_agent_avatars = d.pop("show_agent_avatars")

        storefront_id = d.pop("storefront_id")

        tagline = d.pop("tagline")

        tenant_id = d.pop("tenant_id")

        updated_at = isoparse(d.pop("updated_at"))




        welcome_message = d.pop("welcome_message")

        schema = d.pop("$schema", UNSET)

        storefront = cls(
            accent_color=accent_color,
            access_mode=access_mode,
            anon_msg_limit_per_session=anon_msg_limit_per_session,
            anon_rate_limit_per_min=anon_rate_limit_per_min,
            anon_session_ttl_minutes=anon_session_ttl_minutes,
            background_color=background_color,
            created_at=created_at,
            custom_css=custom_css,
            display_name=display_name,
            is_published=is_published,
            layout=layout,
            logo_url=logo_url,
            primary_color=primary_color,
            show_agent_avatars=show_agent_avatars,
            storefront_id=storefront_id,
            tagline=tagline,
            tenant_id=tenant_id,
            updated_at=updated_at,
            welcome_message=welcome_message,
            schema=schema,
        )

        return storefront

