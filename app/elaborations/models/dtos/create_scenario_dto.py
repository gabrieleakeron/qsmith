from pydantic import BaseModel

from elaborations.models.enums.on_failure import OnFailure


class CreateStepOperationDto(BaseModel):
    order: int
    operation_id: str

class CreateScenarioStepDto(BaseModel):
    order: int
    step_id:str
    on_failure:str|None = OnFailure.ABORT
    operations: list[CreateStepOperationDto]|None = []


class CreateScenarioDto(BaseModel):
    code: str
    description: str
    steps: list[CreateScenarioStepDto]


