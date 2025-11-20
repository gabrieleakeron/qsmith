from pydantic import BaseModel
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes


class CreateStepDto(BaseModel):
    code: str
    description: str
    cfg: ConfigurationStepDtoTypes