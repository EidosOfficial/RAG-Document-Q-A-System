from src.db.session import connect
from src.core.embedder import generate_embedding
from langchain_core.documents import Document


def retrieve_similar_chunks(query: str, top_k: int = 3):
    conn = connect()
    cur = conn.cursor()
    encoded_query = generate_embedding([Document(page_content=query)])[0]
    db_query = """
        SELECT content, metadata, 1 - (embedding <=> %s) as similarity
        FROM document_chunks
        ORDER BY embedding <=> %s ASC
        LIMIT %s
    """
    cur.execute(db_query, (encoded_query, encoded_query, top_k))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
