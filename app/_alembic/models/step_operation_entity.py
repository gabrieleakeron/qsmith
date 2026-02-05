from sqlalchemy import Column, Text, Numeric, ForeignKey

from _alembic.constants import SCHEMA
from _alembic.models import Base
from _alembic.models.base_entity import BaseIdEntity


class StepOperationEntity(Base,BaseIdEntity):
    __tablename__ = "step_operations"
    scenario_step_id = Column(Text, ForeignKey(f"{SCHEMA}.scenario_steps.id", ondelete="CASCADE"), nullable=False)
    operation_id = Column(Text, ForeignKey(f"{SCHEMA}.operations.id"), nullable=False)
    order = Column(Numeric, nullable=False)