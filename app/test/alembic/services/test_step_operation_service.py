import unittest

from _alembic.models.operation_entity import OperationEntity
from _alembic.models.scenario_entity import ScenarioEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_entity import StepEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.configuration_operation_dto import SaveInternalDBConfigurationOperationDto
from elaborations.models.dtos.configuration_step_dtos import SleepConfigurationStepDto
from elaborations.models.dtos.create_scenario_dto import CreateScenarioDto, CreateScenarioStepDto, \
    CreateStepOperationDto
from elaborations.models.enums.operation_type import OperationType
from elaborations.models.enums.step_type import StepType
from elaborations.services.alembic.operation_service import OperationService
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.step_service import StepService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.alembic.step_operation_service import StepOperationService
from elaborations.services.scenarios.scenario_dto_service import insert_scenario


def test_delete(alembic_container):
    with managed_session() as session:
        step_id = StepService().insert(
            session,
            StepEntity(
                code="step1_code",
                step_type=StepType.SLEEP.value,
                configuration_json={"param": "value"}
            )
        )
        operation_id = OperationService().insert(
            session,
            OperationEntity(
                operation_type=OperationType.SAVE_INTERNAL_DB.value,
                configuration_json={"table_name": "test_table"}
            )
        )
        scenario_id = ScenarioService().insert(
            session,
            ScenarioEntity(
                code="scenario_code"
            )
        )
        scenario_step_id = ScenarioStepService().insert(
            session,
            ScenarioStepEntity(
                scenario_id=scenario_id,
                step_id=step_id,
                order=0
            )
        )
        StepOperationService().insert(
            session,
            StepOperationEntity(
                scenario_step_id=scenario_step_id,
                operation_id=operation_id,
                order=0
            )
        )

    with managed_session() as session:
        deleted = ScenarioService().delete_by_id(session, scenario_id)
        assert deleted == 1

        steps = ScenarioStepService().get_all(session)
        assert 0 == len(steps)

        operations = StepOperationService().get_all(session)
        assert 0 == len(operations)

if __name__ == "__main__":
    unittest.main()
