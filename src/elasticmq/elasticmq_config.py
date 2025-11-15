from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.connections.broker_connection_service_factory import BrokerConnectionServiceFactory

from brokers.services.sqllite.queue_service import QueueService
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.services.sqlite.json_files_service import JsonFilesService


def init_elasticmq():
    brokers : list[JsonPayload] = JsonFilesService.get_all_by_type(JsonType.BROKER_CONNECTION)
    for b in brokers:
        queues = QueueService.get_all_by_broker(b.id)
        brokers_connection:BrokerConnectionConfigTypes = BrokerConnectionConfigTypes.model_validate(b.payload)
        service = BrokerConnectionServiceFactory.get_service(brokers_connection)
        for q in queues:
            service.create_queue(brokers_connection,q)

