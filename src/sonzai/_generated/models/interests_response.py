from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.interest import Interest





T = TypeVar("T", bound="InterestsResponse")



@_attrs_define
class InterestsResponse:
    """ 
        Attributes:
            interests (list[Interest] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    interests: list[Interest] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.interest import Interest
        interests: list[dict[str, Any]] | None
        if isinstance(self.interests, list):
            interests = []
            for interests_type_0_item_data in self.interests:
                interests_type_0_item = interests_type_0_item_data.to_dict()
                interests.append(interests_type_0_item)


        else:
            interests = self.interests

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "interests": interests,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interest import Interest
        d = dict(src_dict)
        def _parse_interests(data: object) -> list[Interest] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                interests_type_0 = []
                _interests_type_0 = data
                for interests_type_0_item_data in (_interests_type_0):
                    interests_type_0_item = Interest.from_dict(interests_type_0_item_data)



                    interests_type_0.append(interests_type_0_item)

                return interests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Interest] | None, data)

        interests = _parse_interests(d.pop("interests"))


        schema = d.pop("$schema", UNSET)

        interests_response = cls(
            interests=interests,
            schema=schema,
        )

        return interests_response

