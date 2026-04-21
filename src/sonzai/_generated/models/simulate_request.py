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





T = TypeVar("T", bound="SimulateRequest")



@_attrs_define
class SimulateRequest:
    """ 
        Attributes:
            schema (str | Unset): A URL to the JSON Schema for this object.
            config (SimConfig | Unset):
            config_override (EvalAgentConfigOverride | Unset):
            model (str | Unset): Agent LLM model override
            sessions (list[SessionConfig] | None | Unset): Session configurations driving the simulator
            user_id (str | Unset): Stable user ID for CE memory scoping
            user_persona (UserPersona | Unset):
     """

    schema: str | Unset = UNSET
    config: SimConfig | Unset = UNSET
    config_override: EvalAgentConfigOverride | Unset = UNSET
    model: str | Unset = UNSET
    sessions: list[SessionConfig] | None | Unset = UNSET
    user_id: str | Unset = UNSET
    user_persona: UserPersona | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.eval_agent_config_override import EvalAgentConfigOverride
        from ..models.session_config import SessionConfig
        from ..models.sim_config import SimConfig
        from ..models.user_persona import UserPersona
        schema = self.schema

        config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        config_override: dict[str, Any] | Unset = UNSET
        if not isinstance(self.config_override, Unset):
            config_override = self.config_override.to_dict()

        model = self.model

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

        user_id = self.user_id

        user_persona: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_persona, Unset):
            user_persona = self.user_persona.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if config is not UNSET:
            field_dict["config"] = config
        if config_override is not UNSET:
            field_dict["config_override"] = config_override
        if model is not UNSET:
            field_dict["model"] = model
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
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
        schema = d.pop("$schema", UNSET)

        _config = d.pop("config", UNSET)
        config: SimConfig | Unset
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = SimConfig.from_dict(_config)




        _config_override = d.pop("config_override", UNSET)
        config_override: EvalAgentConfigOverride | Unset
        if isinstance(_config_override,  Unset):
            config_override = UNSET
        else:
            config_override = EvalAgentConfigOverride.from_dict(_config_override)




        model = d.pop("model", UNSET)

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


        user_id = d.pop("user_id", UNSET)

        _user_persona = d.pop("user_persona", UNSET)
        user_persona: UserPersona | Unset
        if isinstance(_user_persona,  Unset):
            user_persona = UNSET
        else:
            user_persona = UserPersona.from_dict(_user_persona)




        simulate_request = cls(
            schema=schema,
            config=config,
            config_override=config_override,
            model=model,
            sessions=sessions,
            user_id=user_id,
            user_persona=user_persona,
        )

        return simulate_request

