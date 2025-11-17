from enum import Enum

from pydantic import BaseModel

from elaborations.models.operations import OperationTypes

class OnFailure(Enum):
    CONTINUE = "CONTINUE"
    ABORT = "ABORT"

class StepDto(BaseModel):
    stepType: str
    code: str
    description: str
    on_failure: OnFailure = OnFailure.ABORT

class SleepStepDto(StepDto):
    stepType: str = "sleep"
    duration: int

class DataFromJsonArrayStepDto(StepDto):
    stepType: str = "data-from-json-array"
    json_array_id: str
    operations: list[OperationTypes]

class DataStepDTO(StepDto):
    stepType: str = "data"
    data: list[dict]
    operations: list[OperationTypes]

class DataFromDbStepDto(StepDto):
    stepType: str = "data-from-db"
    connection_id: str
    table_name: str
    order_by: list[str]
    page_size: int = 100
    operations: list[OperationTypes]

class DataFromQueueStepDto(StepDto):
    stepType: str = "data-from-queue"
    queue_id: str
    retry: int = 3
    wait_time_seconds: int = 20
    max_messages: int = 1000
    operations: list[OperationTypes]

StepDtoTypes = SleepStepDto | DataStepDTO | DataFromJsonArrayStepDto | DataFromQueueStepDto | DataFromDbStepDto