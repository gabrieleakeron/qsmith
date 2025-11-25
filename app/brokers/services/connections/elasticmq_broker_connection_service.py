import boto3
from botocore.client import BaseClient

from brokers.models.connections.elastiqmq.broker_elasticmq_connection_config import BrokerElasticmqConnectionConfig
from brokers.services.connections.amazon_broker_connection_service import AmazonBrokerConnectionService

DEFAULT_VISIBILITY_TIMEOUT = 30


class ElasticmqBrokerConnectionService(AmazonBrokerConnectionService):
    def _client(self, config: BrokerElasticmqConnectionConfig)->BaseClient:
        return boto3.client(
            "sqs",
            region_name="region",
            endpoint_url=config.endpointUrl,
            aws_access_key_id="xxx",
            aws_secret_access_key="yyy",
        )
