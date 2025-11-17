from data_sources.services.sqlite.data_source_service import load_json_array
from elaborations.models.dtos.configuration_step_dtos import DataFromJsonArrayConfigurationStepDto
from _alembic.models.step_entity import StepEntity
from elaborations.services.steps.step_executor import StepExecutor


class DataFromJsonArrayStepExecutor(StepExecutor):
    def execute(self, step:StepEntity, cfg: DataFromJsonArrayConfigurationStepDto) -> list[dict[str,str]]:
        json_array = load_json_array(cfg.json_array_id)

        self.log(step.id, f"Try to elaborate {len(json_array)} objects from JSON array")

        return self.execute_operations(step.id,json_array)