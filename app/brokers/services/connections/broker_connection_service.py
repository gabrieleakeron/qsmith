from abc import ABC, abstractmethod

from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.models.dto.create_queue_dto import CreateQueueDto


class BrokerConnectionService(ABC):
    @abstractmethod
    def create_queue(self, connection_config:BrokerConnectionConfigTypes, q: CreateQueueDto):
        pass

    @abstractmethod
    def delete_queue(self, connection_config:BrokerConnectionConfigTypes, queue_url: str):
        pass

    def list_queues(self, connection_config:BrokerConnectionConfigTypes):
        pass
