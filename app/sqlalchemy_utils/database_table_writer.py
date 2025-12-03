from sqlalchemy import (
    MetaData, Table, Column, insert
)
from sqlalchemy.engine.base import Engine

from sqlalchemy_utils.column_type_extractor import extract_column_type


class DatabaseTableWriter:

    @classmethod
    def ensure_table_exists(cls, engine: Engine, table_name: str, schema: dict)-> Table:
        metadata = MetaData()
        metadata.reflect(bind=engine)

        if table_name in metadata.tables:
            return metadata.tables[table_name]

        columns = []

        for key, value in schema.items():
            col_type = extract_column_type(value)
            columns.append(Column(key, col_type))

        table = Table(table_name, metadata, *columns)
        metadata.create_all(engine)

        return table


    @classmethod
    def insert_rows(cls, engine: Engine, table: Table, rows: list[dict]):
        if not rows:
            return

        with engine.begin() as conn:
            conn.execute(insert(table), rows)

