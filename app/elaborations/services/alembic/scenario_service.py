from sqlalchemy.orm import Session

from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.scenario_entity import ScenarioEntity
from _alembic.services.base_id_service import BaseIdEntityService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService


class ScenarioService(BaseIdEntityService):
    def get_entity_class(self) -> type[BaseIdEntity]:
        return ScenarioEntity

    def delete_on_cascade(self, session:Session, _id):
        ScenarioStepService().delete_by_scenario_id(session,_id)

