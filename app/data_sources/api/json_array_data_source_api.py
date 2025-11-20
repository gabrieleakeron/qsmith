from fastapi import APIRouter

from _alembic.services.session_context_manager import managed_session
from exceptions.app_exception import QsmithAppException
from json_utils.models.dtos.create_json_payload_dto import CreateJsonPayloadDto
from _alembic.models.json_payload_entity import JsonPayloadEntity
from json_utils.models.enums.json_type import JsonType
from json_utils.models.dtos.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.alembic.json_files_service import JsonFilesService

router = APIRouter(prefix="/data-source")

@router.post("/json-array")
async def insert_json_array_api(dto: CreateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.insert(session, JsonPayloadEntity(
            code=dto.code,
            description=dto.description,
            json_type=JsonType.JSON_ARRAY,
            payload=dto.payload
        ))
    return {"id":_id, "message": f"Json array [ {dto.code} ] added"}

@router.put("/json-array")
async def update_json_array_api(dto: UpdateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.update(session, JsonPayloadEntity(
            id=dto.id,
            code=dto.code,
            description=dto.description,
            json_type=JsonType.JSON_ARRAY,
            payload=dto.payload
        ))
    return {"message": f"Json array [ {dto.code} ] updated"}

@router.get("/json-array")
async def find_all_json_array_api():
    with managed_session() as session:
        return JsonFilesService.get_all_by_type(session, JsonType.JSON_ARRAY)

@router.get("/json-array/{_id}")
async def find_json_array_api(_id:str):
    with managed_session() as session:
        json_dto:JsonPayloadEntity = JsonFilesService.get_by_id(session,_id)
        if not json_dto:
            raise QsmithAppException(f"No data found with id [ {_id} ]")
        return json_dto

@router.delete("/json-array/{_id}")
async def delete_json_array_api(_id: str):
    with managed_session() as session:
        json_dto: JsonPayloadEntity = JsonFilesService.get_by_id(session,_id)
        count = JsonFilesService.delete_by_id(_id)
        if count == 0:
            raise QsmithAppException(f"No Json array item found with id [ {_id} ]")
        return {"message": f"Json array item with code [ {json_dto.code} ] deleted successfully"}