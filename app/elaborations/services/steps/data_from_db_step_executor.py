from data_sources.models.database_connection_config_types import DatabaseConnectionConfigTypes
from data_sources.services.alembic.database_connection_service import load_database_connection
from elaborations.models.dtos.configuration_step_dtos import DataFromDbConfigurationStepDto
from _alembic.models.step_entity import StepEntity
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor
from sqlalchemy_utils.database_table_reader import DatabaseTableReader
from sqlalchemy_utils.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine


class DataFromDbStepExecutor(StepExecutor):

    def execute(self, step:StepEntity, cfg: DataFromDbConfigurationStepDto) -> list[dict[str, str]]:
        database_connection_cfg:DatabaseConnectionConfigTypes = load_database_connection(step.connection_id)
        engine = create_sqlalchemy_engine(database_connection_cfg)

        self.log(step, f"Start reading table '{step.table_name}'")

        operations_id = self.find_all_operations(step.id)

        total_rows = 0
        results = []
        for rows_chunk in DatabaseTableReader.stream_table(engine, step.table_name, step.order_by, step.page_size):
            results.extend(execute_operations(operations_id, rows_chunk).result)
            total_rows += len(rows_chunk)

        self.log(step, f"Finished reading table '{step.table_name}'. Total rows processed: {total_rows}")

        return results
