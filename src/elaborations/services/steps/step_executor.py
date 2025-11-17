from abc import abstractmethod, ABC

from elaborations.models.operations import OperationTypes
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDtoTypes
from logs.models.logs import LogLevel, LogDto, LogSubjectType
from logs.services.sqlite.log_service import LogService


class StepExecutor(ABC):
    @classmethod
    def log(cls, step:StepDtoTypes, message: str, payload:dict|list[dict] = None, level: LogLevel = LogLevel.INFO):
        LogService.log(LogDto(subject_type=LogSubjectType.STEP_EXECUTION,
                              subject=step.code,
                              message=message,
                              payload=payload,
                              level=level
                              ))
    @abstractmethod
    def execute(self, scenario:Scenario, step:StepDtoTypes)->list[dict[str,str]]:
        pass




