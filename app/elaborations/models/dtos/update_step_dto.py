from pydantic import BaseModel
from elaborations.models.dtos.configuration_step_dtos import ConfigurationStepDtoTypes


class UpdateStepDto(BaseModel):
    id:str
    code: str
    description: str
    cfg: ConfigurationStepDtoTypes