import uuid

from sqlalchemy import Column, Time, Text, func

from _alembic.constants import SCHEMA
from _alembic.models.base import Base
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType


class LogEntity(Base):
    __tablename__ = "logs"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_type = Column(Text, nullable=False, default=LogSubjectType.SERVICE.value)
    subject = Column(Text, nullable=False)
    level = Column(Text, nullable=False, default=LogLevel.INFO.value)
    message = Column(Text, nullable=False)
    payload = Column(Text, nullable=True)
    created_at = Column(Time, nullable=False, default=func.now())