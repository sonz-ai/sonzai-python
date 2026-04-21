from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GenerateCharacterInputBody")



@_attrs_define
class GenerateCharacterInputBody:
    """ 
        Attributes:
            description (str): Free-text personality description
            gender (str): Agent gender
            name (str): Agent display name
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_id (str | Unset): Pre-existing agent UUID (optional)
            fields (list[str] | None | Unset): Optional list of fields to generate
            model (str | Unset): Optional model override for the chosen provider.
            provider (str | Unset): LLM provider for generation (gemini | openrouter | xai). Defaults to gemini.
            regenerate (bool | Unset): Force regeneration even if agent exists
     """

    description: str
    gender: str
    name: str
    schema: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    fields: list[str] | None | Unset = UNSET
    model: str | Unset = UNSET
    provider: str | Unset = UNSET
    regenerate: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        gender = self.gender

        name = self.name

        schema = self.schema

        agent_id = self.agent_id

        fields: list[str] | None | Unset
        if isinstance(self.fields, Unset):
            fields = UNSET
        elif isinstance(self.fields, list):
            fields = self.fields


        else:
            fields = self.fields

        model = self.model

        provider = self.provider

        regenerate = self.regenerate


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "description": description,
            "gender": gender,
            "name": name,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if regenerate is not UNSET:
            field_dict["regenerate"] = regenerate

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        gender = d.pop("gender")

        name = d.pop("name")

        schema = d.pop("$schema", UNSET)

        agent_id = d.pop("agent_id", UNSET)

        def _parse_fields(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_0 = cast(list[str], data)

                return fields_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        fields = _parse_fields(d.pop("fields", UNSET))


        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        regenerate = d.pop("regenerate", UNSET)

        generate_character_input_body = cls(
            description=description,
            gender=gender,
            name=name,
            schema=schema,
            agent_id=agent_id,
            fields=fields,
            model=model,
            provider=provider,
            regenerate=regenerate,
        )

        return generate_character_input_body

