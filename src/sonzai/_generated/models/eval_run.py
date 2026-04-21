from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
import datetime






T = TypeVar("T", bound="EvalRun")



@_attrs_define
class EvalRun:
    """ 
        Attributes:
            adaptation_result (Any):
            adaptation_template_id (str):
            adaptation_template_snapshot (Any):
            agent_id (str):
            agent_name (str):
            character_config (Any):
            completed_at (datetime.datetime | None):
            created_at (datetime.datetime):
            evaluation_cost_usd (float):
            evaluation_result (Any):
            run_id (str):
            simulated_minutes (int):
            simulation_config (Any):
            simulation_cost_usd (float):
            simulation_model (str):
            simulation_state (Any):
            started_at (datetime.datetime):
            status (str):
            template_id (str):
            template_snapshot (Any):
            total_cost_usd (float):
            total_sessions (int):
            total_turns (int):
            transcript (Any):
            user_persona (Any):
            schema (str | Unset): A URL to the JSON Schema for this object.
            error_reason (str | Unset):
            project_id (str | Unset):
            tenant_id (str | Unset):
     """

    adaptation_result: Any
    adaptation_template_id: str
    adaptation_template_snapshot: Any
    agent_id: str
    agent_name: str
    character_config: Any
    completed_at: datetime.datetime | None
    created_at: datetime.datetime
    evaluation_cost_usd: float
    evaluation_result: Any
    run_id: str
    simulated_minutes: int
    simulation_config: Any
    simulation_cost_usd: float
    simulation_model: str
    simulation_state: Any
    started_at: datetime.datetime
    status: str
    template_id: str
    template_snapshot: Any
    total_cost_usd: float
    total_sessions: int
    total_turns: int
    transcript: Any
    user_persona: Any
    schema: str | Unset = UNSET
    error_reason: str | Unset = UNSET
    project_id: str | Unset = UNSET
    tenant_id: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        adaptation_result = self.adaptation_result

        adaptation_template_id = self.adaptation_template_id

        adaptation_template_snapshot = self.adaptation_template_snapshot

        agent_id = self.agent_id

        agent_name = self.agent_name

        character_config = self.character_config

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        created_at = self.created_at.isoformat()

        evaluation_cost_usd = self.evaluation_cost_usd

        evaluation_result = self.evaluation_result

        run_id = self.run_id

        simulated_minutes = self.simulated_minutes

        simulation_config = self.simulation_config

        simulation_cost_usd = self.simulation_cost_usd

        simulation_model = self.simulation_model

        simulation_state = self.simulation_state

        started_at = self.started_at.isoformat()

        status = self.status

        template_id = self.template_id

        template_snapshot = self.template_snapshot

        total_cost_usd = self.total_cost_usd

        total_sessions = self.total_sessions

        total_turns = self.total_turns

        transcript = self.transcript

        user_persona = self.user_persona

        schema = self.schema

        error_reason = self.error_reason

        project_id = self.project_id

        tenant_id = self.tenant_id


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "adaptation_result": adaptation_result,
            "adaptation_template_id": adaptation_template_id,
            "adaptation_template_snapshot": adaptation_template_snapshot,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "character_config": character_config,
            "completed_at": completed_at,
            "created_at": created_at,
            "evaluation_cost_usd": evaluation_cost_usd,
            "evaluation_result": evaluation_result,
            "run_id": run_id,
            "simulated_minutes": simulated_minutes,
            "simulation_config": simulation_config,
            "simulation_cost_usd": simulation_cost_usd,
            "simulation_model": simulation_model,
            "simulation_state": simulation_state,
            "started_at": started_at,
            "status": status,
            "template_id": template_id,
            "template_snapshot": template_snapshot,
            "total_cost_usd": total_cost_usd,
            "total_sessions": total_sessions,
            "total_turns": total_turns,
            "transcript": transcript,
            "user_persona": user_persona,
        })
        if schema is not UNSET:
            field_dict["$schema"] = schema
        if error_reason is not UNSET:
            field_dict["error_reason"] = error_reason
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if tenant_id is not UNSET:
            field_dict["tenant_id"] = tenant_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        adaptation_result = d.pop("adaptation_result")

        adaptation_template_id = d.pop("adaptation_template_id")

        adaptation_template_snapshot = d.pop("adaptation_template_snapshot")

        agent_id = d.pop("agent_id")

        agent_name = d.pop("agent_name")

        character_config = d.pop("character_config")

        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)



                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))


        created_at = isoparse(d.pop("created_at"))




        evaluation_cost_usd = d.pop("evaluation_cost_usd")

        evaluation_result = d.pop("evaluation_result")

        run_id = d.pop("run_id")

        simulated_minutes = d.pop("simulated_minutes")

        simulation_config = d.pop("simulation_config")

        simulation_cost_usd = d.pop("simulation_cost_usd")

        simulation_model = d.pop("simulation_model")

        simulation_state = d.pop("simulation_state")

        started_at = isoparse(d.pop("started_at"))




        status = d.pop("status")

        template_id = d.pop("template_id")

        template_snapshot = d.pop("template_snapshot")

        total_cost_usd = d.pop("total_cost_usd")

        total_sessions = d.pop("total_sessions")

        total_turns = d.pop("total_turns")

        transcript = d.pop("transcript")

        user_persona = d.pop("user_persona")

        schema = d.pop("$schema", UNSET)

        error_reason = d.pop("error_reason", UNSET)

        project_id = d.pop("project_id", UNSET)

        tenant_id = d.pop("tenant_id", UNSET)

        eval_run = cls(
            adaptation_result=adaptation_result,
            adaptation_template_id=adaptation_template_id,
            adaptation_template_snapshot=adaptation_template_snapshot,
            agent_id=agent_id,
            agent_name=agent_name,
            character_config=character_config,
            completed_at=completed_at,
            created_at=created_at,
            evaluation_cost_usd=evaluation_cost_usd,
            evaluation_result=evaluation_result,
            run_id=run_id,
            simulated_minutes=simulated_minutes,
            simulation_config=simulation_config,
            simulation_cost_usd=simulation_cost_usd,
            simulation_model=simulation_model,
            simulation_state=simulation_state,
            started_at=started_at,
            status=status,
            template_id=template_id,
            template_snapshot=template_snapshot,
            total_cost_usd=total_cost_usd,
            total_sessions=total_sessions,
            total_turns=total_turns,
            transcript=transcript,
            user_persona=user_persona,
            schema=schema,
            error_reason=error_reason,
            project_id=project_id,
            tenant_id=tenant_id,
        )

        return eval_run

