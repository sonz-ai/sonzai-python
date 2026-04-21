from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.workbench_generate_character_generated import WorkbenchGenerateCharacterGenerated
  from ..models.workbench_generate_character_usage import WorkbenchGenerateCharacterUsage





T = TypeVar("T", bound="WorkbenchGenerateCharacterBody")



@_attrs_define
class WorkbenchGenerateCharacterBody:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            agent_id (str | Unset):
            existing (bool | Unset):
            generated (WorkbenchGenerateCharacterGenerated | Unset):
            usage (WorkbenchGenerateCharacterUsage | Unset):
     """

    schema: str | Unset = UNSET
    agent_id: str | Unset = UNSET
    existing: bool | Unset = UNSET
    generated: WorkbenchGenerateCharacterGenerated | Unset = UNSET
    usage: WorkbenchGenerateCharacterUsage | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.workbench_generate_character_generated import WorkbenchGenerateCharacterGenerated
        from ..models.workbench_generate_character_usage import WorkbenchGenerateCharacterUsage
        schema = self.schema

        agent_id = self.agent_id

        existing = self.existing

        generated: dict[str, Any] | Unset = UNSET
        if not isinstance(self.generated, Unset):
            generated = self.generated.to_dict()

        usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if existing is not UNSET:
            field_dict["existing"] = existing
        if generated is not UNSET:
            field_dict["generated"] = generated
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workbench_generate_character_generated import WorkbenchGenerateCharacterGenerated
        from ..models.workbench_generate_character_usage import WorkbenchGenerateCharacterUsage
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        agent_id = d.pop("agent_id", UNSET)

        existing = d.pop("existing", UNSET)

        _generated = d.pop("generated", UNSET)
        generated: WorkbenchGenerateCharacterGenerated | Unset
        if isinstance(_generated,  Unset):
            generated = UNSET
        else:
            generated = WorkbenchGenerateCharacterGenerated.from_dict(_generated)




        _usage = d.pop("usage", UNSET)
        usage: WorkbenchGenerateCharacterUsage | Unset
        if isinstance(_usage,  Unset):
            usage = UNSET
        else:
            usage = WorkbenchGenerateCharacterUsage.from_dict(_usage)




        workbench_generate_character_body = cls(
            schema=schema,
            agent_id=agent_id,
            existing=existing,
            generated=generated,
            usage=usage,
        )

        return workbench_generate_character_body

