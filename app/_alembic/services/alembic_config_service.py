import os

def url_from_env() -> str:
    return os.getenv("DATABASE_URL")