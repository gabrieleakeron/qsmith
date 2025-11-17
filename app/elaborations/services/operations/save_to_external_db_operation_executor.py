import json
from datetime import datetime

from database.models.database_connection_config_types import DatabaseConnectionConfigTypes
from database.services.sqlalchemy.database_table_manager import DatabaseTableManager
from database.services.sqlalchemy.database_table_writer import DatabaseTableWriter
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from database.services.sqlite.database_connection_service import load_database_connection
from elaborations.models.dtos.configuration_operation_dto import SaveToExternalDBConfigurationOperationDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto


class SaveToExternalDbOperationExecutor(OperationExecutor):

    def execute(self, operation_id:str, cfg: SaveToExternalDBConfigurationOperationDto, data:list[dict])->ExecutionResultDto:
        connection:DatabaseConnectionConfigTypes = load_database_connection(cfg.connection_id)

        engine = create_sqlalchemy_engine(connection)
        DatabaseTableManager.drop_table(engine, cfg.table_name)

        columns = {
            "oid":"TEXT",
            "message_payload":"TEXT",
            "occurred_at":"TIMESTAMP"
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

        self.log(operation_id,message)

        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
