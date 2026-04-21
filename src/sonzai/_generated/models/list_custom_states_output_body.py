from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.custom_state import CustomState





T = TypeVar("T", bound="ListCustomStatesOutputBody")



@_attrs_define
class ListCustomStatesOutputBody:
    """ 
        Attributes:
            states (list[CustomState] | None): List of custom states
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    states: list[CustomState] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_state import CustomState
        states: list[dict[str, Any]] | None
        if isinstance(self.states, list):
            states = []
            for states_type_0_item_data in self.states:
                states_type_0_item = states_type_0_item_data.to_dict()
                states.append(states_type_0_item)


        else:
            states = self.states

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "states": states,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_state import CustomState
        d = dict(src_dict)
        def _parse_states(data: object) -> list[CustomState] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                states_type_0 = []
                _states_type_0 = data
                for states_type_0_item_data in (_states_type_0):
                    states_type_0_item = CustomState.from_dict(states_type_0_item_data)



                    states_type_0.append(states_type_0_item)

                return states_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[CustomState] | None, data)

        states = _parse_states(d.pop("states"))


        schema = d.pop("$schema", UNSET)

        list_custom_states_output_body = cls(
            states=states,
            schema=schema,
        )

        return list_custom_states_output_body

