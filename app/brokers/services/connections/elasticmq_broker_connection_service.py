import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from brokers.models.connections.elastiqmq.broker_elasticmq_connection_config import BrokerElasticmqConnectionConfig
from brokers.models.dto.create_queue_dto import CreateQueueDto
from brokers.services.connections.broker_connection_service import BrokerConnectionService

DEFAULT_VISIBILITY_TIMEOUT = 30

def client(config: BrokerElasticmqConnectionConfig)->BaseClient:
    return boto3.client(
        "sqs",
        region_name="region",
        endpoint_url=config.endpointUrl,
        aws_access_key_id="xxx",
        aws_secret_access_key="yyy",
    )

class ElasticmqBrokerConnectionService(BrokerConnectionService):

    def create_queue(self,config:BrokerElasticmqConnectionConfig, q: CreateQueueDto):
        sqs: BaseClient = client(config)

        attributes = self.create_attributes(q)

        try:
            resp = sqs.create_queue(
                QueueName=q.code,
                Attributes=attributes
            )
            queue_url = resp.get("QueueUrl")
            print(f" Coda creata: {queue_url} ")
            return {"queueUrl": queue_url}

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
            if not q.name.endswith(".fifo"):
                q.name += ".fifo"
            if q.contentBasedDeduplication:
                attributes["ContentBasedDeduplication"] = "true"

        return attributes

    def delete_queue(self, config:BrokerElasticmqConnectionConfig, queue_url:str):
        sqs: BaseClient = client(config)
        try:
            sqs.delete_queue(QueueUrl=queue_url)
            print(f" Coda eliminata: {queue_url} ")
            return {"message": f"Queue {queue_url} deleted successfully"}
        except ClientError as e:
            raise Exception(f"Error deleting SQS queue: {e}")

    def list_queues(self, config:BrokerElasticmqConnectionConfig):
        sqs: BaseClient = client(config)
        try:
            resp = sqs.list_queues()
            queue_urls = resp.get("QueueUrls", [])
            print(f" Code trovate: {len(queue_urls)} ")
            return {"queueUrls": queue_urls}
        except ClientError as e:
            raise Exception(f"Error listing SQS queues: {e}")
