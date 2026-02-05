from sqlalchemy import Column, Text, JSON

from _alembic.models import Base
from _alembic.models.code_desc_entity import CodeDescEntity


class StepEntity(Base,CodeDescEntity):
    __tablename__ = "steps"
    step_type = Column(Text, nullable=False)
    configuration_json = Column(JSON, nullable=False)