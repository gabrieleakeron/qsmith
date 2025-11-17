import uuid

from sqlalchemy import Column, Text, Numeric, ForeignKey

from _alembic.constants import SCHEMA
from _alembic.models.base import Base

class StepOperationEntity(Base):
    __tablename__ = "step_operations"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_step_id = Column(Text, ForeignKey(f"{SCHEMA}.scenario_steps.id", ondelete="CASCADE"), nullable=False)
    operation_id = Column(Text, ForeignKey(f"{SCHEMA}.operations.id"), nullable=False)
    order = Column(Numeric, nullable=False)