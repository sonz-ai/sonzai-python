from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.user_persona_record import UserPersonaRecord





T = TypeVar("T", bound="ListUserPersonasOutputBody")



@_attrs_define
class ListUserPersonasOutputBody:
    """ 
        Attributes:
            personas (list[UserPersonaRecord] | None): Personas owned by the caller's tenant (auto-seeded with defaults)
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    personas: list[UserPersonaRecord] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.user_persona_record import UserPersonaRecord
        personas: list[dict[str, Any]] | None
        if isinstance(self.personas, list):
            personas = []
            for personas_type_0_item_data in self.personas:
                personas_type_0_item = personas_type_0_item_data.to_dict()
                personas.append(personas_type_0_item)


        else:
            personas = self.personas

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "personas": personas,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_persona_record import UserPersonaRecord
        d = dict(src_dict)
        def _parse_personas(data: object) -> list[UserPersonaRecord] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                personas_type_0 = []
                _personas_type_0 = data
                for personas_type_0_item_data in (_personas_type_0):
                    personas_type_0_item = UserPersonaRecord.from_dict(personas_type_0_item_data)



                    personas_type_0.append(personas_type_0_item)

                return personas_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UserPersonaRecord] | None, data)

        personas = _parse_personas(d.pop("personas"))


        schema = d.pop("$schema", UNSET)

        list_user_personas_output_body = cls(
            personas=personas,
            schema=schema,
        )

        return list_user_personas_output_body

