import uuid

from logs.models.log_type import LogType, LogLevel
from sqlite_core.connection_factory import ConnectionFactory


def log(message:str, log_type:LogType=LogType.ELABORATION, level:LogLevel=LogLevel.INFO):
    LogService.insert(log_type, level, message)

class LogService:

    @classmethod
    def insert(cls, l_type:LogType, l_level:LogLevel,message:str)->str:
        id = str(uuid.uuid4())
        with ConnectionFactory.create_connection() as cx:
            cx.execute("""
                INSERT INTO logs (id, l_type, l_level, message)
                VALUES (?, ?, ?, ?)
            """, (id, l_type.value, l_level.value, message))
        return id

    @classmethod
    def get_logs(cls, l_type:LogType=None, l_level:LogLevel=None, limit:int=100):
        with ConnectionFactory.create_connection() as cx:
            query = "SELECT id, l_type, l_level, message, created_date FROM logs"
            conditions = []
            params = []

            if l_type:
                conditions.append("l_type = ?")
                params.append(l_type.value)
            if l_level:
                conditions.append("l_level = ?")
                params.append(l_level.value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY created_date DESC LIMIT ?"
            params.append(limit)

            cursor = cx.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "l_type": row[1],
                    "l_level": row[2],
                    "message": row[3],
                    "created_date": row[4]
                }
                for row in rows
            ]


    @classmethod
    def clean_logs(cls, older_than_days:int=30)->int:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                DELETE FROM logs
                WHERE created_date <= datetime('now', ? || ' days')
            """, (-older_than_days,))
            return result.rowcount