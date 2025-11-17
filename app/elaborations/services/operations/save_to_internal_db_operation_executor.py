import json
from datetime import datetime

from sqlalchemy import create_engine

from _alembic.services.alembic_config_service import url_from_env
from database.services.sqlalchemy.database_table_manager import DatabaseTableManager
from database.services.sqlalchemy.database_table_writer import DatabaseTableWriter
from elaborations.models.dtos.configuration_operation_dto import SaveInternalDBConfigurationOperationDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto


class SaveInternalDbOperationExecutor(OperationExecutor):
    def execute(self, operation_id:str, cfg: SaveInternalDBConfigurationOperationDto, data:list[dict])->ExecutionResultDto:
        engine = create_engine(url_from_env())
        DatabaseTableManager.drop_table(engine, cfg.table_name)

        columns = {
            "oid": "TEXT",
            "message_payload": "TEXT",
            "occurred_at": "TIMESTAMP"
        }
        primary_key = "oid"
        DatabaseTableManager.create_table(engine, cfg.table_name, columns, primary_key)

        rows = []
        for index, item in enumerate(data):
            rows.append({
                "oid": str(index),
                "message_payload": json.dumps(item),
                "occurred_at": datetime.now()
            })

        DatabaseTableWriter.insert_rows(engine, cfg.table_name, rows)

        message = f"Created {len(rows)} rows in {cfg.table_name} table"

        self.log(operation_id, message)

        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
