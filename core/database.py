import psycopg2
import json
from psycopg2.extras import DictCursor
from pgvector.psycopg2 import register_vector
import os

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
        self._create_tables()

    def _createtables(self):
        with self.conn as curr:
            curr.execute("CREATE EXTENSION IF NOT EXISTS")


            curr.execute("""
                         CREATE TABLE IF NOT EXISTS users (
                            id  SERIAL PRIMARY KEY,
                            user_id TEXT UNIQUE NOT NULL,
                            face_vector vector(<face_shape>),
                            voice_vector vector(<voice_shape>),
                            metadata TEXT,
                            is_active BOOLEAN DEFAULT TRUE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )
                         """)
            
            curr.execute("""
                        CREATE TABLE IF NOT EXISTS auth_logs (
                            id SERIAL PRIMARY KEY
                            user_id TEXT,
                            face_score FLOAT,
                            voice_score FLOAT,
                            status TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )
                        """)
    def add_user(self,user_id,face_vector,voice_vector,metadata=None):
        try:
            meta_json = json.dump(metadata) if metadata else None 
            with self.conn.cursor() as curr:
                curr.execute(
                    """
                    INSERT INTO users (user_id,face_vector,voice_vector,metadata)
                    VALUES (%s,%s,%s,%s)     
                    """,
                    (user_id,face_vector,voice_vector,meta_json)
                )
            return True
        except psycopg2.IntegrityError:
            # user_id already exists
            return False

    def get_user_vectors(self,user_id):
        with self.conn.cursor as curr:
            curr.execute("SELECT face_vector,voice_vector,metadata FROM users WHERE user_id = %s and is_active = TRUE",
                         (user_id,)
                         )
            row=curr.fetchone()

            if row:
                meta=json.loads(row[2]) if row[2] else None
                return row[0],row[1],row[2]
            else:
                return None,None,None
    def identify_user(self,face_vector,threshold=0.4):
        with self.conn.cursor as curr:
            curr.execute("""SELECT user_id, (face_vector <-> %s) as distance, metadata
                         FROM users
                         WHERE is_active = TRUE
                         ORDER BY distance ASC
                         LIMIT 1""",
                         (face_vector,))
            row=curr.fetchone()

            if row:
                user_id,distance,metadata=row

                meta=json.loads(metadata) if metadata else None

                return user_id,float(distance),metadata
            return None,None,None

    def get_users_list(self):
        with self.conn.cursor as curr:
            curr.execute("SELECT user_id, is_active, metadata, created_at FROM users")
            rows=curr.fetchall()

            final=[]
            for row in rows:
                meta_dict = json.loads(row[2] if row[2] else None)
                final.append({
                    "user_id":row[0],
                    "is_active":row[1],
                    "metadata":meta_dict,
                    "created_at":row[3]
                })
            return final
    def delete_user(self,user_id,permanent=False):
        with self.conn.cursor as curr:
            if permanent:
                curr.execute("DELETE FROM users WHERE user_id = %s",(user_id))
            else:
                curr.execute("UPDATE users SET is_active = %s WHERE user_id = %s",(False,user_id))
        #postgre returns the number of rows affected by the query, applicable to any command..
        return curr.rowcount>0
    def log_attempt(self, user_id, face_score, voice_score, status):
        with self.conn.cursor as curr:
            curr. execute("""
                          INSERT INTO auth_logs (user_id,face_score,voice_score,status) 
                          VALUES (%s,%s,%s,%s,%s)
                          """,
                          (user_id,face_score,voice_score,status)
            )
    #security:

    def log_attempt_list(self,limit=100):
        with self.conn.cursor() as curr:
            curr.execute("""
            SELECT user_id, status, face_score, voice_score, timestamp
            FROM auth_logs
            ORDER BY timestamp DESC
            LIMIT %s
            """,
            (limit,))

            rows = curr.fetchall()
            final=[]

            for row in rows:
                final.append({
                    "user_id":row[0],
                    "status": row[1],
                    "face_score": row[2],
                    "voice_score": row[3],
                    "timestamp": row[4]
                })
            
            return final
            





    