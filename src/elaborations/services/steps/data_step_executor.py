from elaborations.models.scenario import Scenario
from elaborations.models.steps import DataStepDTO
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor


class DataStepExecutor(StepExecutor):
    def execute(self, scenario:Scenario, step: DataStepDTO) -> list[dict[str, str]]:
        return execute_operations(scenario,step, step.operations, step.data).result