from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.kb_recommendation_score import KBRecommendationScore





T = TypeVar("T", bound="KbGetRecommendationsOutputBody")



@_attrs_define
class KbGetRecommendationsOutputBody:
    """ 
        Attributes:
            recommendations (list[KBRecommendationScore] | None): Scored recommendations
            total (int): Total count
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    recommendations: list[KBRecommendationScore] | None
    total: int
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.kb_recommendation_score import KBRecommendationScore
        recommendations: list[dict[str, Any]] | None
        if isinstance(self.recommendations, list):
            recommendations = []
            for recommendations_type_0_item_data in self.recommendations:
                recommendations_type_0_item = recommendations_type_0_item_data.to_dict()
                recommendations.append(recommendations_type_0_item)


        else:
            recommendations = self.recommendations

        total = self.total

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "recommendations": recommendations,
            "total": total,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kb_recommendation_score import KBRecommendationScore
        d = dict(src_dict)
        def _parse_recommendations(data: object) -> list[KBRecommendationScore] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                recommendations_type_0 = []
                _recommendations_type_0 = data
                for recommendations_type_0_item_data in (_recommendations_type_0):
                    recommendations_type_0_item = KBRecommendationScore.from_dict(recommendations_type_0_item_data)



                    recommendations_type_0.append(recommendations_type_0_item)

                return recommendations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[KBRecommendationScore] | None, data)

        recommendations = _parse_recommendations(d.pop("recommendations"))


        total = d.pop("total")

        schema = d.pop("$schema", UNSET)

        kb_get_recommendations_output_body = cls(
            recommendations=recommendations,
            total=total,
            schema=schema,
        )

        return kb_get_recommendations_output_body

