from json_utils.models.json_payload import JsonPayload
from json_utils.services.sqlite.json_files_service import JsonFilesService


def load_json_array(_id: str) -> list[dict]:

    json_payload:JsonPayload = JsonFilesService.get_by_id(_id)

    if not json_payload:
        raise ValueError(f"Json array '{_id}' not found")

    if isinstance(json_payload.payload, list):
        return json_payload.payload
    else:
        return [json_payload.payload]

