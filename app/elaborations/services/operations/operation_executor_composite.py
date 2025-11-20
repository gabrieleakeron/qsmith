from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.configuration_operation_dto import ConfigurationOperationTypes, PublishConfigurationOperationDto, SaveInternalDBConfigurationOperationDto, \
    SaveToExternalDBConfigurationOperationDto
from elaborations.services.alembic.operation_service import OperationService
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from elaborations.services.operations.publish_to_queue_operation_executor import PublishToQueueOperationExecutor
from elaborations.services.operations.save_to_external_db_operation_executor import SaveToExternalDbOperationExecutor
from elaborations.services.operations.save_to_internal_db_operation_executor import SaveInternalDbOperationExecutor

_EXECUTOR_MAPPING: dict[type[ConfigurationOperationTypes], type[OperationExecutor]] = {
    PublishConfigurationOperationDto: PublishToQueueOperationExecutor,
    SaveInternalDBConfigurationOperationDto: SaveInternalDbOperationExecutor,
    SaveToExternalDBConfigurationOperationDto: SaveToExternalDbOperationExecutor
}

def execute_operations(operation_ids:list[str], data:list[dict])->ExecutionResultDto:
    execution_result = ExecutionResultDto(data=data, result=[])

    with managed_session() as session:

        for op_id in operation_ids:
            op_entity = OperationService.get_by_id(session,op_id)
            cfg = ConfigurationOperationTypes.model_validate(op_entity.configuration_json)
            new_execution_result = execute_operation(op_id, cfg, execution_result.data)
            execution_result.extend(new_execution_result)

    return execution_result

def execute_operation(operation_id:str, cfg:ConfigurationOperationTypes, data:list[dict])->ExecutionResultDto:
    clazz = _EXECUTOR_MAPPING.get(cfg.__class__)
    if clazz is None:
        supported_types = list(_EXECUTOR_MAPPING.keys())
        raise ValueError(
            f"Unsupported operation type: {cfg}. "
            f"Supported types: {supported_types}"
        )
    operation_executor = clazz()
    return operation_executor.execute(operation_id, cfg, data)