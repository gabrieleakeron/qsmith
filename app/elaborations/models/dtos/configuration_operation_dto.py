from pydantic import BaseModel

from elaborations.models.enums.operation_type import OperationType


class ConfigurationOperationDto(BaseModel):
    operationType: str

class PublishConfigurationOperationDto(ConfigurationOperationDto):
    operationType: str = OperationType.PUBLISH.value
    queue_id:str

class SaveInternalDBConfigurationOperationDto(ConfigurationOperationDto):
    operationType: str = OperationType.SAVE_INTERNAL_DB.value
    table_name: str

class SaveToExternalDBConfigurationOperationDto(ConfigurationOperationDto):
    operationType: str = OperationType.SAVE_EXTERNAL_DB.value
    connection_id: str
    table_name: str

ConfigurationOperationTypes = PublishConfigurationOperationDto | SaveInternalDBConfigurationOperationDto | SaveToExternalDBConfigurationOperationDto
