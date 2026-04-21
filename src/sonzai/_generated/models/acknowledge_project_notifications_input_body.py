from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="AcknowledgeProjectNotificationsInputBody")



@_attrs_define
class AcknowledgeProjectNotificationsInputBody:
    """ 
        Attributes:
            notification_ids (list[str] | None): IDs of notifications to acknowledge
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    notification_ids: list[str] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        notification_ids: list[str] | None
        if isinstance(self.notification_ids, list):
            notification_ids = self.notification_ids


        else:
            notification_ids = self.notification_ids

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "notification_ids": notification_ids,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_notification_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notification_ids_type_0 = cast(list[str], data)

                return notification_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        notification_ids = _parse_notification_ids(d.pop("notification_ids"))


        schema = d.pop("$schema", UNSET)

        acknowledge_project_notifications_input_body = cls(
            notification_ids=notification_ids,
            schema=schema,
        )

        return acknowledge_project_notifications_input_body

