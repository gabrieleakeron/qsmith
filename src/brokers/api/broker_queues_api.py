from fastapi import APIRouter

from brokers.models.connections.broker_connection_config_types import BrokerConnectionConfigTypes
from brokers.models.dto.create_queue_dto import CreateQueueDto
from brokers.models.dto.find_all_messages_dto import FindAllMessagesDto
from brokers.models.dto.queue_messages_dto import QueueMessagesDto
from brokers.models.queues.queue_dto import QueueDto
from brokers.services.connections.broker_connection_service_factory import BrokerConnectionServiceFactory
from brokers.services.connections.queue.queue_connection_service_factory import QueueConnectionServiceFactory
from brokers.services.sqllite.broker_connection_service import load_broker_connection
from brokers.services.sqllite.queue_service import QueueService

router = APIRouter(prefix="/broker")

@router.get("/{broker_id}/queue")
async def find_all_queues_api(broker_id:str)->list[dict]:
    queues: list[QueueDto]= QueueService.get_all_by_broker(broker_id)
    result: list[dict] = []
    for queue in queues:
        result.append(queue.model_dump())
    return result

@router.get("/{broker_id}/queue/{queue_id}")
async def find_queue_api(broker_id:str,queue_id:str):
    queue_dto:QueueDto|None = QueueService.get_by_id(queue_id)
    if queue_dto is None:
        return {"error": f"Queue with name '{queue_id}' not found"}
    return queue_dto.model_dump()

@router.post("/{broker_id}/queue")
async def insert_queue_api(broker_id:str, c: CreateQueueDto):
    try:
        connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
        service = BrokerConnectionServiceFactory.get_service(connection_config)
        result= service.create_queue(connection_config,c)
        QueueService.insert(QueueDto(
            broker_id=broker_id,
            code=c.code,
            url=result.get("queueUrl"),
            fifoQueue=c.fifoQueue,
            contentBasedDeduplication=c.contentBasedDeduplication,
            defaultVisibilityTimeout=c.defaultVisibilityTimeout,
            delay=c.delay,
            receiveMessageWait=c.receiveMessageWait
        ))
    except Exception as e:
        return {"error": str(e)}

    return result

@router.delete("/{broker_id}/queue/{queue_id}")
async def delete_queue_api(broker_id:str,queue_id:str):
    try:
        queue_dto:QueueDto|None = QueueService.get_by_id(queue_id)
        if queue_dto is None:
            return {"error": f"Queue with name '{queue_id}' not found"}

        connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
        service = BrokerConnectionServiceFactory.get_service(connection_config)
        result = service.delete_queue(connection_config, queue_dto.url)
        QueueService.delete_by_id(queue_id)

    except Exception as e:
        return {"error": f"Could not delete queue '{queue_id}': {str(e)}"}

    return result

@router.post("/{broker_id}/queue/{queue_id}/messages")
async def publish_messages_api(broker_id:str, queue_id:str, p: QueueMessagesDto):
    connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
    service = QueueConnectionServiceFactory.get_service(connection_config)
    return service.publish_messages(connection_config, queue_id=queue_id, messages=p.messages)

@router.get("/{broker_id}/queue/{queue_id}/test")
async def test_queue_connection_api(broker_id:str,queue_id:str):
    connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
    if connection_config is None:
        return {"message": f"Connection {broker_id} not found"}, 404
    service = QueueConnectionServiceFactory.get_service(connection_config)
    if not service.test_connection(connection_config,queue_id):
        return {"message": f"Connection is not valid"}, 400
    return {"message": f"Connection is valid"}

@router.get("/{broker_id}/queue/{queue_id}/messages")
async def receive_messages_api(broker_id:str, queue_id:str, f: FindAllMessagesDto):
    connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
    service = QueueConnectionServiceFactory.get_service(connection_config)
    msgs = service.receive_messages(connection_config, queue_id=queue_id, max_messages=f.count)
    print(msgs)
    return msgs

@router.delete("/{broker_id}/queue/{queue_id}/messages")
async def ack_messages_api(broker_id:str, queue_id:str,d:QueueMessagesDto):
    connection_config: BrokerConnectionConfigTypes = load_broker_connection(broker_id)
    service = QueueConnectionServiceFactory.get_service(connection_config)
    return service.ack_messages(connection_config, queue_id=queue_id, messages=d.messages)
