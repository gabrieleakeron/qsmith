import os

from alembic.config import Config
from alembic import command
from path_utils.path_service import get_project_root_path


def run_alembic_migrations():
    alembic_path = os.path.join(get_project_root_path(), "alembic", "alembic.ini")
    # stampo i file e le dir presenti in root_path
    if not os.path.isfile(alembic_path):
        print("Alembic configuration file not found!")
        return
    # carico la configurazione di Alembic
    alembic_cfg: Config = Config(alembic_path)
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Errore Alembic:${str(e)}")
    print("Alembic migrations completed.")
