from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="WisdomAuditResponse")



@_attrs_define
class WisdomAuditResponse:
    """ 
        Attributes:
            content (str):
            fact_id (str):
            promotion_confidence (float):
            source_user_count (int):
            schema (str | Unset): A URL to the JSON Schema for this object.
            derived_from_hashes (list[str] | None | Unset):
            promoted_at (str | Unset):
            target_path (str | Unset):
     """

    content: str
    fact_id: str
    promotion_confidence: float
    source_user_count: int
    schema: str | Unset = UNSET
    derived_from_hashes: list[str] | None | Unset = UNSET
    promoted_at: str | Unset = UNSET
    target_path: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        fact_id = self.fact_id

        promotion_confidence = self.promotion_confidence

        source_user_count = self.source_user_count

        schema = self.schema

        derived_from_hashes: list[str] | None | Unset
        if isinstance(self.derived_from_hashes, Unset):
            derived_from_hashes = UNSET
        elif isinstance(self.derived_from_hashes, list):
            derived_from_hashes = self.derived_from_hashes


        else:
            derived_from_hashes = self.derived_from_hashes

        promoted_at = self.promoted_at

        target_path = self.target_path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "content": content,
            "fact_id": fact_id,
            "promotion_confidence": promotion_confidence,
            "source_user_count": source_user_count,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if derived_from_hashes is not UNSET:
            field_dict["derived_from_hashes"] = derived_from_hashes
        if promoted_at is not UNSET:
            field_dict["promoted_at"] = promoted_at
        if target_path is not UNSET:
            field_dict["target_path"] = target_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        fact_id = d.pop("fact_id")

        promotion_confidence = d.pop("promotion_confidence")

        source_user_count = d.pop("source_user_count")

        schema = d.pop("$schema", UNSET)

        def _parse_derived_from_hashes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                derived_from_hashes_type_0 = cast(list[str], data)

                return derived_from_hashes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        derived_from_hashes = _parse_derived_from_hashes(d.pop("derived_from_hashes", UNSET))


        promoted_at = d.pop("promoted_at", UNSET)

        target_path = d.pop("target_path", UNSET)

        wisdom_audit_response = cls(
            content=content,
            fact_id=fact_id,
            promotion_confidence=promotion_confidence,
            source_user_count=source_user_count,
            schema=schema,
            derived_from_hashes=derived_from_hashes,
            promoted_at=promoted_at,
            target_path=target_path,
        )

        return wisdom_audit_response

