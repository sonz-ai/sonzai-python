from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="GenerateAndCreateInputBody")



@_attrs_define
class GenerateAndCreateInputBody:
    """ 
        Attributes:
            description (str): Free-text personality description
            gender (str): Agent gender
            name (str): Agent display name
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_id (str | Unset): Pre-existing agent UUID (optional)
            fields (list[str] | None | Unset): Optional list of fields to generate
            language (str | Unset): Language for generation
            model (str | Unset): Optional model override for the chosen provider.
            project_id (str | Unset): Project UUID to assign agent to
            provider (str | Unset): LLM provider for generation (gemini | openrouter | xai). Defaults to gemini.
     """

    description: str
    gender: str
    name: str
    schema: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    fields: list[str] | None | Unset = UNSET
    language: str | Unset = UNSET
    model: str | Unset = UNSET
    project_id: str | Unset = UNSET
    provider: str | Unset = UNSET





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

        language = self.language

        model = self.model

        project_id = self.project_id

        provider = self.provider


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
        if language is not UNSET:
            field_dict["language"] = language
        if model is not UNSET:
            field_dict["model"] = model
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if provider is not UNSET:
            field_dict["provider"] = provider

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


        language = d.pop("language", UNSET)

        model = d.pop("model", UNSET)

        project_id = d.pop("project_id", UNSET)

        provider = d.pop("provider", UNSET)

        generate_and_create_input_body = cls(
            description=description,
            gender=gender,
            name=name,
            schema=schema,
            agent_id=agent_id,
            fields=fields,
            language=language,
            model=model,
            project_id=project_id,
            provider=provider,
        )

        return generate_and_create_input_body

