import json
import uuid
from typing import Any

from exceptions.app_exception import QsmithAppException
from json_utils.models.create_json_payload_dto import CreateJsonPayloadDto
from json_utils.models.json_payload import JsonPayload
from json_utils.models.json_type import JsonType
from json_utils.models.update_json_payload_dto import UpdateJsonPayloadDto
from sqlite_core.connection_factory import ConnectionFactory


class JsonFilesService:

    @classmethod
    def insert(cls, json_type:JsonType, dto:CreateJsonPayloadDto)->str:
        id = str(uuid.uuid4())
        with ConnectionFactory.create_connection() as cx:
            cx.execute("""
                       INSERT INTO json_payloads (id, code, description, json_type, payload)
                       VALUES (?, ?, ?, ?, ?)
                   """, (id, dto.code, dto.description, json_type.value, json.dumps(dto.payload,ensure_ascii=True)))
        return id

    @classmethod
    def update(cls, json_type:JsonType, dto:UpdateJsonPayloadDto)->str:
        with ConnectionFactory.create_connection() as cx:

            result = cx.execute("""
                UPDATE json_payloads
                SET code = ?, description = ?, json_type = ?, payload = ?, modified_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (dto.code, dto.description, json_type.value, json.dumps(dto.payload, ensure_ascii=True), dto.id))

            if result.rowcount == 0:
                raise QsmithAppException(f"JSON payload with id {dto.id} not found for update.")

        return dto.id

    @classmethod
    def get_by_id(cls, _id:str)-> JsonPayload | None:
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT code, description, json_type, payload
                FROM json_payloads
                WHERE id = ?
            """, (_id,))
            row = cursor.fetchone()
            if row:
                code = row[0]
                description = row[1]
                j_type = JsonType(row[2])
                payload = json.loads(row[3])
                dto = JsonPayload(id=_id, code=code, description=description, json_type=j_type, payload=payload)
                return dto
            return None

    @classmethod
    def get_codes_by_type(cls, j_type: JsonType)->list[str]:
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT code
                FROM json_payloads
                WHERE json_type = ?
            """, (j_type.value,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]

    @classmethod
    def get_all_by_type(cls, j_type: JsonType)->list[JsonPayload]:
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT id, code, description, payload
                FROM json_payloads
                WHERE json_type = ?
            """, (j_type.value,))
            rows = cursor.fetchall()
            result = []
            for row in rows:
                id = row[0]
                code = row[1]
                description = row[2]
                json_data = json.loads(row[3])
                dto = JsonPayload(id=id, code=code, description=description, json_type=j_type, payload=json_data)
                result.append(dto)
            return result

    @classmethod
    def delete_by_id(cls, _id:str)->Any:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                DELETE FROM json_payloads
                WHERE id = ?
            """, (_id,))
            return result.rowcount
