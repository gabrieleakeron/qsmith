from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.step_entity import StepEntity
from _alembic.services.base_id_service import BaseIdEntityService

class StepService(BaseIdEntityService):
    def get_entity_class(self) -> type[BaseIdEntity]:
        return StepEntity