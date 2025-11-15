from typing import Any
from fastapi import APIRouter
from logs.services.sqlite.log_service import LogService

router = APIRouter(prefix="/logs")

@router.get("/")
async def get_logs_api() -> list[dict[str,Any]]:
    return LogService.get_logs()

@router.delete("/")
async def clear_logs_api() -> dict[str, str]:
    LogService.clean_logs()
    return {"message": "All logs cleared successfully"}