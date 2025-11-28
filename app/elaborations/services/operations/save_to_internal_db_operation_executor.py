import json
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from _alembic.services.alembic_config_service import url_from_env
from elaborations.models.dtos.configuration_operation_dto import SaveInternalDBConfigurationOperationDto
from elaborations.services.operations.operation_executor import OperationExecutor, ExecutionResultDto
from sqlalchemy_utils.database_table_writer import DatabaseTableWriter


class SaveInternalDbOperationExecutor(OperationExecutor):
    def execute(self, session:Session,  operation_id:str, cfg: SaveInternalDBConfigurationOperationDto, data:list[dict])->ExecutionResultDto:
        engine = create_engine(url_from_env())

        DatabaseTableWriter.insert_rows(engine, cfg.table_name, data)

        message = f"Created {len(data)} rows in {cfg.table_name} table"

        self.log(operation_id, message)

        return ExecutionResultDto(
            data=data,
            result=[{"message": message}]
        )
