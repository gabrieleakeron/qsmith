from sqlalchemy import text


class DatabaseTableWriter:
    @classmethod
    def insert_rows(cls, engine, table_name: str, rows: list[dict]):
        with engine.connect() as connection:
            for row in rows:
                columns = ', '.join(row.keys())
                placeholders = ', '.join([f":{key}" for key in row.keys()])
                sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
                connection.execute(sql,row)

            connection.commit()
