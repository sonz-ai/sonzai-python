from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AgentModelsModelEntry")



@_attrs_define
class AgentModelsModelEntry:
    """ 
        Attributes:
            default_model (str): Default model for this provider
            provider (str): Provider identifier
            provider_name (str): Human-readable provider name
     """

    default_model: str
    provider: str
    provider_name: str





    def to_dict(self) -> dict[str, Any]:
        default_model = self.default_model

        provider = self.provider

        provider_name = self.provider_name


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default_model": default_model,
            "provider": provider,
            "provider_name": provider_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default_model = d.pop("default_model")

        provider = d.pop("provider")

        provider_name = d.pop("provider_name")

        agent_models_model_entry = cls(
            default_model=default_model,
            provider=provider,
            provider_name=provider_name,
        )

        return agent_models_model_entry

