from elaborations.models.operations import OperationTypes, PublishOperationDto, SaveInternalDBOperationDto, \
    SaveToExternalDBOperationDto
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDtoTypes
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from elaborations.services.operations.publish_to_queue_operation_executor import PublishToQueueOperationExecutor
from elaborations.services.operations.save_to_external_db_operation_executor import SaveToExternalDbOperationExecutor
from elaborations.services.operations.save_to_internal_db_operation_executor import SaveInternalDbOperationExecutor

_CONNECTOR_MAPPING: dict[type[OperationTypes], type[OperationExecutor]] = {
    PublishOperationDto: PublishToQueueOperationExecutor,
    SaveInternalDBOperationDto: SaveInternalDbOperationExecutor,
    SaveToExternalDBOperationDto: SaveToExternalDbOperationExecutor
}

def execute_operations(scenario:Scenario, step:StepDtoTypes, operations:list[OperationTypes], data:list[dict])->ExecutionResultDto:
    execution_result = ExecutionResultDto(data=data, result=[])

    for op in operations:
        new_execution_result = execute_operation(scenario, step, op, execution_result.data)
        execution_result.extend(new_execution_result)

    return execution_result

def execute_operation(scenario:Scenario, step:StepDtoTypes, op:OperationTypes, data:list[dict])->ExecutionResultDto:
    executor_class = _CONNECTOR_MAPPING.get(op.__class__)
    if executor_class is None:
        supported_types = list(_CONNECTOR_MAPPING.keys())
        raise ValueError(
            f"Unsupported operation type: {op}. "
            f"Supported types: {supported_types}"
        )
    operation_executor = executor_class()
    return operation_executor.execute(scenario, step, op, data)