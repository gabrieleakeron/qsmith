from datetime import time
from enum import Enum
from pydantic import BaseModel

class LogSubjectType(str,Enum):
    SCENARIO_EXECUTION = "SCENARIO_EXECUTION",
    STEP_EXECUTION = "STEP_EXECUTION",
    OPERATION_EXECUTION = "OPERATION_EXECUTION",
    SERVICE = "SERVICE"

class LogLevel(str,Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class LogDto(BaseModel):
    id: str | None = None
    subject_type: LogSubjectType = LogSubjectType.SERVICE
    subject:str
    level: LogLevel = LogLevel.INFO
    message: str
    payload: dict | list[dict] | None = None
    created_at: str | None = None
