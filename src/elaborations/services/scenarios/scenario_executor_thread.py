import threading

from elaborations.models.steps import OnFailure
from logs.models.logs import LogLevel, LogDto, LogSubjectType
from elaborations.models.scenario import Scenario
from elaborations.services.steps.step_executor_composite import execute_step
from logs.services.sqlite.log_service import LogService


def log(scenario:Scenario,message:str, level:LogLevel=LogLevel.INFO, payload:dict|list[dict]=None):
    LogService.log(LogDto(subject_type=LogSubjectType.SCENARIO_EXECUTION,
                          subject=scenario.id,
                          message=message,
                          level=level,
                            payload=payload
                          ))

class ScenarioExecutorThread(threading.Thread):
    def __init__(self,scenario:Scenario):
        super().__init__(name=f"scenario-{scenario.id}",daemon=True)
        self.scenario = scenario

    def run(self):
        log(self.scenario, message=f"Starting execution of scenario '{self.scenario.code}'")

        results = []
        total_steps = len(self.scenario.steps)
        for index, step in enumerate(self.scenario.steps):
            log(self.scenario,
                message=f"Executing step {index + 1} of {total_steps} ('{step.code}') in scenario '{self.scenario.code}'")
            try:
                results.append(execute_step(self.scenario, step))
            except Exception as step_exception:
                log(self.scenario, message=f"Error executing step '{step.code}' in scenario '{self.scenario.code}'",
                    level=LogLevel.ERROR, payload={"error": str(step_exception)})
                if step.on_failure == OnFailure.ABORT:
                    break

        log(self.scenario, message=f"Finished execution of scenario '{self.scenario.code}'", payload={"results": results})








