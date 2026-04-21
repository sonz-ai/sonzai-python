from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="KbPromoteNodeInputBody")



@_attrs_define
class KbPromoteNodeInputBody:
    """ 
        Attributes:
            tenant_id (str): Target tenant; server rejects if it does not match the authenticated tenant.
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    tenant_id: str
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "tenant_id": tenant_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant_id = d.pop("tenant_id")

        schema = d.pop("$schema", UNSET)

        kb_promote_node_input_body = cls(
            tenant_id=tenant_id,
            schema=schema,
        )

        return kb_promote_node_input_body

