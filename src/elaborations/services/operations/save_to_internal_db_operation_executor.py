import json

from elaborations.models.operations import OperationTypes
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from elaborations.services.operations.operation_executor import OperationExecutor
from elaborations.services.sqlite.scenario_results_service import ScenarioResultsService


class SaveInternalDbOperationExecutor(OperationExecutor):
    def execute(self, scenario:Scenario, step:StepDto, operation: OperationTypes, data:list[dict])->dict[str, str]:

        rows = 0
        for index, item in enumerate(data):
            ScenarioResultsService.insert(scenario.name, step.description, json.dumps(item))
            rows += 1

        return {"message": f"Created {rows} rows in scenario_results table"}
