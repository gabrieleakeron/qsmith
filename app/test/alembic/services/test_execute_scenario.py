import json
import unittest

from _alembic.models.operation_entity import OperationEntity
from _alembic.models.scenario_entity import ScenarioEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_entity import StepEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.enums.operation_type import OperationType
from elaborations.models.enums.step_type import StepType
from elaborations.services.alembic.operation_service import OperationService
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.alembic.step_operation_service import StepOperationService
from elaborations.services.alembic.step_service import StepService
from elaborations.services.scenarios.scenario_executor_thread import ScenarioExecutionInput, _execute
from logs.services.alembic.log_service import LogService


def test_execution(alembic_container):
    with managed_session() as session:
        step_id = StepService().insert(
            session,
            StepEntity(
                code="step1_code",
                step_type=StepType.SLEEP.value,
                configuration_json={
                    "stepType": "sleep",
                    "duration": 2
                }
            )
        )
        operation_id = OperationService().insert(
            session,
            OperationEntity(
                operation_type=OperationType.SAVE_INTERNAL_DB.value,
                configuration_json={
                    "operationType": "save-internal-db",
                    "table_name": "test_table"
                }
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

    _execute(ScenarioExecutionInput(
        scenario_id=scenario_id,
        scenario_code="scenario_code"
    ))

    with managed_session() as session:
        logs = LogService().get_logs(session)

        for log in logs:
            print(f" {log.level} - {log.message} - {json.dumps(log.payload)} ")


if __name__ == "__main__":
    unittest.main()
