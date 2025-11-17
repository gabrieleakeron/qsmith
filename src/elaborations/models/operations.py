from pydantic import BaseModel

class OperationDto(BaseModel):
    operationType: str

class PublishOperationDto(OperationDto):
    operationType: str = "publish"
    queue_id:str

class SaveInternalDBOperationDto(OperationDto):
    operationType: str = "save-internal-db"

class SaveToExternalDBOperationDto(OperationDto):
    operationType: str = "save-external-db"
    connection_id: str
    table_name: str

OperationTypes = PublishOperationDto | SaveInternalDBOperationDto | SaveToExternalDBOperationDto
