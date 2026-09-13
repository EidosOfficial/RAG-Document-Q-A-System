from openai import OpenAI
from config import settings
from dotenv import load_dotenv

load_dotenv()
_client = None


def get_client():
    global _client
    if _client is None:
        _client = OpenAI(base_url=settings.OLLAMA_BASE_URL, api_key="ollama")
    return _client


def get_response(query: str, context: str) -> str:
    system_prompt_with_context = f"""
        You are an expert technical assistant. Answer the question using ONLY the provided context snippets.
        Provide a detailed, thorough, and structured explanation based on the context.
        If the answer cannot be found in the context, say 'I cannot find the answer in the provided documents.'

        --- CONTEXT SNIPPETS ---
        {context}
        ------------------------

        User Question: {query}
        Answer:
    """
    client = get_client()
    response = client.chat.completions.create(
        model=settings.OLLAMA_FAST_MODEL,
        messages=[
            {"role": "system", "content": system_prompt_with_context},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=800,
    )

    return response.choices[0].message.content


def get_streaming_response(query: str, context: str):
    system_prompt_with_context = f"""
        You are an expert technical assistant. Answer the question using ONLY the provided context snippets.
        Provide a detailed, thorough, and structured explanation based on the context.
        If the answer cannot be found in the context, say 'I cannot find the answer in the provided documents.'

        --- CONTEXT SNIPPETS ---
        {context}
        ------------------------

        User Question: {query}
        Answer:
    """
    client = get_client()
    stream = client.chat.completions.create(
        model=settings.OLLAMA_FAST_MODEL,
        messages=[
            {"role": "system", "content": system_prompt_with_context},
            {"role": "user", "content": query},
        ],
        temperature=0.0,
        max_tokens=800,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def evaluate_context(context: str, question: str) -> str:
    system_prompt = f"""
        You are a strict evaluator. 
        Read the provided context and the user question.
        Determine if the context contains enough factual information to fully answer the question.
        Do not assume or extrapolate information not directly mentioned in the text.
        Respond with strictly "yes" or "no" and nothing else.

        Context: 
        {context}

        Question: 
        {question}

        Answer (yes/no):
    """
    client = get_client()
    response = client.chat.completions.create(
        model=settings.OLLAMA_THINKING_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.lower()


def rewrite_question(query: str):
    system_prompt = f"""
        You are an expert search engine optimizer and retrieval specialist for a Vector Database (RAG system).

        Your task is to rewrite the following user question to maximize its effectiveness for semantic vector search. Vector searches rely on conceptual similarity, rich keywords, and clarity rather than conversational pleasantries or complex question structures.

        Follow these strict rules:
        1. Strip out conversational filler (e.g., "Can you tell me...", "Please explain...", "Hi there, I need help with...").
        2. Identify the core concepts, entities, technical terms, and intent of the question.
        3. Expand the query with highly relevant keywords, synonyms, or industry-standard terms that are likely to appear in the reference documentation.
        4. Keep the output concise, factual, and optimized as a search query, not a conversational response.
        5. Output ONLY the finalized search query. Do not include any introductory or concluding remarks.

        Original User Question:
        "{query}"

        Optimized Vector Search Query:
    """
    client = get_client()
    response = client.chat.completions.create(
        model=settings.OLLAMA_THINKING_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content.lower()
