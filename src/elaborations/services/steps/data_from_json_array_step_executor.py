from data_sources.services.sqlite.data_source_service import load_json_array
from elaborations.models.scenario import Scenario
from elaborations.models.steps import DataFromJsonArrayStepDto
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor


class DataFromJsonArrayStepExecutor(StepExecutor):
    def execute(self, scenario:Scenario, step: DataFromJsonArrayStepDto) -> list[dict[str,str]]:
        json_array = load_json_array(step.json_array_id)
        self.log(step, f"Try to export {len(json_array)}")
        return execute_operations(scenario, step, step.operations, json_array).result