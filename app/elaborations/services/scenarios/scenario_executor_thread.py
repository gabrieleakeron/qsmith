import threading
from dataclasses import dataclass

from sqlalchemy.orm import Session

from _alembic.models.log_entity import LogEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.enums.on_failure import OnFailure
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.steps.step_executor_composite import execute_step
from exceptions.app_exception import QsmithAppException
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService


@dataclass
class ScenarioExecutionInput:
    scenario_id: str
    scenario_code: str


def log(session:Session, scenario_id: str, message: str, level: LogLevel = LogLevel.INFO, payload: dict | list[dict] = None):
    log_entity = LogEntity()
    log_entity.subject_type = LogSubjectType.SCENARIO_EXECUTION,
    log_entity.subject = scenario_id,
    log_entity.message = message,
    log_entity.level = level,
    log_entity.payload = payload
    LogService().log(session, log_entity)


def _execute(scenario_input: ScenarioExecutionInput):
    with managed_session() as session:
        log(session, scenario_input.scenario_id, message=f"Starting execution of scenario '{scenario_input.scenario_code}'")

        scenario_steps: list[ScenarioStepEntity] = ScenarioStepService().get_all_by_scenario_id(session,
                                                                                                scenario_input.scenario_id)

        results = []
        total_steps = len(scenario_steps)
        for scenario_step in scenario_steps:
            log(session, scenario_input.scenario_id,
                message=f"Executing scenario_step {scenario_step.order} of {total_steps} in scenario '{scenario_input.scenario_code}'")
            try:
                results.append(execute_step(session, scenario_step))
            except Exception as step_exception:
                log(session, scenario_input.scenario_id,
                    message=f"Error executing scenario_step n.'{scenario_step.order}' in scenario '{scenario_input.scenario_code}'",
                    level=LogLevel.ERROR, payload={"error": str(step_exception)})
                if scenario_step.on_failure == OnFailure.ABORT:
                    break

        log(session, scenario_input.scenario_id, message=f"Finished execution of scenario '{scenario_input.scenario_code}'",
            payload={"results": results})


class ScenarioExecutorThread(threading.Thread):

    def __init__(self, scenario_id: str):
        super().__init__(name=f"scenario-{scenario_id}", daemon=True)
        with managed_session() as session:
            scenario = ScenarioService().get_by_id(session, scenario_id)
            if not scenario:
                message = f"Scenario with id '{scenario_id}' not found"
                log(scenario_id, message=message, level=LogLevel.ERROR)
                raise QsmithAppException(message)
            self.scenario_id = scenario.id
            self.scenario_code = scenario.code

    def run(self):
        _execute(ScenarioExecutionInput(
            scenario_id=self.scenario_id,
            scenario_code=self.scenario_code
        ))
