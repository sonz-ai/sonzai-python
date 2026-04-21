from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.proactive_notification_entry import ProactiveNotificationEntry





T = TypeVar("T", bound="ProactiveNotificationsResponse")



@_attrs_define
class ProactiveNotificationsResponse:
    """ 
        Attributes:
            notifications (list[ProactiveNotificationEntry] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    notifications: list[ProactiveNotificationEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.proactive_notification_entry import ProactiveNotificationEntry
        notifications: list[dict[str, Any]] | None
        if isinstance(self.notifications, list):
            notifications = []
            for notifications_type_0_item_data in self.notifications:
                notifications_type_0_item = notifications_type_0_item_data.to_dict()
                notifications.append(notifications_type_0_item)


        else:
            notifications = self.notifications

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "notifications": notifications,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.proactive_notification_entry import ProactiveNotificationEntry
        d = dict(src_dict)
        def _parse_notifications(data: object) -> list[ProactiveNotificationEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notifications_type_0 = []
                _notifications_type_0 = data
                for notifications_type_0_item_data in (_notifications_type_0):
                    notifications_type_0_item = ProactiveNotificationEntry.from_dict(notifications_type_0_item_data)



                    notifications_type_0.append(notifications_type_0_item)

                return notifications_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ProactiveNotificationEntry] | None, data)

        notifications = _parse_notifications(d.pop("notifications"))


        schema = d.pop("$schema", UNSET)

        proactive_notifications_response = cls(
            notifications=notifications,
            schema=schema,
        )

        return proactive_notifications_response

