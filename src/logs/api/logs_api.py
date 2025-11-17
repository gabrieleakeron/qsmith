from fastapi import APIRouter

from logs.models.logs import LogDto
from logs.services.sqlite.log_service import LogService

router = APIRouter(prefix="/logs")

@router.get("/")
async def get_logs_api() -> list[LogDto]:
    return LogService.get_logs()

@router.delete("/{days}")
async def clear_logs_api(days:int) -> dict[str, str]:
    LogService.clean_logs(days)
    return {"message": "All logs cleared successfully"}