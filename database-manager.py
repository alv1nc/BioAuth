from models.database import DatabaseManager
import psycopg2
from pgvector.psycopg2 import register_vector

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            "dbname": "bio_auth",
            "user": "postgres",
            "password": "password123",
            "host": "localhost",
            "port": "5432"
        }

        self.conn= psycopg2.connect(**self.db_config)
        self.conn.autocommit = True

        register_vector(self.conn)

        with self.conn.cursor() as curr:
            curr.execute("DROP TABLE IF EXISTS users;")
DatabaseManager()