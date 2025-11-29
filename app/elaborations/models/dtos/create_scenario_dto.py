from pydantic import BaseModel

from elaborations.models.enums.on_failure import OnFailure


class CreateStepOperationDto(BaseModel):
    operation_id: str

class CreateScenarioStepDto(BaseModel):
    step_id:str
    on_failure:str|None = OnFailure.ABORT

class CreateScenarioDto(BaseModel):
    code: str
    description: str


