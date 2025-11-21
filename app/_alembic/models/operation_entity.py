from sqlalchemy import Column, Text, JSON

from _alembic.models.base import Base
from _alembic.models.base_entity import BaseIdEntity


class OperationEntity(Base,BaseIdEntity):
    __tablename__ = "operations"
    operation_type = Column(Text, nullable=False)
    configuration_json = Column(JSON, nullable=False)