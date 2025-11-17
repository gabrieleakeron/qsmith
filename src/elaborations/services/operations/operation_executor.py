from abc import abstractmethod, ABC

from pydantic.dataclasses import dataclass

from elaborations.models.operations import OperationTypes
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from logs.models.logs import LogLevel, LogSubjectType, LogDto
from logs.services.sqlite.log_service import LogService

@dataclass
class ExecutionResultDto:
    data: list[dict]
    result:list[dict[str,str]]
    def extend(self, new_result):
        self.data = new_result.data
        self.result.extend(new_result.result)

class OperationExecutor(ABC):

    @classmethod
    def log(cls, operation: OperationTypes, message: str, payload:dict|list[dict] = None, level: LogLevel = LogLevel.INFO):
        LogService.log(LogDto(subject_type=LogSubjectType.OPERATION_EXECUTION,
                              subject=operation.operationType,
                              message=message,
                              payload=payload,
                              level=level
                              ))
    @abstractmethod
    def execute(self, scenario:Scenario, step:StepDto, op:OperationTypes, data:list[dict])->ExecutionResultDto:
        pass




