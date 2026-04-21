from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.agent_models_model_entry import AgentModelsModelEntry





T = TypeVar("T", bound="GetAgentModelsOutputBody")



@_attrs_define
class GetAgentModelsOutputBody:
    """ 
        Attributes:
            default_model (str): Default LLM model
            default_provider (str): Default LLM provider
            providers (list[AgentModelsModelEntry] | None): Available provider/model combinations
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    default_model: str
    default_provider: str
    providers: list[AgentModelsModelEntry] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_models_model_entry import AgentModelsModelEntry
        default_model = self.default_model

        default_provider = self.default_provider

        providers: list[dict[str, Any]] | None
        if isinstance(self.providers, list):
            providers = []
            for providers_type_0_item_data in self.providers:
                providers_type_0_item = providers_type_0_item_data.to_dict()
                providers.append(providers_type_0_item)


        else:
            providers = self.providers

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default_model": default_model,
            "default_provider": default_provider,
            "providers": providers,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_models_model_entry import AgentModelsModelEntry
        d = dict(src_dict)
        default_model = d.pop("default_model")

        default_provider = d.pop("default_provider")

        def _parse_providers(data: object) -> list[AgentModelsModelEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                providers_type_0 = []
                _providers_type_0 = data
                for providers_type_0_item_data in (_providers_type_0):
                    providers_type_0_item = AgentModelsModelEntry.from_dict(providers_type_0_item_data)



                    providers_type_0.append(providers_type_0_item)

                return providers_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AgentModelsModelEntry] | None, data)

        providers = _parse_providers(d.pop("providers"))


        schema = d.pop("$schema", UNSET)

        get_agent_models_output_body = cls(
            default_model=default_model,
            default_provider=default_provider,
            providers=providers,
            schema=schema,
        )

        return get_agent_models_output_body

