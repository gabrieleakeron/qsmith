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
    query: str | None = None
    order_by: list[str] | None = None
    stream: bool = True
    chunk_size: int = 100

class DataFromQueueConfigurationStepDto(ConfigurationStepDto):
    stepType: str = StepType.DATA_FROM_QUEUE.value
    queue_id: str
    retry: int = 3
    wait_time_seconds: int = 20
    max_messages: int = 1000


ConfigurationStepDtoTypes = SleepConfigurationStepDto | DataConfigurationStepDTO |DataFromJsonArrayConfigurationStepDto | DataFromQueueConfigurationStepDto |DataFromDbConfigurationStepDto


def convert_to_config_step_type(data: dict):
    step_type = data.get("stepType")
    if step_type == StepType.SLEEP.value:
        return SleepConfigurationStepDto(
            duration=data.get("duration")
        )
    elif step_type == StepType.DATA.value:
        return DataConfigurationStepDTO(
            data=data.get("data")
        )
    elif step_type == StepType.DATA_FROM_JSON_ARRAY.value:
        return DataFromJsonArrayConfigurationStepDto(
            json_array_id=data.get("json_array_id")
        )
    elif step_type == StepType.DATA_FROM_DB.value:
        return DataFromDbConfigurationStepDto(
            connection_id=data.get("connection_id"),
            table_name=data.get("table_name"),
            query=data.get("query"),
            order_by=data.get("order_by"),
            chunk_size=data.get("chunk_size", 100)
        )
    elif step_type == StepType.DATA_FROM_QUEUE.value:
        return DataFromQueueConfigurationStepDto(
            queue_id=data.get("queue_id"),
            retry=data.get("retry", 3),
            wait_time_seconds=data.get("wait_time_seconds", 20),
            max_messages=data.get("max_messages", 1000)
        )
    else:
        raise ValueError(f"Unsupported step type: {step_type}")