from _alembic.models import Base
from _alembic.models.code_desc_entity import CodeDescEntity


class ScenarioEntity(Base,CodeDescEntity):
    __tablename__ = "scenarios"