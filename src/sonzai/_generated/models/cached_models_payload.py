from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CachedModelsPayload")



@_attrs_define
class CachedModelsPayload:
    """ 
        Attributes:
            default_model (str):
            providers (list[Any] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    default_model: str
    providers: list[Any] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        default_model = self.default_model

        providers: list[Any] | None
        if isinstance(self.providers, list):
            providers = self.providers


        else:
            providers = self.providers

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default_model": default_model,
            "providers": providers,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default_model = d.pop("default_model")

        def _parse_providers(data: object) -> list[Any] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                providers_type_0 = cast(list[Any], data)

                return providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Any] | None, data)

        providers = _parse_providers(d.pop("providers"))


        schema = d.pop("$schema", UNSET)

        cached_models_payload = cls(
            default_model=default_model,
            providers=providers,
            schema=schema,
        )

        return cached_models_payload

