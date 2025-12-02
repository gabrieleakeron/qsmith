import json
import threading
import time

from _alembic.models.json_payload_entity import JsonPayloadEntity
from _alembic.services.session_context_manager import managed_session
from brokers.models.dto.configurations.queue_configuration_types import convert_queue_configuration_types
from brokers.services.alembic.queue_service import QueueService
from brokers.services.connections.queue.queue_connection_service import QueueConnectionService
from json_utils.models.enums.json_type import JsonType
from json_utils.services.alembic.json_files_service import JsonFilesService
from logs.models.dtos.log_dto import LogDto
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType
from logs.services.alembic.log_service import LogService


class QueueReaderThread(threading.Thread):
    def __init__(self, queue_id: str, service: QueueConnectionService, connection_config):
        super().__init__(name=f"queue_reader-{queue_id}", daemon=True)
        self._stop_event = threading.Event()
        self.service = service
        self.queue_id = queue_id
        self.connection_config = connection_config
        self.round_counter = 0
        with managed_session() as session:
            queue_entity = QueueService().get_by_id(session, queue_id)
            self.code = queue_entity.code
            cfg = convert_queue_configuration_types(queue_entity.configuration_json)
            self.receiveMessageWait = cfg.receiveMessageWait if cfg.receiveMessageWait else 20

    def loop(self):
        while not self._stop_event.is_set():

            msgs = self.service.receive_messages(self.connection_config, queue_id=self.queue_id)

            if not msgs or len(msgs) == 0:
                time.sleep(self.receiveMessageWait)
                continue

            self.round_counter += 1

            log_dto = LogDto(
                subject_type=LogSubjectType.SERVICE,
                subject=self.name,
                message=f"{len(msgs)} Messages received from queue {self.code} in round {str(self.round_counter)}",
                level=LogLevel.INFO
            )
            LogService().log(log_dto)

            bodies = []
            for m in msgs:
                body = json.loads(m["Body"])
                if isinstance(body, list):
                    for b in body:
                        bodies.append(b)
                else:
                    bodies.append(body)

            with managed_session() as session:
                entity: JsonPayloadEntity = JsonPayloadEntity()
                entity.json_type = JsonType.JSON_ARRAY.value
                entity.code = f"{self.code}_round_{str(self.round_counter)}"
                entity.payload=[bodies]
                JsonFilesService().insert(session, entity)

    def run(self):
        try:
            self.loop()
        except Exception as e:
            log_dto = LogDto(
                subject_type=LogSubjectType.SERVICE,
                subject=self.name,
                message=f"Error in queue reader thread for queue {self.code}: {str(e)}",
                level=LogLevel.ERROR
            )
            LogService().log(log_dto)

    def stop(self):
        self._stop_event.set()
        log_dto = LogDto(
            subject_type=LogSubjectType.SERVICE,
            subject=self.name,
            message=f"Queue reader thread for queue {self.code} is stopping.",
            level=LogLevel.INFO
        )
        LogService().log(log_dto)
