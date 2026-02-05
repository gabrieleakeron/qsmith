from sqlalchemy import Column, Text

from _alembic.models.base_entity import BaseIdEntity


class CodeDescEntity(BaseIdEntity):
    code = Column(Text, nullable=False )
    description = Column(Text, nullable=True )