from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_candidate import KbCandidate
  from ..models.kb_resolution_info import KbResolutionInfo





T = TypeVar("T", bound="InventoryWriteResponse")



@_attrs_define
class InventoryWriteResponse:
    """ 
        Attributes:
            status (str):
            schema (str | Unset): A URL to the JSON Schema for this object.
            candidates (list[KbCandidate] | None | Unset):
            error (str | Unset):
            fact_id (str | Unset):
            kb_resolution (KbResolutionInfo | Unset):
     """

    status: str
    schema: str | Unset = UNSET
    candidates: list[KbCandidate] | None | Unset = UNSET
    error: str | Unset = UNSET
    fact_id: str | Unset = UNSET
    kb_resolution: KbResolutionInfo | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_candidate import KbCandidate
        from ..models.kb_resolution_info import KbResolutionInfo
        status = self.status

        schema = self.schema

        candidates: list[dict[str, Any]] | None | Unset
        if isinstance(self.candidates, Unset):
            candidates = UNSET
        elif isinstance(self.candidates, list):
            candidates = []
            for candidates_type_0_item_data in self.candidates:
                candidates_type_0_item = candidates_type_0_item_data.to_dict()
                candidates.append(candidates_type_0_item)


        else:
            candidates = self.candidates

        error = self.error

        fact_id = self.fact_id

        kb_resolution: dict[str, Any] | Unset = UNSET
        if not isinstance(self.kb_resolution, Unset):
            kb_resolution = self.kb_resolution.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if candidates is not UNSET:
            field_dict["candidates"] = candidates
        if error is not UNSET:
            field_dict["error"] = error
        if fact_id is not UNSET:
            field_dict["fact_id"] = fact_id
        if kb_resolution is not UNSET:
            field_dict["kb_resolution"] = kb_resolution

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_candidate import KbCandidate
        from ..models.kb_resolution_info import KbResolutionInfo
        d = dict(src_dict)
        status = d.pop("status")

        schema = d.pop("$schema", UNSET)

        def _parse_candidates(data: object) -> list[KbCandidate] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                candidates_type_0 = []
                _candidates_type_0 = data
                for candidates_type_0_item_data in (_candidates_type_0):
                    candidates_type_0_item = KbCandidate.from_dict(candidates_type_0_item_data)



                    candidates_type_0.append(candidates_type_0_item)

                return candidates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KbCandidate] | None | Unset, data)

        candidates = _parse_candidates(d.pop("candidates", UNSET))


        error = d.pop("error", UNSET)

        fact_id = d.pop("fact_id", UNSET)

        _kb_resolution = d.pop("kb_resolution", UNSET)
        kb_resolution: KbResolutionInfo | Unset
        if isinstance(_kb_resolution,  Unset):
            kb_resolution = UNSET
        else:
            kb_resolution = KbResolutionInfo.from_dict(_kb_resolution)




        inventory_write_response = cls(
            status=status,
            schema=schema,
            candidates=candidates,
            error=error,
            fact_id=fact_id,
            kb_resolution=kb_resolution,
        )

        return inventory_write_response

