import json
from src.services.vector_service import retrieve_similar_chunks
from src.core.llm import get_response, get_streaming_response


def answer_question(query: str, top_k: int = 3) -> dict:
    """
    Orchestrates Retrieval + LLM Generation into a clean Q&A workflow.
    """
    db_rows = retrieve_similar_chunks(query, top_k=top_k)

    context_snippets = []
    sources_list = []

    for content, metadata, similarity in db_rows:
        source_file = metadata.get("source", "Unknown") if metadata else "Unknown"
        context_snippets.append(f"Source ({source_file}):\n{content}")
        sources_list.append(
            {"source": source_file, "similarity": round(float(similarity), 4)}
        )

    formatted_context = "\n\n".join(context_snippets)

    llm_answer = get_response(query=query, context=formatted_context)

    return {"question": query, "answer": llm_answer, "sources": sources_list}


def stream_answer_question(query: str, top_k: int = 3):
    """
    Retrieves vector context and returns a generator that yields LLM answer tokens in real-time.
    """
    db_rows = retrieve_similar_chunks(query, top_k=top_k)
    context_snippets = []
    sources_list = []
    for content, metadata, similarity in db_rows:
        source_file = metadata.get("source", "Unknown") if metadata else "Unknown"
        context_snippets.append(f"Source ({source_file}):\n{content}")
        sources_list.append(
            {"source": source_file, "similarity": round(float(similarity), 4)}
        )

    yield f"data: {json.dumps({'type': 'sources', 'sources': sources_list})}\n\n"
    formatted_context = "\n\n".join(context_snippets)
    for token in get_streaming_response(query=query, context=formatted_context):
        yield f"data: {json.dumps({'type': 'answer', 'text': token})}\n\n"
    yield "data: [DONE]\n\n"

    # return get_streaming_response(query=query, context=formatted_context)
