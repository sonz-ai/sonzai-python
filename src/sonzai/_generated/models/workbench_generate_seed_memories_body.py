from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.workbench_seed_memory_item import WorkbenchSeedMemoryItem





T = TypeVar("T", bound="WorkbenchGenerateSeedMemoriesBody")



@_attrs_define
class WorkbenchGenerateSeedMemoriesBody:
    """ 
        Attributes:
            memories (list[WorkbenchSeedMemoryItem] | None):
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    memories: list[WorkbenchSeedMemoryItem] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.workbench_seed_memory_item import WorkbenchSeedMemoryItem
        memories: list[dict[str, Any]] | None
        if isinstance(self.memories, list):
            memories = []
            for memories_type_0_item_data in self.memories:
                memories_type_0_item = memories_type_0_item_data.to_dict()
                memories.append(memories_type_0_item)


        else:
            memories = self.memories

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "memories": memories,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workbench_seed_memory_item import WorkbenchSeedMemoryItem
        d = dict(src_dict)
        def _parse_memories(data: object) -> list[WorkbenchSeedMemoryItem] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                memories_type_0 = []
                _memories_type_0 = data
                for memories_type_0_item_data in (_memories_type_0):
                    memories_type_0_item = WorkbenchSeedMemoryItem.from_dict(memories_type_0_item_data)



                    memories_type_0.append(memories_type_0_item)

                return memories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[WorkbenchSeedMemoryItem] | None, data)

        memories = _parse_memories(d.pop("memories"))


        schema = d.pop("$schema", UNSET)

        workbench_generate_seed_memories_body = cls(
            memories=memories,
            schema=schema,
        )

        return workbench_generate_seed_memories_body

