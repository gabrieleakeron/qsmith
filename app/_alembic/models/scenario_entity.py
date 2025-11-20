import uuid

from sqlalchemy import Column, Text

from _alembic.constants import SCHEMA
from _alembic.models.base import Base

class ScenarioEntity(Base):
    __tablename__ = "scenarios"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(Text, nullable=False)
    description = Column(Text, nullable=True)