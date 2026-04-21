from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.webhook import Webhook





T = TypeVar("T", bound="ListWebhooksOutputBody")



@_attrs_define
class ListWebhooksOutputBody:
    """ 
        Attributes:
            webhooks (list[Webhook] | None): List of registered webhooks
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    webhooks: list[Webhook] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.webhook import Webhook
        webhooks: list[dict[str, Any]] | None
        if isinstance(self.webhooks, list):
            webhooks = []
            for webhooks_type_0_item_data in self.webhooks:
                webhooks_type_0_item = webhooks_type_0_item_data.to_dict()
                webhooks.append(webhooks_type_0_item)


        else:
            webhooks = self.webhooks

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "webhooks": webhooks,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook import Webhook
        d = dict(src_dict)
        def _parse_webhooks(data: object) -> list[Webhook] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                webhooks_type_0 = []
                _webhooks_type_0 = data
                for webhooks_type_0_item_data in (_webhooks_type_0):
                    webhooks_type_0_item = Webhook.from_dict(webhooks_type_0_item_data)



                    webhooks_type_0.append(webhooks_type_0_item)

                return webhooks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Webhook] | None, data)

        webhooks = _parse_webhooks(d.pop("webhooks"))


        schema = d.pop("$schema", UNSET)

        list_webhooks_output_body = cls(
            webhooks=webhooks,
            schema=schema,
        )

        return list_webhooks_output_body

