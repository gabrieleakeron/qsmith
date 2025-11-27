from sqlalchemy import text


class DatabaseTableWriter:
    @classmethod
    def insert_rows(cls, engine, table_name: str, rows: list[dict]):
        with engine.connect() as connection:
            if not rows:
                return

            columns = rows[0].keys()
            col_names = ', '.join([f'"{col}"' for col in columns])
            placeholders = ', '.join([f":{col}" for col in columns])

            sql = text(f"INSERT INTO \"{table_name}\" ({col_names}) VALUES ({placeholders})")

            with engine.begin() as conn:
                conn.execute(sql, rows)
