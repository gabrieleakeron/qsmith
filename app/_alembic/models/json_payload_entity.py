from sqlalchemy import Column, Text, DateTime, func

from _alembic.constants import SCHEMA
from _alembic.models.base import Base

class JsonPayloadEntity(Base):
    __tablename__ = "json_payloads"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Text, primary_key=True )
    code = Column(Text, nullable=False )
    description = Column(Text, nullable=True )
    json_type = Column(Text, nullable=False )
    payload = Column(Text, nullable=False )
    created_date = Column(DateTime, nullable=False, default=func.now())
    modified_date = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())