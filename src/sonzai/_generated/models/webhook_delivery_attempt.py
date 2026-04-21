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






T = TypeVar("T", bound="WebhookDeliveryAttempt")



@_attrs_define
class WebhookDeliveryAttempt:
    """ 
        Attributes:
            attempt_id (str):
            attempt_number (int):
            created_at (datetime.datetime):
            duration_ms (int):
            event_type (str):
            project_id (str):
            response_code (int):
            status (str):
            webhook_url (str):
            error_message (str | Unset):
            request_body (str | Unset):
            response_body (str | Unset):
     """

    attempt_id: str
    attempt_number: int
    created_at: datetime.datetime
    duration_ms: int
    event_type: str
    project_id: str
    response_code: int
    status: str
    webhook_url: str
    error_message: str | Unset = UNSET
    request_body: str | Unset = UNSET
    response_body: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        attempt_id = self.attempt_id

        attempt_number = self.attempt_number

        created_at = self.created_at.isoformat()

        duration_ms = self.duration_ms

        event_type = self.event_type

        project_id = self.project_id

        response_code = self.response_code

        status = self.status

        webhook_url = self.webhook_url

        error_message = self.error_message

        request_body = self.request_body

        response_body = self.response_body


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "attempt_id": attempt_id,
            "attempt_number": attempt_number,
            "created_at": created_at,
            "duration_ms": duration_ms,
            "event_type": event_type,
            "project_id": project_id,
            "response_code": response_code,
            "status": status,
            "webhook_url": webhook_url,
        })
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if request_body is not UNSET:
            field_dict["request_body"] = request_body
        if response_body is not UNSET:
            field_dict["response_body"] = response_body

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt_id = d.pop("attempt_id")

        attempt_number = d.pop("attempt_number")

        created_at = isoparse(d.pop("created_at"))




        duration_ms = d.pop("duration_ms")

        event_type = d.pop("event_type")

        project_id = d.pop("project_id")

        response_code = d.pop("response_code")

        status = d.pop("status")

        webhook_url = d.pop("webhook_url")

        error_message = d.pop("error_message", UNSET)

        request_body = d.pop("request_body", UNSET)

        response_body = d.pop("response_body", UNSET)

        webhook_delivery_attempt = cls(
            attempt_id=attempt_id,
            attempt_number=attempt_number,
            created_at=created_at,
            duration_ms=duration_ms,
            event_type=event_type,
            project_id=project_id,
            response_code=response_code,
            status=status,
            webhook_url=webhook_url,
            error_message=error_message,
            request_body=request_body,
            response_body=response_body,
        )

        return webhook_delivery_attempt

