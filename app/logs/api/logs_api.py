from fastapi import APIRouter

from _alembic.services.session_context_manager import managed_session
from logs.models.dtos.log_dto import LogDto
from logs.services.alembic.log_service import LogService

router = APIRouter(prefix="/logs")

@router.get("/")
async def get_logs_api() -> list[LogDto]:
    with managed_session() as session:
        logs = LogService().get_logs(session)
        return [LogDto.model_validate(log) for log in logs]

@router.delete("/{days}")
async def clear_logs_api(days:int) -> dict[str, str]:
    with managed_session() as session:
        LogService().clean_logs(session,days)
    return {"message": "All logs cleared successfully"}