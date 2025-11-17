from pydantic import BaseModel


class JsonPayloadDto(BaseModel):
    code: str
    payload: dict | list[dict]