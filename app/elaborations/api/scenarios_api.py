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
async def insert_scenario_api(scenario_dto:CreateScenarioDto):
    with managed_session() as session:
        scenario_id = ScenarioService.insert(
            session,
            ScenarioEntity(
                code = scenario_dto.code,
                description = scenario_dto.description
            )
        )
        for index, step in enumerate(scenario_dto.steps):
            scenario_step_id = ScenarioStepService.insert(
                session,
                ScenarioStepEntity(
                    scenario_id = scenario_id,
                    step_id = step.step_id,
                    order = index,
                    on_failure = step.on_failure
                )
            )
            for op_index, operation in enumerate(step.operations):
                StepOperationService.insert(
                    session,
                    StepOperationEntity(
                        scenario_step_id = scenario_step_id,
                        operation_id = operation.operation_id,
                        order = op_index
                    )
                )
    return {"id":scenario_id, "message": "Scenario added"}


@router.get("/scenario")
async def find_all_scenarios_api():
    with managed_session() as session:
        return ScenarioService.get_all(session)

@router.get("/scenario/{_id}")
async def find_scenario_api(_id:str):
    with managed_session() as session:
        scenario = ScenarioService.get_by_id(session, _id)
        if not scenario:
            raise QsmithAppException(f"No scenario found with id [ {_id} ]")
    return scenario

@router.delete("/scenario/{_id}")
async def delete_scenario_api(_id: str):
    with managed_session() as session:
        result = ScenarioService.delete_by_id(session,_id)
        if result == 0:
            raise QsmithAppException(f"No scenario found with id [ {_id} ]")
        return {"message": f"{result} scenario(s) deleted"}

@router.get("/scenario/{_id}/execute")
async def execute_scenario_api(_id):
    execute_scenario_by_id(_id)
    return {"message": "Scenario started"}



