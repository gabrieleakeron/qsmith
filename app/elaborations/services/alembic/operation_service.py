from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.operation_entity import OperationEntity
from _alembic.services.base_id_service import BaseIdEntityService


class OperationService(BaseIdEntityService):
    def get_entity_class(self) -> type[BaseIdEntity]:
        return OperationEntity
