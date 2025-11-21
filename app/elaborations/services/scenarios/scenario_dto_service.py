from _alembic.models.scenario_entity import ScenarioEntity
from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_operation_entity import StepOperationEntity
from _alembic.services.session_context_manager import managed_session
from elaborations.models.dtos.create_scenario_dto import CreateScenarioDto
from elaborations.services.alembic.scenario_service import ScenarioService
from elaborations.services.alembic.scenario_step_service import ScenarioStepService
from elaborations.services.alembic.step_operation_service import StepOperationService

def insert_scenario(scenario_dto: CreateScenarioDto) -> str:
    with managed_session() as session:
        scenario_id = ScenarioService().insert(
            session,
            ScenarioEntity(
                code=scenario_dto.code,
                description=scenario_dto.description
            )
        )
        for index, step in enumerate(scenario_dto.steps):
            scenario_step_id = ScenarioStepService().insert(
                session,
                ScenarioStepEntity(
                    scenario_id=scenario_id,
                    step_id=step.step_id,
                    order=index,
                    on_failure=step.on_failure
                )
            )
            for op_index, operation in enumerate(step.operations):
                StepOperationService().insert(
                    session,
                    StepOperationEntity(
                        scenario_step_id=scenario_step_id,
                        operation_id=operation.operation_id,
                        order=op_index
                    )
                )
    return scenario_id
