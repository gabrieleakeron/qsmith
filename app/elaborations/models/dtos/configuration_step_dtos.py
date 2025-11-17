from pydantic import BaseModel

from elaborations.models.enums.step_type import StepType


class ConfigurationStepDto(BaseModel):
    stepType: str

class SleepConfigurationStepDto(ConfigurationStepDto):
    stepType: str = StepType.SLEEP.value
    duration: int

class DataFromJsonArrayConfigurationStepDto(ConfigurationStepDto):
    stepType: str = StepType.DATA_FROM_JSON_ARRAY.value
    json_array_id: str

class DataConfigurationStepDTO(ConfigurationStepDto):
    stepType: str = StepType.DATA.value
    data: list[dict]

class DataFromDbConfigurationStepDto(ConfigurationStepDto):
    stepType: str = StepType.DATA_FROM_DB.value
    connection_id: str
    table_name: str
    order_by: list[str]
    page_size: int = 100

class DataFromQueueConfigurationStepDto(ConfigurationStepDto):
    stepType: str = StepType.DATA_FROM_QUEUE.value
    queue_id: str
    retry: int = 3
    wait_time_seconds: int = 20
    max_messages: int = 1000

ConfigurationStepDtoTypes = SleepConfigurationStepDto | DataConfigurationStepDTO |DataFromJsonArrayConfigurationStepDto | DataFromQueueConfigurationStepDto |DataFromDbConfigurationStepDto