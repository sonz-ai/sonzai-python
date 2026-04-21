from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.significant_moment import SignificantMoment





T = TypeVar("T", bound="SignificantMomentsResponse")



@_attrs_define
class SignificantMomentsResponse:
    """ 
        Attributes:
            moments (list[SignificantMoment] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    moments: list[SignificantMoment] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.significant_moment import SignificantMoment
        moments: list[dict[str, Any]] | None
        if isinstance(self.moments, list):
            moments = []
            for moments_type_0_item_data in self.moments:
                moments_type_0_item = moments_type_0_item_data.to_dict()
                moments.append(moments_type_0_item)


        else:
            moments = self.moments

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "moments": moments,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.significant_moment import SignificantMoment
        d = dict(src_dict)
        def _parse_moments(data: object) -> list[SignificantMoment] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                moments_type_0 = []
                _moments_type_0 = data
                for moments_type_0_item_data in (_moments_type_0):
                    moments_type_0_item = SignificantMoment.from_dict(moments_type_0_item_data)



                    moments_type_0.append(moments_type_0_item)

                return moments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SignificantMoment] | None, data)

        moments = _parse_moments(d.pop("moments"))


        schema = d.pop("$schema", UNSET)

        significant_moments_response = cls(
            moments=moments,
            schema=schema,
        )

        return significant_moments_response

