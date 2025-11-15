from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.sqllite.broker_connection_service import load_broker_connection
from elaborations.models.operations import PublishOperationDto
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from elaborations.services.operations.operation_executor import OperationExecutor
from brokers.services.connections.queue.queue_connection_service_factory import QueueConnectionServiceFactory


class PublishToQueueOperationExecutor(OperationExecutor):
    def execute(self, scenario:Scenario, step:StepDto, operation: PublishOperationDto, data:list[dict]):
        connection_config: BrokerConnectionConfigTypes = load_broker_connection(operation.connectionConfig)
        service = QueueConnectionServiceFactory().get_service(connection_config)
        return service.publish_messages(connection_config,operation.queue,data)
