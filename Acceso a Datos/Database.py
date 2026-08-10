import sqlite3
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path="cletaeats.db"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance.db_path = db_path
                cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS store (
                    key TEXT PRIMARY KEY,
                    data BLOB
                )
            ''')

    def get_connection(self):
        return sqlite3.connect(self.db_path)
