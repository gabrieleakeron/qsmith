from _alembic.models.step_entity import StepEntity
from elaborations.models.dtos.configuration_step_dtos import DataConfigurationStepDTO
from elaborations.services.steps.step_executor import StepExecutor


class DataStepExecutor(StepExecutor):
    def execute(self, step:StepEntity, cfg: DataConfigurationStepDTO) -> list[dict[str, str]]:
        self.log(step, f"Try to export {len(step.data)}")
        return self.execute_operations(step.id,cfg.data)