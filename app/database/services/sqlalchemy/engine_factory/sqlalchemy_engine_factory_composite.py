from database.models.database_connection_config_types import DatabaseConnectionConfigTypes
from database.models.postgres_connection_config import PostgresConnectionConfig
from database.services.sqlalchemy.engine_factory.postgres_sqlalchemy_engine_factory import \
    PostgresSQLAlchemyEngineFactory
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory import SQLAlchemyEngineFactory

_CONNECTOR_MAPPING: dict[type[DatabaseConnectionConfigTypes], type[SQLAlchemyEngineFactory]] = {
    PostgresConnectionConfig: PostgresSQLAlchemyEngineFactory,
}

def create_sqlalchemy_engine(connection_cfg: DatabaseConnectionConfigTypes):
    factory_class = _CONNECTOR_MAPPING.get(type(connection_cfg))
    if factory_class is None:
        supported_types = list(_CONNECTOR_MAPPING.keys())
        raise ValueError(
            f"Unsupported sqlalchemy engine factory type: {connection_cfg}. "
            f"Supported types: {supported_types}"
        )
    factory_class = factory_class()
    return factory_class.create_engine(connection_cfg)