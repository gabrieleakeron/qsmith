
from pydantic.dataclasses import dataclass
from json_utils.models.json_type import JsonType

@dataclass
class JsonPayload:
    id:str
    code: str
    description:str|None
    json_type: JsonType
    payload: dict | list[dict]