import re
from src.agent.state import AgentState
from src.services.vector_service import retrieve_similar_chunks
from src.core.llm import (
    evaluate_context,
    rewrite_question,
    get_response,
)


def retrieve_node(state: AgentState):
    retrieved_chunks = retrieve_similar_chunks(query=state["question"], top_k=3)
    context_snippets = []
    for content, metadata, similarity in retrieved_chunks:
        source_file = metadata.get("source", "unknown") if metadata else "Unknown"
        context_snippets.append(f"Source({source_file}):\n{content})")

    return {
        "retrieved_chunks": retrieved_chunks,
        "context": "\n\n".join(context_snippets),
    }


def evaluate_context_node(state: AgentState):
    llm_evaluation_response = evaluate_context(
        context=state["context"], question=state["question"]
    )

    return {"is_sufficient": llm_evaluation_response}


def rewrite_query_node(state: AgentState):
    new_question = rewrite_question(query=state["question"])
    current_retries = state.get("retry_count", 0)

    return {
        "question": new_question,
        "retry_count": current_retries + 1,
    }


def generate_answer_node(state: AgentState):
    answer = get_response(query=state["question"], context=state["context"])

    return {"generation": answer}


def calculator_node(state: AgentState):
    question = state["question"]
    try:
        math_match = re.search(r"[\d\.\s\+\-\*\/\(\)]+", question)
        if math_match:
            expr = math_match.group(0).strip()
            result = eval(expr)
            res_str = f"Calculated Results: {expr} = {result}"
        else:
            res_str = "Could not parse math expression."
    except Exception as e:
        res_str = f"Calculation Error: {str(e)}"

    return {"generation": res_str}


# MARK: Decision Functions
def route_question(state: AgentState):
    question = state["question"].lower()
    if "calculate" in question or "math" in question:
        return "calculator"
    return "retrieve"


def decide_to_generate_or_rewrite(state: AgentState):
    if state.get("is_sufficient") == "yes":
        return "generate"
    if state.get("retry_count", 0) >= 2:
        return "generate"
    return "rewrite"
