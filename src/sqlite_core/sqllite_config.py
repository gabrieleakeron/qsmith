from sqlite_core.connection_factory import ConnectionFactory

def init_db():
    with ConnectionFactory.create_connection() as cx:
        cx.execute("PRAGMA journal_mode=WAL;")
        cx.execute("PRAGMA synchronous=NORMAL;")
        cx.execute("PRAGMA temp_store=MEMORY;")
        cx.execute("PRAGMA cache_size=-50000;")

        cx.execute("""
            CREATE TABLE IF NOT EXISTS json_payloads(
              id TEXT PRIMARY KEY,
              code TEXT,
              description TEXT,
              json_type TEXT,
              payload TEXT,
              created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
              modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cx.execute("""
            CREATE TABLE IF NOT EXISTS queues(
              id TEXT PRIMARY KEY,
              code TEXT,
              broker_id TEXT,
              payload TEXT,
              created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
              modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cx.execute("""
            CREATE TABLE IF NOT EXISTS scenario_results(
              id TEXT PRIMARY KEY,
              scenario TEXT NOT NULL,
              step TEXT,
              payload TEXT,
              created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
              modified_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cx.execute("""
            CREATE TABLE IF NOT EXISTS logs(
              id TEXT PRIMARY KEY,
              l_level TEXT,
              l_type TEXT,
              message TEXT,
              created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
