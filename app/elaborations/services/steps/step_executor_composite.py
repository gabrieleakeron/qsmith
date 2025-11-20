import json

from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes, SleepConfigurationStepDto, DataConfigurationStepDTO, DataFromJsonArrayConfigurationStepDto, \
    DataFromDbConfigurationStepDto, DataFromQueueConfigurationStepDto
from _alembic.models.step_entity import StepEntity
from elaborations.services.alembic.step_service import StepService
from elaborations.services.steps.data_from_db_step_executor import DataFromDbStepExecutor
from elaborations.services.steps.data_from_json_array_step_executor import DataFromJsonArrayStepExecutor
from elaborations.services.steps.data_from_queue_step_executor import DataFromQueueStepExecutor
from elaborations.services.steps.data_step_executor import DataStepExecutor
from elaborations.services.steps.sleep_step_executor import SleepStepExecutor
from elaborations.services.steps.step_executor import StepExecutor
from exceptions.app_exception import QsmithAppException

_EXECUTOR_MAPPING: dict[type[ConfigurationStepDtoTypes], type[StepExecutor]] = {
    SleepConfigurationStepDto: SleepStepExecutor,
    DataConfigurationStepDTO: DataStepExecutor,
    DataFromJsonArrayConfigurationStepDto:DataFromJsonArrayStepExecutor,
    DataFromDbConfigurationStepDto:DataFromDbStepExecutor,
    DataFromQueueConfigurationStepDto:DataFromQueueStepExecutor
}

def execute_step(step_id:str)->list[dict[str,str]]:
    with managed_session() as session:
        step: StepEntity = StepService.get_by_id(session, step_id)
        if not step:
            raise QsmithAppException(f"Step with id '{step_id}' not found")

        cfg = ConfigurationStepDtoTypes.model_validate(json.load(step.configuration_json))

        clazz = _EXECUTOR_MAPPING.get(cfg)
        if clazz is None:
            supported_types = list(_EXECUTOR_MAPPING.keys())
            raise ValueError(
                f"Unsupported step type: {cfg}. "
                f"Supported types: {supported_types}"
            )
        step_executor = clazz()
        return step_executor.execute(step, cfg)


