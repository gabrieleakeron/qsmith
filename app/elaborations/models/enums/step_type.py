from enum import Enum


class StepType(str,Enum):
    SLEEP = "sleep"
    DATA_FROM_JSON_ARRAY = "data-from-json-array"
    DATA = "data"
    DATA_FROM_DB = "data-from-db"
    DATA_FROM_QUEUE = "data-from-queue"