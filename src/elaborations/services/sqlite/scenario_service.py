from json_utils.models.json_payload import JsonPayload
from json_utils.services.sqlite.json_files_service import JsonFilesService
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from elaborations.services.scenarios.scenario_executor_thread import ScenarioExecutorThread
from elaborations.services.sqlite.scenario_results_service import ScenarioResultsService


def load_scenario(_id:str)-> Scenario:
    json_payload: JsonPayload = JsonFilesService.get_by_id(_id)

    if not json_payload:
        raise ValueError(f"Scenario '{_id}' not found")

    steps: list[StepDto] = []

    if isinstance(json_payload.payload, list):
        for step in json_payload.payload:
            steps.append(StepDto.model_validate(step))
    else:
        steps.append(StepDto.model_validate(json_payload.payload))

    scenario = Scenario(
        id=json_payload.id,
        code=json_payload.code,
        description=json_payload.description,
        steps=steps
    )

    return scenario

def execute_scenario(_id: str):
    scenario = load_scenario(_id)

    if not scenario:
        raise ValueError(f"Scenario '{_id}' not found")

    ScenarioResultsService.delete_by_scenario(_id)

    ScenarioExecutorThread(scenario).start()


