from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="VoiceLiveWSTokenOutputBody")



@_attrs_define
class VoiceLiveWSTokenOutputBody:
    """ 
        Attributes:
            auth_token (str): Short-lived authentication token
            ws_url (str): WebSocket URL for the voice live session
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    auth_token: str
    ws_url: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        auth_token = self.auth_token

        ws_url = self.ws_url

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "authToken": auth_token,
            "wsUrl": ws_url,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auth_token = d.pop("authToken")

        ws_url = d.pop("wsUrl")

        schema = d.pop("$schema", UNSET)

        voice_live_ws_token_output_body = cls(
            auth_token=auth_token,
            ws_url=ws_url,
            schema=schema,
        )

        return voice_live_ws_token_output_body

