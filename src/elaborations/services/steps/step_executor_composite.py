from elaborations.models.scenario import Scenario
from elaborations.models.steps import DataStepDTO, SleepStepDto, DataFromJsonArrayStepDto, \
    StepDto, StepDtoTypes
from elaborations.services.steps.data_from_json_array_step_executor import DataFromJsonArrayStepExecutor
from elaborations.services.steps.data_step_executor import DataStepExecutor
from elaborations.services.steps.sleep_step_executor import SleepStepExecutor
from elaborations.services.steps.step_executor import StepExecutor

_CONNECTOR_MAPPING: dict[type[StepDto], type[StepExecutor]] = {
    SleepStepDto: SleepStepExecutor,
    DataStepDTO: DataStepExecutor,
    DataFromJsonArrayStepDto:DataFromJsonArrayStepExecutor
}

def execute_step(scenario:Scenario, step:StepDtoTypes)->list[dict[str,str]]:
    executor_class = _CONNECTOR_MAPPING.get(type(step))
    if executor_class is None:
        supported_types = list(_CONNECTOR_MAPPING.keys())
        raise ValueError(
            f"Unsupported step type: {step.stepType}. "
            f"Supported types: {supported_types}"
        )
    step_executor = executor_class()
    return step_executor.execute(scenario, step)