from contextlib import contextmanager

from _alembic.services.session_factory import SessionFactory


@contextmanager
def managed_session():
    session = SessionFactory.create_session()
    try:
        with session.begin():
            yield session
    finally:
        session.close()
