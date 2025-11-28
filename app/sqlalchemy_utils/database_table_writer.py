import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, Float, String, Boolean,
    Date, DateTime, insert
)
from sqlalchemy.engine.base import Engine


class DatabaseTableWriter:
    @classmethod
    def infer_column_type(cls, value):
        """Infer SQLAlchemy column type from a Python value."""
        if value is None:
            return String()  # fallback
        if isinstance(value, bool):
            return Boolean()
        if isinstance(value, int):
            return Integer()
        if isinstance(value, float):
            return Float()
        if isinstance(value, (str,)):
            return String()
        if isinstance(value, datetime.datetime):
            return DateTime()
        if isinstance(value, datetime.date):
            return Date()
        return String()  # fallback per tipi complessi


    @classmethod
    def ensure_table_exists(cls, engine: Engine, table_name: str, sample_row: dict):
        """Create table if it does not exist, using sample_row to infer columns."""
        metadata = MetaData()
        metadata.reflect(bind=engine)

        # Se la tabella esiste, non fare nulla
        if table_name in metadata.tables:
            return metadata.tables[table_name]

        # La tabella non esiste → creiamola
        columns = []

        for key, value in sample_row.items():
            col_type = cls.infer_column_type(value)
            columns.append(Column(key, col_type))

        table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)

        return table


    @classmethod
    def insert_rows(cls, engine: Engine, table_name: str, rows: list[dict]):
        if not rows:
            return

        table = cls.ensure_table_exists(engine, table_name, rows[0])

        with engine.begin() as conn:
            conn.execute(insert(table), rows)

