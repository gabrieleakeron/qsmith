from fastapi import APIRouter

from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_scenario_dto import CreateScenarioStepDto, CreateStepOperationDto
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.alembic.step_operation_service import StepOperationService
from exceptions.app_exception import QsmithAppException

router = APIRouter(prefix="/elaborations")


@router.get("/scenario/step/{step_id}/operation")
async def find_all_by_step_api(step_id:str):
    with managed_session() as session:
        all = StepOperationService().get_all_by_step(session,step_id)
        results = []
        for step in all:
            results.append({
                "scenario_step_id": step.scenario_step_id,
                "operation_id": step.operation_id,
                "order": step.order
            })
        return results


@router.put("/scenario/step/{step_id}/operation")
async def insert_scenario_step_api(step_id: str, dto:CreateStepOperationDto):
    with managed_session() as session:
        entity = StepOperationEntity()
        entity.scenario_step_id = step_id
        entity.operation_id = dto.operation_id
        entity.order = dto.order
        step_operation_id = StepOperationService().insert(session,entity)
        return {"id": step_operation_id, "message": "Step operation added"}


@router.delete("/scenario/{scenario_id}/step")
async def delete_scenario_step_api(_id: str):
    with managed_session() as session:
        result = ScenarioService().delete_by_id(session, _id)
        if result == 0:
            raise QsmithAppException(f"No tep operation found with id [ {_id} ]")
        return {"message": f"{result} step operation(s) deleted"}

