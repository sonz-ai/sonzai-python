from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SeedIdentityMemoryTemplate")



@_attrs_define
class SeedIdentityMemoryTemplate:
    """ 
        Attributes:
            fact_type (str):
            importance (float):
            template (str):
            entities (list[str] | None | Unset):
     """

    fact_type: str
    importance: float
    template: str
    entities: list[str] | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        fact_type = self.fact_type

        importance = self.importance

        template = self.template

        entities: list[str] | None | Unset
        if isinstance(self.entities, Unset):
            entities = UNSET
        elif isinstance(self.entities, list):
            entities = self.entities


        else:
            entities = self.entities


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "factType": fact_type,
            "importance": importance,
            "template": template,
        })
        if entities is not UNSET:
            field_dict["entities"] = entities

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fact_type = d.pop("factType")

        importance = d.pop("importance")

        template = d.pop("template")

        def _parse_entities(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entities_type_0 = cast(list[str], data)

                return entities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        entities = _parse_entities(d.pop("entities", UNSET))


        seed_identity_memory_template = cls(
            fact_type=fact_type,
            importance=importance,
            template=template,
            entities=entities,
        )

        return seed_identity_memory_template

