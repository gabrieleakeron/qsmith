from fastapi import APIRouter

from _alembic.services.session_context_manager import managed_session
from sqlalchemy_utils.database_table_reader import DatabaseTableReader
from sqlalchemy_utils.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from data_sources.services.alembic.database_connection_service import load_database_connection
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
        entity = JsonPayloadEntity()
        entity.code = dto.code
        entity.description = dto.description
        entity.json_type = JsonType.DATABASE_CONNECTION.value
        entity.payload = dto.payload
        _id = JsonFilesService().insert(session, entity)
    return {"id":_id,"message": "Database connection added"}

@router.put("/connection")
async def update_database_connection_api(dto: UpdateJsonPayloadDto):
    with managed_session() as session:
        _id = JsonFilesService().update(session, dto.id,
                                        code=dto.code,
                                        description=dto.description,
                                        json_type=JsonType.DATABASE_CONNECTION.value,
                                        payload=dto.payload)
    return {"message": "Database connection updated"}

@router.get("/connection")
async def find_database_connections_api():
    result = []
    with managed_session() as session:
        all =  JsonFilesService().get_all_by_type(session,JsonType.DATABASE_CONNECTION)
        for data in all:
            result.append({
                "id": data.id,
                "code": data.code,
                "description": data.description,
                "payload": data.payload
            })
    return result

@router.get("/connection/{_id}")
async def find_database_connection_by_id_api(_id:str):
    with managed_session() as session:
        entity: JsonPayloadEntity = JsonFilesService().get_by_id(session,_id)
        if not entity:
            raise QsmithAppException(f"No database connection found with id [ {_id} ]")
        return {
            "id": entity.id,
            "code": entity.code,
            "description": entity.description,
            "payload": entity.payload
        }

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
        count = JsonFilesService().delete_by_id(session,_id)
        if count == 0:
            raise QsmithAppException(f"No database connection found with id [ {_id} ]")
        return {"message": f"Database connection deleted successfully"}