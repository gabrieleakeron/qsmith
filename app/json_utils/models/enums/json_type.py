from enum import Enum


class JsonType(str,Enum):
    BROKER_CONNECTION = "broker-connection"
    DATABASE_CONNECTION = "database-connection"
    SCENARIO = "scenario"
    JSON_ARRAY = "json-array"