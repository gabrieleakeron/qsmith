from sqlalchemy import text

class DatabaseTableReader:

    @classmethod
    def test_connection(cls, engine) -> bool:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @classmethod
    def stream_table(cls,engine,table_name:str, order_by:list[str], chunk_size=100):
        with engine.connect().execution_options(stream_results=True) as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name} ORDER BY {', '.join(order_by)}"))
            while True:
                rows = result.fetchmany(chunk_size)
                if not rows:
                    break
                yield [dict(r) for r in rows]