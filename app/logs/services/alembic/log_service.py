import time

from sqlalchemy.orm import InstrumentedAttribute, Session

from _alembic.models.log_entity import LogEntity
from logs.models.enums.log_level import LogLevel
from logs.models.enums.log_subject_type import LogSubjectType


class LogService:

    @classmethod
    def log(cls, session: Session, log_entity: LogEntity)->str:
        session.add(log_entity)
        session.flush()
        session.refresh(log_entity)
        return log_entity.id

    @classmethod
    def logs(cls, session: Session, log_entity: list[LogEntity])->list[str]:
        ids = []
        for log in log_entity:
            session.add(log)
            session.flush()
            session.refresh(log)
            ids.append(log.id)
        return ids

    @classmethod
    def get_logs(cls, session: Session, subject:LogSubjectType=None, level:LogLevel=None, limit:int=100)->list[LogEntity]:
        query = session.query(LogEntity)
        if subject:
            subject_attr: InstrumentedAttribute = LogEntity.subject_type
            query = query.filter(subject_attr == subject.value)
        if level:
            level_attr: InstrumentedAttribute = LogEntity.level
            query = query.filter(level_attr == level.value)
        query = query.order_by(LogEntity.created_at.desc()).limit(limit)
        return query.all()

    @classmethod
    def clean_logs(cls,session: Session, older_than_days:int=30)->int:
        threshold = int(time.time()) - older_than_days * 86400
        deleted = session.query(LogEntity).filter(LogEntity.created_at < threshold).delete()
        return deleted