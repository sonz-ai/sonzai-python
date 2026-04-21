from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateAPIKeyInputBody")



@_attrs_define
class CreateAPIKeyInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            expires_days (int | Unset): Expiry in days; 0 = never expires
            name (str | Unset): Label for the key (defaults to "Default key")
            scopes (list[str] | None | Unset): Permission scopes; empty = ["*"]
     """

    schema: str | Unset = UNSET
    expires_days: int | Unset = UNSET
    name: str | Unset = UNSET
    scopes: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        schema = self.schema

        expires_days = self.expires_days

        name = self.name

        scopes: list[str] | None | Unset
        if isinstance(self.scopes, Unset):
            scopes = UNSET
        elif isinstance(self.scopes, list):
            scopes = self.scopes


        else:
            scopes = self.scopes


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if expires_days is not UNSET:
            field_dict["expires_days"] = expires_days
        if name is not UNSET:
            field_dict["name"] = name
        if scopes is not UNSET:
            field_dict["scopes"] = scopes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        expires_days = d.pop("expires_days", UNSET)

        name = d.pop("name", UNSET)

        def _parse_scopes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scopes_type_0 = cast(list[str], data)

                return scopes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        scopes = _parse_scopes(d.pop("scopes", UNSET))


        create_api_key_input_body = cls(
            schema=schema,
            expires_days=expires_days,
            name=name,
            scopes=scopes,
        )

        return create_api_key_input_body

