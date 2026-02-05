from fastapi import APIRouter

from _alembic.models.scenario_entity import ScenarioEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_scenario_dto import CreateScenarioDto
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.alembic.step_operation_service import StepOperationService
from elaborations.services.scenarios.scenario_executor_service import execute_scenario_by_id
from exceptions.app_exception import QsmithAppException

router = APIRouter(prefix="/elaborations")


@router.post("/scenario")
async def insert_scenario_api(scenario_dto: CreateScenarioDto):
    with managed_session() as session:
        scenario_entity = ScenarioEntity()
        scenario_entity.code = scenario_dto.code
        scenario_entity.description = scenario_dto.description
        scenario_id = ScenarioService().insert(session, scenario_entity)
        for step in scenario_dto.steps:
            sse = ScenarioStepEntity()
            sse.order = step.order
            sse.scenario_id = scenario_id
            sse.step_id = step.step_id
            sse.on_failure = step.on_failure
            scenario_step_id= ScenarioStepService().insert(session,sse)
            for operation in step.operations:
                op_entity = StepOperationEntity()
                op_entity.order = operation.order
                op_entity.scenario_step_id = scenario_step_id
                op_entity.operation_id = operation.operation_id
                StepOperationService().insert(session,op_entity)
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
