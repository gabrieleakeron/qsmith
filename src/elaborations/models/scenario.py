from pydantic import BaseModel
from elaborations.models.steps import StepDtoTypes

class Scenario(BaseModel):
    id:str
    code: str
    description: str
    steps: list[StepDtoTypes]


