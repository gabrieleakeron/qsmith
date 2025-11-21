from fastapi import APIRouter

from _alembic.services.session_context_manager import managed_session
from database.services.sqlalchemy.database_table_reader import DatabaseTableReader
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from database.services.alembic.database_connection_service import load_database_connection
from exceptions.app_exception import QsmithAppException
from json_utils.models.dtos.create_json_payload_dto import CreateJsonPayloadDto
from _alembic.models.json_payload_entity import JsonPayloadEntity
from json_utils.models.enums.json_type import JsonType
from json_utils.models.dtos.update_json_payload_dto import UpdateJsonPayloadDto
from json_utils.services.alembic.json_files_service import JsonFilesService

router = APIRouter(prefix="/database")

@router.post("/connection")
async def insert_database_connection_api(dto: CreateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.insert(session, JsonPayloadEntity(
            code=dto.code,
            description=dto.description,
            json_type=JsonType.DATABASE_CONNECTION,
            payload=dto.payload
        ))
    return {"id":_id,"message": "Database connection added"}

@router.put("/connection")
async def update_database_connection_api(dto: UpdateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService.update(session, JsonPayloadEntity(
            id=dto.id,
            code=dto.code,
            description=dto.description,
            json_type=JsonType.DATABASE_CONNECTION,
            payload=dto.payload
        ))
    return {"message": "Database connection updated"}

@router.get("/connection")
async def find_database_connections_api():
    with managed_session() as session:
        return JsonFilesService.get_all_by_type(session,JsonType.DATABASE_CONNECTION)

@router.get("/connection/{_id}")
async def get_database_connection_api(_id:str):
    with managed_session() as session:
        json_dto: JsonPayloadEntity = JsonFilesService.get_by_id(session,_id)
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
    with managed_session() as session:
        json_dto: JsonPayloadEntity = JsonFilesService.get_by_id(session,_id)
        count = JsonFilesService.delete_by_id(_id)
        if count == 0:
            raise QsmithAppException(f"No database connection found with id [ {_id} ]")
        return {"message": f"Database connection with code [ {json_dto.code} ] deleted successfully"}