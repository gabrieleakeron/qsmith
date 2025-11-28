from abc import abstractmethod, ABC

from sqlalchemy.orm import Session

from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes
from _alembic.models.step_entity import StepEntity
from elaborations.services.alembic.step_operation_service import StepOperationService
from elaborations.services.operations.operation_executor_composite import execute_operations
from _alembic.models.log_entity import LogEntity
from logs.models.dtos.log_dto import LogDto
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService


class StepExecutor(ABC):
    @classmethod
    def log(cls, step_id: str, message: str, payload: dict | list[dict] = None, level: LogLevel = LogLevel.INFO):
        log_dto = LogDto(
            subject_type=LogSubjectType.STEP_EXECUTION,
            subject=step_id,
            message=message,
            level=level,
            payload=payload
        )
        LogService().log(log_dto)

    @classmethod
    def execute_operations(cls, session:Session, step_id: str, data) -> list[dict[str, str]]:
        operation_ids = cls.find_all_operations(session,step_id)
        return execute_operations(session, operation_ids, data).result

    @classmethod
    def find_all_operations(cls, session:Session, step_id):
        step_operations = StepOperationService().get_all_by_step(session, step_id)
        operation_ids = [op.operation_id for op in step_operations]
        return operation_ids

    @abstractmethod
    def execute(self, session: Session, scenario_step:ScenarioStepEntity, step: StepEntity, cfg: ConfigurationStepDtoTypes) -> list[dict[str, str]]:
        pass
