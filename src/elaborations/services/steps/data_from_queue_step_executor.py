from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.sqllite.broker_connection_service import load_broker_connection
from brokers.services.sqllite.queue_service import QueueService
from elaborations.models.scenario import Scenario
from elaborations.models.steps import DataFromQueueStepDto
from brokers.services.connections.queue.queue_connection_service_factory import QueueConnectionServiceFactory
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor
import time


class DataFromQueueStepExecutor(StepExecutor):

    def execute(self, scenario:Scenario, step: DataFromQueueStepDto) -> list[dict[str, str]]:

        queue = QueueService.get_by_id(step.queue_id)
        broker_connection:BrokerConnectionConfigTypes = load_broker_connection(queue.broker_id)
        service = QueueConnectionServiceFactory.get_service(broker_connection)

        retry = step.retry
        wait_time_seconds = step.wait_time_seconds
        max_messages = step.max_messages

        all_msgs = []

        while self.work_is_not_finished(all_msgs, max_messages, retry):

            msgs = service.receive_messages(broker_connection, queue_id=step.queue_id)

            if len(msgs) == 0:
                time.sleep(wait_time_seconds)
                retry -= 1
                continue

            all_msgs.extend(msgs)

            service.ack_messages(broker_connection, queue_id=step.queue_id, messages=msgs)

        self.log(step, f"Try to export {len(all_msgs)} messages read from queue '{queue.code}'")

        return execute_operations(scenario, step, step.operations, all_msgs).result

    @staticmethod
    def work_is_not_finished(all_msgs, max_messages, retry):
        right_size = len(all_msgs) == 0 and len(all_msgs)< max_messages
        return  retry > 0 and right_size