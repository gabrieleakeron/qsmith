from sqlalchemy.orm import Session, InstrumentedAttribute

from _alembic.models.step_operation_entity import StepOperationEntity


class StepOperationService:
    @classmethod
    def insert(cls, session: Session, entity: StepOperationEntity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity.id

    @classmethod
    def update(cls, session: Session, entity: StepOperationEntity) -> StepOperationEntity:
        session.merge(entity)
        session.flush()
        session.refresh(entity)
        return entity

    @classmethod
    def get_by_id(cls, session: Session, _id: str) -> StepOperationEntity | None:
        id_attr: InstrumentedAttribute = StepOperationEntity.id
        return session.query(StepOperationEntity).filter(id_attr == _id).one_or_none()

    @classmethod
    def get_all_by_step(cls, session: Session, step_id: str) -> list[StepOperationEntity]:
        scenario_id_attr: InstrumentedAttribute = StepOperationEntity.scenario_id
        return session.query(StepOperationEntity).filter(scenario_id_attr == step_id).order_by(StepOperationEntity.order).all()

    @classmethod
    def delete_by_id(cls, session: Session, _id: str) -> int:
        id_attr: InstrumentedAttribute = StepOperationEntity.id
        deleted = session.query(StepOperationEntity).filter(id_attr == _id).delete()
        return deleted

    @classmethod
    def delete_by_scenario_id(cls, session: Session, step_id: str) -> int:
        scenario_id_attr: InstrumentedAttribute = StepOperationEntity.scenario_id
        deleted = session.query(StepOperationEntity).filter(scenario_id_attr == step_id).delete()
        return deleted