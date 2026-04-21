from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="UpsertCustomStateByKeyInputBody")



@_attrs_define
class UpsertCustomStateByKeyInputBody:
    """ 
        Attributes:
            key (str): State key
            value (Any): State value
            schema (str | Unset): A URL to the JSON Schema for this object.
            content_type (str | Unset): Content type (text or json, defaults to text)
            instance_id (str | Unset): Optional instance ID
            scope (str | Unset): Scope (global or user, defaults to global)
            user_id (str | Unset): User ID (required when scope=user)
     """

    key: str
    value: Any
    schema: str | Unset = UNSET
    content_type: str | Unset = UNSET
    instance_id: str | Unset = UNSET
    scope: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        schema = self.schema

        content_type = self.content_type

        instance_id = self.instance_id

        scope = self.scope

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "key": key,
            "value": value,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if content_type is not UNSET:
            field_dict["content_type"] = content_type
        if instance_id is not UNSET:
            field_dict["instance_id"] = instance_id
        if scope is not UNSET:
            field_dict["scope"] = scope
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        value = d.pop("value")

        schema = d.pop("$schema", UNSET)

        content_type = d.pop("content_type", UNSET)

        instance_id = d.pop("instance_id", UNSET)

        scope = d.pop("scope", UNSET)

        user_id = d.pop("user_id", UNSET)

        upsert_custom_state_by_key_input_body = cls(
            key=key,
            value=value,
            schema=schema,
            content_type=content_type,
            instance_id=instance_id,
            scope=scope,
            user_id=user_id,
        )

        return upsert_custom_state_by_key_input_body

