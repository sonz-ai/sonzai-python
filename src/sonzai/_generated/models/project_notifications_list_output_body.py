from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.notification import Notification





T = TypeVar("T", bound="ProjectNotificationsListOutputBody")



@_attrs_define
class ProjectNotificationsListOutputBody:
    """ 
        Attributes:
            count (int): Number of notifications returned
            notifications (list[Notification] | None): List of pending notifications
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    count: int
    notifications: list[Notification] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.notification import Notification
        count = self.count

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
            "count": count,
            "notifications": notifications,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification import Notification
        d = dict(src_dict)
        count = d.pop("count")

        def _parse_notifications(data: object) -> list[Notification] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                notifications_type_0 = []
                _notifications_type_0 = data
                for notifications_type_0_item_data in (_notifications_type_0):
                    notifications_type_0_item = Notification.from_dict(notifications_type_0_item_data)



                    notifications_type_0.append(notifications_type_0_item)

                return notifications_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Notification] | None, data)

        notifications = _parse_notifications(d.pop("notifications"))


        schema = d.pop("$schema", UNSET)

        project_notifications_list_output_body = cls(
            count=count,
            notifications=notifications,
            schema=schema,
        )

        return project_notifications_list_output_body

