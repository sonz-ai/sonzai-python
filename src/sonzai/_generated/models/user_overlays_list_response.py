from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.user_overlay_response import UserOverlayResponse





T = TypeVar("T", bound="UserOverlaysListResponse")



@_attrs_define
class UserOverlaysListResponse:
    """ 
        Attributes:
            overlays (list[UserOverlayResponse] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    overlays: list[UserOverlayResponse] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_overlay_response import UserOverlayResponse
        overlays: list[dict[str, Any]] | None
        if isinstance(self.overlays, list):
            overlays = []
            for overlays_type_0_item_data in self.overlays:
                overlays_type_0_item = overlays_type_0_item_data.to_dict()
                overlays.append(overlays_type_0_item)


        else:
            overlays = self.overlays

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "overlays": overlays,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_overlay_response import UserOverlayResponse
        d = dict(src_dict)
        def _parse_overlays(data: object) -> list[UserOverlayResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                overlays_type_0 = []
                _overlays_type_0 = data
                for overlays_type_0_item_data in (_overlays_type_0):
                    overlays_type_0_item = UserOverlayResponse.from_dict(overlays_type_0_item_data)



                    overlays_type_0.append(overlays_type_0_item)

                return overlays_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UserOverlayResponse] | None, data)

        overlays = _parse_overlays(d.pop("overlays"))


        schema = d.pop("$schema", UNSET)

        user_overlays_list_response = cls(
            overlays=overlays,
            schema=schema,
        )

        return user_overlays_list_response

