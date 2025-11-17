import json
import time
import uuid

from logs.models.logs import LogSubjectType, LogLevel, LogDto
from sqlite_core.connection_factory import ConnectionFactory

class LogService:

    @classmethod
    def log(cls, log_dto: LogDto)->str:
        _id = str(uuid.uuid4())
        with ConnectionFactory.create_connection() as cx:
            cx.execute("""
                INSERT INTO logs (id, subject_type, subject, level, message, payload, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _id,
                log_dto.subject_type.value,
                log_dto.subject,
                log_dto.level.value,
                log_dto.message,
                json.dumps(log_dto.payload, ensure_ascii=True) if log_dto.payload else None,
                int(time.time() * 1000)
            ))
        return _id

    @classmethod
    def get_logs(cls, subject:LogSubjectType=None, level:LogLevel=None, limit:int=100)->list[LogDto]:
        with ConnectionFactory.create_connection() as cx:
            query = "SELECT id, subject_type, subject, level, message, payload, created_at FROM logs"
            conditions = []
            params = []

            if subject:
                conditions.append("subject = ?")
                params.append(subject.value)
            if level:
                conditions.append("level = ?")
                params.append(level.value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor = cx.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [
                LogDto(
                    id=row[0],
                    subject_type=LogSubjectType(row[1]),
                    subject=row[2],
                    level=LogLevel(row[3]),
                    message=row[4],
                    payload=json.loads(row[5]) if row[5] else None,
                    created_at=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[6]/1000))
                )
                for row in rows
            ]

    @classmethod
    def clean_logs(cls, older_than_days:int=30)->int:
        with ConnectionFactory.create_connection() as cx:
            cutoff_timestamp = int((time.time() - older_than_days * 86400) * 1000)
            result = cx.execute("""
                DELETE FROM logs WHERE created_at < ?
            """, (cutoff_timestamp,))
            return result.rowcount