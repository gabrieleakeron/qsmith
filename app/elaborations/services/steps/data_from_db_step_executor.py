from sqlalchemy.orm import Session

from _alembic.models.scenario_step_entity import ScenarioStepEntity
from _alembic.models.step_entity import StepEntity
from data_sources.models.database_connection_config_types import DatabaseConnectionConfigTypes
from data_sources.services.alembic.database_connection_service import load_database_connection
from elaborations.models.dtos.configuration_step_dtos import DataFromDbConfigurationStepDto
from elaborations.services.operations.operation_executor_composite import execute_operations
from elaborations.services.steps.step_executor import StepExecutor
from sqlalchemy_utils.database_table_reader import DatabaseTableReader, ReadTableConfig
from sqlalchemy_utils.engine_factory.sqlalchemy_engine_factory_composite import create_sqlalchemy_engine


class DataFromDbStepExecutor(StepExecutor):

    def execute(self, session: Session, scenario_step: ScenarioStepEntity, step: StepEntity,
                cfg: DataFromDbConfigurationStepDto) -> list[dict[str, str]]:
        database_connection_cfg: DatabaseConnectionConfigTypes = load_database_connection(cfg.connection_id)
        engine = create_sqlalchemy_engine(database_connection_cfg)

        self.log(scenario_step.step_id, f"Start reading table '{cfg.table_name}'")

        operations_id = self.find_all_operations(session, scenario_step.id)

        total_rows = 0
        results: list[dict[str, str]] = []

        for chunk in DatabaseTableReader.read_table_chunks(
                engine,
                ReadTableConfig(
                    table_name=cfg.table_name,
                    query=cfg.query,
                    chunk_size=cfg.chunk_size,
                    stream=cfg.stream,
                    order_by=cfg.order_by
                )
        ):
            chunk_len = len(chunk)
            if chunk_len == 0:
                continue

            op_result = execute_operations(session, operations_id, chunk)

            results.extend(op_result.result)

            total_rows += chunk_len

            self.log(scenario_step.step_id,
                     f"Processed chunk of {chunk_len} rows from '{cfg.table_name}'. Total so far: {total_rows}")

        self.log(scenario_step.step_id,
                 f"Finished reading table '{cfg.table_name}'. Total rows processed: {total_rows}")

        return results
