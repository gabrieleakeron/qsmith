import json

from elaborations.models.operations import OperationTypes
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from elaborations.services.sqlite.scenario_results_service import ScenarioResultsService


class SaveInternalDbOperationExecutor(OperationExecutor):
    def execute(self, scenario:Scenario, step:StepDto, operation: OperationTypes, data:list[dict])->ExecutionResultDto:

        rows = 0
        for index, item in enumerate(data):
            ScenarioResultsService.insert(scenario.code, step.description, json.dumps(item))
            rows += 1

        message = f"Created {rows} rows in scenario_results table"

        self.log(operation,message)

        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
