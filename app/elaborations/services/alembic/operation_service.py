from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.operation_entity import OperationEntity


class OperationService:
    @classmethod
    def insert(cls,session:Session,entity:OperationEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls,session:Session,entity:OperationEntity)->OperationEntity:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity

    @classmethod
    def get_by_id(cls,session:Session,_id:str)->OperationEntity|None:
        id_attr: InstrumentedAttribute = OperationEntity.id
        return session.query(OperationEntity).filter(id_attr==_id).one_or_none()

    @classmethod
    def get_all(cls,session:Session)->list[OperationEntity]:
        return session.query(OperationEntity).all()

    @classmethod
    def delete_by_id(cls,session:Session,_id:str)->int:
        id_attr: InstrumentedAttribute = OperationEntity.id
        deleted = session.query(OperationEntity).filter(id_attr==_id).delete()
        return deleted