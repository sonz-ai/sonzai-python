from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.atomic_fact import AtomicFact





T = TypeVar("T", bound="MemoryResponseContents")



@_attrs_define
class MemoryResponseContents:
    """ 
     """

    additional_properties: dict[str, list[AtomicFact] | None] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.atomic_fact import AtomicFact
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            
            if isinstance(prop, list):
                field_dict[prop_name] = []
                for additional_property_type_0_item_data in prop:
                    additional_property_type_0_item = additional_property_type_0_item_data.to_dict()
                    field_dict[prop_name].append(additional_property_type_0_item)


            else:
                field_dict[prop_name] = prop


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.atomic_fact import AtomicFact
        d = dict(src_dict)
        memory_response_contents = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            def _parse_additional_property(data: object) -> list[AtomicFact] | None:
                if data is None:
                    return data
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_0 = []
                    _additional_property_type_0 = data
                    for additional_property_type_0_item_data in (_additional_property_type_0):
                        additional_property_type_0_item = AtomicFact.from_dict(additional_property_type_0_item_data)



                        additional_property_type_0.append(additional_property_type_0_item)

                    return additional_property_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                return cast(list[AtomicFact] | None, data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        memory_response_contents.additional_properties = additional_properties
        return memory_response_contents

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> list[AtomicFact] | None:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: list[AtomicFact] | None) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
