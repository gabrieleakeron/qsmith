import threading

from logs.models.log_type import LogLevel
from logs.services.sqlite.log_service import log
from elaborations.models.scenario import Scenario
from elaborations.services.steps.step_executor_composite import execute_step


class ScenarioExecutorThread(threading.Thread):

    def __init__(self,scenario:Scenario):
        super().__init__(name=f"scenario-{scenario.id}",daemon=True)
        self.scenario = scenario


    def run(self):
        results = []

        try:
            for step in self.scenario.steps:
                results.append(execute_step(self.scenario, step))

            log(message=f"Scenario '{self.scenario.code}' executed with {len(results)} step(s)")

        except Exception as e:
            log(message=f"Error executing scenario '{self.scenario.code}': {str(e)}", level=LogLevel.ERROR)



