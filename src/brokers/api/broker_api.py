from fastapi import APIRouter

from json_utils.models.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.models.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.sqlite.json_files_service import JsonFilesService

router = APIRouter(prefix="/broker")

@router.post("/connection")
async def insert_broker_connection_api(dto: CreateJsonPayloadDto):
    _id = JsonFilesService.insert(JsonType.BROKER_CONNECTION, dto)
    return {"id":_id, "message": f"Broker connection [ {dto.code} ] added"}

@router.put("/connection")
async def update_broker_connection_api(dto: UpdateJsonPayloadDto):
    JsonFilesService.update(JsonType.BROKER_CONNECTION, dto)
    return {"message": f"Broker connection [ {dto.code} ] updated"}

@router.get("/connection")
async def find_all_broker_connections_api():
    return JsonFilesService.get_all_by_type(JsonType.BROKER_CONNECTION)

@router.get("/connection/{_id}")
async def find_broker_connection_api(_id:str):
    json_dto:JsonPayload = JsonFilesService.get_by_id(_id)
    if not json_dto:
        return {"message": f"No data found with id [ {_id} ]"}, 400
    return json_dto

@router.delete("/connection/{_id}")
async def delete_broker_connection_api(_id: str):
    json_dto: JsonPayload = JsonFilesService.get_by_id(_id)
    count = JsonFilesService.delete_by_id(_id)
    if count == 0:
        return {"message": f"No broker connection found with id [ {_id} ]"}
    return {"message": f"Broker connection with code [ {json_dto.code} ] deleted successfully"}

