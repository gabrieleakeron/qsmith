import json

from fastapi import APIRouter

from _alembic.models.step_entity import StepEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_step_dto import CreateStepDto
from elaborations.services.alembic.step_service import StepService
from exceptions.app_exception import QsmithAppException

router = APIRouter(prefix="/elaborations")

@router.post("/step")
async def insert_step_api(dto:CreateStepDto):
    with managed_session() as session:
        step_id = StepService.insert(
            session,
            StepEntity(
                code=dto.code,
                description=dto.description,
                step_type=dto.cfg.stepType,
                configuration_json=json.dumps(dto.cfg, ensure_ascii=True)
            )
        )

    return {"id":step_id, "message": "Step added"}


@router.get("/step")
async def find_all_step_api():
    with managed_session() as session:
        steps = StepService.get_all(session)
        return steps

@router.get("/step/{_id}")
async def find_step_by_id_api(_id:str):
    with managed_session() as session:
        step = StepService.get_by_id(session, _id)
        if not step:
            raise QsmithAppException(f"No step found with id [ {_id} ]")
        return step

@router.delete("/step/{_id}")
async def delete_step_by_id_api(_id: str):
    with managed_session() as session:
        result = StepService.delete_by_id(session, _id)
        if result == 0:
            raise QsmithAppException(f"No step found with id [ {_id} ]")
        return {"message": f"{result} step(s) deleted"}


