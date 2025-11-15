from database.models.database_connection_config_types import DatabaseConnectionConfigTypes
from database.services.sqlalchemy.database_table_reader import DatabaseTableReader
from database.services.sqlalchemy.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine
from database.services.sqlite.database_connection_service import load_database_connection
from elaborations.models.scenario import Scenario
from elaborations.models.steps import DataFromDbStepDto
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor


class DataFromDbStepExecutor(StepExecutor):

    def execute(self, scenario:Scenario, step: DataFromDbStepDto) -> list[dict[str, str]]:

        database_connection_cfg:DatabaseConnectionConfigTypes = load_database_connection(step.connectionConfig)

        engine = create_sqlalchemy_engine(database_connection_cfg)

        results = []
        for rows_chunk in DatabaseTableReader.stream_table(engine, step.table_name, step.order_by, step.page_size):
            results.extend(execute_operations(scenario, step, step.operations, rows_chunk).result)

        return results
