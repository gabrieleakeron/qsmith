import time

from elaborations.models.scenario import Scenario
from elaborations.models.steps import SleepStepDto
from elaborations.services.steps.step_executor import StepExecutor


class SleepStepExecutor(StepExecutor):
    def execute(self, scenario:Scenario, step: SleepStepDto) -> list[dict[str, str]]:
        time.sleep(step.duration)
        self.log(step, f"Slept for {step.duration} seconds")
        return [{"status": "slept", "duration": str(step.duration)}]