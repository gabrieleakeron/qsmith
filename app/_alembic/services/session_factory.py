from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from _alembic.services.alembic_config_service import url_from_env


class SessionFactory:

    @staticmethod
    def create_session() -> Session:
        engine = create_engine(url_from_env(), pool_pre_ping=True)
        session_local = sessionmaker(bind=engine)
        return session_local()
