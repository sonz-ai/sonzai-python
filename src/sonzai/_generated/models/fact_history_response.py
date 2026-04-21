from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.atomic_fact import AtomicFact





T = TypeVar("T", bound="FactHistoryResponse")



@_attrs_define
class FactHistoryResponse:
    """ 
        Attributes:
            current (AtomicFact):
            previous_versions (list[AtomicFact] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    current: AtomicFact
    previous_versions: list[AtomicFact] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.atomic_fact import AtomicFact
        current = self.current.to_dict()

        previous_versions: list[dict[str, Any]] | None
        if isinstance(self.previous_versions, list):
            previous_versions = []
            for previous_versions_type_0_item_data in self.previous_versions:
                previous_versions_type_0_item = previous_versions_type_0_item_data.to_dict()
                previous_versions.append(previous_versions_type_0_item)


        else:
            previous_versions = self.previous_versions

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "current": current,
            "previous_versions": previous_versions,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.atomic_fact import AtomicFact
        d = dict(src_dict)
        current = AtomicFact.from_dict(d.pop("current"))




        def _parse_previous_versions(data: object) -> list[AtomicFact] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                previous_versions_type_0 = []
                _previous_versions_type_0 = data
                for previous_versions_type_0_item_data in (_previous_versions_type_0):
                    previous_versions_type_0_item = AtomicFact.from_dict(previous_versions_type_0_item_data)



                    previous_versions_type_0.append(previous_versions_type_0_item)

                return previous_versions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[AtomicFact] | None, data)

        previous_versions = _parse_previous_versions(d.pop("previous_versions"))


        schema = d.pop("$schema", UNSET)

        fact_history_response = cls(
            current=current,
            previous_versions=previous_versions,
            schema=schema,
        )

        return fact_history_response

