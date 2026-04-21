from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="PropertySource")



@_attrs_define
class PropertySource:
    """ 
        Attributes:
            doc_id (str):
            eff_date (datetime.datetime):
     """

    doc_id: str
    eff_date: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        doc_id = self.doc_id

        eff_date = self.eff_date.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "doc_id": doc_id,
            "eff_date": eff_date,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        doc_id = d.pop("doc_id")

        eff_date = isoparse(d.pop("eff_date"))




        property_source = cls(
            doc_id=doc_id,
            eff_date=eff_date,
        )

        return property_source

