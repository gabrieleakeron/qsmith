import threading

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


def log(scenario_id:str, message:str, level:LogLevel=LogLevel.INFO, payload:dict|list[dict]=None):
    with managed_session() as session:
        LogService.log(session,LogEntity(subject_type=LogSubjectType.SCENARIO_EXECUTION,
                          subject=scenario_id,
                          message=message,
                          level=level,
                            payload=payload
                          ))

class ScenarioExecutorThread(threading.Thread):
    def __init__(self,scenario_id:str):
        super().__init__(name=f"scenario-{scenario_id}",daemon=True)
        with managed_session() as session:
            self.scenario = ScenarioService.get_by_id(session, scenario_id)
            if not self.scenario:
                message = f"Scenario with id '{scenario_id}' not found"
                log(scenario_id, message=message, level=LogLevel.ERROR)
                raise QsmithAppException(message)

    def run(self):
        with managed_session() as session:
            log(self.scenario.id, message=f"Starting execution of scenario '{self.scenario.code}'")

            scenario_steps:list[ScenarioStepEntity] = ScenarioStepService.get_all_by_scenario(session, self.scenario.id)

            results = []
            total_steps = len(scenario_steps)
            for scenario_step in scenario_steps:
                log(self.scenario.id, message=f"Executing scenario_step {scenario_step.order} of {total_steps} ('{scenario_step.code}') in scenario '{self.scenario.code}'")
                try:
                    results.append(execute_step(scenario_step.step_id))
                except Exception as step_exception:
                    log(self.scenario, message=f"Error executing scenario_step n.'{scenario_step.order}' in scenario '{self.scenario.code}'",
                        level=LogLevel.ERROR, payload={"error": str(step_exception)})
                    if scenario_step.on_failure == OnFailure.ABORT:
                        break

            log(self.scenario, message=f"Finished execution of scenario '{self.scenario.code}'",
                payload={"results": results})









