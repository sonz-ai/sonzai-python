from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.big_5_scores_input import Big5ScoresInput
  from ..models.dimensions_input import DimensionsInput





T = TypeVar("T", bound="UpdatePersonalityInputBody")



@_attrs_define
class UpdatePersonalityInputBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            big5 (Big5ScoresInput | Unset):
            dimensions (DimensionsInput | Unset):
     """

    schema: str | Unset = UNSET
    big5: Big5ScoresInput | Unset = UNSET
    dimensions: DimensionsInput | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.big_5_scores_input import Big5ScoresInput
        from ..models.dimensions_input import DimensionsInput
        schema = self.schema

        big5: dict[str, Any] | Unset = UNSET
        if not isinstance(self.big5, Unset):
            big5 = self.big5.to_dict()

        dimensions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dimensions, Unset):
            dimensions = self.dimensions.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if big5 is not UNSET:
            field_dict["big5"] = big5
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.big_5_scores_input import Big5ScoresInput
        from ..models.dimensions_input import DimensionsInput
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        _big5 = d.pop("big5", UNSET)
        big5: Big5ScoresInput | Unset
        if isinstance(_big5,  Unset):
            big5 = UNSET
        else:
            big5 = Big5ScoresInput.from_dict(_big5)




        _dimensions = d.pop("dimensions", UNSET)
        dimensions: DimensionsInput | Unset
        if isinstance(_dimensions,  Unset):
            dimensions = UNSET
        else:
            dimensions = DimensionsInput.from_dict(_dimensions)




        update_personality_input_body = cls(
            schema=schema,
            big5=big5,
            dimensions=dimensions,
        )

        return update_personality_input_body

