from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.delete_agent_output_body_deleted import DeleteAgentOutputBodyDeleted





T = TypeVar("T", bound="DeleteAgentOutputBody")



@_attrs_define
class DeleteAgentOutputBody:
    """ 
        Attributes:
            deleted (DeleteAgentOutputBodyDeleted): Counts of deleted sub-resources
            errors (list[str] | None): Partial-failure error messages
            status (str): ok or partial
            success (bool): Whether the delete fully succeeded
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    deleted: DeleteAgentOutputBodyDeleted
    errors: list[str] | None
    status: str
    success: bool
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.delete_agent_output_body_deleted import DeleteAgentOutputBodyDeleted
        deleted = self.deleted.to_dict()

        errors: list[str] | None
        if isinstance(self.errors, list):
            errors = self.errors


        else:
            errors = self.errors

        status = self.status

        success = self.success

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "deleted": deleted,
            "errors": errors,
            "status": status,
            "success": success,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_agent_output_body_deleted import DeleteAgentOutputBodyDeleted
        d = dict(src_dict)
        deleted = DeleteAgentOutputBodyDeleted.from_dict(d.pop("deleted"))




        def _parse_errors(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                errors_type_0 = cast(list[str], data)

                return errors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        errors = _parse_errors(d.pop("errors"))


        status = d.pop("status")

        success = d.pop("success")

        schema = d.pop("$schema", UNSET)

        delete_agent_output_body = cls(
            deleted=deleted,
            errors=errors,
            status=status,
            success=success,
            schema=schema,
        )

        return delete_agent_output_body

