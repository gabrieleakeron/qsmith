from abc import abstractmethod, ABC

from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDtoTypes


class StepExecutor(ABC):
    @abstractmethod
    def execute(self, scenario:Scenario, step:StepDtoTypes)->list[dict[str,str]]:
        pass




