from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.services.base_id_service import BaseIdEntityService
from elaborations.services.alembic.step_operation_service import StepOperationService


class ScenarioStepService(BaseIdEntityService):
    def get_entity_class(self) -> type[BaseIdEntity]:
        return ScenarioStepEntity

    def get_all_by_scenario_id(self,session:Session,scenario_id:str)->list[ScenarioStepEntity]:
        scenario_id_attr: InstrumentedAttribute = ScenarioStepEntity.scenario_id
        return session.query(ScenarioStepEntity).filter(scenario_id_attr==scenario_id).order_by(ScenarioStepEntity.order).all()

    def delete_by_scenario_id(self, session:Session, scenario_id:str)->int:
        scenario_id_attr: InstrumentedAttribute = ScenarioStepEntity.scenario_id
        query = session.query(ScenarioStepEntity).filter(scenario_id_attr == scenario_id)
        steps = query.all()
        count = 0
        for step in steps :
            self.delete_on_cascade(session,step.id)
            session.delete(step)
            count += 1
        session.flush()
        return count

    def delete_on_cascade(self, session: Session, _id: str):
        StepOperationService().delete_by_step_id(session,_id)

