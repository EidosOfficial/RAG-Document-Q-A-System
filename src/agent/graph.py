from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes import (
    retrieve_node,
    evaluate_context_node,
    rewrite_query_node,
    generate_answer_node,
    calculator_node,
    route_question,
    decide_to_generate_or_rewrite,
)

# Initialize StateGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("evaluate", evaluate_context_node)
workflow.add_node("rewrite", rewrite_query_node)
workflow.add_node("generate", generate_answer_node)
workflow.add_node("calculator", calculator_node)

# Conditional Start routing
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "calculator": "calculator",
        "retrieve": "retrieve",
    },
)

# Add Fixed Edges
workflow.add_edge("retrieve", "evaluate")
workflow.add_edge("calculator", END)
workflow.add_edge("generate", END)

# Add Self Correction Loop
workflow.add_conditional_edges(
    "evaluate",
    decide_to_generate_or_rewrite,
    {"generate": "generate", "rewrite": "rewrite"},
)

workflow.add_edge("rewrite", "retrieve")

agent_app = workflow.compile()
