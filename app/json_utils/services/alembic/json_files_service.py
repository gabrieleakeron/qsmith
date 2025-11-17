from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.json_payload_entity import JsonPayloadEntity
from json_utils.models.enums.json_type import JsonType


class JsonFilesService:

    @classmethod
    def insert(cls,session:Session,entity:JsonPayloadEntity)->str:
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls, session:Session, entity:JsonPayloadEntity)->str:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def get_by_id(cls, session:Session, _id:str)-> JsonPayloadEntity | None:
        return session.get(JsonPayloadEntity, _id)

    @classmethod
    def get_codes_by_type(cls, session:Session, j_type: JsonType)->list[str]:
        cursor = session.execute(text("""
            SELECT code
            FROM json_payloads
            WHERE json_type = :j_type
        """, {"j_type": j_type.value}))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    @classmethod
    def get_all_by_type(cls, session:Session, j_type: JsonType)->list[JsonPayloadEntity]:
        json_type_attr: InstrumentedAttribute = JsonPayloadEntity.json_type
        query = session.query(JsonPayloadEntity).filter(json_type_attr == j_type.value)
        return query.all()


    @classmethod
    def delete_by_id(cls, session:Session, _id:str)->Any:
        entity = session.get(JsonPayloadEntity, _id)
        if not entity:
            return 0
        session.delete(entity)
        return 1
