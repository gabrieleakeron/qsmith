
from sqlalchemy.orm import Session

from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_entity import StepEntity
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes, SleepConfigurationStepDto, \
    DataConfigurationStepDTO, DataFromJsonArrayConfigurationStepDto, \
    DataFromDbConfigurationStepDto, DataFromQueueConfigurationStepDto, convert_to_config_step_type, ConfigurationStepDto
from elaborations.services.alembic.step_service import StepService
from elaborations.services.steps.data_from_db_step_executor import DataFromDbStepExecutor
from elaborations.services.steps.data_from_json_array_step_executor import DataFromJsonArrayStepExecutor
from elaborations.services.steps.data_from_queue_step_executor import DataFromQueueStepExecutor
from elaborations.services.steps.data_step_executor import DataStepExecutor
from elaborations.services.steps.sleep_step_executor import SleepStepExecutor
from elaborations.services.steps.step_executor import StepExecutor
from exceptions.app_exception import QsmithAppException

_EXECUTOR_MAPPING: dict[type[ConfigurationStepDto], type[StepExecutor]] = {
    SleepConfigurationStepDto: SleepStepExecutor,
    DataConfigurationStepDTO: DataStepExecutor,
    DataFromJsonArrayConfigurationStepDto: DataFromJsonArrayStepExecutor,
    DataFromDbConfigurationStepDto: DataFromDbStepExecutor,
    DataFromQueueConfigurationStepDto: DataFromQueueStepExecutor
}


def execute_step(session: Session, scenario_step:ScenarioStepEntity) -> list[dict[str, str]]:
    step: StepEntity = StepService().get_by_id(session, scenario_step.step_id)
    if not step:
        raise QsmithAppException(f"Step with id '{scenario_step.step_id}' not found")

    cfg = convert_to_config_step_type(step.configuration_json)

    clazz = _EXECUTOR_MAPPING.get(type(cfg))
    if clazz is None:
        supported_types = list(_EXECUTOR_MAPPING.keys())
        raise ValueError(
            f"Unsupported step type: {cfg}. "
            f"Supported types: {supported_types}"
        )
    step_executor = clazz()
    return step_executor.execute(session,scenario_step, step, cfg)
