from database.models.database_connection_config_types import DatabaseConnectionConfigTypes
from database.models.db_type import DbType
from database.models.postgres_connection_config import PostgresConnectionConfig
from json_utils.services.sqlite.json_files_service import JsonFilesService

_CONNECTION_MAPPING:dict[str, type[DatabaseConnectionConfigTypes]] = {
    DbType.POSTGRES: PostgresConnectionConfig
}


def load_database_connection(_id: str)->DatabaseConnectionConfigTypes:
    json_payload = JsonFilesService.get_by_id(_id)

    if not json_payload:
        raise ValueError(f"Database connection '{_id}' not found")

    config_class = _CONNECTION_MAPPING.get(json_payload.payload.get("database_type"))

    if not config_class:
        raise ValueError(f"Unsupported database connection type: {json_payload.payload.get('database_type')}")

    return config_class.model_validate(json_payload.payload)