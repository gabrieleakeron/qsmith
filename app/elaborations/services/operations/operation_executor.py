from abc import abstractmethod, ABC

from pydantic.dataclasses import dataclass

from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.configuration_operation_dto import ConfigurationOperationTypes
from _alembic.models.log_entity import LogEntity
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService


@dataclass
class ExecutionResultDto:
    data: list[dict]
    result:list[dict[str,str]]
    def extend(self, new_result):
        self.data = new_result.data
        self.result.extend(new_result.result)

class OperationExecutor(ABC):
    @classmethod
    def log(cls,operation_id:str,message: str, payload: dict | list[dict] = None, level: LogLevel = LogLevel.INFO):
        with managed_session() as session:
            LogService.log(session,LogEntity(subject_type=LogSubjectType.OPERATION_EXECUTION,
                              subject=operation_id,
                              message=message,
                              payload=payload,
                              level=level
                              ))
    @abstractmethod
    def execute(self, operation_id:str, op:ConfigurationOperationTypes, data:list[dict])->ExecutionResultDto:
        pass




