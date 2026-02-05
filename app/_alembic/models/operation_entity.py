from sqlalchemy import Column, Text, JSON

from _alembic.models.base import Base
from _alembic.models.code_desc_entity import CodeDescEntity


class OperationEntity(Base,CodeDescEntity):
    __tablename__ = "operations"
    operation_type = Column(Text, nullable=False)
    configuration_json = Column(JSON, nullable=False)