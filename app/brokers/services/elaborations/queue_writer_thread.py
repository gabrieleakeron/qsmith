import threading

from sqlalchemy import create_engine

from _alembic.services.alembic_config_service import url_from_env
from _alembic.services.session_context_manager import managed_session
from brokers.models.dto.configurations.queue_configuration_types import convert_queue_configuration_types
from brokers.services.alembic.queue_service import QueueService
from brokers.services.connections.queue.queue_connection_service import QueueConnectionService
from logs.models.dtos.log_dto import LogDto
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService
from sqlalchemy_utils.database_table_reader import ReadTableConfig, DatabaseTableReader


class QueueWriterThread(threading.Thread):

    def __init__(self, export_tabel_name:str, queue_id: str, service: QueueConnectionService, connection_config):
        super().__init__(name=f"queue_reader-{queue_id}", daemon=True)
        self._stop_event = threading.Event()
        self.export_tabel_name = export_tabel_name
        self.queue_id = queue_id
        self.service = service
        self.connection_config = connection_config
        with managed_session() as session:
            queue_entity = QueueService().get_by_id(session, queue_id)
            self.code = queue_entity.code
            cfg = convert_queue_configuration_types(queue_entity.configuration_json)
            self.receiveMessageWait = cfg.receiveMessageWait if cfg.receiveMessageWait else 20

    def log(self, message:str, level: LogLevel):
        log_dto = LogDto(
            subject_type=LogSubjectType.SERVICE,
            subject=self.name,
            message=message,
            level=level
        )
        LogService().log(log_dto)

    def run(self):
        engine = create_engine(url_from_env())

        export_table_name = f'public."{self.export_tabel_name}"'
        try:
            rows = DatabaseTableReader.read_full_table(engine, ReadTableConfig(export_table_name, order_by=["id"]))
        except Exception as e:
            self.log(f"Error reading export table {self.export_tabel_name}: {str(e)}", LogLevel.ERROR)
            return

        bodies = [row["body"] for row in rows]

        self.service.publish_messages(self.connection_config, queue_id=self.queue_id, messages=bodies)

        self.log(f"{len(bodies)} Messages sent to queue {self.code}", LogLevel.INFO)


    def stop(self):
        self._stop_event.set()
        log_dto = LogDto(
            subject_type=LogSubjectType.SERVICE,
            subject=self.name,
            message=f"Queue writer thread for queue {self.code} is stopping.",
            level=LogLevel.INFO
        )
        LogService().log(log_dto)
