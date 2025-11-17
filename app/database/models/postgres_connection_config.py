from database.models.database_connection_config import DatabaseConnectionConfig
from database.models.db_type import DbType


class PostgresConnectionConfig(DatabaseConnectionConfig):
    database_type: str  = DbType.POSTGRES
    host: str
    port: int = 5432
    database: str
    db_schema:str
    user: str
    password: str

