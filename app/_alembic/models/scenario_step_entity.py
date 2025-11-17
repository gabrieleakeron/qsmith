import uuid

from sqlalchemy import Column, Text, Numeric, ForeignKey

from _alembic.constants import SCHEMA
from _alembic.models.base import Base
from elaborations.models.enums.on_failure import OnFailure


class ScenarioStepEntity(Base):
    __tablename__ = "scenario_steps"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id = Column(Text, ForeignKey(f"{SCHEMA}.scenarios.id", ondelete="CASCADE"), nullable=False)
    step_id = Column(Text, ForeignKey(f"{SCHEMA}.steps.id"), nullable=False)
    order = Column(Numeric, nullable=False, default=0)
    on_failure = Column(Text, nullable=False, default=OnFailure.ABORT.value)