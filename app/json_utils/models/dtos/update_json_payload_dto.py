from pydantic import BaseModel

class UpdateJsonPayloadDto(BaseModel):
    id:str|None = None
    code: str
    description:str| None = None
    payload: dict | list[dict]
