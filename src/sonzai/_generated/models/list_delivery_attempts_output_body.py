from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.webhook_delivery_attempt import WebhookDeliveryAttempt





T = TypeVar("T", bound="ListDeliveryAttemptsOutputBody")



@_attrs_define
class ListDeliveryAttemptsOutputBody:
    """ 
        Attributes:
            attempts (list[WebhookDeliveryAttempt] | None): List of delivery attempts
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    attempts: list[WebhookDeliveryAttempt] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.webhook_delivery_attempt import WebhookDeliveryAttempt
        attempts: list[dict[str, Any]] | None
        if isinstance(self.attempts, list):
            attempts = []
            for attempts_type_0_item_data in self.attempts:
                attempts_type_0_item = attempts_type_0_item_data.to_dict()
                attempts.append(attempts_type_0_item)


        else:
            attempts = self.attempts

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "attempts": attempts,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook_delivery_attempt import WebhookDeliveryAttempt
        d = dict(src_dict)
        def _parse_attempts(data: object) -> list[WebhookDeliveryAttempt] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                attempts_type_0 = []
                _attempts_type_0 = data
                for attempts_type_0_item_data in (_attempts_type_0):
                    attempts_type_0_item = WebhookDeliveryAttempt.from_dict(attempts_type_0_item_data)



                    attempts_type_0.append(attempts_type_0_item)

                return attempts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WebhookDeliveryAttempt] | None, data)

        attempts = _parse_attempts(d.pop("attempts"))


        schema = d.pop("$schema", UNSET)

        list_delivery_attempts_output_body = cls(
            attempts=attempts,
            schema=schema,
        )

        return list_delivery_attempts_output_body

