import json

from fastapi import APIRouter

from _alembic.models.json_payload_entity import JsonPayloadEntity
from _alembic.services.session_context_manager import managed_session
from json_utils.models.dtos.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.dtos.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.models.enums.json_type import JsonType
from json_utils.services.alembic.json_files_service import JsonFilesService

router = APIRouter(prefix="/broker")

@router.post("/connection")
async def insert_broker_connection_api(dto: CreateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.insert(session,JsonPayloadEntity(
        code=dto.code,
        description=dto.description,
        json_type=JsonType.BROKER_CONNECTION,
        payload=json.dumps(dto.payload, ensure_ascii=True)
        ))
    return {"id":_id, "message": f"Broker connection [ {dto.code} ] added"}

@router.put("/connection")
async def update_broker_connection_api(dto: UpdateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.update(session, JsonPayloadEntity(
            id=dto.id,
            code=dto.code,
            description=dto.description,
            json_type=JsonType.BROKER_CONNECTION,
            payload=json.dumps(dto.payload, ensure_ascii=True)
        ))
    return {"message": f"Broker connection [ {dto.code} ] updated"}

@router.get("/connection")
async def find_all_broker_connections_api():
    with managed_session() as session:
        return JsonFilesService.get_all_by_type(session,JsonType.BROKER_CONNECTION)

@router.get("/connection/{_id}")
async def find_broker_connection_api(_id:str):
    with managed_session() as session:
        entity:JsonPayloadEntity = JsonFilesService.get_by_id(session, _id)
        if not entity:
            return {"message": f"No data found with id [ {_id} ]"}, 400
        return entity

@router.delete("/connection/{_id}")
async def delete_broker_connection_api(_id: str):
    with managed_session() as session:
        count = JsonFilesService.delete_by_id(session,_id)
        if count == 0:
            return {"message": f"No broker connection found with id [ {_id} ]"}
        return {"message": f"Broker connection deleted successfully"}

