from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.scenario_entity import ScenarioEntity


class ScenarioService:

    @classmethod
    def insert(cls,session:Session,scenario_entity:ScenarioEntity):
        session.add(scenario_entity)
        session.flush()
        session.refresh(scenario_entity)
        return scenario_entity.id

    @classmethod
    def update(cls,session:Session,scenario_entity:ScenarioEntity)->ScenarioEntity:
        session.merge(scenario_entity)
        session.flush()
        session.refresh(scenario_entity)
        return scenario_entity

    @classmethod
    def get_by_id(cls,session:Session,_id:str)->ScenarioEntity|None:
        id_attr: InstrumentedAttribute = ScenarioEntity.id
        return session.query(ScenarioEntity).filter(id_attr==_id).one_or_none()

    @classmethod
    def get_all(cls,session:Session)->list[ScenarioEntity]:
        return session.query(ScenarioEntity).all()

    @classmethod
    def delete_by_id(cls,session:Session,_id:str)->int:
        id_attr: InstrumentedAttribute = ScenarioEntity.id
        deleted = session.query(ScenarioEntity).filter(id_attr==_id).delete()
        return deleted
