from langchain.memory import ConversationBufferMemory
import psycopg2
from datetime import datetime
from agents.config import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)

class Memory:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.conversation_history = []

    def save_message(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        self.memory.save_context({"input": message}, {"output": ""})

    def save_response(self, response):
        if self.conversation_history:
            self.conversation_history[-1]["response"] = response
        self.memory.save_context({"input": ""}, {"output": response})

    def get_history(self):
        return self.conversation_history

class PostgresMemory:
    def __init__(
        self,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    ):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        self._ensure_table()

    def _ensure_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(64),
                    role VARCHAR(16),
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def save_message(self, session_id, role, message):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO conversation_history (session_id, role, message, timestamp) VALUES (%s, %s, %s, %s)",
                (session_id, role, message, datetime.now())
            )
            self.conn.commit()

    def get_history(self, session_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT role, message, timestamp FROM conversation_history WHERE session_id = %s ORDER BY timestamp ASC",
                (session_id,)
            )
            return cur.fetchall()

    def get_relevant_history(self, session_id, current_message, limit=3):
        """
        Fetches up to `limit` most recent messages from this session that share keywords with the current message.
        """
        with self.conn.cursor() as cur:
            # Simple keyword search (for demo); for production, use embeddings for semantic similarity
            cur.execute(
                """
                SELECT role, message, timestamp FROM conversation_history
                WHERE session_id = %s AND message ILIKE %s
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (session_id, f"%{current_message.split()[0]}%", limit)
            )
            return cur.fetchall()

# Usage: memory = PostgresMemory(password="yourpassword")
