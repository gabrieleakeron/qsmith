import time

from elaborations.models.dtos.configuration_step_dtos import SleepConfigurationStepDto
from _alembic.models.step_entity import StepEntity
from elaborations.services.steps.step_executor import StepExecutor


class SleepStepExecutor(StepExecutor):
    def execute(self,step:StepEntity, cfg: SleepConfigurationStepDto) -> list[dict[str, str]]:
        time.sleep(cfg.duration)
        self.log(step.id, f"Slept for {cfg.duration} seconds")
        return [{"status": "slept", "duration": str(cfg.duration)}]