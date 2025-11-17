from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.queue_entity import QueueEntity


class QueueService:
    @classmethod
    def insert(cls,session:Session,entity:QueueEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls,session:Session,entity:QueueEntity)->QueueEntity:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity

    @classmethod
    def get_by_id(cls,session:Session,_id:str)->QueueEntity|None:
        id_attr: InstrumentedAttribute = QueueEntity.id
        return session.query(QueueEntity).filter(id_attr==_id).one_or_none()

    @classmethod
    def get_all_by_broker_id(cls,session:Session,broker_id:str)->list[QueueEntity]:
        broker_id_attr: InstrumentedAttribute = QueueEntity.broker_id
        return session.query(QueueEntity).filter(broker_id_attr==broker_id).all()

    @classmethod
    def delete_by_id(cls,session:Session,_id:str)->int:
        id_attr: InstrumentedAttribute = QueueEntity.id
        deleted = session.query(QueueEntity).filter(id_attr==_id).delete()
        return deleted

    @classmethod
    def delete_by_broker_id(cls,session:Session,broker_id:str)->int:
        broker_id_attr: InstrumentedAttribute = QueueEntity.broker_id
        deleted = session.query(QueueEntity).filter(broker_id_attr==broker_id).delete()
        return deleted