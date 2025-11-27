import json

from fastapi import APIRouter

from _alembic.models.operation_entity import OperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_operation_dto import CreateOperationDto
from elaborations.services.alembic.operation_service import OperationService
from exceptions.app_exception import QsmithAppException

router = APIRouter(prefix="/elaborations")

@router.post("/operation")
async def insert_operation_api(dto:CreateOperationDto):
    with managed_session() as session:
        entity = OperationEntity()
        entity.code = dto.code,
        entity.description = dto.description,
        entity.operation_type = dto.cfg.operationType,
        entity.configuration_json = dto.cfg
        op_id = OperationService().insert(
            session,
            entity
        )
    return {"id":op_id, "message": "Operation added"}


@router.get("/operation")
async def find_all_operation_api():
    with managed_session() as session:
        steps = OperationService().get_all(session)
        result= []
        for step in steps:
            result.append({
                "id": step.id,
                "code": step.code,
                "description": step.description,
                "operation_type": step.operation_type,
                "configuration_json": step.configuration_json
            })
        return result

@router.get("/operation/{_id}")
async def find_operation_by_id_api(_id:str):
    with managed_session() as session:
        step = OperationService().get_by_id(session, _id)
        if not step:
            raise QsmithAppException(f"No Operation found with id [ {_id} ]")
        return {
                "id": step.id,
                "code": step.code,
                "description": step.description,
                "operation_type": step.operation_type,
                "configuration_json": step.configuration_json
            }

@router.delete("/operation/{_id}")
async def delete_operation_by_id_api(_id: str):
    with managed_session() as session:
        result = OperationService().delete_by_id(session, _id)
        if result == 0:
            raise QsmithAppException(f"No Operation found with id [ {_id} ]")
        return {"message": f"{result} Operation(s) deleted"}


