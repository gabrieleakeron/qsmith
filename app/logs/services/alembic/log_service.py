import time
from datetime import timedelta, datetime

from sqlalchemy.orm import InstrumentedAttribute, Session

from _alembic.models.base_entity import BaseIdEntity
from _alembic.models.log_entity import LogEntity
from _alembic.services.base_id_service import BaseIdEntityService
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType


class LogService(BaseIdEntityService):

    def get_entity_class(self) -> type[BaseIdEntity]:
        return LogEntity

    def log(self, session: Session, log_entity: LogEntity)->str:
        super().insert(session, log_entity)
        return log_entity.id

    def logs(self, session: Session, entities: list[LogEntity])->list[str]:
        return super().inserts(session, entities)

    def get_logs(self, session: Session, subject:LogSubjectType=None, level:LogLevel=None, limit:int=100)->list[LogEntity]:
        query = session.query(LogEntity)
        if subject:
            subject_attr: InstrumentedAttribute = LogEntity.subject_type
            query = query.filter(subject_attr == subject.value)
        if level:
            level_attr: InstrumentedAttribute = LogEntity.level
            query = query.filter(level_attr == level.value)
        query = query.order_by(LogEntity.created_at.desc()).limit(limit)
        return query.all()


    def clean_logs(self,session: Session, older_than_days:int=30)->int:
        threshold_dt = datetime.utcnow() - timedelta(days=int(older_than_days))
        created_at_attr: InstrumentedAttribute = LogEntity.created_at
        deleted = session.query(LogEntity).filter(created_at_attr < threshold_dt).delete()
        return deleted