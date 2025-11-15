from abc import abstractmethod, ABC

from pydantic.dataclasses import dataclass

from elaborations.models.operations import OperationTypes
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto

@dataclass
class ExecutionResultDto:
    data: list[dict]
    result:list[dict[str,str]]
    def extend(self, new_result):
        self.data = new_result.data
        self.result.extend(new_result.result)

class OperationExecutor(ABC):
    @abstractmethod
    def execute(self, scenario:Scenario, step:StepDto, op:OperationTypes, data:list[dict])->ExecutionResultDto:
        pass




