from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.eval_agent_config_override import EvalAgentConfigOverride
  from ..models.evaluate_transcript_msg import EvaluateTranscriptMsg





T = TypeVar("T", bound="EvaluateRequest")



@_attrs_define
class EvaluateRequest:
    """ 
        Attributes:
            messages (list[EvaluateTranscriptMsg] | None): Transcript messages — at least 2 required
            template_id (str): Quality-eval template UUID
            schema (str | Unset): A URL to the JSON Schema for this object.
            adaptation_template_id (str | Unset): Optional adaptation-eval template UUID; defaults to tenant's first
                adaptation template
            config_override (EvalAgentConfigOverride | Unset):
            model (str | Unset): Override LLM model (judge model comes from the template)
            provider (str | Unset): Override LLM provider for this run (e.g. gemini, openrouter). Accepted for forward-
                compat; currently unused server-side (judge provider comes from the template).
            quality_only (bool | Unset): Skip adaptation evaluation and only run quality scoring
            simulation_config (Any | Unset): Opaque simulator config to include on the run record
            simulation_state (Any | Unset): Opaque simulator state to include on the run record
            user_persona (Any | Unset): Synthetic user persona used during the simulation
     """

    messages: list[EvaluateTranscriptMsg] | None
    template_id: str
    schema: str | Unset = UNSET
    adaptation_template_id: str | Unset = UNSET
    config_override: EvalAgentConfigOverride | Unset = UNSET
    model: str | Unset = UNSET
    provider: str | Unset = UNSET
    quality_only: bool | Unset = UNSET
    simulation_config: Any | Unset = UNSET
    simulation_state: Any | Unset = UNSET
    user_persona: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_config_override import EvalAgentConfigOverride
        from ..models.evaluate_transcript_msg import EvaluateTranscriptMsg
        messages: list[dict[str, Any]] | None
        if isinstance(self.messages, list):
            messages = []
            for messages_type_0_item_data in self.messages:
                messages_type_0_item = messages_type_0_item_data.to_dict()
                messages.append(messages_type_0_item)


        else:
            messages = self.messages

        template_id = self.template_id

        schema = self.schema

        adaptation_template_id = self.adaptation_template_id

        config_override: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_override, Unset):
            config_override = self.config_override.to_dict()

        model = self.model

        provider = self.provider

        quality_only = self.quality_only

        simulation_config = self.simulation_config

        simulation_state = self.simulation_state

        user_persona = self.user_persona


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "messages": messages,
            "template_id": template_id,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if adaptation_template_id is not UNSET:
            field_dict["adaptation_template_id"] = adaptation_template_id
        if config_override is not UNSET:
            field_dict["config_override"] = config_override
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if quality_only is not UNSET:
            field_dict["quality_only"] = quality_only
        if simulation_config is not UNSET:
            field_dict["simulation_config"] = simulation_config
        if simulation_state is not UNSET:
            field_dict["simulation_state"] = simulation_state
        if user_persona is not UNSET:
            field_dict["user_persona"] = user_persona

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_config_override import EvalAgentConfigOverride
        from ..models.evaluate_transcript_msg import EvaluateTranscriptMsg
        d = dict(src_dict)
        def _parse_messages(data: object) -> list[EvaluateTranscriptMsg] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                messages_type_0 = []
                _messages_type_0 = data
                for messages_type_0_item_data in (_messages_type_0):
                    messages_type_0_item = EvaluateTranscriptMsg.from_dict(messages_type_0_item_data)



                    messages_type_0.append(messages_type_0_item)

                return messages_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[EvaluateTranscriptMsg] | None, data)

        messages = _parse_messages(d.pop("messages"))


        template_id = d.pop("template_id")

        schema = d.pop("$schema", UNSET)

        adaptation_template_id = d.pop("adaptation_template_id", UNSET)

        _config_override = d.pop("config_override", UNSET)
        config_override: EvalAgentConfigOverride | Unset
        if isinstance(_config_override,  Unset):
            config_override = UNSET
        else:
            config_override = EvalAgentConfigOverride.from_dict(_config_override)




        model = d.pop("model", UNSET)

        provider = d.pop("provider", UNSET)

        quality_only = d.pop("quality_only", UNSET)

        simulation_config = d.pop("simulation_config", UNSET)

        simulation_state = d.pop("simulation_state", UNSET)

        user_persona = d.pop("user_persona", UNSET)

        evaluate_request = cls(
            messages=messages,
            template_id=template_id,
            schema=schema,
            adaptation_template_id=adaptation_template_id,
            config_override=config_override,
            model=model,
            provider=provider,
            quality_only=quality_only,
            simulation_config=simulation_config,
            simulation_state=simulation_state,
            user_persona=user_persona,
        )

        return evaluate_request

