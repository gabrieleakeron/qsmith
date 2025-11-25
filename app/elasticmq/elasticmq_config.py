from _alembic.models.json_payload_entity import JsonPayloadEntity
from _alembic.services.session_context_manager import managed_session
from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes, \
    convert_to_broker_connection_config
from brokers.models.dto.create_queue_dto import CreateQueueDto
from brokers.models.dto.queue_configuration_dto import QueueConfigurationDto
from brokers.services.alembic.queue_service import QueueService
from brokers.services.connections.broker_connection_service_factory import BrokerConnectionServiceFactory
from json_utils.models.enums.json_type import JsonType
from json_utils.services.alembic.json_files_service import JsonFilesService


def init_elasticmq():
    with managed_session() as session:
        brokers : list[JsonPayloadEntity] = JsonFilesService().get_all_by_type(session,JsonType.BROKER_CONNECTION)
        for b in brokers:
            queues = QueueService().get_all_by_broker_id(session, b.id)
            brokers_connection: BrokerConnectionConfigTypes = convert_to_broker_connection_config(b.payload)
            service = BrokerConnectionServiceFactory.get_service(brokers_connection)
            for queue_entity in queues:
                cfg_dto = QueueConfigurationDto.model_validate(queue_entity.configuration_json)
                service.create_queue(brokers_connection, CreateQueueDto(
                    code=queue_entity.code,
                    description=queue_entity.description,
                    fifoQueue=cfg_dto.fifoQueue,
                    contentBasedDeduplication=cfg_dto.contentBasedDeduplication,
                    defaultVisibilityTimeout=cfg_dto.defaultVisibilityTimeout,
                    delay=cfg_dto.delay,
                    receiveMessageWait=cfg_dto.receiveMessageWait
                ))