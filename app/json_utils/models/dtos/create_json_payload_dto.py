from pydantic import BaseModel

class CreateJsonPayloadDto(BaseModel):
    code: str
    description:str| None = None
    payload: dict | list[dict]
