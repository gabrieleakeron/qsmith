import json
from typing import Any

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from _alembic.models.queue_entity import QueueEntity
from _alembic.services.session_context_manager import managed_session
from brokers.models.connections.amazon.broker_amazon_connection_config import BrokerAmazonConnectionConfig
from brokers.models.dto.configurations.queue_configuration_dto import QueueConfigurationDto
from brokers.models.dto.configurations.queue_configuration_types import convert_queue_configuration_types
from brokers.services.alembic.queue_service import QueueService
from brokers.services.connections.queue.queue_connection_service import QueueConnectionService
from exceptions.app_exception import QsmithAppException

SHORT_VISIBILITY_TIMEOUT = 5
DEFAULT_VISIBILITY_TIMEOUT = 30
MAX_NUMBER_OF_MESSAGES = 10
WAIT_TIME_SECONDS = 20

class AmazonSQSConnectionService(QueueConnectionService):

    def _client(self, config: BrokerAmazonConnectionConfig)->BaseClient:
        return boto3.client(
            "sqs",
            region_name=config.region,
            endpoint_url=config.endpointUrl,
            aws_access_key_id=config.accessKeyId,
            aws_secret_access_key=config.secretsAccessKey,
        )
    def _extract_url_from_queue(self,queue_cfg_dto:QueueConfigurationDto) -> str:
        if not queue_cfg_dto:
            raise Exception(f"Queue {queue_cfg_dto} not found")
        return queue_cfg_dto.url

    def test_connection(self, config:BrokerAmazonConnectionConfig, queue_id:str) -> tuple[BaseClient, str]:

        with managed_session() as session:
            queue: QueueEntity = QueueService().get_by_id(session,queue_id)
            queue_url  = self._extract_url_from_queue(convert_queue_configuration_types(queue.configuration_json))

        sqs = self.test_url_connection(config, queue_url)

        return sqs, queue_url

    def test_url_connection(self, config, url):
        try:
            sqs = self._client(config)
            sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["All"])
        except ClientError as e:
            raise Exception(f"Error accessing SQS queue: {e}")
        return sqs

    def publish_messages(self, config:BrokerAmazonConnectionConfig, queue_id:str, messages:list[Any]) -> list[dict[str, Any]]:

        sqs,queue_url = self.test_connection(config,queue_id)

        results = []
        for msg in messages:

            try:
                if queue_url.endswith(".fifo"):
                    resp = sqs.send_message(
                        QueueUrl=queue_url,
                        MessageBody=json.dumps(msg),
                        MessageGroupId= "default"
                    )
                else:
                    resp = sqs.send_message(
                        QueueUrl=queue_url,
                        MessageBody=json.dumps(msg)
                    )

                mid = resp.get("MessageId")
                http_status = resp.get("ResponseMetadata", {}).get("HTTPStatusCode")

                results.append({"status": "ok", "message_id": mid, "http_status": http_status})

            except Exception as e:
                raise QsmithAppException(f"Error publishing message to SQS queue: {e}")

        return results

    def receive_messages(self, config:BrokerAmazonConnectionConfig, queue_id:str, max_messages: int = 10) -> list[Any]:

        sqs,queue_url = self.test_connection(config,queue_id)

        all_msgs = []

        to_receive = min(MAX_NUMBER_OF_MESSAGES, max_messages)
        resp = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=to_receive,
            WaitTimeSeconds=WAIT_TIME_SECONDS,
            VisibilityTimeout=SHORT_VISIBILITY_TIMEOUT
        )

        msgs = resp.get("Messages", []) or []

        if not msgs:
            return all_msgs

        for m in msgs:
            all_msgs.append(m)

        return all_msgs

    def ack_messages(self, config:BrokerAmazonConnectionConfig, queue_id:str, messages: list[Any])-> list[dict]:

        sqs,queue_url = self.test_connection(config,queue_id)

        deleted_msgs:list[dict] = []
        for m in messages:
            try:
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=m["ReceiptHandle"]
                )
                mid = m["MessageId"]
                deleted_msgs.append({
                    "status": "ok",
                    "message_id": mid
                })
                print(f" Messaggio eliminato  MessageId={mid} ")
            except ClientError as e:
                mid = m.get("MessageId", "unknown")
                print(f" Errore eliminazione messaggio  MessageId={mid} Error={e}")

        return deleted_msgs
