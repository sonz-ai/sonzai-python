from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.personality_delta import PersonalityDelta
  from ..models.personality_profile import PersonalityProfile
  from ..models.user_overlay_response import UserOverlayResponse





T = TypeVar("T", bound="UserOverlayDetailResponse")



@_attrs_define
class UserOverlayDetailResponse:
    """ 
        Attributes:
            base (PersonalityProfile):
            evolution (list[PersonalityDelta] | None):
            overlay (UserOverlayResponse):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    base: PersonalityProfile
    evolution: list[PersonalityDelta] | None
    overlay: UserOverlayResponse
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.personality_delta import PersonalityDelta
        from ..models.personality_profile import PersonalityProfile
        from ..models.user_overlay_response import UserOverlayResponse
        base = self.base.to_dict()

        evolution: list[dict[str, Any]] | None
        if isinstance(self.evolution, list):
            evolution = []
            for evolution_type_0_item_data in self.evolution:
                evolution_type_0_item = evolution_type_0_item_data.to_dict()
                evolution.append(evolution_type_0_item)


        else:
            evolution = self.evolution

        overlay = self.overlay.to_dict()

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "base": base,
            "evolution": evolution,
            "overlay": overlay,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.personality_delta import PersonalityDelta
        from ..models.personality_profile import PersonalityProfile
        from ..models.user_overlay_response import UserOverlayResponse
        d = dict(src_dict)
        base = PersonalityProfile.from_dict(d.pop("base"))




        def _parse_evolution(data: object) -> list[PersonalityDelta] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                evolution_type_0 = []
                _evolution_type_0 = data
                for evolution_type_0_item_data in (_evolution_type_0):
                    evolution_type_0_item = PersonalityDelta.from_dict(evolution_type_0_item_data)



                    evolution_type_0.append(evolution_type_0_item)

                return evolution_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[PersonalityDelta] | None, data)

        evolution = _parse_evolution(d.pop("evolution"))


        overlay = UserOverlayResponse.from_dict(d.pop("overlay"))




        schema = d.pop("$schema", UNSET)

        user_overlay_detail_response = cls(
            base=base,
            evolution=evolution,
            overlay=overlay,
            schema=schema,
        )

        return user_overlay_detail_response

