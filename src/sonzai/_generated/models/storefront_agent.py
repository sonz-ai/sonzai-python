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






T = TypeVar("T", bound="StorefrontAgent")



@_attrs_define
class StorefrontAgent:
    """ 
        Attributes:
            agent_id (str):
            available_models (list[str] | None):
            available_providers (list[str] | None):
            avatar_url (str):
            created_at (datetime.datetime):
            description (str):
            display_name (str):
            is_visible (bool):
            placeholder_text (str):
            slug (str):
            sort_order (int):
            storefront_id (str):
            updated_at (datetime.datetime):
            welcome_message (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            instance_id (str | Unset):
     """

    agent_id: str
    available_models: list[str] | None
    available_providers: list[str] | None
    avatar_url: str
    created_at: datetime.datetime
    description: str
    display_name: str
    is_visible: bool
    placeholder_text: str
    slug: str
    sort_order: int
    storefront_id: str
    updated_at: datetime.datetime
    welcome_message: str
    schema: str | Unset = UNSET
    instance_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        available_models: list[str] | None
        if isinstance(self.available_models, list):
            available_models = self.available_models


        else:
            available_models = self.available_models

        available_providers: list[str] | None
        if isinstance(self.available_providers, list):
            available_providers = self.available_providers


        else:
            available_providers = self.available_providers

        avatar_url = self.avatar_url

        created_at = self.created_at.isoformat()

        description = self.description

        display_name = self.display_name

        is_visible = self.is_visible

        placeholder_text = self.placeholder_text

        slug = self.slug

        sort_order = self.sort_order

        storefront_id = self.storefront_id

        updated_at = self.updated_at.isoformat()

        welcome_message = self.welcome_message

        schema = self.schema

        instance_id = self.instance_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agent_id": agent_id,
            "available_models": available_models,
            "available_providers": available_providers,
            "avatar_url": avatar_url,
            "created_at": created_at,
            "description": description,
            "display_name": display_name,
            "is_visible": is_visible,
            "placeholder_text": placeholder_text,
            "slug": slug,
            "sort_order": sort_order,
            "storefront_id": storefront_id,
            "updated_at": updated_at,
            "welcome_message": welcome_message,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        def _parse_available_models(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                available_models_type_0 = cast(list[str], data)

                return available_models_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        available_models = _parse_available_models(d.pop("available_models"))


        def _parse_available_providers(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                available_providers_type_0 = cast(list[str], data)

                return available_providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        available_providers = _parse_available_providers(d.pop("available_providers"))


        avatar_url = d.pop("avatar_url")

        created_at = isoparse(d.pop("created_at"))




        description = d.pop("description")

        display_name = d.pop("display_name")

        is_visible = d.pop("is_visible")

        placeholder_text = d.pop("placeholder_text")

        slug = d.pop("slug")

        sort_order = d.pop("sort_order")

        storefront_id = d.pop("storefront_id")

        updated_at = isoparse(d.pop("updated_at"))




        welcome_message = d.pop("welcome_message")

        schema = d.pop("$schema", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        storefront_agent = cls(
            agent_id=agent_id,
            available_models=available_models,
            available_providers=available_providers,
            avatar_url=avatar_url,
            created_at=created_at,
            description=description,
            display_name=display_name,
            is_visible=is_visible,
            placeholder_text=placeholder_text,
            slug=slug,
            sort_order=sort_order,
            storefront_id=storefront_id,
            updated_at=updated_at,
            welcome_message=welcome_message,
            schema=schema,
            instance_id=instance_id,
        )

        return storefront_agent

