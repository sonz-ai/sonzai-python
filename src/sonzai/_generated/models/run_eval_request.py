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
  from ..models.session_config import SessionConfig
  from ..models.sim_config import SimConfig
  from ..models.user_persona import UserPersona





T = TypeVar("T", bound="RunEvalRequest")



@_attrs_define
class RunEvalRequest:
    """ 
        Attributes:
            template_id (str): Quality-eval template UUID
            schema (str | Unset): A URL to the JSON Schema for this object.
            adaptation_template_id (str | Unset): Optional adaptation-eval template UUID; defaults to the tenant's first
                adaptation template
            config_override (EvalAgentConfigOverride | Unset):
            model (str | Unset): LLM model override
            quality_only (bool | Unset): Skip adaptation evaluation
            sessions (list[SessionConfig] | None | Unset): Session configurations driving the simulator
            simulation_config (SimConfig | Unset):
            user_persona (UserPersona | Unset):
     """

    template_id: str
    schema: str | Unset = UNSET
    adaptation_template_id: str | Unset = UNSET
    config_override: EvalAgentConfigOverride | Unset = UNSET
    model: str | Unset = UNSET
    quality_only: bool | Unset = UNSET
    sessions: list[SessionConfig] | None | Unset = UNSET
    simulation_config: SimConfig | Unset = UNSET
    user_persona: UserPersona | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_config_override import EvalAgentConfigOverride
        from ..models.session_config import SessionConfig
        from ..models.sim_config import SimConfig
        from ..models.user_persona import UserPersona
        template_id = self.template_id

        schema = self.schema

        adaptation_template_id = self.adaptation_template_id

        config_override: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_override, Unset):
            config_override = self.config_override.to_dict()

        model = self.model

        quality_only = self.quality_only

        sessions: list[dict[str, Any]] | None | Unset
        if isinstance(self.sessions, Unset):
            sessions = UNSET
        elif isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)


        else:
            sessions = self.sessions

        simulation_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.simulation_config, Unset):
            simulation_config = self.simulation_config.to_dict()

        user_persona: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_persona, Unset):
            user_persona = self.user_persona.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
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
        if quality_only is not UNSET:
            field_dict["quality_only"] = quality_only
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if simulation_config is not UNSET:
            field_dict["simulation_config"] = simulation_config
        if user_persona is not UNSET:
            field_dict["user_persona"] = user_persona

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.eval_agent_config_override import EvalAgentConfigOverride
        from ..models.session_config import SessionConfig
        from ..models.sim_config import SimConfig
        from ..models.user_persona import UserPersona
        d = dict(src_dict)
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

        quality_only = d.pop("quality_only", UNSET)

        def _parse_sessions(data: object) -> list[SessionConfig] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in (_sessions_type_0):
                    sessions_type_0_item = SessionConfig.from_dict(sessions_type_0_item_data)



                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SessionConfig] | None | Unset, data)

        sessions = _parse_sessions(d.pop("sessions", UNSET))


        _simulation_config = d.pop("simulation_config", UNSET)
        simulation_config: SimConfig | Unset
        if isinstance(_simulation_config,  Unset):
            simulation_config = UNSET
        else:
            simulation_config = SimConfig.from_dict(_simulation_config)




        _user_persona = d.pop("user_persona", UNSET)
        user_persona: UserPersona | Unset
        if isinstance(_user_persona,  Unset):
            user_persona = UNSET
        else:
            user_persona = UserPersona.from_dict(_user_persona)




        run_eval_request = cls(
            template_id=template_id,
            schema=schema,
            adaptation_template_id=adaptation_template_id,
            config_override=config_override,
            model=model,
            quality_only=quality_only,
            sessions=sessions,
            simulation_config=simulation_config,
            user_persona=user_persona,
        )

        return run_eval_request

