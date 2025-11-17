import json

from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.scenario_result_entity import ScenarioResultEntity


class ScenarioResultsService:

    @classmethod
    def insert(cls,session:Session,entity:ScenarioResultEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def get_results_by_scenario(cls, session:Session, scenario_id: str):
        scenario_attr: InstrumentedAttribute = ScenarioResultEntity.scenario
        cursor = session.query(ScenarioResultEntity).filter(scenario_attr == scenario_id).all()
        return [json.loads(row.payload) for row in cursor if row.payload]

    @classmethod
    def delete_by_scenario(cls, session:Session, scenario_id: str)->int:
        scenario_attr: InstrumentedAttribute = ScenarioResultEntity.scenario
        deleted = session.query(ScenarioResultEntity).filter(scenario_attr == scenario_id).delete()
        return deleted

