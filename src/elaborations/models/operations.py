from pydantic import BaseModel

class OperationDto(BaseModel):
    operationType: str

class PublishOperationDto(OperationDto):
    operationType: str = "publish"
    connectionConfig: str
    queue:str

class SaveInternalDBOperationDto(OperationDto):
    operationType: str = "save-internal-db"

class SaveToExternalDBOperationDto(OperationDto):
    operationType: str = "save-external-db"
    connectionConfig: str
    table_name: str

OperationTypes = PublishOperationDto | SaveInternalDBOperationDto | SaveToExternalDBOperationDto
