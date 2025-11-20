import uuid

from sqlalchemy import Column, Text

from _alembic.constants import SCHEMA
from _alembic.models.base import Base


class OperationEntity(Base):
    __tablename__ = "operations"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    operation_type = Column(Text, nullable=False)
    configuration_json = Column(Text, nullable=False)