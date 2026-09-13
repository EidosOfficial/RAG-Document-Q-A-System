import psycopg
from pgvector.psycopg import register_vector

from config import settings


_connection = None


def connect():
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg.connect(settings.DATABASE_URL)
    cur = _connection.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    _connection.commit()
    register_vector(_connection)
    return _connection


def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS document_chunks (id UUID PRIMARY KEY, content TEXT, metadata JSONB, embedding VECTOR(384))"
    )
    conn.commit()


def clear_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE document_chunks")
    conn.commit()
    cur.close()
    conn.close()
