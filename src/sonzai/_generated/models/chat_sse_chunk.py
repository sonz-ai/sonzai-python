from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.chat_sse_choice import ChatSSEChoice
  from ..models.chat_sse_chunk_error import ChatSSEChunkError





T = TypeVar("T", bound="ChatSSEChunk")



@_attrs_define
class ChatSSEChunk:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            build_duration_ms (int | Unset): Context build latency in milliseconds (context_ready frame only)
            choices (list[ChatSSEChoice] | None | Unset): Streaming choices — present on delta and terminal
                (finish_reason=stop) frames
            data (Any | Unset): Side-effect payload on type=side_effects frames
            enriched_context (Any | Unset): Full enriched-context JSON included on context_ready frames (debug / inspection
                only)
            error (ChatSSEChunkError | Unset):
            message_index (int | Unset): 0-based agentic turn index (message_boundary frames only)
            side_effects (Any | Unset): Side effects produced during this turn (terminal chunks only)
            type_ (str | Unset): Event type discriminator (context_ready | side_effects | message_boundary). Absent on delta
                and complete frames.
            used_fast_path (bool | Unset): True when a continuation token was used to skip a full context rebuild
                (context_ready frame only)
     """

    schema: str | Unset = UNSET
    build_duration_ms: int | Unset = UNSET
    choices: list[ChatSSEChoice] | None | Unset = UNSET
    data: Any | Unset = UNSET
    enriched_context: Any | Unset = UNSET
    error: ChatSSEChunkError | Unset = UNSET
    message_index: int | Unset = UNSET
    side_effects: Any | Unset = UNSET
    type_: str | Unset = UNSET
    used_fast_path: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.chat_sse_choice import ChatSSEChoice
        from ..models.chat_sse_chunk_error import ChatSSEChunkError
        schema = self.schema

        build_duration_ms = self.build_duration_ms

        choices: list[dict[str, Any]] | None | Unset
        if isinstance(self.choices, Unset):
            choices = UNSET
        elif isinstance(self.choices, list):
            choices = []
            for choices_type_0_item_data in self.choices:
                choices_type_0_item = choices_type_0_item_data.to_dict()
                choices.append(choices_type_0_item)


        else:
            choices = self.choices

        data = self.data

        enriched_context = self.enriched_context

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        message_index = self.message_index

        side_effects = self.side_effects

        type_ = self.type_

        used_fast_path = self.used_fast_path


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if build_duration_ms is not UNSET:
            field_dict["build_duration_ms"] = build_duration_ms
        if choices is not UNSET:
            field_dict["choices"] = choices
        if data is not UNSET:
            field_dict["data"] = data
        if enriched_context is not UNSET:
            field_dict["enriched_context"] = enriched_context
        if error is not UNSET:
            field_dict["error"] = error
        if message_index is not UNSET:
            field_dict["message_index"] = message_index
        if side_effects is not UNSET:
            field_dict["side_effects"] = side_effects
        if type_ is not UNSET:
            field_dict["type"] = type_
        if used_fast_path is not UNSET:
            field_dict["used_fast_path"] = used_fast_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_sse_choice import ChatSSEChoice
        from ..models.chat_sse_chunk_error import ChatSSEChunkError
        d = dict(src_dict)
        schema = d.pop("$schema", UNSET)

        build_duration_ms = d.pop("build_duration_ms", UNSET)

        def _parse_choices(data: object) -> list[ChatSSEChoice] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                choices_type_0 = []
                _choices_type_0 = data
                for choices_type_0_item_data in (_choices_type_0):
                    choices_type_0_item = ChatSSEChoice.from_dict(choices_type_0_item_data)



                    choices_type_0.append(choices_type_0_item)

                return choices_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ChatSSEChoice] | None | Unset, data)

        choices = _parse_choices(d.pop("choices", UNSET))


        data = d.pop("data", UNSET)

        enriched_context = d.pop("enriched_context", UNSET)

        _error = d.pop("error", UNSET)
        error: ChatSSEChunkError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = ChatSSEChunkError.from_dict(_error)




        message_index = d.pop("message_index", UNSET)

        side_effects = d.pop("side_effects", UNSET)

        type_ = d.pop("type", UNSET)

        used_fast_path = d.pop("used_fast_path", UNSET)

        chat_sse_chunk = cls(
            schema=schema,
            build_duration_ms=build_duration_ms,
            choices=choices,
            data=data,
            enriched_context=enriched_context,
            error=error,
            message_index=message_index,
            side_effects=side_effects,
            type_=type_,
            used_fast_path=used_fast_path,
        )

        return chat_sse_chunk

