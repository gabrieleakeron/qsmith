from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.alembic.broker_connection_service import load_broker_connection
from brokers.services.alembic.queue_service import QueueService
from brokers.services.connections.queue.queue_connection_service_factory import QueueConnectionServiceFactory
from elaborations.models.dtos.configuration_operation_dto import PublishConfigurationOperationDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto


class PublishToQueueOperationExecutor(OperationExecutor):
    def execute(self, operation_id:str, cfg: PublishConfigurationOperationDto, data:list[dict])->ExecutionResultDto:
        queue = QueueService.get_by_id(cfg.queue_id)
        connection_config: BrokerConnectionConfigTypes = load_broker_connection(queue.broker_id)
        service = QueueConnectionServiceFactory().get_service(connection_config)
        messages = service.publish_messages(connection_config, cfg.queue_id, data)
        message=f"Published {len(messages)} message(s) to queue '{queue.code}'"
        self.log(operation_id, message=message, payload=messages)
        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
