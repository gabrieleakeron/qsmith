from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.base_id_service import BaseIdEntityService


class StepOperationService(BaseIdEntityService):
    def get_entity_class(self) -> type[BaseIdEntity]:
        return StepOperationEntity

    def get_all_by_step(self, session: Session, scenario_step_id: str) -> list[StepOperationEntity]:
        scenario_id_attr: InstrumentedAttribute = StepOperationEntity.scenario_step_id
        return session.query(StepOperationEntity).filter(scenario_id_attr == scenario_step_id).order_by(StepOperationEntity.order).all()

    def delete_by_step_id(self, session: Session, step_id: str) -> int:
        scenario_id_attr: InstrumentedAttribute = StepOperationEntity.scenario_step_id
        query = session.query(StepOperationEntity).filter(scenario_id_attr == step_id)
        count = 0
        for op in query.all() :
            session.delete(op)
            count += 1
        session.flush()
        return count