from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ResetMemoryResponse")



@_attrs_define
class ResetMemoryResponse:
    """ 
        Attributes:
            facts_deleted (int):
            nodes_deleted (int):
            status (str):
            success (bool):
            schema (str | Unset): A URL to the JSON Schema for this object.
            facts_failed (int | Unset):
            failed_fact_ids (list[str] | None | Unset):
            failed_node_ids (list[str] | None | Unset):
            nodes_failed (int | Unset):
     """

    facts_deleted: int
    nodes_deleted: int
    status: str
    success: bool
    schema: str | Unset = UNSET
    facts_failed: int | Unset = UNSET
    failed_fact_ids: list[str] | None | Unset = UNSET
    failed_node_ids: list[str] | None | Unset = UNSET
    nodes_failed: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        facts_deleted = self.facts_deleted

        nodes_deleted = self.nodes_deleted

        status = self.status

        success = self.success

        schema = self.schema

        facts_failed = self.facts_failed

        failed_fact_ids: list[str] | None | Unset
        if isinstance(self.failed_fact_ids, Unset):
            failed_fact_ids = UNSET
        elif isinstance(self.failed_fact_ids, list):
            failed_fact_ids = self.failed_fact_ids


        else:
            failed_fact_ids = self.failed_fact_ids

        failed_node_ids: list[str] | None | Unset
        if isinstance(self.failed_node_ids, Unset):
            failed_node_ids = UNSET
        elif isinstance(self.failed_node_ids, list):
            failed_node_ids = self.failed_node_ids


        else:
            failed_node_ids = self.failed_node_ids

        nodes_failed = self.nodes_failed


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "facts_deleted": facts_deleted,
            "nodes_deleted": nodes_deleted,
            "status": status,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if facts_failed is not UNSET:
            field_dict["facts_failed"] = facts_failed
        if failed_fact_ids is not UNSET:
            field_dict["failed_fact_ids"] = failed_fact_ids
        if failed_node_ids is not UNSET:
            field_dict["failed_node_ids"] = failed_node_ids
        if nodes_failed is not UNSET:
            field_dict["nodes_failed"] = nodes_failed

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        facts_deleted = d.pop("facts_deleted")

        nodes_deleted = d.pop("nodes_deleted")

        status = d.pop("status")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        facts_failed = d.pop("facts_failed", UNSET)

        def _parse_failed_fact_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                failed_fact_ids_type_0 = cast(list[str], data)

                return failed_fact_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        failed_fact_ids = _parse_failed_fact_ids(d.pop("failed_fact_ids", UNSET))


        def _parse_failed_node_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                failed_node_ids_type_0 = cast(list[str], data)

                return failed_node_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        failed_node_ids = _parse_failed_node_ids(d.pop("failed_node_ids", UNSET))


        nodes_failed = d.pop("nodes_failed", UNSET)

        reset_memory_response = cls(
            facts_deleted=facts_deleted,
            nodes_deleted=nodes_deleted,
            status=status,
            success=success,
            schema=schema,
            facts_failed=facts_failed,
            failed_fact_ids=failed_fact_ids,
            failed_node_ids=failed_node_ids,
            nodes_failed=nodes_failed,
        )

        return reset_memory_response

