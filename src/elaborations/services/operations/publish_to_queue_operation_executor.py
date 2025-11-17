from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.sqllite.broker_connection_service import load_broker_connection
from brokers.services.sqllite.queue_service import QueueService
from elaborations.models.operations import PublishOperationDto
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from brokers.services.connections.queue.queue_connection_service_factory import QueueConnectionServiceFactory


class PublishToQueueOperationExecutor(OperationExecutor):
    def execute(self, scenario:Scenario, step:StepDto, operation: PublishOperationDto, data:list[dict])->ExecutionResultDto:
        queue = QueueService.get_by_id(operation.queue_id)
        connection_config: BrokerConnectionConfigTypes = load_broker_connection(queue.broker_id)
        service = QueueConnectionServiceFactory().get_service(connection_config)
        messages = service.publish_messages(connection_config, operation.queue_id, data)
        message=f"Published {len(messages)} message(s) to queue '{queue.code}'"
        self.log(operation,message=message , payload=messages)
        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
