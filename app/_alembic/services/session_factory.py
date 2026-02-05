from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from _alembic.services.alembic_config_service import url_from_env


class SessionFactory:
    _engines = {}

    @staticmethod
    def create_session() -> Session:
        if not SessionFactory._engines:
            SessionFactory._engines['default'] = create_engine(url_from_env(), pool_pre_ping=True)
        engine = SessionFactory._engines['default']
        SessionFactory.SessionLocal = sessionmaker(bind=engine)
        return SessionFactory.SessionLocal()
