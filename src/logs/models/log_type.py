from enum import Enum

class LogType(Enum):
    ELABORATION = "ELABORATION"
    SERVICE = "SERVICE"

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"