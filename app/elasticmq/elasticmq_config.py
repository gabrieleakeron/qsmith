from _alembic.services.session_context_manager import managed_session
from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.services.connections.broker_connection_service_factory import BrokerConnectionServiceFactory

from brokers.services.alembic.queue_service import QueueService
from _alembic.models.json_payload_entity import JsonPayloadEntity
from json_utils.models.enums.json_type import JsonType
from json_utils.services.alembic.json_files_service import JsonFilesService


def init_elasticmq():
    with managed_session() as session:
        brokers : list[JsonPayloadEntity] = JsonFilesService.get_all_by_type(session,JsonType.BROKER_CONNECTION)
        for b in brokers:
            queues = QueueService.get_all_by_broker_id(session, b.id)
            brokers_connection: BrokerConnectionConfigTypes = BrokerConnectionConfigTypes.model_validate(b.payload)
            service = BrokerConnectionServiceFactory.get_service(brokers_connection)
            for q in queues:
                service.create_queue(brokers_connection, q)