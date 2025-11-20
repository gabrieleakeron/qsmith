from pydantic import BaseModel

from _alembic.constants import SCHEMA
from _alembic.models import Base
from sqlalchemy import Column, Text, Numeric, Boolean


class QueueEntity(Base):
    __tablename__ = "queues"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True)
    broker_id = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    configuration_json = Column(Text, nullable=False)



