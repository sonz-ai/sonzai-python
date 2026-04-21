from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="PersonalityDelta")



@_attrs_define
class PersonalityDelta:
    """ 
        Attributes:
            delta (float):
            new_value (float):
            old_value (float):
            timestamp (datetime.datetime):
            trait_category (str):
            trait_name (str):
            trigger_type (str):
            applied_delta (float | Unset):
            confidence (float | Unset):
            dampening_factor (float | Unset):
            is_significant_moment (bool | Unset):
            posterior_precision (float | Unset):
            prediction_error (float | Unset):
            prior_precision (float | Unset):
            proposed_delta (float | Unset):
            reasoning (str | Unset):
            user_id (str | Unset):
     """

    delta: float
    new_value: float
    old_value: float
    timestamp: datetime.datetime
    trait_category: str
    trait_name: str
    trigger_type: str
    applied_delta: float | Unset = UNSET
    confidence: float | Unset = UNSET
    dampening_factor: float | Unset = UNSET
    is_significant_moment: bool | Unset = UNSET
    posterior_precision: float | Unset = UNSET
    prediction_error: float | Unset = UNSET
    prior_precision: float | Unset = UNSET
    proposed_delta: float | Unset = UNSET
    reasoning: str | Unset = UNSET
    user_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        delta = self.delta

        new_value = self.new_value

        old_value = self.old_value

        timestamp = self.timestamp.isoformat()

        trait_category = self.trait_category

        trait_name = self.trait_name

        trigger_type = self.trigger_type

        applied_delta = self.applied_delta

        confidence = self.confidence

        dampening_factor = self.dampening_factor

        is_significant_moment = self.is_significant_moment

        posterior_precision = self.posterior_precision

        prediction_error = self.prediction_error

        prior_precision = self.prior_precision

        proposed_delta = self.proposed_delta

        reasoning = self.reasoning

        user_id = self.user_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "delta": delta,
            "new_value": new_value,
            "old_value": old_value,
            "timestamp": timestamp,
            "trait_category": trait_category,
            "trait_name": trait_name,
            "trigger_type": trigger_type,
        })
        if applied_delta is not UNSET:
            field_dict["applied_delta"] = applied_delta
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if dampening_factor is not UNSET:
            field_dict["dampening_factor"] = dampening_factor
        if is_significant_moment is not UNSET:
            field_dict["is_significant_moment"] = is_significant_moment
        if posterior_precision is not UNSET:
            field_dict["posterior_precision"] = posterior_precision
        if prediction_error is not UNSET:
            field_dict["prediction_error"] = prediction_error
        if prior_precision is not UNSET:
            field_dict["prior_precision"] = prior_precision
        if proposed_delta is not UNSET:
            field_dict["proposed_delta"] = proposed_delta
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        delta = d.pop("delta")

        new_value = d.pop("new_value")

        old_value = d.pop("old_value")

        timestamp = isoparse(d.pop("timestamp"))




        trait_category = d.pop("trait_category")

        trait_name = d.pop("trait_name")

        trigger_type = d.pop("trigger_type")

        applied_delta = d.pop("applied_delta", UNSET)

        confidence = d.pop("confidence", UNSET)

        dampening_factor = d.pop("dampening_factor", UNSET)

        is_significant_moment = d.pop("is_significant_moment", UNSET)

        posterior_precision = d.pop("posterior_precision", UNSET)

        prediction_error = d.pop("prediction_error", UNSET)

        prior_precision = d.pop("prior_precision", UNSET)

        proposed_delta = d.pop("proposed_delta", UNSET)

        reasoning = d.pop("reasoning", UNSET)

        user_id = d.pop("user_id", UNSET)

        personality_delta = cls(
            delta=delta,
            new_value=new_value,
            old_value=old_value,
            timestamp=timestamp,
            trait_category=trait_category,
            trait_name=trait_name,
            trigger_type=trigger_type,
            applied_delta=applied_delta,
            confidence=confidence,
            dampening_factor=dampening_factor,
            is_significant_moment=is_significant_moment,
            posterior_precision=posterior_precision,
            prediction_error=prediction_error,
            prior_precision=prior_precision,
            proposed_delta=proposed_delta,
            reasoning=reasoning,
            user_id=user_id,
        )

        return personality_delta

