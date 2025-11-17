from pydantic import BaseModel


class DatabaseConnectionConfig(BaseModel):
    database_type: str