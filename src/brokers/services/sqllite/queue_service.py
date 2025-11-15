import json
import uuid
from typing import Any
from brokers.models.queues.queue_dto import QueueDto
from exceptions.app_exception import QsmithAppException
from sqlite_core.connection_factory import ConnectionFactory


class QueueService:

    @classmethod
    def insert(cls,queue_dto:QueueDto)->str:
        _id = str(uuid.uuid4())
        with ConnectionFactory.create_connection() as cx:
            cx.execute("""
                INSERT INTO queues (id, broker_id, code, payload)
                VALUES (?, ?, ?, ?)
            """, (_id, queue_dto.broker_id, queue_dto.code, json.dumps(queue_dto.model_dump(), ensure_ascii=True)))
        return _id

    @classmethod
    def update(cls,queue_dto:QueueDto)->str:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                UPDATE queues
                SET broker_id = ?, code = ?, payload = ?, modified_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (queue_dto.broker_id, queue_dto.code, json.dumps(queue_dto.model_dump(), ensure_ascii=True), queue_dto.id))
            if result.rowcount == 0:
                raise QsmithAppException(f"Queue with id {queue_dto.id} not found for update.")

        return queue_dto.id

    @classmethod
    def get_by_id(cls, _id:str)-> QueueDto | None:
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT payload, broker_id, id, code
                FROM queues
                WHERE id = ?
            """, (_id,))
            row = cursor.fetchone()
            if row:
                dto = QueueDto.model_validate(json.loads(row[0]))
                dto.broker_id = row[1]
                dto.id = row[2]
                dto.code = row[3]
                return dto
            return None

    @classmethod
    def get_all_by_broker(cls,broker_id:str)->list[QueueDto]:
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT payload, broker_id, id, code
                FROM queues
                WHERE broker_id = ?
            """, (broker_id,))

            rows = cursor.fetchall()

            queues: list[QueueDto] = []
            for row in rows:
                dto = QueueDto.model_validate(json.loads(row[0]))
                dto.broker_id = row[1]
                dto.id = row[2]
                dto.code = row[3]
                queues.append(dto)

            return queues

    @classmethod
    def delete_by_id(cls, _id: str)->Any:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                DELETE FROM queues
                WHERE id = ?
            """, (_id,))
            return result.rowcount

    @classmethod
    def delete_by_broker_id(cls, broker_id: str)->Any:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                DELETE FROM queues
                WHERE broker_id = ?
            """, (broker_id,))
            return result.rowcount