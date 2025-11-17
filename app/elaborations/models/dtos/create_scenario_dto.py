from pydantic import BaseModel

from elaborations.models.dtos.configuration_operation_dto import ConfigurationOperationTypes
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes
from elaborations.models.enums.on_failure import OnFailure


class CreateStepOperationDto(BaseModel):
    operation_id: str
    cfg: ConfigurationOperationTypes
    order: int

class CreateScenarioStepDto(BaseModel):
    step_id:str
    cfg: ConfigurationStepDtoTypes
    operations: list[CreateStepOperationDto]
    on_failure:str|None = OnFailure.ABORT
    order: int

class CreateScenarioDto(BaseModel):
    code: str
    description: str
    steps: list[CreateScenarioStepDto]


