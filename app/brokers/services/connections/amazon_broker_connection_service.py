import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from brokers.models.connections.amazon.broker_amazon_connection_config import BrokerAmazonConnectionConfig
from brokers.models.dto.create_queue_dto import CreateQueueDto
from brokers.services.connections.broker_connection_service import BrokerConnectionService

DEFAULT_VISIBILITY_TIMEOUT = 30


class AmazonBrokerConnectionService(BrokerConnectionService):
    def _client(self, config: BrokerAmazonConnectionConfig)->BaseClient:
        return boto3.client(
            "sqs",
            region_name=config.region,
            endpoint_url=config.endpointUrl,
            aws_access_key_id=config.accessKeyId,
            aws_secret_access_key=config.secretsAccessKey,
        )

    def create_queue(self,config:BrokerAmazonConnectionConfig, q: CreateQueueDto):
        sqs: BaseClient = self._client(config)

        attributes = self.create_attributes(q)

        try:
            resp = sqs.create_queue(
                QueueName=q.code,
                Attributes=attributes
            )
            queue_url = resp.get("QueueUrl")
            print(f" Coda creata: {queue_url} ")
            return {"queue_url": queue_url}

        except ClientError as e:
            raise Exception(f"Error creating SQS queue: {e}")

    def create_attributes(self, q:CreateQueueDto):
        attributes = {
            "VisibilityTimeout": str(q.defaultVisibilityTimeout or DEFAULT_VISIBILITY_TIMEOUT),
            "DelaySeconds": str(q.delay or 0),
            "ReceiveMessageWaitTimeSeconds": str(q.receiveMessageWait or 0),
        }

        if q.fifoQueue:
            attributes["FifoQueue"] = "true"
            if not q.code.endswith(".fifo"):
                q.code += ".fifo"
            if q.contentBasedDeduplication:
                attributes["ContentBasedDeduplication"] = "true"

        return attributes

    def delete_queue(self, config:BrokerAmazonConnectionConfig, queue_url:str):
        sqs: BaseClient = self._client(config)
        try:
            sqs.delete_queue(QueueUrl=queue_url)
            print(f" Coda eliminata: {queue_url} ")
            return {"message": f"Queue {queue_url} deleted successfully"}
        except ClientError as e:
            raise Exception(f"Error deleting SQS queue: {e}")

    def list_queues(self, config:BrokerAmazonConnectionConfig):
        sqs: BaseClient = self._client(config)
        try:
            resp = sqs.list_queues()
            queue_urls = resp.get("QueueUrls", [])
            print(f" Code trovate: {len(queue_urls)} ")
            return {"queueUrls": queue_urls}
        except ClientError as e:
            raise Exception(f"Error listing SQS queues: {e}")
