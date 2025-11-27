import json
from datetime import datetime

from sqlalchemy.orm import Session

from _alembic.models.json_payload_entity import JsonPayloadEntity
from data_sources.models.database_connection_config_types import DatabaseConnectionConfigTypes
from elaborations.models.dtos.configuration_operation_dto import SaveToExternalDBConfigurationOperationDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from json_utils.services.alembic.json_files_service import JsonFilesService
from sqlalchemy_utils.database_table_manager import DatabaseTableManager
from sqlalchemy_utils.database_table_writer import DatabaseTableWriter
from sqlalchemy_utils.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from data_sources.models.database_connection_config_types import convert_database_connection_config


class SaveToExternalDbOperationExecutor(OperationExecutor):

    def execute(self, session:Session, operation_id:str, cfg: SaveToExternalDBConfigurationOperationDto, data:list[dict])->ExecutionResultDto:
        connection:DatabaseConnectionConfigTypes = self.load_database_connection(session,cfg.connection_id)

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

    def load_database_connection(self,session:Session, _id:str):
        json_payload_entity: JsonPayloadEntity = JsonFilesService().get_by_id(session, _id)

        if not json_payload_entity:
            raise ValueError(f"Database connection '{_id}' not found")

        return convert_database_connection_config(json_payload_entity.payload)
