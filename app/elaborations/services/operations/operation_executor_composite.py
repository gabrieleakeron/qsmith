from sqlalchemy.orm import Session

from _alembic.models.log_entity import LogEntity
from elaborations.models.dtos.configuration_operation_dto import ConfigurationOperationTypes, \
    PublishConfigurationOperationDto, SaveInternalDBConfigurationOperationDto, \
    SaveToExternalDBConfigurationOperationDto, convert_to_config_operation_type, ConfigurationOperationDto
from elaborations.services.alembic.operation_service import OperationService
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from elaborations.services.operations.publish_to_queue_operation_executor import PublishToQueueOperationExecutor
from elaborations.services.operations.save_to_external_db_operation_executor import SaveToExternalDbOperationExecutor
from elaborations.services.operations.save_to_internal_db_operation_executor import SaveInternalDbOperationExecutor
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService

_EXECUTOR_MAPPING: dict[type[ConfigurationOperationDto], type[OperationExecutor]] = {
    PublishConfigurationOperationDto: PublishToQueueOperationExecutor,
    SaveInternalDBConfigurationOperationDto: SaveInternalDbOperationExecutor,
    SaveToExternalDBConfigurationOperationDto: SaveToExternalDbOperationExecutor
}


def log(session,message: str,level: LogLevel = LogLevel.INFO):
    log_entity = LogEntity()
    log_entity.subject_type = LogSubjectType.OPERATION_EXECUTION,
    log_entity.subject='N/A'
    log_entity.message = message
    log_entity.level = level
    LogService().log(session, log_entity)


def execute_operations(session: Session, operation_ids: list[str], data: list[dict]) -> ExecutionResultDto:
    execution_result = ExecutionResultDto(data=data, result=[])

    log(session, f"Starting execution {len(operation_ids)} operations")

    for op_id in operation_ids:
        op_entity = OperationService().get_by_id(session, op_id)
        cfg = convert_to_config_operation_type(op_entity.configuration_json)
        new_execution_result = execute_operation(session, op_id, cfg, execution_result.data)
        execution_result.extend(new_execution_result)

    return execution_result


def execute_operation(session:Session, operation_id: str, cfg: ConfigurationOperationTypes, data: list[dict]) -> ExecutionResultDto:
    clazz = _EXECUTOR_MAPPING.get(type(cfg))
    if clazz is None:
        supported_types = list(_EXECUTOR_MAPPING.keys())
        message =  f"Unsupported operation type: {cfg}. "
        log(session, message, level=LogLevel.ERROR)
        raise ValueError(

            f"Supported types: {supported_types}"
        )
    operation_executor = clazz()
    return operation_executor.execute(session, operation_id, cfg, data)
