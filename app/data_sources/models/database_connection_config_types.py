from data_sources.models.postgres_connection_config import PostgresConnectionConfig

DatabaseConnectionConfigTypes = PostgresConnectionConfig

def convert_database_connection_config(config: dict) -> DatabaseConnectionConfigTypes:
    return PostgresConnectionConfig(**config)
