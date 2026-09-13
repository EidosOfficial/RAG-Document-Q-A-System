from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(docs):
    embeddings = model.encode([doc.page_content for doc in docs])
    return embeddings
