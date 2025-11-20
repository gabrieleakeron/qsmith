from _alembic.models.json_payload_entity import JsonPayloadEntity
from json_utils.services.alembic.json_files_service import JsonFilesService


def load_json_array(_id: str) -> list[dict]:

    json_payload:JsonPayloadEntity = JsonFilesService.get_by_id(_id)

    if not json_payload:
        raise ValueError(f"Json array '{_id}' not found")

    if isinstance(json_payload.payload, list):
        return json_payload.payload
    else:
        return [json_payload.payload]

