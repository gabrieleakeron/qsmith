from abc import ABC, abstractmethod
from typing import Any

from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes


class QueueConnectionService(ABC):

    @abstractmethod
    def test_connection(self, broker_connection_config:BrokerConnectionConfigTypes,queue_id:str) -> bool:
        pass

    @abstractmethod
    def publish_messages(
            self,
            broker_connection_config:BrokerConnectionConfigTypes,
            queue_id:str,
            messages: list[Any]) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def receive_messages(
            self,
            broker_connection_config:BrokerConnectionConfigTypes,
            queue_id:str,
            max_messages: int = 10,
    ) -> list[Any]:
        pass

    @abstractmethod
    def ack_messages(
            self,
            broker_connection_config:BrokerConnectionConfigTypes,
            queue_id:str,
            messages: list[Any]
    ) -> list[dict]:
        pass

