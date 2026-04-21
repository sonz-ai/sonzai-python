from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.eval_template import EvalTemplate





T = TypeVar("T", bound="ListEvalTemplatesOutputBody")



@_attrs_define
class ListEvalTemplatesOutputBody:
    """ 
        Attributes:
            templates (list[EvalTemplate] | None): List of eval templates
            schema (str | Unset): A URL to the JSON Schema for this object.
     """

    templates: list[EvalTemplate] | None
    schema: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_template import EvalTemplate
        templates: list[dict[str, Any]] | None
        if isinstance(self.templates, list):
            templates = []
            for templates_type_0_item_data in self.templates:
                templates_type_0_item = templates_type_0_item_data.to_dict()
                templates.append(templates_type_0_item)


        else:
            templates = self.templates

        schema = self.schema


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "templates": templates,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_template import EvalTemplate
        d = dict(src_dict)
        def _parse_templates(data: object) -> list[EvalTemplate] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                templates_type_0 = []
                _templates_type_0 = data
                for templates_type_0_item_data in (_templates_type_0):
                    templates_type_0_item = EvalTemplate.from_dict(templates_type_0_item_data)



                    templates_type_0.append(templates_type_0_item)

                return templates_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[EvalTemplate] | None, data)

        templates = _parse_templates(d.pop("templates"))


        schema = d.pop("$schema", UNSET)

        list_eval_templates_output_body = cls(
            templates=templates,
            schema=schema,
        )

        return list_eval_templates_output_body

