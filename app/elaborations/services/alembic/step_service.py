from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.step_entity import StepEntity


class StepService:

    @classmethod
    def insert(cls,session:Session,entity:StepEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls,session:Session,entity:StepEntity)->StepEntity:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity

    @classmethod
    def get_by_id(cls,session:Session,_id:str)->StepEntity|None:
        id_attr: InstrumentedAttribute = StepEntity.id
        return session.query(StepEntity).filter(id_attr==_id).one_or_none()

    @classmethod
    def get_all(cls,session:Session)->list[StepEntity]:
        return session.query(StepEntity).all()

    @classmethod
    def delete_by_id(cls,session:Session,_id:str)->int:
        id_attr: InstrumentedAttribute = StepEntity.id
        deleted = session.query(StepEntity).filter(id_attr==_id).delete()
        return deleted