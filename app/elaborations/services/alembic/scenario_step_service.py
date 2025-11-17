from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.scenario_step_entity import ScenarioStepEntity


class ScenarioStepService:
    @classmethod
    def insert(cls,session:Session,entity:ScenarioStepEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls,session:Session,entity:ScenarioStepEntity)->ScenarioStepEntity:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity

    @classmethod
    def get_by_id(cls,session:Session,_id:str)->ScenarioStepEntity|None:
        id_attr: InstrumentedAttribute = ScenarioStepEntity.id
        return session.query(ScenarioStepEntity).filter(id_attr==_id).one_or_none()

    @classmethod
    def get_all_by_scenario(cls,session:Session,scenario_id:str)->list[ScenarioStepEntity]:
        scenario_id_attr: InstrumentedAttribute = ScenarioStepEntity.scenario_id
        return session.query(ScenarioStepEntity).filter(scenario_id_attr==scenario_id).order_by(ScenarioStepEntity.order).all()

    @classmethod
    def delete_by_id(cls,session:Session,_id:str)->int:
        id_attr: InstrumentedAttribute = ScenarioStepEntity.id
        deleted = session.query(ScenarioStepEntity).filter(id_attr==_id).delete()
        return deleted

    @classmethod
    def delete_by_scenario_id(cls,session:Session,scenario_id:str)->int:
        scenario_id_attr: InstrumentedAttribute = ScenarioStepEntity.scenario_id
        deleted = session.query(ScenarioStepEntity).filter(scenario_id_attr==scenario_id).delete()
        return deleted