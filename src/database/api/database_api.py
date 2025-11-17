import json

from fastapi import APIRouter

from database.services.sqlalchemy.database_table_reader import DatabaseTableReader
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory import SQLAlchemyEngineFactory
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from database.services.sqlite.database_connection_service import load_database_connection
from exceptions.app_exception import QsmithAppException
from json_utils.models.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.models.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.sqlite.json_files_service import JsonFilesService

router = APIRouter(prefix="/database")

@router.post("/connection")
async def insert_database_connection_api(database_dto: CreateJsonPayloadDto):
    _id = JsonFilesService.insert(JsonType.DATABASE_CONNECTION, database_dto)
    return {"id":_id,"message": "Database connection added"}

@router.put("/connection")
async def update_database_connection_api(database_dto: UpdateJsonPayloadDto):
    JsonFilesService.update(JsonType.DATABASE_CONNECTION,database_dto)
    return {"message": "Database connection updated"}

@router.get("/connection")
async def get_database_connections_api():
    return JsonFilesService.get_all_by_type(JsonType.DATABASE_CONNECTION)

@router.get("/connection/{_id}")
async def get_database_connection_api(_id:str):
    json_dto: JsonPayload = JsonFilesService.get_by_id(_id)
    if not json_dto:
        raise QsmithAppException(f"No database connection found with id [ {_id} ]")
    return json_dto

@router.get("/connection/{_id}/test")
async def test_database_connection_api(_id: str):
    connection = load_database_connection(_id)
    if not connection:
        raise QsmithAppException(f"No database connection found with id [ {_id} ]")

    engine = create_sqlalchemy_engine(connection)

    if DatabaseTableReader.test_connection(engine):
        return {"message": "Connection successful"}

    return {"message": "Connection failed"}

@router.delete("/connection/{_id}")
async def delete_database_connection_api(_id: str):
    json_dto: JsonPayload = JsonFilesService.get_by_id(_id)
    count = JsonFilesService.delete_by_id(_id)
    if count == 0:
        raise QsmithAppException(f"No database connection found with id [ {_id} ]")
    return {"message": f"Database connection with code [ {json_dto.code} ] deleted successfully"}