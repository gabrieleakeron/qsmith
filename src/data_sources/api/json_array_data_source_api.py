import json

from fastapi import APIRouter

from exceptions.app_exception import QsmithAppException
from json_utils.models.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.models.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.sqlite.json_files_service import JsonFilesService

router = APIRouter(prefix="/data-source")

@router.post("/json-array")
async def insert_json_array_api(dto: CreateJsonPayloadDto):
    _id = JsonFilesService.insert(JsonType.JSON_ARRAY, dto)
    return {"id":_id, "message": f"Json array [ {dto.code} ] added"}

@router.put("/json-array")
async def update_json_array_api(dto: UpdateJsonPayloadDto):
    JsonFilesService.update(JsonType.JSON_ARRAY, dto)
    return {"message": f"Json array [ {dto.code} ] updated"}

@router.get("/json-array")
async def find_all_json_array_api():
    return JsonFilesService.get_all_by_type(JsonType.JSON_ARRAY)

@router.get("/json-array/{_id}")
async def find_json_array_api(_id:str):
    json_dto:JsonPayload = JsonFilesService.get_by_id(_id)
    if not json_dto:
        raise QsmithAppException(f"No data found with id [ {_id} ]")
    return json_dto

@router.delete("/json-array/{_id}")
async def delete_json_array_api(_id: str):
    json_dto: JsonPayload = JsonFilesService.get_by_id(_id)
    count = JsonFilesService.delete_by_id(_id)
    if count == 0:
        raise QsmithAppException(f"No Json array item found with id [ {_id} ]")
    return {"message": f"Json array item with code [ {json_dto.code} ] deleted successfully"}