from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpsertWebhookForTenantInputBody")



@_attrs_define
class UpsertWebhookForTenantInputBody:
    """ 
        Attributes:
            webhook_url (str): Destination URL for webhook delivery
            schema (str | Unset): A URL to the JSON Schema for this object.
            auth_header (str | Unset): Optional Authorization header value sent with each delivery
     """

    webhook_url: str
    schema: str | Unset = UNSET
    auth_header: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        webhook_url = self.webhook_url

        schema = self.schema

        auth_header = self.auth_header


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "webhook_url": webhook_url,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if auth_header is not UNSET:
            field_dict["auth_header"] = auth_header

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        webhook_url = d.pop("webhook_url")

        schema = d.pop("$schema", UNSET)

        auth_header = d.pop("auth_header", UNSET)

        upsert_webhook_for_tenant_input_body = cls(
            webhook_url=webhook_url,
            schema=schema,
            auth_header=auth_header,
        )

        return upsert_webhook_for_tenant_input_body

