from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from json_utils.models.json_payload import JsonPayload
from json_utils.services.sqlite.json_files_service import JsonFilesService


def load_broker_connection(_id: str):

    json_dto:JsonPayload = JsonFilesService.get_by_id(_id)

    if not json_dto:
        raise ValueError(f"Broker connection '{_id}' not found")

    return BrokerConnectionConfigTypes.model_validate(json_dto.payload)