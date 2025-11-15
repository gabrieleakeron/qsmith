import sqlite3
import os

class ConnectionFactory:
    @classmethod
    def create_connection(cls):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        db_path = os.path.join(path, "data/qsmith.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return sqlite3.connect(db_path, timeout=30, check_same_thread=False, autocommit=True)