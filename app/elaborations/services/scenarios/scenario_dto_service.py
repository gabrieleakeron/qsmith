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
        scenario_enity = ScenarioEntity()
        scenario_enity.code = scenario_dto.code,
        scenario_enity.description = scenario_dto.description
        scenario_id = ScenarioService().insert(session,scenario_enity)
        for index, step in enumerate(scenario_dto.steps):
            scenario_step_entity = ScenarioStepEntity()
            scenario_step_entity.scenario_id = scenario_id,
            scenario_step_entity.step_id = step.step_id,
            scenario_step_entity.order = index,
            scenario_step_entity.on_failure = step.on_failure
            scenario_step_id = ScenarioStepService().insert(session,scenario_step_entity)
            for op_index, operation in enumerate(step.operations):
                step_operation_entity = StepOperationEntity()
                step_operation_entity.scenario_step_id = scenario_step_id,
                step_operation_entity.operation_id = operation.operation_id,
                step_operation_entity.order = op_index
                StepOperationService().insert(session,step_operation_entity)
    return scenario_id
