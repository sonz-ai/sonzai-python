from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.insert_fact_entry import InsertFactEntry
  from ..models.insert_rel_entry import InsertRelEntry





T = TypeVar("T", bound="KbInsertFactsInputBody")



@_attrs_define
class KbInsertFactsInputBody:
    """ 
        Attributes:
            facts (list[InsertFactEntry] | None): Entities to insert or update
            schema (str | Unset): A URL to the JSON Schema for this object.
            relationships (list[InsertRelEntry] | None | Unset): Edges to create between entities
            source (str | Unset): Source identifier (defaults to 'api')
     """

    facts: list[InsertFactEntry] | None
    schema: str | Unset = UNSET
    relationships: list[InsertRelEntry] | None | Unset = UNSET
    source: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.insert_fact_entry import InsertFactEntry
        from ..models.insert_rel_entry import InsertRelEntry
        facts: list[dict[str, Any]] | None
        if isinstance(self.facts, list):
            facts = []
            for facts_type_0_item_data in self.facts:
                facts_type_0_item = facts_type_0_item_data.to_dict()
                facts.append(facts_type_0_item)


        else:
            facts = self.facts

        schema = self.schema

        relationships: list[dict[str, Any]] | None | Unset
        if isinstance(self.relationships, Unset):
            relationships = UNSET
        elif isinstance(self.relationships, list):
            relationships = []
            for relationships_type_0_item_data in self.relationships:
                relationships_type_0_item = relationships_type_0_item_data.to_dict()
                relationships.append(relationships_type_0_item)


        else:
            relationships = self.relationships

        source = self.source


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts": facts,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.insert_fact_entry import InsertFactEntry
        from ..models.insert_rel_entry import InsertRelEntry
        d = dict(src_dict)
        def _parse_facts(data: object) -> list[InsertFactEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                facts_type_0 = []
                _facts_type_0 = data
                for facts_type_0_item_data in (_facts_type_0):
                    facts_type_0_item = InsertFactEntry.from_dict(facts_type_0_item_data)



                    facts_type_0.append(facts_type_0_item)

                return facts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[InsertFactEntry] | None, data)

        facts = _parse_facts(d.pop("facts"))


        schema = d.pop("$schema", UNSET)

        def _parse_relationships(data: object) -> list[InsertRelEntry] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                relationships_type_0 = []
                _relationships_type_0 = data
                for relationships_type_0_item_data in (_relationships_type_0):
                    relationships_type_0_item = InsertRelEntry.from_dict(relationships_type_0_item_data)



                    relationships_type_0.append(relationships_type_0_item)

                return relationships_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[InsertRelEntry] | None | Unset, data)

        relationships = _parse_relationships(d.pop("relationships", UNSET))


        source = d.pop("source", UNSET)

        kb_insert_facts_input_body = cls(
            facts=facts,
            schema=schema,
            relationships=relationships,
            source=source,
        )

        return kb_insert_facts_input_body

