import json

from fastapi import APIRouter

from json_utils.models.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.models.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.sqlite.json_files_service import JsonFilesService
from elaborations.services.sqlite.scenario_results_service import ScenarioResultsService
from elaborations.services.sqlite.scenario_service import execute_scenario

router = APIRouter(prefix="/elaborations")

@router.post("/scenario")
async def insert_scenario_api(scenario_dto:CreateJsonPayloadDto):
    JsonFilesService.insert(JsonType.SCENARIO,scenario_dto)
    return {"message": "Scenario added"}

@router.put("/scenario")
async def update_scenario_api(scenario_dto:UpdateJsonPayloadDto):
    JsonFilesService.update(JsonType.SCENARIO,scenario_dto)
    return {"message": "Scenario updated"}

@router.get("/scenario")
async def find_all_scenarios_api()->list[str]:
    return JsonFilesService.get_codes_by_type(JsonType.SCENARIO)

@router.get("/scenario/{_id}")
async def find_scenario_api(_id:str):
    json_dto: JsonPayload = JsonFilesService.get_by_id(_id)
    if not json_dto:
        return {"message": f"No scenario found with id [ {_id} ]"}, 400
    return json.dumps(json_dto.payload)

@router.delete("/scenario/{_id}")
async def delete_scenario_api(_id: str):
    result = JsonFilesService.delete_by_id(_id)
    return {"message": f"{result} scenario(s) deleted"}

@router.get("/scenario/{_id}/execute")
async def execute_scenario_api(_id):
    execute_scenario(_id)
    return {"message": "Scenario started"}

@router.get("/scenario/{_id}/results")
async def find_all_scenario_results_api(_id:str):
    return ScenarioResultsService.get_results_by_scenario(_id)

@router.delete("/scenario/{_id}/results")
async def delete_all_scenario_result_api(_id:str):
    result = ScenarioResultsService.delete_by_scenario(_id)
    return {"message": f"{result} result(s) deleted"}

