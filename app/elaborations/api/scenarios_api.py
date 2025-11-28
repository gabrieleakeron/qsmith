from fastapi import APIRouter

from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_scenario_dto import CreateScenarioDto
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.scenarios.scenario_dto_service import insert_scenario
from elaborations.services.scenarios.scenario_executor_service import execute_scenario_by_id
from exceptions.app_exception import QsmithAppException

router = APIRouter(prefix="/elaborations")


@router.post("/scenario")
async def insert_scenario_api(scenario_dto: CreateScenarioDto):
    scenario_id = insert_scenario(scenario_dto)
    return {"id": scenario_id, "message": "Scenario added"}


@router.get("/scenario")
async def find_all_scenarios_api():
    with managed_session() as session:
        all = ScenarioService().get_all(session)
        results = []
        for scenario in all:
            results.append({
                "id": scenario.id,
                "code": scenario.code,
                "description": scenario.description
            })
        return results


@router.get("/scenario/{_id}")
async def find_scenario_api(_id: str):
    with managed_session() as session:
        scenario = ScenarioService().get_by_id(session, _id)
        if not scenario:
            raise QsmithAppException(f"No scenario found with id [ {_id} ]")
        return {
            "id": scenario.id,
            "code": scenario.code,
            "description": scenario.description
        }


@router.delete("/scenario/{_id}")
async def delete_scenario_api(_id: str):
    with managed_session() as session:
        result = ScenarioService().delete_by_id(session, _id)
        if result == 0:
            raise QsmithAppException(f"No scenario found with id [ {_id} ]")
        return {"message": f"{result} scenario(s) deleted"}


@router.get("/scenario/{_id}/execute")
async def execute_scenario_api(_id):
    execute_scenario_by_id(_id)
    return {"message": "Scenario started"}
