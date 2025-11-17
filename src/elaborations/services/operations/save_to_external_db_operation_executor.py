import json
from datetime import datetime

from database.models.database_connection_config_types import DatabaseConnectionConfigTypes
from database.services.sqlalchemy.database_table_manager import DatabaseTableManager
from database.services.sqlalchemy.database_table_writer import DatabaseTableWriter
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from elaborations.models.operations import SaveToExternalDBOperationDto
from elaborations.models.scenario import Scenario
from elaborations.models.steps import StepDto
from database.services.sqlite.database_connection_service import load_database_connection
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto


class SaveToExternalDbOperationExecutor(OperationExecutor):

    def execute(self, scenario:Scenario, step:StepDto, operation: SaveToExternalDBOperationDto, data:list[dict])->ExecutionResultDto:
        connection:DatabaseConnectionConfigTypes = load_database_connection(operation.connection_id)

        engine = create_sqlalchemy_engine(connection)
        DatabaseTableManager.drop_table(engine, operation.table_name)

        columns = {
            "oid":"TEXT",
            "message_payload":"TEXT",
            "occurred_at":"TIMESTAMP"
        }
        primary_key = "oid"
        DatabaseTableManager.create_table(engine, operation.table_name, columns, primary_key)

        rows = []
        for index, item in enumerate(data):
            rows.append({
                "oid": str(index),
                "message_payload": json.dumps(item),
                "occurred_at": datetime.now()
            })

        DatabaseTableWriter.insert_rows(engine, operation.table_name, rows)

        message = f"Created {len(rows)} rows in {operation.table_name} table"

        self.log(operation,message )

        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
